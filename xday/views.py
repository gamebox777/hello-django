from django.shortcuts import render, redirect
from .models import QuizSession, Question, Answer, Result
import random
from django.utils import timezone
from datetime import timedelta, date

# Create your views here.

def start(request):
    if request.method == 'POST':
        # ユーザー識別（セッションID）
        user_id = request.session.session_key or request.session.create()
        # セッション作成
        session = QuizSession.objects.create(user_id=user_id, started_at=timezone.now())
        # 問題抽選
        questions = []
        # カテゴリごとに抽選
        for cat, num in [('EATING',2),('BODY',2),('MIND',2),('ECOLOGY',1),('SURVIVAL',1)]:
            qs = list(Question.objects.filter(category=cat))
            questions += random.sample(qs, min(num, len(qs)))
        # ワイルドカード（残り2問）
        used_ids = [q.id for q in questions]
        wild_pool = list(Question.objects.exclude(id__in=used_ids))
        if len(wild_pool) >= 2:
            questions += random.sample(wild_pool, 2)
        else:
            questions += wild_pool[:2]
        # 問題IDリストをセッションに保存
        qid_list = [q.id for q in questions]
        request.session['xday_session_id'] = session.id
        request.session['xday_qids'] = qid_list
        request.session['xday_answers'] = []
        request.session['xday_lp'] = 0
        return redirect('xday_quiz')
    return render(request, 'xday/start.html')

def quiz(request):
    qids = request.session.get('xday_qids', [])
    answers = request.session.get('xday_answers', [])
    lp = request.session.get('xday_lp', 0)
    current = len(answers) + 1
    if current > 10:
        return redirect('xday_result')
    question = Question.objects.get(id=qids[len(answers)])
    if request.method == 'POST':
        choice = request.POST.get('choice')
        is_correct = (choice == 'Yes' and question.correct_yes) or (choice == 'No' and not question.correct_yes)
        lp += 1 if is_correct else -1
        answers.append({'qid': question.id, 'choice': choice, 'is_correct': is_correct})
        request.session['xday_answers'] = answers
        request.session['xday_lp'] = lp
        if len(answers) >= 10:
            # セッション保存、Answer保存、Result計算
            session_id = request.session['xday_session_id']
            session = QuizSession.objects.get(id=session_id)
            session.lp_total = lp
            session.finished_at = timezone.now()
            session.save()
            for idx, ans in enumerate(answers):
                Answer.objects.create(
                    session=session,
                    question_id=ans['qid'],
                    user_choice=ans['choice'],
                    is_correct=ans['is_correct']
                )
            lifespan_years = int(lp * 1.5)
            xday = date.today() + timedelta(days=lifespan_years * 365)
            Result.objects.create(session=session, lifespan_years=lifespan_years, xday_date=xday)
            return redirect('xday_result')
        return redirect('xday_quiz')
    return render(request, 'xday/quiz.html', {
        'question': question,
        'current': current
    })

def result(request):
    session_id = request.session.get('xday_session_id')
    if not session_id:
        return redirect('xday_start')
    session = QuizSession.objects.get(id=session_id)
    try:
        result = Result.objects.get(session=session)
    except Result.DoesNotExist:
        return redirect('xday_start')
    # 評価コメント
    lp = session.lp_total
    if lp >= 5:
        comment = "延命マスター！この調子で健康長寿"
    elif lp <= -5:
        comment = "死神が背後に…今すぐ対策を！"
    else:
        comment = "まだ巻き返せる！生活習慣を見直そう"
    return render(request, 'xday/result.html', {
        'lp': lp,
        'lifespan_years': result.lifespan_years,
        'xday': result.xday_date,
        'comment': comment
    })

def history(request):
    user_id = request.session.session_key
    sessions = QuizSession.objects.filter(user_id=user_id).order_by('-started_at')
    return render(request, 'xday/history.html', {'sessions': sessions})

def history_detail(request, session_id):
    session = QuizSession.objects.get(id=session_id)
    answers = Answer.objects.filter(session=session).select_related('question')
    result = Result.objects.get(session=session)
    return render(request, 'xday/history_detail.html', {
        'session': session,
        'answers': answers,
        'result': result
    })
