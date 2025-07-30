from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = c.fetchall()
    conn.close()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        conn = sqlite3.connect('expense.db')
        c = conn.cursor()
        c.execute("INSERT INTO expenses (title, amount, category, date) VALUES (?, ?, ?, ?)",
                  (title, amount, category, date))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    if request.method == 'POST':
        title = request.form['title']
        amount = request.form['amount']
        category = request.form['category']
        date = request.form['date']
        c.execute("UPDATE expenses SET title=?, amount=?, category=?, date=? WHERE id=?",
                  (title, amount, category, date, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    c.execute("SELECT * FROM expenses WHERE id=?", (id,))
    expense = c.fetchone()
    conn.close()
    return render_template('edit.html', expense=expense)

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('expense.db')
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
