from database import QuizDB

db = QuizDB(host=config.REDIS_HOST, port=config.REDIS_PORT)

class Quiz(Base):
    def __init__(self, id):
        self.id = id

    QUESTION_HASH = "{0}:question".format(self.id)
    ANSWER_HASH = "{0}:answer".format(self.id)

    def new_card(self, question, answer):

        assert db.hlen(QUESTION_HASH) == db.hlen(ANSWER_HASH)

        q_id = max([int(i) for i in db.hkeys(QUESTION_HASH)]) + 1
        db.hset(QUESTION_HASH, q_id, question)
        db.hset(ANSWER_HASH, q_id, answer)

    def delete_card(self, q_id):
        db.hdel(QUESTION_HASH, q_id)
        db.hdel(ANSWER_HASH, q_id)

    def update_question(self, q_id, updated_question):
        db.hset(QUESTION_HASH, q_id, updated_question)

    def update_answer(self, q_id, updated_answer):
        db.hset(ANSWER_HASH, q_id, updated_answer)
