from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_socketio import SocketIO, send
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.permanent_session_lifetime = timedelta(days=1)
socketio = SocketIO(app)

# Fixed security code
SECURITY_CODE = "paris"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        code = request.form['code']
        if code == SECURITY_CODE:
            session.permanent = True
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            flash("Invalid security code. Please try again.")
    return render_template('login.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html', username=session['username'])

@socketio.on('message')
def handle_message(msg):
    username = session.get('username', 'Anonymous')
    send(f"{username}: {msg}", broadcast=True)
# Just testing commit for Render deployment

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

