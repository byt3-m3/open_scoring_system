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
