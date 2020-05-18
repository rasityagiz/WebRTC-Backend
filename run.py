from flask import Flask, request
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')

online_users = []
connected_users = []


@app.route("/", methods=["GET"])
def home():

    """ Helps to check whether server is on
        or not.
        Go to http://localhost:5000 to see. """

    return "<h1>It's working!</h1>"


@socketio.on('message')
def handle_message(message):

    """ Message event. It is used to display
        some action such as connecting. """

    print('received message: ' + message)


@socketio.on('enter')
def handle_user_enter_event(user_name):

    """ 'enter' event, triggers when a client
        write a nickname and become available
        for video call. """

    new_user = {'name': user_name, 'sid': request.sid}
    if user_name not in online_users:
        connected_users.append(new_user)
        online_users.append(user_name)
        print('A new user logged in: ' + user_name)
    emit('online users', online_users, broadcast=True)


@socketio.on('exit')
def user_exit_event(user_name):

    """ 'exit' event, triggers when a client
        remove their name from available clients. """

    print('A user logged out: ' + user_name)
    connected_users.remove({'name': user_name, 'sid': request.sid})
    online_users.remove(user_name)
    emit('online users', online_users, broadcast=True)


@socketio.on('offer to server')
def handle_call_offer_event(offer):

    """ Provide for the caller to send their
        offer to the client they choose. """

    print('Received Offer: {}'.format(offer))
    target_client = None
    for client in connected_users:
        if client['name'] == offer['target']:
            target_client = client['sid']
    emit('offer from server', offer, room=target_client)


@socketio.on('answer to server')
def call_answer_event(answer):

    """ Provide the callee to send their
        answer to the caller. """

    print('Received Answer: {}'.format(answer))
    target_client = None
    for client in connected_users:
        if client['name'] == answer['target']:
            target_client = client['sid']
    emit('answer from server', answer, room=target_client)


@socketio.on('new ice candidate to server')
def new_ice_candidate_event(new_ice_candidate):

    """ Used to transfer new ice candidates
        between peers. """

    print('New Ice Candidate Received.')
    target_client = None
    for client in connected_users:
        if client['name'] == new_ice_candidate['target']:
            target_client = client['sid']
    emit('new ice candidate from server', new_ice_candidate, room=target_client)


@socketio.on('disconnect')
def disconnect_event():

    """ An event that automatically triggers when
        a client disconnects."""

    print('User disconnected.')
    for user in connected_users:
        if user['sid'] == request.sid:
            disconnected_user = user
            connected_users.remove(disconnected_user)
            online_users.remove(user['name'])
    emit('online users', online_users, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
