from flask import Flask, request
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

online_users = []
connected_users = []


@app.route("/", methods=["GET"])
def home():
    return "<h1>It's working!</h1>"


@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


@socketio.on('enter')
def handle_user_enter_event(user_name):
    print('A new user logged in: ' + user_name)
    new_user = {'name': user_name, 'sid': request.sid}
    connected_users.append(new_user)
    online_users.append(user_name)
    emit('online users', online_users, broadcast=True)


@socketio.on('exit')
def user_exit_event(user_name):
    print('A user logged out: ' + user_name)
    connected_users.remove({'name': user_name, 'sid': request.sid})
    online_users.remove(user_name)
    emit('online users', online_users, broadcast=True)


@socketio.on('offer to server')
def handle_call_offer_event(offer):
    print('Received Offer: {}'.format(offer))
    target_client = None
    for client in connected_users:
        if client['name'] == offer['target']:
            target_client = client['sid']
    emit('offer from server', offer, room=target_client)


@socketio.on('answer to server')
def call_answer_event(answer):
    print('Received Answer: {}'.format(answer))
    target_client = None
    for client in connected_users:
        if client['name'] == answer['target']:
            target_client = client['sid']
    emit('answer from server', answer, room=target_client)


@socketio.on('new ice candidate to server')
def new_ice_candidate_event(new_ice_candidate):
    print('New Ice Candidate Received.')
    target_client = None
    for client in connected_users:
        if client['name'] == new_ice_candidate['target']:
            target_client = client['sid']
    emit('new ice candidate from server', new_ice_candidate, room=target_client)


@socketio.on('disconnect')
def disconnect_event():
    print('User disconnected.')
    disconnected_user = None
    for user in connected_users:
        if user['sid'] == request.sid:
            disconnected_user = user
    connected_users.remove(disconnected_user)
    online_users.remove(user['name'])
    emit('online users', online_users, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
