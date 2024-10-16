from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Use environment variable for security

# Define possible choices
CHOICES = ['rock', 'paper', 'scissor']
MAX_ROUNDS = 5

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'player_score' not in session:
        session['player_score'] = 0
        session['computer_score'] = 0
        session['rounds_played'] = 0
        session['result'] = None
        session['player_choice'] = None
        session['computer_choice'] = None

    if request.method == 'POST' and 'choice' in request.form:
        player_choice = request.form['choice']
        computer_choice = random.choice(CHOICES)
        session['player_choice'] = player_choice
        session['computer_choice'] = computer_choice
        session['rounds_played'] += 1

        # Determine the winner
        if player_choice == computer_choice:
            result = 'Draw'
        elif (player_choice == 'rock' and computer_choice == 'scissor') or \
             (player_choice == 'paper' and computer_choice == 'rock') or \
             (player_choice == 'scissor' and computer_choice == 'paper'):
            result = 'You Won'
            session['player_score'] += 1
        else:
            result = 'Computer Won'
            session['computer_score'] += 1

        session['result'] = result

        if session['rounds_played'] >= MAX_ROUNDS:
            if session['player_score'] > session['computer_score']:
                final_result = "You are the overall winner!"
            elif session['player_score'] < session['computer_score']:
                final_result = "Computer is the overall winner!"
            else:
                final_result = "It's a draw overall!"
            session['final_result'] = final_result
            session['game_over'] = True
        else:
            session['final_result'] = None
            session['game_over'] = False

    return render_template('index.html',
                           player_score=session.get('player_score', 0),
                           computer_score=session.get('computer_score', 0),
                           rounds_played=session.get('rounds_played', 0),
                           max_rounds=MAX_ROUNDS,
                           player_choice=session.get('player_choice'),
                           computer_choice=session.get('computer_choice'),
                           result=session.get('result'),
                           final_result=session.get('final_result'),
                           game_over=session.get('game_over', False))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
