from flask import Flask, g, render_template, request
import sqlite3
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html")

@app.route('/submit/', methods=['POST', 'GET'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        insert_message(request)
        return render_template('submit.html', thanks=True)

@app.route('/view/')
def view():
    rand_messages = random_messages(5)
    return render_template('view.html', messages = rand_messages)

def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('messages_db.sqlite')
    cursor = g.message_db.cursor()
    cmd = "CREATE TABLE IF NOT EXISTS messages(id INTEGER, name TEXT, message TEXT);"
    cursor.execute(cmd)
    return g.message_db

def insert_message(request):
    name = request.form["name"]
    message = request.form["message"]

    db = get_message_db()
    cursor = db.cursor()

    ID = cursor.execute("SELECT COUNT(*) FROM messages;").fetchone()[0] + 1
    db.execute(f'INSERT INTO messages (ID, handle, message) VALUES ({ID}, "{name}", "{message}")')
    
    db.commit()
    db.close()


def random_messages(n):
    db = get_message_db()
    rand_messages = db.execute(f'SELECT handle, message FROM messages ORDER BY RANDOM() LIMIT {n}').fetchall()
    db.close()
    return rand_messages