from flask import Flask, render_template
from redis import StrictRedis
import random
import config

app = Flask(__name__)
app.debug = config.DEBUG

db = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)

@app.route('/')
def main():
    available_quizzes = db.smembers('quizzes')
    return render_template('templates/main.html', quizzes=available_quizzes)

@app.route('/quiz/start/<quiz_name>')
def start_quiz(quiz_name):
    return render_template('templates/quiz-start.html', quiz_name=quiz_name)

@app.route('/quiz/<quiz_name>')
def quiz(quiz_name):
    #FIXME: naive random implementation, needs to be score-weighted
    all_questions = db.hkeys(quiz_name)
    question = random.choice(all_questions)
    answer = db.hget(quiz_name, question)

    return render_template('templates/quiz.html', quiz_name=quiz_name,
            question=question, answer=answer)
