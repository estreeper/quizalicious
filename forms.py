from wtforms import Form, TextField, TextAreaField, validators

class AddQuiz(Form):
    title = TextField('Name of quiz', [validators.Length(max=60), 
                                        validators.required()])
    creator = TextField('Creator', [validators.Length(max=200)])

class AddQuizQuestion(Form):
    question = TextAreaField('Question', [validators.required(),
                                        validators.Length(max=5000)])
    answer = TextAreaField('Answer', [validators.required(),
                                        validators.Length(max=5000)])
