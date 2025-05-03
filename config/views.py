# config/views.py
from django.shortcuts import render, redirect
import random
from .models import Record

def title(request):
    name = request.session.get('player_name', None)
    ip = get_client_ip(request)
    my_record = None
    if name:
        my_record = Record.objects.filter(name=name, ip_address=ip).order_by('-win_streak').first()
    all_records = Record.objects.all().order_by('-win_streak', '-played_at')
    return render(request, 'title.html', {'my_record': my_record, 'all_records': all_records})

def home(request):
    result = None
    player_choice = None
    computer_choice = None
    win_streak = request.session.get('win_streak', 0)
    
    if request.method == 'POST':
        player_choice = request.POST.get('choice')
        choices = ['グー', 'チョキ', 'パー']
        computer_choice = random.choice(choices)
        
        if player_choice == computer_choice:
            result = '引き分け'
        elif (player_choice == 'グー' and computer_choice == 'チョキ') or \
             (player_choice == 'チョキ' and computer_choice == 'パー') or \
             (player_choice == 'パー' and computer_choice == 'グー'):
            result = '勝ち'
            win_streak += 1
            request.session['win_streak'] = win_streak
        else:
            result = '負け'
            streak = win_streak
            request.session['win_streak'] = 0
            request.session['last_streak'] = streak
            return redirect('record')
    
    return render(request, 'home.html', {
        'result': result,
        'player_choice': player_choice,
        'computer_choice': computer_choice,
        'win_streak': win_streak
    })

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def record(request):
    last_streak = request.session.get('last_streak', 0)
    message = None
    default_name = request.session.get('player_name', '')
    if request.method == 'POST':
        name = request.POST.get('name')
        ip = get_client_ip(request)
        if name and last_streak > 0:
            request.session['player_name'] = name  # 名前をセッションに保存
            # 名前＆IPが一致するレコードがあれば更新、なければ新規作成
            record, created = Record.objects.get_or_create(name=name, ip_address=ip, defaults={'win_streak': last_streak})
            if not created:
                if last_streak > record.win_streak:
                    record.win_streak = last_streak
                    record.save()
            message = f"{name}さんの{last_streak}連勝を記録しました！"
            request.session['last_streak'] = 0
            return redirect('title')
        else:
            message = "名前を入力してください。"
    return render(request, 'record.html', {'last_streak': last_streak, 'message': message, 'default_name': default_name})

def root_redirect(request):
    return redirect('/xday/')

# 記録画面のビューは後で追加
