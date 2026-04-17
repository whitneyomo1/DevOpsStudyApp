import time
import sqlite3
import random

def generate_quiz():
    conn = sqlite3.connect("flashcards.db")
    cursor = conn.cursor()

    # get flashcards
    cursor.execute("SELECT question, answer FROM flashcards")
    flashcards = cursor.fetchall()

    if len(flashcards) < 2:
        print("Not enough flashcards to generate quiz")
        conn.close()
        return

    # clear old quizzes
    cursor.execute("DELETE FROM quiz_questions")

    for q, a in flashcards:
        # pick a wrong answer
        # wrong_answers = [x[1] for x in flashcards if x[1] != a]
        # wrong = random.choice(wrong_answers)

        quiz_question = f"What is the meaning of '{q}'?"
        answer = f"Correct: {a}"

        cursor.execute(
            "INSERT INTO quiz_questions (question, answer) VALUES (?, ?)",
            (quiz_question, answer)
        )

    conn.commit()
    conn.close()
    print("Quiz generated!")

def run_worker():
    while True:
        print("Worker running: generating quiz...")
        generate_quiz()
        time.sleep(30)  # runs every 30 seconds

if __name__ == "__main__":
    run_worker()