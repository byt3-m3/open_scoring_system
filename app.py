import json

from flask import Flask, render_template, request, session, redirect, url_for, g, Response

from scorekeeper.db import TeamsDB, EventsDB, BuzzerTrackerDB
from scorekeeper.forms import LoginForm

# TODO: Establishes connection the  Monogo Databases
team_db = TeamsDB("192.168.99.100:27017")
event_db = EventsDB("192.168.99.100:27017")
buzzer_db = BuzzerTrackerDB("192.168.99.100:27017")

JSON_RESPONSE_HEADERS = {'content-type': 'application/json; charset=utf-8'}


def validate_user(uname, password):
    """
    This function provides User validation for the specified username and password.

    :param uname:
    :param password:
    :return: True if user is authenticated, else False.
    """
    if team_db.get_team_doc(uname):
        doc = team_db.get_team_doc(uname)
        if doc['passwd'] == password:
            return True

    return False


app = Flask(__name__)

# app.config['SECRET_KEY'] = os.urandom(24)
app.config['SECRET_KEY'] = "MY_KEY"


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()

    # Runs if Form is submitted and posted
    if login_form.validate_on_submit():
        form = request.form
        user = form['username']
        passwd = form['password']

        result = validate_user(user, passwd)
        # TODO: Runs if the User validation fails
        if result is False:
            return redirect(url_for('login'))

        session['username'] = user

        return redirect(url_for('home', username=user, token=session['csrf_token']))

    return render_template('login.j2', form=login_form)


@app.route('/home')
def home():
    # TODO: Extracts the session and team object from the request.

    team_doc = team_db.get_team_doc(session['username'])
    sorted_docs = team_db.get_teams_positions()

    new_docs = []
    for indx, doc in enumerate(sorted_docs):
        doc['index'] = indx + 1
        new_docs.append(doc)

    return render_template("index.j2", team_data=team_doc, sorted_docs=new_docs)


@app.route('/')
def index():
    if session.get("username"):
        if session['username'] == "ringmaster":
            return redirect(url_for("ringmaster"))

    if g.user:
        return redirect(url_for("home"))

    return redirect(url_for('login'))


@app.route('/pcap1', methods=['GET', 'POST'])
def pcap1():
    event_data = event_db.get_event("PCAP1")

    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP1')

    event_questions = event_db.get_event_questions("PCAP1")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("pcap1.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/pcap2', methods=['GET', 'POST'])
def pcap2():
    event_data = event_db.get_event("PCAP2")

    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP2')
    event_questions = event_db.get_event_questions("PCAP2")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("pcap1.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/pcap3', methods=['GET', 'POST'])
def pcap3():
    event_data = event_db.get_event("PCAP3")
    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP3')
    event_questions = event_db.get_event_questions("PCAP3")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("pcap1.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route("/opcyberjustice")
def opcyberjustice():
    event_data = event_db.get_event("OCJ")

    event_responses = team_db.get_responses_by_event_id(session['username'], 'OCJ')
    event_questions = event_db.get_event_questions("OCJ")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("pcap1.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/buzzer', methods=['GET', 'POST'])
def buzzer():
    event_data = event_db.get_event("PCAP3")
    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP3')
    event_questions = event_db.get_event_questions("PCAP3")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("buzzer.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/ringmaster', methods=['GET'])
def ringmaster():
    team_doc = team_db.get_team_doc(session['username'])
    games_list = event_db.get_game_list()

    docs = team_db.get_all_docs()

    return render_template("ringmaster.j2", team_data=team_doc, games_list=games_list, team_docs=docs)


# Routes used for FrontEnd data calls
@app.route("/getscore")
def getscore():
    """
    Gets the users scores from the database.

    :return str: string representation of the front end.
    """
    JSON_RESPONSE_HEADERS = {'content-type': 'application/json; charset=utf-8'}

    points = team_db.get_points(session['username'])
    # return Response()
    return Response(str(points))


@app.route("/validate_resp", methods=['POST', 'GET'])
def validate_resp():
    """
    This Endpoints preforms validation for the user input provided by the frontend.
    :return:
    """

    data = request.form

    user_resp = data['response']
    event_id = data['event_id']
    q_id = data['q_id']

    questions = event_db.get_event_questions(event_id)
    team_obj = team_db.get_team_doc(session['username'])

    for question in questions:

        if question.validate(user_resp):

            if question.q_id == q_id:

                single_resp = team_db.get_response_by_event_id(session['username'], event_id, q_id)
                print(single_resp)
                # Triggers if the q_id is already present in the response list
                if single_resp:
                    if single_resp['q_id'] == q_id:

                        if single_resp['points_awarded']:

                            return Response(json.dumps({"result": True}), status=200, headers=JSON_RESPONSE_HEADERS)

                        else:
                            single_resp['response'] = user_resp
                            team_obj['points'] += int(question.point_value)
                            # team_db.incr_points(session['username'], int(question.point_value))
                            single_resp['points_awarded'] = True
                            team_db.update_data(session['username'], team_obj)
                            del team_obj
                            return Response(json.dumps({"result": True}), status=200, headers=JSON_RESPONSE_HEADERS)
                    else:

                        new_response = {
                            "event_id": event_id,
                            "q_id": q_id,
                            "response": user_resp,
                            "points_awarded": True
                        }
                        team_obj['points'] += int(question.point_value)
                        team_obj['responses'].append(new_response)

                        team_db.update_data(session['username'], team_obj)
                        del team_obj
                        return Response(json.dumps({"result": True}), status=200, headers=JSON_RESPONSE_HEADERS)
                else:
                    new_response = {
                        "event_id": event_id,
                        "q_id": q_id,
                        "response": user_resp,
                        "points_awarded": True
                    }
                    team_obj['points'] += int(question.point_value)
                    team_obj['responses'].append(new_response)
                    print("Bad Hit")

                    team_db.update_data(session['username'], team_obj)
                    del team_obj
                    return Response(json.dumps({"result": True}), status=200, headers=JSON_RESPONSE_HEADERS)
                    print("Bad sssHit")

    return Response(json.dumps({"result": False}), status=200, headers=JSON_RESPONSE_HEADERS)


@app.route('/dropsession')
def dropsession():
    """
    This endpoint drops the users active session.
    :return:
    """
    session.pop('username', None)
    return redirect(url_for("login"))


@app.route('/rest_response')
def reset_response():
    if team_db.reset_responses(session['username']):
        return Response

    return Response


@app.route('/buzzed', methods=['POST'])
def buzzed():
    data = request.form
    team_name = session['username']
    user_resp = data['user_resp']

    resp_example = {
        "team_name": team_name,
        "response": user_resp,
        "time_stamp": 0.0,
        "time": "",
        "submitted": False
    }

    result = buzzer_db.buzzed(resp_example)

    return Response(json.dumps({"result": result}), status=200, headers=JSON_RESPONSE_HEADERS)


@app.route('/buzzer_clear', methods=['POST'])
def buzzer_clear():
    team_name = session['username']
    if buzzer_db.remove_response(team_name):
        return Response(json.dumps({"result": True}), status=200, headers=JSON_RESPONSE_HEADERS)

    return Response(json.dumps({"result": False}), status=200, headers=JSON_RESPONSE_HEADERS)


@app.route('/buzzer_load', methods=['POST'])
def buzzer_load():
    team_name = session['username']
    if buzzer_db.is_present(team_name):
        doc = buzzer_db.get_response(team_name)
        del doc['_id']
        print(doc)
        return Response(json.dumps({"doc": doc, "result": True}), status=200, headers=JSON_RESPONSE_HEADERS)

    return Response(json.dumps({"result": False, "doc": None}), status=200, headers=JSON_RESPONSE_HEADERS)


@app.route("/register", methods=['POST'])
def register():
    """
    Registers a new team to the database. Checks if the team is already present, will not over right if True.

    :return:
    """
    data = request.json

    name = data.get("name")
    passwd = data.get("passwd")
    if team_db.add_team(name, passwd):
        return Response(json.dumps({"msg": f'User: "{name}" has been created', "result": True}), status=200,
                        headers=JSON_RESPONSE_HEADERS)

    else:
        return Response(json.dumps({"msg": "User Already Present in Database", "result": False}), status=200, headers=JSON_RESPONSE_HEADERS)

@app.route("/unregister", methods=['POST'])
def unregister():
    data = request.json
    name = data.get("name")
    if team_db.remove_team(name):
        return Response(json.dumps({"msg": f'User: "{name}" has been removed', "result": True}), status=200,
                        headers=JSON_RESPONSE_HEADERS)
    print(name)

    return Response(json.dumps({"msg": "Nothing to remove", "result": False}), status=200, headers=JSON_RESPONSE_HEADERS)

@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
