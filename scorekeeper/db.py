import time
from datetime import datetime
from pprint import pprint

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

    def get_game_list(self):
        doc = self.collections.find_one({'event_id': "GAME_LIST"})

        return doc['artifacts']['events']

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

    def get_teams_positions(self):
        docs = self.get_all_docs()
        if len(docs) > 0:
            return sorted(docs, key=lambda i: i['points'], reverse=True)
        else:
            return docs

    def get_all_docs(self):
        _docs = self.collections.find({})
        docs = []
        if _docs:
            for doc in _docs:
                del doc['responses']
                del doc['passwd']
                del doc['_id']
                docs.append(doc)
            return docs
        else:
            return []

        pass

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

    def reset_all_responses(self):
        docs = self.get_all_docs()
        if len(docs) > 0:
            for doc in docs:
                self.reset_responses(doc['name'])
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


class BuzzerTrackerDB:
    def __init__(self, host):
        self._client = MongoClient(host)
        self.db = self._client['cyber_warrior']
        self.collections = self.db['cw_buzzer_tracker']

    def get_responses(self):
        """
        Returns a list of responses from the database.

        :return:
        """
        _docs = self.collections.find({})

        docs = []
        for i in _docs:
            docs.append(i)

        return docs

    def reset(self):
        """
        Clears all records from the database.

        :return:
        """
        docs = self.get_responses()
        if docs:
            for doc in docs:
                self.remove_response(doc['team_name'])
            return True

        return False

    def buzzed(self, doc):
        """
        Takes the users buzzer submission, applies the time stamp and pushes to the datebase.

        :param team_name:
        :return:
        """
        if self.get_response(doc['team_name']):
            self.remove_response(doc['team_name'])

        timestamp = time.time()
        _time = datetime.now()

        doc['time_stamp'] = float(timestamp)
        doc['time'] = str(_time)
        doc['submitted'] = True

        resp_example = {
            "team_name": doc['team_name'],
            "response": "",
            "time_stamp": float(timestamp),
            "time": str(_time),
            "submitted": True
        }

        if self.add_response(doc):
            return True
        else:
            return False

    def get_positions(self):
        """
        Retrieves all responses and sorts them by the time stamp.

        :return:
        """

        docs = self.get_responses()
        result = sorted(docs, key=lambda i: i['time_stamp'])
        from pprint import pprint
        pprint(result)

    def add_response(self, doc):
        if not self.get_response(doc['team_name']):
            self.collections.insert_one(doc)
            return True

        return False

    def remove_response(self, team_name):
        if self.get_response(team_name):
            self.collections.find_one_and_delete({"team_name": team_name})
            return True

        return False

    def get_response(self, team_name):
        doc = self.collections.find_one({"team_name": team_name})
        if doc:
            return doc

    def is_submitted(self, team_name):
        doc = self.collections.find_one({"team_name": team_name})
        if doc:
            if doc['submitted']:
                return True
            return False

        return False

    def is_present(self, team_name):
        if self.get_response(team_name):
            return True
        else:
            return False


def events_test():
    e = EventsDB("192.168.99.100:27017")

    print(e.get_game_list())


def test_teams_class_2():
    t = TeamsDB("192.168.99.100:27017")
    pprint(t.reset_all_responses())


def test_teams_class():
    t = TeamsDB("192.168.99.100:27017")
    t.reset_responses("team5")
    print(t.remove_team("team1"))
    print(t.remove_team("team2"))
    print(t.remove_team("team3"))
    print(t.remove_team("team4"))
    print(t.remove_team("team5"))
    print(t.add_team("team1", "team1"))
    print(t.add_team("team2", "team2"))
    print(t.add_team("team3", "team3"))
    print(t.add_team("team4", "team4"))
    print(t.add_team("team5", "team5"))

    print(t.reset_points("team1"))

    # Adding New Responses Test
    resp_1 = t.make_response(event_id="PCAP1", q_id="PCAP1_1", response="", result="test")
    resp_2 = t.make_response(event_id="PCAP1", q_id="PCAP1_2", response="", result="test")
    resp_3 = t.make_response(event_id="PCAP1", q_id="PCAP1_3", response="", result="test")
    resp_4 = t.make_response(event_id="PCAP1", q_id="PCAP1_4", response="", result="test")
    print(t.add_responses("team1", [resp_1, resp_2, resp_3, resp_4]))
    print(t.add_responses("team2", [resp_1, resp_2, resp_3, resp_4]))
    print(t.add_responses("team3", [resp_1, resp_2, resp_3, resp_4]))
    print(t.add_responses("team4", [resp_1, resp_2, resp_3, resp_4]))
    print(t.add_responses("team5", [resp_1, resp_2, resp_3, resp_4]))


def test_buzzer_class():
    buzzer_db = BuzzerTrackerDB("192.168.99.100:27017")
    # print(buzzer_db.is_submitted("team5"))
    # print(buzzer_db.get_response("team5"))
    # print(buzzer_db.get_responses())
    team_names = ['team1', 'team2', 'team3', 'team4', 'team5']

    # for team in team_names:
    #     resp_example = {
    #         "team_name": team,
    #         "response": "",
    #         "time_stamp": 0,
    #         "submitted": True
    #     }
    #     print(buzzer_db.add_response(resp_example))
    buzzer_db.buzzed("team2")
    buzzer_db.buzzed("team1")

    buzzer_db.buzzed("team3")
    buzzer_db.buzzed("team4")
    buzzer_db.buzzed("team5")

    buzzer_db.get_positions()


if __name__ == '__main__':
    events_test()
