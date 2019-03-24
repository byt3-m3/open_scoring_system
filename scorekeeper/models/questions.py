from couchdb import Server

db_server = Server("http://192.168.99.100:5984")
db_server.login("cyberadmin", "cyberadmin")

event_db = db_server['cw_events']


class Event:
    def __init__(self, event_id):
        self._event_id = event_id
        self.facts = {}

        self.questions = []
        self.responses = []
        self._get_event_facts()
        self._make_questions()
        self.question_count = len(self.questions)

    def test_func(self, data):
        return (data)

    def get_question_by_qid(self, qid):

        for i in self.questions:
            if i.q_id == qid:
                return i

    @staticmethod
    def get_event_by_event_id(event_id):
        result = event_db.view("query/by_name", startkey=event_id, endkey=event_id, include_docs=True)
        if len(result.rows) == 1:
            data = result.rows.pop()
            return data['doc']

    def _make_questions(self):
        questions = self._get_questions()
        for question in questions:
            q = Question()
            q.q_id = question['q_id']
            q.text = question['question']
            q.answer = question['answer']

            self.questions.append(q)

    def _get_questions(self):
        result = event_db.view("query/by_name", startkey=self._event_id, endkey=self._event_id, include_docs=True)
        if len(result.rows) == 1:
            data = result.rows.pop()
            return data['doc']['questions']

    def _get_event_facts(self):
        result = event_db.view("query/by_name", startkey=self._event_id, endkey=self._event_id, include_docs=True)
        if len(result.rows) == 1:
            data = result.rows.pop()
            self.facts = data['doc']


class Question:

    def __init__(self, *args, **kwargs):

        self.q_id = kwargs.get("q_id")
        self.event_id = kwargs.get("event_id")
        self._answer = kwargs.get("answer")
        self._text = kwargs.get("text")
        self._point_value = kwargs.get("point_value", 0)

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value):
        self._answer = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value

    @property
    def point_value(self):
        return self._point_value

    @point_value.setter
    def point_value(self, value):
        if isinstance(value, int):
            self._point_value = value
        else:
            raise Exception("Invalid Data Type, Must be Int")

    def validate(self, resp):
        if self.answer == resp:
            return True
        else:
            return False

    def __dict__(self):
        return {
            "text": self.text,
            "answer": self.answer,
            "point_value": self.point_value,
            "event_id": self.event_id,
            "q_id": self.q_id
        }

    def __repr__(self):
        return f"<Question(question={self.text})>"



