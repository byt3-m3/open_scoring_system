import argparse
import json

from flask import Flask, render_template, request, session, redirect, url_for, g, Response

from scorekeeper.const import (JSON_RESPONSE_HEADERS,
                               STATUS_201_CREATED,
                               STATUS_417_EXPECTATION_FAILED,
                               STATUS_200_SUCCESS,
                               STATUS_400_BAD_REQUEST)
from scorekeeper.db import TeamsDB, EventsDB, BuzzerTrackerDB
from scorekeeper.forms import LoginForm

# TODO: Establishes connection the  MongoDB Servers
team_db = TeamsDB("192.168.99.100:27017")
event_db = EventsDB("192.168.99.100:27017")
buzzer_db = BuzzerTrackerDB("192.168.99.100:27017")


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
    if g.user:
        return redirect(url_for("home"))

    return redirect(url_for('login'))


@app.route("/monitor")
def monitor():
    team_doc = team_db.get_team_doc(session['username'])
    return render_template("monitor.j2", team_data=team_doc)


@app.route('/pcap1', methods=['GET', 'POST'])
def pcap1():
    event_data = event_db.get_event("PCAP1")

    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP1')

    event_questions = event_db.get_event_questions("PCAP1")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("event_template.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/pcap2', methods=['GET', 'POST'])
def pcap2():
    event_data = event_db.get_event("PCAP2")

    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP2')
    event_questions = event_db.get_event_questions("PCAP2")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("event_template.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/pcap3', methods=['GET', 'POST'])
def pcap3():
    event_data = event_db.get_event("PCAP3")
    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP3')
    event_questions = event_db.get_event_questions("PCAP3")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("event_template.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route("/opcyberjustice")
def opcyberjustice():
    event_data = event_db.get_event("OCJ")

    event_responses = team_db.get_responses_by_event_id(session['username'], 'OCJ')
    event_questions = event_db.get_event_questions("OCJ")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("event_template.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/buzzer', methods=['GET', 'POST'])
def buzzer():
    event_data = event_db.get_event("PCAP3")
    event_responses = team_db.get_responses_by_event_id(session['username'], 'PCAP3')
    event_questions = event_db.get_event_questions("PCAP3")

    team_doc = team_db.get_team_doc(session['username'])

    return render_template("buzzer.j2", team_data=team_doc, questions=event_questions, event_data=event_data,
                           event_responses=event_responses)


@app.route('/pcapoverview', methods=['GET'])
def pcapoverview():
    team_doc = team_db.get_team_doc(session['username'])

    return render_template("pcapoverview.j2", team_data=team_doc)
    pass


@app.route('/ringmaster', methods=['GET'])
def ringmaster():
    team_doc = team_db.get_team_doc(session['username'])
    games_list = event_db.get_game_list()

    docs = team_db.get_all_docs()

    return render_template("ringmaster.j2", team_data=team_doc, games_list=games_list, team_docs=docs)


@app.route('/instructions')
def instructions():
    team_doc = team_db.get_team_doc(session['username'])
    return render_template("instructions.j2", team_data=team_doc)


@app.before_request
def before_request():
    g.user = None
    if 'username' in session:
        g.user = session['username']


### API Endpoints used for FrontEnd data calls ###
@app.route("/api/v1/getteamscore", methods=['POST'])
def getteamscore():
    """
    Gets the current score for the specified team

    :return
    """
    data = request.json

    if isinstance(team_db.get_points(data.get('name')), int):
        points = team_db.get_points(data.get('name'))

        return Response(json.dumps({"name": data.get("name"), "points": points}),
                        status=STATUS_200_SUCCESS,
                        headers=JSON_RESPONSE_HEADERS)

    return Response(json.dumps({"name": data.get("name"), "msg": f"Error finding team"}),
                    status=STATUS_400_BAD_REQUEST,
                    headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/validate_response", methods=['POST'])
def validate_response():
    data = request.json
    response = data.get("response")
    name = data.get("name")
    q_id = data.get("q_id")
    event_id = data.get("event_id")

    if not team_db.get_team_doc(name):
        return Response(json.dumps({"result": False, "msg": "Invalid Team Name"}),
                        status=STATUS_400_BAD_REQUEST,
                        headers=JSON_RESPONSE_HEADERS)

    question = event_db.get_question(event_id, q_id)
    if question:
        if question.get("answer"):
            if question.get("answer") == response:

                cached_resp = team_db.get_response_by_event_id(name, event_id, q_id)

                if cached_resp:
                    if cached_resp['points_awarded']:
                        return Response(json.dumps({"result": True, "msg": "Points Already Awarded"}),
                                        status=STATUS_200_SUCCESS,
                                        headers=JSON_RESPONSE_HEADERS)

                team_obj = team_db.get_team_doc(name)

                new_response = {
                    "event_id": event_id,
                    "q_id": q_id,
                    "response": response,
                    "points_awarded": True,
                    "point_value": question['point_value']
                }

                team_obj['responses'].append(new_response)
                team_obj['points'] += int(question['point_value'])
                team_db.update_data(name, team_obj)

                return Response(json.dumps({"result": True, "msg": "Correct"}),
                                status=STATUS_200_SUCCESS,
                                headers=JSON_RESPONSE_HEADERS)
            else:
                return Response(json.dumps({"result": False, "msg": "Incorrect"}),
                                status=STATUS_200_SUCCESS,
                                headers=JSON_RESPONSE_HEADERS)

    return Response(json.dumps({"result": False, "msg": "Event not Found"}),
                    status=STATUS_417_EXPECTATION_FAILED,
                    headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/new_response", methods=['POST'])
def new_response():
    if request.json:
        data = request.json

    if not event_db.get_event(data.get("event_id")):
        return Response(json.dumps({"result": False, "msg": f"Invalid event_id provided"}),
                        status=STATUS_417_EXPECTATION_FAILED,
                        headers=JSON_RESPONSE_HEADERS)

    new_response = {
        "team_name": data['team_name'],
        "event_id": data['event_id'],
        "q_id": data['q_id'],
        "response": data['response'],
        "point_value": data['point_value']
    }
    if team_db.get_team_doc(new_response.get("team_name")):
        ## TODO: Adds new response to team.
        try:
            if team_db.add_response(new_response.get("team_name"), new_response):
                return Response(json.dumps({"result": True, "msg": "Response Successful"}),
                                status=STATUS_200_SUCCESS,
                                headers=JSON_RESPONSE_HEADERS)
        except Exception as err:

            return Response(json.dumps({"result": False, "msg": f"{str(err)}"}),
                            status=STATUS_400_BAD_REQUEST,
                            headers=JSON_RESPONSE_HEADERS)
    else:
        return Response(json.dumps({"result": False, "msg": f"Team {new_response.get('team_name')} does not exist"}),
                        status=STATUS_417_EXPECTATION_FAILED,
                        headers=JSON_RESPONSE_HEADERS)


@app.route('/api/v1/dropsession')
def dropsession():
    """
    This endpoint drops the users active session.
    :return:
    """
    session.pop('username', None)
    return redirect(url_for("login"))


@app.route('/api/v1/reset_response', methods=['POST'])
def reset_response():
    """
    Resets the responses and clear the points for the provided name.

    :return:
    """
    data = request.json

    try:
        name = data['name']
        if team_db.reset_responses(name):
            return Response(json.dumps({"msg": f'User: "{name}" responses have been cleared', "result": True}),
                            status=STATUS_200_SUCCESS,
                            headers=JSON_RESPONSE_HEADERS)
        else:
            return Response(json.dumps({"msg": f'User: "{name}" not found', "result": False}),
                            status=STATUS_417_EXPECTATION_FAILED,
                            headers=JSON_RESPONSE_HEADERS)

    except Exception as err:
        return Response(json.dumps({"msg": f'ERROR: {str(err)}', "result": False}),
                        status=STATUS_400_BAD_REQUEST,
                        headers=JSON_RESPONSE_HEADERS)


@app.route('/api/v1/team_buzzed', methods=['POST'])
def team_buzzed():
    """
    Creates buzzed record in the buzzer_tracker database. This function will timestamp each buzzed event.

    :return:
    """
    data = request.json

    try:

        team_name = data['team_name']
        user_resp = data['user_resp']

        resp_example = {
            "team_name": team_name,
            "response": user_resp,
            "time_stamp": 0.0,
            "time": "",
            "submitted": False
        }
        if not team_db.get_team_doc(team_name):
            return Response(json.dumps({"msg": f'not a valid team', "result": False}),
                            status=STATUS_400_BAD_REQUEST,
                            headers=JSON_RESPONSE_HEADERS)

        if buzzer_db.buzzed(resp_example):
            return Response(json.dumps({"msg": f'User: {team_name} buzz has been submitted', "result": True}),
                            status=STATUS_201_CREATED,
                            headers=JSON_RESPONSE_HEADERS)
        else:
            return Response(json.dumps({"msg": f'Unable process buzz', "result": False}),
                            status=STATUS_417_EXPECTATION_FAILED,
                            headers=JSON_RESPONSE_HEADERS)

    except Exception as err:

        return Response(json.dumps({"msg": f'ERROR: {str(err)}', "result": False}),
                        status=STATUS_400_BAD_REQUEST,
                        headers=JSON_RESPONSE_HEADERS)


@app.route('/api/v1/clear_buzz', methods=['POST'])
def clear_buzz():
    """
    Clears the buzz entry from the buzz tracker database.

    :return:
    """
    data = request.json

    try:
        name = data['name']
        if buzzer_db.remove_response(name):
            return Response(json.dumps({"msg": f'User: "{name}" buzzes cleared', "result": True}),
                            status=STATUS_200_SUCCESS,
                            headers=JSON_RESPONSE_HEADERS)
        else:
            return Response(json.dumps({"msg": f'Unable to clear buzz', "result": False}),
                            status=STATUS_417_EXPECTATION_FAILED,
                            headers=JSON_RESPONSE_HEADERS)

    except Exception as err:
        return Response(json.dumps({"msg": f'ERROR: {str(err)}', "result": False}),
                        status=STATUS_400_BAD_REQUEST,
                        headers=JSON_RESPONSE_HEADERS)


@app.route('/api/v1/reset_buzzers', methods=['GET'])
def reset_buzzers():
    if buzzer_db.reset():
        return Response(
            json.dumps({"msg": f'Successful', "data": None}),
            status=STATUS_200_SUCCESS,
            headers=JSON_RESPONSE_HEADERS)
    else:
        return Response(
            json.dumps({"msg": f'Nothing to Remove', "data": None}),
            status=STATUS_417_EXPECTATION_FAILED,
            headers=JSON_RESPONSE_HEADERS)


@app.route('/api/v1/buzzers', methods=['GET'])
def buzzers():
    sorted_docs = buzzer_db.get_positions()

    new_docs = []
    for indx, doc in enumerate(sorted_docs):
        doc['index'] = indx + 1
        del doc['_id']
        new_docs.append(doc)

    return Response(
        json.dumps({"msg": f'Successful', "data": new_docs}),
        status=STATUS_200_SUCCESS,
        headers=JSON_RESPONSE_HEADERS)
    pass


@app.route('/api/v1/onload_buzz_check', methods=['POST'])
def onload_buzz_check():
    try:
        data = request.json
        team_name = data['team_name']

        if buzzer_db.is_present(team_name):
            doc = buzzer_db.get_response(team_name)
            del doc['_id']
            return Response(json.dumps({"doc": doc, "result": True}),
                            status=STATUS_200_SUCCESS,
                            headers=JSON_RESPONSE_HEADERS)
        else:
            print(team_name)
            return Response(json.dumps({"doc": None, "result": False, "msg": f'{team_name} not found'}),
                            status=STATUS_417_EXPECTATION_FAILED,
                            headers=JSON_RESPONSE_HEADERS)

    except Exception as err:
        return Response(
            json.dumps({"doc": None, "err": str(err), "result": False, "msg": "unable to load user record"}),
            status=STATUS_400_BAD_REQUEST,
            headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/register", methods=['POST'])
def register():
    """
    Registers a new team to the database. Checks if the team is already present, will not over right if True.

    :return:
    """
    data = request.json

    name = data.get("name")
    passwd = data.get("passwd")
    alias = data.get("alias")
    if team_db.add_team(name, passwd, alias):
        return Response(json.dumps({"msg": f'User: "{name}" has been created', "result": True}),
                        status=STATUS_201_CREATED,
                        headers=JSON_RESPONSE_HEADERS)

    else:
        return Response(json.dumps({"msg": "User Already Present in Database", "result": False}),
                        status=STATUS_417_EXPECTATION_FAILED,
                        headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/unregister", methods=['POST'])
def unregister():
    data = request.json
    name = data.get("name")
    if team_db.remove_team(name):
        return Response(json.dumps({"msg": f'User: "{name}" has been removed', "result": True}),
                        status=STATUS_200_SUCCESS,
                        headers=JSON_RESPONSE_HEADERS)

    return Response(json.dumps({"msg": "Nothing to remove", "result": False}), status=STATUS_417_EXPECTATION_FAILED,
                    headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/new_event", methods=['POST'])
def new_event():
    """
    Adds a new event to the database.

    :return:
    """
    data = request.json

    if event_db.add_event(doc=data):
        return Response(json.dumps({"msg": f'Event: "{data.get("event_id")}" has been created', "result": True}),
                        status=STATUS_201_CREATED,
                        headers=JSON_RESPONSE_HEADERS)
    else:
        return Response(json.dumps({"msg": f'Event: "{data.get("event_id")}" Already Exist', "result": False}),
                        status=417,
                        headers=STATUS_417_EXPECTATION_FAILED)


@app.route("/api/v1/new_event_questions", methods=['POST'])
def new_event_questions():
    """
    Adds new questions to the supplied event ID.

    :return:
    """
    data = request.json

    if event_db.add_event_questions(data):
        return Response(json.dumps({"msg": f'Question for: "{data.get("event_id")}" has been added', "result": True}),
                        status=STATUS_201_CREATED,
                        headers=JSON_RESPONSE_HEADERS)

    return Response(json.dumps(
        {"msg": f'Unable to add question for: "{data.get("event_id")}", possible duplicate q_id in database',
         "result": False}), status=STATUS_417_EXPECTATION_FAILED,
        headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/remove_event_questions", methods=['POST'])
def remove_event_questions():
    """
    Removes a list of questions from an event.

    :return:
    """
    data = request.json

    if event_db.remove_event_questions(data):
        return Response(
            json.dumps({"msg": f'Questions for: "{data.get("event_id")}" has been removed', "result": True}),
            status=STATUS_200_SUCCESS,
            headers=JSON_RESPONSE_HEADERS)
    else:
        return Response(json.dumps({"msg": f'Error removing Questions for: "{data.get("event_id")}"', "result": False}),
                        status=STATUS_417_EXPECTATION_FAILED,
                        headers=JSON_RESPONSE_HEADERS)


@app.route("/api/v1/leaderboard", methods=['GET'])
def leaderboard():
    """
    Retrieves the current team standings of the game.

    :return:
    """

    sorted_docs = team_db.get_teams_positions()

    new_docs = []
    for i, doc in enumerate(sorted_docs):
        doc['index'] = i + 1
        new_docs.append(doc)

    return Response(
        json.dumps({"msg": f'Successful', "data": new_docs}),
        status=STATUS_200_SUCCESS,
        headers=JSON_RESPONSE_HEADERS)


@app.route("/remove_event", methods=['POST'])
def remove_event():
    """
    Removes an event from the database.

    :return:
    """
    data = request.json
    if event_db.remove_event(data.get("event_id")):
        return Response(json.dumps({"msg": f'Event: "{data.get("event_id")}" has been removed', "result": True}),
                        status=STATUS_200_SUCCESS,
                        headers=JSON_RESPONSE_HEADERS)
    else:
        return Response(json.dumps({"msg": f'Nothing to remove', "result": True}), status=STATUS_417_EXPECTATION_FAILED,
                        headers=JSON_RESPONSE_HEADERS)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="CLI Helper for the OpenScoreServer WebApp")

    parser.add_argument("-d", "--debug", help="Runs the App in debug mode", action="store_true")
    parser.add_argument("-n", "--normal", help="Runs the App in normal mode", action="store_true")

    args = parser.parse_args()
    if args.debug:
        app.run(debug=True, host="0.0.0.0")

    if args.normal:
        app.run(host="0.0.0.0")

    parser.print_help()
