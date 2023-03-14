import threading
import socket
import ChatGraphics
from tkinter import *

IP = "127.0.0.1"
PORT = 1403
NAME = "SEAN"
BUFFER = 1024
NAME_TAKEN = "The name you entered is already taken, please try another one"
CONNECTION_SUCCESS = "Connected to chat"
CREATE_MESSAGE = "Creating Room For This User:"
NON_EXISTENT_ROOM = "Room doesn't exits"
CONNECTION_ERROR = "Connection Unsuccessful"
CLIENT_DISCONNECTED = "Client Has Disconnected"
USER = "You: "
ADD_USER_COMMAND = "ADD USER~~"
INVITE_ONLY_MESSAGE = "MODE INVITE ONLY~~"
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
LOG_IN = "LOG IN"
ZERO = 0
START = "Start"
USERS_CHAT = "'s Chat Room"
TEXT_BOX_HEIGHT = 25
TEXT_BOX_WIDTH = 40
EMPTY_STRING = ""
INVITE = "invite"
FIRST_TEXT_LINE = '1.0'
END_STRING = "end"
DISABLED_STRING = "disabled"
INVITE_ONLY_TEXT = "Invite Only"
ENTRY_BD = 2
ENTRY_WIDTH = 18
INVITE_BUTTON_X = 100
INVITE_BUTTON_Y = 100
INVITE_SEND_X_RATIO = 0.3
INVITED_SEND_Y_RATIO = 0.25
INVITE_BOX_X_RATIO = 0.1
TIME_OUT_TIMER = 0.4
NEXT_LINE = "\n"
ENTER = '<Return>'
CRASH = "server crashed"
LOCKED_NAME = "You"
MEMBERS_TEXT = "Members: "
ROOM_MEMBER = 1
MEMBERS_X_RATIO = 0.02
MEMBERS_Y_RATIO = 0.02
COLON = ":"
DISCONNECTED = " Has Disconnected"
CONNECTED = " Has Connected"
SECOND_INDEX = 1


def main():
    run = Chat()
    run.connect()
    run.client.close()


def first_screen(error):  # calls the first screen function with the correct values, returns the user input
    screen = ChatGraphics.Graphics(SCREEN_WIDTH, SCREEN_HEIGHT, LOG_IN)
    screen.opening(error)
    return screen.txt


class Chat:  # all of the communication is in this class, responsible also for the some of the graphics
    def __init__(self):
        self.client = socket.socket()
        self.name = EMPTY_STRING
        self.group = []
        self.group_start = False
        self.screen = None
        self.exit = False
        self.created_room = False
        self.invite_only = False
        self.invite_box = None
        self.invite_button = EMPTY_STRING
        self.members = ROOM_MEMBER

    def connect(self):  # connects to the server, using try and except, calls the graphics function to get user input
        # and if the name is not taken continues with the name the user has given
        try:
            error = False
            name = EMPTY_STRING
            self.client.connect((IP, PORT))
            message = NAME_TAKEN
            while message == NAME_TAKEN:
                name = first_screen(error)
                if len(name) > ZERO and name != LOCKED_NAME:
                    self.client.send(name.encode())
                    message = self.client.recv(BUFFER).decode()
                    error = True
                elif name == LOCKED_NAME:
                    error = True

                else:
                    print(CLIENT_DISCONNECTED)
                    return
            self.name = name
            self.start_program()

        except socket.error:
            print(CONNECTION_ERROR)
        except KeyboardInterrupt:
            pass

    def start_program(self):  # here the function lets the user choose whether to join a room or create one using
        # the graphics functions, if the user wants to join the function checks if the room exists and not locked or
        # if locked invited the user, if the room is available continue if not try again, if the user wants to create a
        # room it informs the server (if the user created the room he can lock the room and let only certain users join)
        name = EMPTY_STRING
        error = False
        try:
            answer = NON_EXISTENT_ROOM
            while answer == NON_EXISTENT_ROOM:
                screen = ChatGraphics.Graphics(SCREEN_WIDTH, SCREEN_HEIGHT, START)
                screen.choice(error)
                if screen.join:
                    if screen.txt != self.name and len(screen.txt) > ZERO:
                        self.client.send(screen.txt.encode())
                        answer = self.client.recv(BUFFER).decode()
                        if answer != NON_EXISTENT_ROOM:
                            self.members = int(answer.split(COLON)[SECOND_INDEX])
                        name = screen.txt
                        error = True
                    elif screen.txt == self.name:
                        error = True
                elif screen.create:
                    self.client.send(CREATE_MESSAGE.encode())
                    self.created_room = True
                    name = self.name
                    break
                else:
                    print(CLIENT_DISCONNECTED)
                    return
            self.communicate(name)
        except socket.error:
            print(CONNECTION_ERROR)

    def communicate(self, screen_name):  # start the chat, creates suitable graphics, and calls the functions that are
        # responsible for receiving user input and sending it to the server
        self.screen = ChatGraphics.Graphics(SCREEN_WIDTH, SCREEN_HEIGHT, screen_name + USERS_CHAT)
        self.invite_box = Entry(self.screen.screen, bd=ENTRY_BD, width=ENTRY_WIDTH,
                                bg=ChatGraphics.COLOR_BOXES, fg=ChatGraphics.LETTERS_COLORS)
        self.invite_button = Button(text=INVITE, bg=ChatGraphics.COLOR_BOXES, fg=ChatGraphics.LETTERS_COLORS,
                                    activebackground=ChatGraphics.ACTIVE_COLOR)
        texts = Text(width=TEXT_BOX_WIDTH, height=TEXT_BOX_HEIGHT, bg=ChatGraphics.COLOR_BOXES,
                     fg=ChatGraphics.LETTERS_COLORS)
        texts.insert(FIRST_TEXT_LINE, EMPTY_STRING)
        texts.place(x=ChatGraphics.CHAT_TEST_X, y=ChatGraphics.CHAT_TEXT_Y)
        texts.yview_pickplace(END_STRING)
        texts.configure(state=DISABLED_STRING)
        if self.created_room:
            invite = Button(text=INVITE_ONLY_TEXT, command=self.invite_change, bg=ChatGraphics.COLOR_BOXES,
                            fg=ChatGraphics.LETTERS_COLORS, activebackground=ChatGraphics.ACTIVE_COLOR)
            invite.place(x=INVITE_BUTTON_X, y=INVITE_BUTTON_Y)
        members_online = Label(text=MEMBERS_TEXT + str(self.members), bg=ChatGraphics.COLOR_BOXES,
                               fg=ChatGraphics.LETTERS_COLORS)
        members_online.place(relx=MEMBERS_X_RATIO, rely=MEMBERS_Y_RATIO)
        messages_thread = threading.Thread(target=self.messages)
        messages_thread.start()
        self.chat_messages()
        messages_thread.join()

    def invite_change(self):  # if the invite only button is pressed it send that to the server (to lock the room) and
        # gives the user proper ways to send invites
        try:
            self.client.send(INVITE_ONLY_MESSAGE.encode())
            self.invite_only = not self.invite_only
            if self.invite_only:
                self.invite_box = Entry(self.screen.screen, bd=ENTRY_BD, width=ENTRY_WIDTH,
                                        bg=ChatGraphics.COLOR_BOXES, fg=ChatGraphics.LETTERS_COLORS)
                self.invite_button = Button(text=INVITE, bg=ChatGraphics.COLOR_BOXES, fg=ChatGraphics.LETTERS_COLORS,
                                            activebackground=ChatGraphics.ACTIVE_COLOR, command=self.invite_user)
                self.invite_button.place(relx=INVITE_SEND_X_RATIO, rely=INVITED_SEND_Y_RATIO)
                self.invite_box.place(relx=INVITE_BOX_X_RATIO, rely=INVITED_SEND_Y_RATIO)
            else:
                self.invite_box.destroy()
                self.invite_button.destroy()
        except socket.error:
            print(CRASH)
            self.screen.screen.destroy()
            self.exit = True

    def invite_user(self):  # if the user has entered a user name he wanted to add (while the room is invite only using
        # the correct input box) it send that to the server in a special format (so that the server can recognize it's
        # not a user input for a normal message
        try:
            if self.invite_box.get() != EMPTY_STRING:
                self.client.send((ADD_USER_COMMAND + self.invite_box.get()).encode())
                self.invite_box.delete(ZERO, len(self.invite_box.get()))
        except socket.error:
            self.screen.screen.destroy()
            self.exit = True

    def messages(self):  # receives the message sent by the server, shows them to the user until exist or crash
        self.client.settimeout(TIME_OUT_TIMER)
        while True:
            try:
                message = self.client.recv(BUFFER).decode()
                if COLON not in message:
                    if CONNECTED in message:
                        self.members += ROOM_MEMBER
                    else:
                        self.members -= ROOM_MEMBER
                    members_online = Label(text=MEMBERS_TEXT + str(self.members), bg=ChatGraphics.COLOR_BOXES,
                                           fg=ChatGraphics.LETTERS_COLORS)
                    members_online.place(relx=MEMBERS_X_RATIO, rely=MEMBERS_Y_RATIO)
                self.screen.txt = self.screen.txt + NEXT_LINE + message
                texts = Text(width=TEXT_BOX_WIDTH, height=TEXT_BOX_HEIGHT, bg=ChatGraphics.COLOR_BOXES,
                             fg=ChatGraphics.LETTERS_COLORS)
                texts.insert(FIRST_TEXT_LINE, self.screen.txt)
                texts.place(x=ChatGraphics.CHAT_TEST_X, y=ChatGraphics.CHAT_TEXT_Y)
                texts.yview_pickplace(END_STRING)
                texts.configure(state=DISABLED_STRING)

            except socket.timeout:
                if self.exit:
                    break
            except socket.error:
                self.screen.screen.quit()  # we always need to quit the screen at this point so the part that is
                # responsible for sending messages wont get stuck in the same mode until he send a message and instead
                # just automatically exits in case of a server crash
                break

    def chat_messages(self):  # gives the user means to send messages, calls other functions to send the message
        # if enter is pressed
        self.screen.text_box = Entry(self.screen.screen, bd=ENTRY_BD, width=ChatGraphics.TEXT_BOX_WIDTH,
                                     bg=ChatGraphics.COLOR_BOXES, fg=ChatGraphics.LETTERS_COLORS)
        self.screen.text_box.place(x=ChatGraphics.CHAT_BOX_X, y=ChatGraphics.CHAT_BOX_Y)
        self.screen.screen.bind(ENTER, self.enter_pressed)

        self.screen.screen.mainloop()
        self.exit = True

    def enter_pressed(self, event):  # sends the message to the server, adds the server to all of the messages, reset
        # the input box that the user used to send the message
        try:
            print(event)
            if ADD_USER_COMMAND not in self.screen.text_box.get() and \
                    INVITE_ONLY_MESSAGE not in self.screen.text_box.get():
                self.screen.txt = self.screen.txt + NEXT_LINE + USER + self.screen.text_box.get()
                self.client.send(self.screen.text_box.get().encode())
                texts = Text(width=TEXT_BOX_WIDTH, height=TEXT_BOX_HEIGHT, bg=ChatGraphics.COLOR_BOXES,
                             fg=ChatGraphics.LETTERS_COLORS)
                texts.insert(FIRST_TEXT_LINE, self.screen.txt)
                texts.place(x=ChatGraphics.CHAT_TEST_X, y=ChatGraphics.CHAT_TEXT_Y)
                texts.configure(state=DISABLED_STRING)
                texts.yview_pickplace(END_STRING)

            self.screen.text_box.delete(ZERO, len(self.screen.text_box.get()))
        except socket.error:
            self.exit = True
            self.screen.screen.destroy()


if __name__ == '__main__':
    main()
