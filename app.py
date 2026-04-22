from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flashcards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
""")
    conn.commit()
    conn.close()
    
init_db()

@app.route("/")
def home():
    return redirect("/add")

@app.route("/add", methods=["GET", "POST"])
def add_flashcard():
    if request.method == "POST":
        word = request.form["word"]
        translation = request.form["translation"]  
        
        conn = sqlite3.connect("flashcards.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM flashcards WHERE question = ?", (word,))
        if cursor.fetchone():
            conn.close()
            message = "Word already added!"
            return render_template("add.html", message=message)
                                #    , message="This question already exists!")
                                
        cursor.execute("INSERT INTO flashcards (question, answer) VALUES (?, ?)", 
                        (word, translation))
        conn.commit()
        conn.close()  
        message = "Successfully added"
        logging.info("Add flashcard route called")
        return render_template("add.html", message=message)
    
    return render_template("add.html")

@app.route("/study")
def study():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer FROM flashcards")
    flashcards = cursor.fetchall()
    conn.close()
    
    return render_template("study.html", flashcards=flashcards)

@app.route("/delete/<int:id>", methods=["POST"])
def delete_flashcard(id):
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM flashcards WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/review")

@app.route("/review")
def review():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer FROM flashcards")
    flashcards = cursor.fetchall()
    conn.close()
    
    return render_template("review.html", flashcards=flashcards)

@app.route("/quiz")
def quiz():
    return render_template("quiz.html")

@app.route("/api/quiz")
def get_quiz():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM quiz_questions")
    data = cursor.fetchall()
    conn.close()

    return jsonify([
        {"question": r[0], "answer": r[1]}
        for r in data
    ])

@app.route("/api/flashcards", methods=["GET"])
def api_flashcards():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer FROM flashcards")
    data = cursor.fetchall()
    conn.close()

    flashcards = [
        {"id": row[0], "question": row[1], "answer": row[2]}
        for row in data
    ]

    return jsonify(flashcards)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

