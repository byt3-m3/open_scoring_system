from pymongo import MongoClient


# from scorekeeper.models.questions import Question

class Question:

    def __init__(self, event_id, **kwargs):

        self.q_id = kwargs.get("q_id")
        self.event_id = event_id
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


class EventsDB:
    def __init__(self, host):
        self._client = MongoClient(host)
        self.db = self._client['cyber_warrior']
        self.collections = self.db['cw_events']

    def get_event_questions(self, event_id):
        result = self.collections.find_one({"event_id": event_id})
        question_list = []
        for question in result['questions']:
            question_list.append(Question(event_id, **question))

        return question_list

    def get_event(self, event_id):
        result = self.collections.find_one({"event_id": event_id})
        return result
        # print(result['questions'])


class TeamsDB:

    def __init__(self, host):
        self._client = MongoClient(host)
        self.db = self._client['cyber_warrior']
        self.collections = self.db['cw_users']

    def update_data(self, team_name, doc):
        self.collections.update_one({"name": team_name}, {"$set": doc})

    def get_points(self, name):
        doc = self.get_team_doc(name)
        return doc['points']

    def get_team_doc(self, name):
        for doc in self.collections.find({"name": name}):
            return (doc)

    def add_responses(self, name, responses):
        doc = self.get_team_doc(name)
        if not doc['responses']:
            self.collections.update_one({"name": name}, {"$set": {"responses": responses}})
            return True
        else:
            raise Exception("'responses' Already Present for record '{}'".format(name))

    def get_responses(self, name):
        doc = self.get_team_doc(name)
        if doc.get("responses"):
            return doc['responses']
        else:
            return []

    def get_responses_by_event_id(self, team_name, event_id):
        doc = self.get_team_doc(team_name)
        if doc.get("responses"):
            event_responses = []
            for response in doc.get("responses"):

                if response.get("event_id") == event_id:
                    event_responses.append(response)

            return event_responses
        else:
            return []

    def get_response_by_event_id(self, team_name, event_id, q_id):
        resp = self.get_responses_by_event_id(team_name, event_id)
        for r in resp:
            if r['q_id'] == q_id:
                return r

    def incr_points(self, name, value):
        if isinstance(value, int):
            self.collections.update_one({"name": name}, {"$inc": {"points": value}})
            return True
        else:
            raise ValueError("Invalid Data Type")

    def reset_points(self, name):
        self.collections.update_one({"name": name}, {"$set": {"points": 0}})

    def reset_responses(self, name):
        doc = self.get_team_doc(name)
        if doc:
            doc['responses'] = []
            self.update_data(name, doc)
            self.reset_points(name)
            return True

        return False


    def add_team(self, name, passwd):
        doc = self._default_model()

        doc['name'] = name
        doc['passwd'] = passwd
        if self.get_team_doc(name):
            return False
        else:
            self.collections.insert_one(doc)
            return True

    def remove_team(self, name):
        if self.get_team_doc(name):
            self.collections.delete_one({"name": name})
            return True
        else:
            return False

        pass

    def _default_model(self):
        return {
            "name": "",
            "passwd": "",
            "responses": [],
            "points": 0
        }

    def make_response(self, **kwargs):
        return {
            "event_id": kwargs.get("event_id"),
            "q_id": kwargs.get("q_id"),
            "response": kwargs.get("response"),
            "result": kwargs.get("event_id"),
            "validated": kwargs.get("validated", False),
            "points_awarded": kwargs.get("points_awarded", False)
        }


if __name__ == '__main__':
    # E = EventsDB("192.168.99.100:27017")
    #
    # print(E.get_event("PCAP1"))

    t = TeamsDB("192.168.99.100:27017")

    t.reset_responses("team5")

    # print(t.remove_team("team1"))
    # print(t.remove_team("team2"))
    # print(t.remove_team("team3"))
    # print(t.remove_team("team4"))
    # print(t.remove_team("team5"))
    # print(t.add_team("team1", "team1"))
    # print(t.add_team("team2", "team2"))
    # print(t.add_team("team3", "team3"))
    # print(t.add_team("team4", "team4"))
    # print(t.add_team("team5", "team5"))

    # print(t.reset_points("team1"))

    # # Adding New Responses Test
    # resp_1 = t.make_response(event_id="PCAP1", q_id="PCAP1_1", response="", result="test")
    # resp_2 = t.make_response(event_id="PCAP1", q_id="PCAP1_2", response="", result="test")
    # resp_3 = t.make_response(event_id="PCAP1", q_id="PCAP1_3", response="", result="test")
    # resp_4 = t.make_response(event_id="PCAP1", q_id="PCAP1_4", response="", result="test")
    # print(t.add_responses("team1", [resp_1, resp_2, resp_3, resp_4]))
    # print(t.add_responses("team2", [resp_1, resp_2, resp_3, resp_4]))
    # print(t.add_responses("team3", [resp_1, resp_2, resp_3, resp_4]))
    # print(t.add_responses("team4", [resp_1, resp_2, resp_3, resp_4]))
    # print(t.add_responses("team5", [resp_1, resp_2, resp_3, resp_4]))

    # print(t.get_team_doc("team1"))
    # print(t.get_responses("team1"))
    # res = t.collections.find({"responses": {"$elemMatch": {"q_id": "PCAP1_3"}}})
    # for i in res:
    #     print(i)
