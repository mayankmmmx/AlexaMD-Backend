# hack for harambe
from flask import Flask, Response, request, jsonify
#import Routes.create_account
#import Routes.login
#import Routes.get_user
#import Routes.enter_match_queue
#import Routes.submit_match
#import Routes.get_questions
#import Routes.poll_match
#import Routes.get_leaderboard
application = Flask(__name__)


@application.route('/')
@application.route('/index')
def index():
    return "Welcome to AlexaMD's RESTful API!"

'''
@application.route('/harambe/create_account', methods=['POST'])
def route_create_account():
    if request.headers['Content-Type'] == 'application/json':
        return jsonify(Routes.create_account.respond(request.get_json()))


@application.route('/harambe/login', methods=['GET'])
def route_login():
    return jsonify(Routes.login.respond(request.args))


@application.route('/harambe/get_user', methods=['GET'])
def route_get_user():
    return jsonify(Routes.get_user.respond(request.args))


@application.route('/harambe/enter_match_queue', methods=['POST'])
def route_enter_match_queue():
    if request.headers['Content-Type'] == 'application/json':
        return jsonify(Routes.enter_match_queue.respond(request.get_json()))


@application.route('/harambe/submit_match', methods=['GET'])
def route_submit_match():
    return jsonify(Routes.submit_match.respond(request.args))


@application.route('/harambe/get_questions', methods=['GET'])
def route_get_questions():
    return jsonify(Routes.get_questions.respond(request.args))


@application.route('/harambe/poll_match', methods=['POST'])
def route_poll_match():
    if request.headers['Content-Type'] == 'application/json':
        return jsonify(Routes.poll_match.respond(request.get_json()))


@application.route('/harambe/get_leaderboard', methods=['GET'])
def route_get_leaderboard():
    return jsonify(Routes.get_leaderboard.respond(request.args))

'''
if __name__ == "__main__":
    application.run(debug=True)
