from flask import Flask, render_template, request, url_for, flash, redirect
from redis import StrictRedis
from forms import AddQuizQuestion
from probchoice import ProbabalisticChoice
import random
import config

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY

db = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)
random_chooser = ProbabalisticChoice()

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
    hash_name = "{0}:questions".format(quiz_url_name)
    all_questions = db.hkeys(hash_name)

    # Collect the information needed for probabalisticchoice function
    #FIXME set up proper users rather than using the config file
    #FIXME oh no, very very ugly! define somewhere else, get db logic out!
    correct_sset = "{0}:correct:{1}".format(quiz_url_name, config.USERNAME)
    incorrect_sset = "{0}:incorrect:{1}".format(quiz_url_name, config.USERNAME)
    scores_sset = "{0}:scores:{1}".format(quiz_url_name, config.USERNAME)
    probs_sset = "{0}:probs:{1}".format(quiz_url_name, config.USERNAME)
    quiz_name = db.hget(quiz_url_name, 'quiz_name')
    # this will initialize the questions in the sorted set if they are not there or do nothing if they are
    for q in all_questions:
        db.zincrby(scores_sset, q, amount=0)

    if request.args.get('answer') == 'correct':
        db.zincrby(scores_sset, question, amount=1)
    if request.args.get('answer') == 'incorrect':
        db.zincrby(scores_sset, question, amount=-1)

    # calculate the probabilities
    #FIXME all this should be migrated out too
    multiplier = config.MULTIPLIER

    pairs = db.zrange(probs_sset, -1, -1, withscores=True)
    question = random_chooser.probabalisticchoice(pairs)

    answer = db.hget(hash_name, question)
    


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
