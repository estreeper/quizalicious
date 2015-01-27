from redis import StrictRedis

class QuizDB(StrictRedis):
    def get_all_quizzes(self):
        return self.smembers('quiz')
