from flask import Flask, render_template, request, url_for, flash, redirect
from redis import StrictRedis
from forms import AddQuizQuestion
import random
import config

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY

db = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)

@app.route('/')
def main():
    available_quizzes = db.smembers('quizzes')
    return render_template('main.html', quizzes=available_quizzes)

@app.route('/quiz/start/<quiz_url_name>')
def start_quiz(quiz_url_name):
    description, created_by, quiz_name = db.hmget(quiz_url_name, 
            'description', 'created_by', 'quiz_name')
    return render_template('quiz-start.html', quiz_name=quiz_name,
            description=description, created_by=created_by,
            quiz_url_name=quiz_url_name)

@app.route('/quiz/<quiz_url_name>')
def quiz(quiz_url_name):
    #FIXME: naive random implementation, needs to be score-weighted
    hash_name = "{0}:questions".format(quiz_url_name)
    all_questions = db.hkeys(hash_name)
    question = random.choice(all_questions)
    answer = db.hget(hash_name, question)
    quiz_name = db.hget(quiz_url_name, 'quiz_name')

    return render_template('quiz.html', quiz_name=quiz_name,
            question=question, answer=answer, 
            quiz_url_name=quiz_url_name)

@app.route('/quiz/<quiz_url_name>/add/question', methods=['GET', 'POST'])
def add_question(quiz_url_name):
    hash_name = "{0}:questions".format(quiz_url_name)
    form = AddQuizQuestion(request.form)
    error=[]
    if request.method == 'POST':
        if form.validate():
            question = form.question.data
            answer = form.answer.data
            db.hset(hash_name, question, answer)
            flash("Question added!")
            return redirect('/quiz/{0}/add/question'.format(quiz_url_name))
        else:
            flash("It's no good! Check errors below.")
            error=form.errors

    return render_template('add_question.html', form=form, error=error,
                            quiz_url_name=quiz_url_name)


if __name__ == '__main__':
    app.run()
