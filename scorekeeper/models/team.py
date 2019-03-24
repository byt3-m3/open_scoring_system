from couchdb import Server
import json
# TODO: Connects to CouchDB server.
db_server = Server("http://192.168.99.100:5984")
db_server.login("cyberadmin", "cyberadmin")

# TODO: Establishes connection the  Databases
user_db = db_server['cw_users']


class Team:
    def __init__(self, **kwargs):
        # doc = get_doc_from_db(name)

        self._id = kwargs.get("_id")
        self._rev = kwargs.get("_rev")
        self.name = kwargs.get("name")
        self._passwd = kwargs.get("passwd")
        self.points = kwargs.get("points", 0)
        self.responses = kwargs.get("responses", [])

        self.questions = list()

    def __dict__(self):
        return {
            "_id": self._id,
            "name": self.name,
            "passwd": self._passwd,
            "responses": self.responses,
            "points": self.points,
        }

    def add_response(self, response):
        self.responses.append(response)

    def get_response(self, q_id):
        pass

    def get_responses(self):
        return self.responses

    def update(self):

        doc = get_doc_from_db(self.name)
        # print(doc)
        # print("\n", doc)
        data = self.__dict__().update(doc)
        # self.__dict__()['_rev'] = get_doc_rev(self._id)
        doc["responses"].append(*self.responses)

        # print(data)
        print(doc)

        user_db.save(doc)

    def increment_score(self, value):
        doc = get_doc_from_db(self.name)
        print(doc)

        doc['points'] = doc['points'] + value

        self._points = doc['points']

        user_db.save(doc)


def get_doc_rev(id):
    result = user_db.view("query/rev_by_id", startkey=id, endkey=id)
    for i in result.rows:
        return i.get("value")

def get_doc_from_db(name):
    result = user_db.view("query/by_name", startkey=name, endkey=name, include_docs=True)
    for i in result.rows:
        return i.get("doc")


class TeamResponse:
    def __init__(self):
        self.q_id = ""
        self.response = ""
        self.event_id = ""
        self.result = bool
        self.question = ""

    @staticmethod
    def make_response(event_id, q_id, response, question, result):
        t = TeamResponse()

        t.q_id = q_id
        t.event_id = event_id
        t.response = response
        t.question = question
        t.result = result

        return t

    def __dict__(self):
        return {
            "event_id": self.event_id,
            "q_id": self.q_id,
            "response": self.response,
            "result": self.result

        }
