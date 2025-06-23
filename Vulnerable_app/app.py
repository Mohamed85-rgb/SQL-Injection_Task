from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# In-memory database for simplicity
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    password TEXT
                )''')
    c.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        # ⚠️ Vulnerable query (no sanitization!)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print("[DEBUG] Executing query:", query)
        c.execute(query)
        result = c.fetchone()
        conn.close()

        if result:
            message = '✅ Login successful!'
        else:
            message = '❌ Invalid credentials.'

    # Simple inline HTML for quick testing
    return render_template_string('''
        <h2>Vulnerable Login</h2>
        <form method="post">
            Username: <input type="text" name="username"/><br><br>
            Password: <input type="text" name="password"/><br><br>
            <input type="submit" value="Login"/>
        </form>
        <p>{{ message }}</p>
    ''', message=message)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
