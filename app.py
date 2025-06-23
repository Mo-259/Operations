from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(__name__)
app.secret_key = 'change-this-secret'

# Dummy users for demo purposes
USERS = {
    'agent1': {'password': 'pass', 'role': 'agent'},
    'admin1': {'password': 'pass', 'role': 'admin'}
}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = USERS.get(username)
        if user and user['password'] == password:
            session['user'] = {'username': username, 'role': user['role']}
            if user['role'] == 'agent':
                return redirect(url_for('agent_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/agent')
def agent_dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'agent':
        return redirect(url_for('login'))
    return render_template('agent_dashboard.html', user=user)

@app.route('/admin')
def admin_dashboard():
    user = session.get('user')
    if not user or user.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template('admin_dashboard.html', user=user)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
