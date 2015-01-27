from database import QuizDB
import config

db = QuizDB(host=config.REDIS_HOST, port=config.REDIS_PORT)

class Quiz:

    QUESTION_HASH = ''
    ANSWER_HASH = ''

    def __init__(self, id):
        self.id = id
        self.QUESTION_HASH = "{0}:question".format(self.id)
        self.ANSWER_HASH = "{0}:answer".format(self.id)

    def new_card(self, question, answer):

        assert db.hlen(self.QUESTION_HASH) == db.hlen(self.ANSWER_HASH)

        questions = db.hkeys(self.QUESTION_HASH)
        if len(questions) > 0:
            q_id = max([int(i) for i in db.hkeys(self.QUESTION_HASH)]) + 1
        else:
            q_id = 0
        db.hset(self.QUESTION_HASH, q_id, question)
        db.hset(self.ANSWER_HASH, q_id, answer)

    def delete_card(self, q_id):
        db.hdel(self.QUESTION_HASH, q_id)
        db.hdel(self.ANSWER_HASH, q_id)

    def update_question(self, q_id, updated_question):
        db.hset(self.QUESTION_HASH, q_id, updated_question)

    def update_answer(self, q_id, updated_answer):
        db.hset(self.ANSWER_HASH, q_id, updated_answer)
