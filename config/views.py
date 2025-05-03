# config/views.py
from django.shortcuts import render
import random

def home(request):
    result = None
    player_choice = None
    computer_choice = None
    
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
        else:
            result = '負け'
    
    return render(request, 'home.html', {
        'result': result,
        'player_choice': player_choice,
        'computer_choice': computer_choice
    })
