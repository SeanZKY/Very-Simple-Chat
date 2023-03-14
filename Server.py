import threading
import socket

PORT = 1403
IP = "127.0.0.1"
LISTEN_CHANNEL = 1
BUFFER = 1024
NAME_TAKEN = "The name you entered is already taken, please try another one"
CONNECTION_SUCCESS = "Connected to chat"
SPACE = ""
COLON = ":"
EMPTY_MESSAGE = ""
NON_EXISTENT_ROOM = "Room doesn't exits"
CREATE_MESSAGE = "Creating Room For This User:"
ROOM_JOINED = "Successfully Joined Room, members:"
START_ERROR = "Server Has Failed To Start"
USER_DISCONNECTED = "User Has Disconnected"
INVITE_ONLY_MESSAGE = "MODE INVITE ONLY~~"
ADD_USER_COMMAND = "ADD USER~~"
ONE = 1
ZERO = 0
DISCONNECTED = " Has Disconnected"
CONNECTED = " Has Connected"


def main():
    run = Communicate()
    run.start()


class Room:  # for rooms, every room has a name and the a list of client that are in it and more as you can see
    def __init__(self, name, client):
        self.name = name
        self.users = [client]
        self.invite_only = False
        self.members = ONE
        self.invited = []

    def change_mode(self):  # change the invite only mode to the the opposite of what it was
        self.invite_only = not self.invite_only

    def invite_user(self, name, user):  # adds a user name into the invited list
        if name not in self.invited and user not in self.users:
            self.invited.append(name)

    def add_user(self, name, user_name, user):  # adds a user to the room if he entered the room's name and if the room
        # is not invited only or it is and the user is invited, update other variables (returns true if the user
        # has joined the room and False if not)
        if name == self.name and (not self.invite_only or (self.invite_only and user_name in self.invited)):
            self.members += ONE
            if user_name in self.invited:
                self.invited.remove(user_name)
            self.users.append(user)
            return True
        return False

    def user_remove(self, user):  # removes the user from the room, up dated the other variable
        self.users.remove(user)
        self.members -= ONE


class Communicate:  # responsible for all the communicating between the client and the server
    def __init__(self):
        self.users = {}
        self.room_lst = []

    def start(self):  # start the server, check for clients trying to connect, if a client is connected he is
        # taken cared of by other function running in parallel
        try:
            server_socket = socket.socket()
            server_socket.bind((IP, PORT))
            while True:
                server_socket.listen(LISTEN_CHANNEL)
                client_socket, client_address = server_socket.accept()
                connection_thread = threading.Thread(target=self.connect, args=(client_socket,))
                connection_thread.start()
        except socket.error:
            print(START_ERROR)

    def connect(self, client):  # checks the name given by the user, only if the name is not in one of the
        # room or one of the clients has it, it sends an approval message if not it sends that the name is taken
        try:
            name = client.recv(BUFFER).decode()
            if name == EMPTY_MESSAGE:
                print(USER_DISCONNECTED)
                return
            while name in self.users.values() or self.name_in_lst(name):
                client.send(NAME_TAKEN.encode())
                name = client.recv(BUFFER).decode()
            self.users[client] = name
            client.send(CONNECTION_SUCCESS.encode())
            self.choose_room(client)
        except socket.error:
            print(USER_DISCONNECTED)

    def name_in_lst(self, name):  # returns if one of the rooms has the same name given to the function
        for room in self.room_lst:
            if room.name == name:
                return True
        return False

    def choose_room(self, client):  # checks if the user want to create or join a room, if the user wants to create
        # a room it adds a new room to the lst if he wants to join it checks if it's exist and only then adds him to
        # the room using the room functions
        exit_loop = False
        group_name = EMPTY_MESSAGE
        while not exit_loop:
            try:
                message = client.recv(BUFFER).decode()
                if message == CREATE_MESSAGE:
                    group_name = Room(self.users[client], client)
                    self.room_lst.append(group_name)
                    break

                for room in self.room_lst:
                    if room.add_user(message, self.users[client], client):
                        group_name = room
                        client.send((ROOM_JOINED + str(room.members)).encode())
                        self.send_message(self.users[client] + CONNECTED, self.users[client], room, True)
                        exit_loop = True
                if not exit_loop:
                    client.send(NON_EXISTENT_ROOM.encode())
            except socket.error:
                self.users.pop(client)
                print(USER_DISCONNECTED)
                return
        self.start_chat(client, group_name)

    def start_chat(self, client, group):  # once the user is in a group for every message that user send, broadcast the
        # message to all other members in group unless the message is a command to change the server mode from invite
        # only to not (or the opposite) and then it does it, if the user wants to add a user it does it too
        try:
            while True:
                message = client.recv(BUFFER).decode()
                if message == EMPTY_MESSAGE:
                    self.remove_group_user(self.users[client], client, group)
                    break

                elif message == INVITE_ONLY_MESSAGE:
                    for room in self.room_lst:
                        if room.name == self.users[client]:
                            room.change_mode()
                elif ADD_USER_COMMAND in message:
                    name = message.split(ADD_USER_COMMAND)[ONE]
                    for value in self.users.keys():
                        if self.users[value] == name:
                            group.invite_user(name, value)

                else:
                    self.send_message(message, self.users[client], group)
        except socket.error:
            self.remove_group_user(self.users[client], client, group)

    def send_message(self, message, sender, group, system_message=False):  # broadcast the message to everyone in the
        # group (not including the client itself)
        for user in group.users:
            if not self.users[user] == sender:
                try:
                    if not system_message:
                        user.send((sender + COLON + SPACE + message).encode())
                    else:
                        user.send(message.encode())
                except socket.error:
                    self.remove_group_user(user, self.users[user], group)

    def remove_group_user(self, sender, client, group):  # removes a user from the group, also removes him for the
        # users list and update the necessary variables
        message = sender + DISCONNECTED
        self.users.pop(client)
        group.user_remove(client)
        if group.members == ZERO:
            self.room_lst.remove(group)
        else:
            for user in group.users:
                try:
                    user.send(message.encode())
                except socket.error:
                    self.remove_group_user(user, self.users[user], group)  # recursion - if the user we are trying
                    # to inform is not connected we need to remove him


if __name__ == '__main__':
    main()
