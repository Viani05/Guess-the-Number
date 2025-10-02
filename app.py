from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

MAX_SCORE = 100
PENALTY = 10

def reset_game():
    session['number'] = random.randint(1, 100)
    session['tries'] = 0
    session['score'] = MAX_SCORE

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Simple hardcoded check
        if username == 'player' and password == '1234':
            session['user'] = username
            return redirect(url_for('index'))
        else:
            message = 'Invalid credentials. Try again.'
    return render_template('login.html', message=message)

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user' not in session:
        return redirect(url_for('login'))

    number = session.get('number')
    tries = session.get('tries', 0)
    score = session.get('score', MAX_SCORE)

    if number is None:
        reset_game()
        number = session['number']

    message = ''

    if request.method == 'POST':
        guess = int(request.form['guess'])
        tries += 1
        score -= PENALTY

        if guess < number:
            message = 'Too low!'
        elif guess > number:
            message = 'Too high!'
        else:
            message = f'🎉 Correct! You guessed it in {tries} tries. Your score: {score}'
            session.clear()
            return render_template('index.html', message=message, score=score)

        if score <= 0:
            message = f'😢 Game over! You ran out of points. The number was {number}.'
            session.clear()
            return render_template('index.html', message=message, score=0)

        session['tries'] = tries
        session['score'] = score

    return render_template('index.html', message=message, score=score)

if __name__ == '__main__':
    app.run(debug=True)