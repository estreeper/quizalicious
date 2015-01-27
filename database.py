from redis import StrictRedis

class QuizDB(StrictRedis):
    def get_all_quizzes(self):
        return self.smembers('quiz')

    def get_question(self, quizid, questionid):
        return self.hget("{0}:question".format(quizid), questionid)

