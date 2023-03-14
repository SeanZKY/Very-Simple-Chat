from tkinter import *

LOGIN_SCREEN_WIDTH = 600
LOGIN_SCREEN_HEIGHT = 600
TEXT_BOX_WIDTH = 32
DISTANCE = 80
MULTIPLIER = 2
SHORT_DISTANCE = 90
MAX_CHAR = 10
MIN_CHAR = 2
BUTTONS_DISTANCE = 70
CHAT_BOX_Y = 500
CHAT_BOX_X = 250
CHAT_TEST_X = 250
CHAT_TEXT_Y = 50
LOG_IN = "Log In"
EMPTY_STRING = ""
USER_ENTER = "Please Enter "
SEPARATOR_STRING = "-"
CHARACTERS = " Characters "
LABEL_FONT = "Arial"
FONT_SIZE = 12
USER_NAME = "username:"
TEXT_BOX_BD = 2
CONTINUE = "Continue"
ROOM_CHOICE = "Please Enter A Room's Name Or Create One"
ROOM_NAME = "Room Name:"
CREATE_GROUP = "Create Group"
JOIN_GROUP = "Join Group"
COLOR_BOXES = "gray30"
LIMITS_X_POS_RATION = 0.35
LIMITS_Y_POS_RATION = 0.1
ROOM_CHOICE_X_POS_RATIO = 0.24
ROOM_CHOICE_Y_POS_RATIO = 0.1
NAME_MESSAGE_X_POS_RATIO = 0.27
NAME_MESSAGE_Y_POS_RATIO = 0.5
BUTTON_X_POS_RATIO = 0.74
BUTTON_Y_POS_RATIO = 0.5
TEXT_BOX_X_POS_RATIO = 0.39
TEXT_BOX_Y_POS_RATIO = 0.5
ACTIVE_COLOR = "gray60"
LETTERS_COLORS = "snow"
SECOND_MESSAGE_X_POS_RATIO = 0.2
SECOND_MESSAGE_Y_POS_RATIO = 0.5
SECOND_TEXTBOX_X_POS_RATIO = 0.35
SECOND_TEXTBOX_Y_POS_RATIO = 0.5
CREATE_BUTTON_X_POS_RATIO = 0.85
CREATE_BUTTON_Y_POS_RATIO = 0.5
JOIN_BUTTON_X_POS_RATIO = 0.72
JOIN_BUTTON_Y_POS_RATIO = 0.5
NAME_TAKEN_MESSAGE = "This Name Is Already Taken Or Locked Please Try A Different One"
NAME_TAKEN_X_RATIO = 0.29
NAME_TAKEN_Y_RATIO = 0.4
ERROR_COLOR = "red"
ROOM_UNAVAILABLE_MESSAGE = "Room Is Not Available, Please Try A Different Room Or Wait To Get Invited"
ROOM_MESSAGE_X_RATIO = 0.2
ROOM_MESSAGE_Y_RATIO = 0.2
BACKGROUND = 'background'


def main():
    obj = Graphics(LOGIN_SCREEN_WIDTH, LOGIN_SCREEN_HEIGHT, LOG_IN)
    obj.opening()
    print(obj.txt)


class Graphics:  # responsible for the first and second screens and helps with the third screen
    def __init__(self, screen_width, screen_height, screen_name):
        self.screen = Tk()
        self.screen.title(screen_name)
        self.screen.minsize()
        self.x = screen_width
        self.y = screen_height
        self.screen.minsize(self.x, self.y)
        self.screen.maxsize(self.x, self.y)
        self.screen[BACKGROUND] = COLOR_BOXES
        self.text_box = Entry()
        self.txt = EMPTY_STRING
        self.create = False
        self.join = False

    def opening(self, error=False):  # the opening screen, it lets the user choose his user name and once done,
        # it updates it one of the class variables which is then used to get the user name in the other file
        if error:
            name_taken = Label(self.screen, text=NAME_TAKEN_MESSAGE, bg=COLOR_BOXES, fg=ERROR_COLOR)
            name_taken.place(relx=NAME_TAKEN_X_RATIO, rely=NAME_TAKEN_Y_RATIO)
        limits = Label(self.screen, text=USER_ENTER + str(MIN_CHAR) + SEPARATOR_STRING + str(MAX_CHAR) + CHARACTERS,
                       font=(LABEL_FONT, FONT_SIZE), bg=COLOR_BOXES, fg=LETTERS_COLORS)
        limits.place(relx=LIMITS_X_POS_RATION, rely=LIMITS_Y_POS_RATION)
        name_message = Label(self.screen, text=USER_NAME, bg=COLOR_BOXES, fg=LETTERS_COLORS)
        name_message.place(relx=NAME_MESSAGE_X_POS_RATIO, rely=NAME_MESSAGE_Y_POS_RATIO)
        self.text_box = Entry(self.screen, bd=TEXT_BOX_BD, width=TEXT_BOX_WIDTH, bg=COLOR_BOXES, fg=LETTERS_COLORS)
        button = Button(self.screen, text=CONTINUE, command=self.update_name, bg=COLOR_BOXES,
                        activebackground=ACTIVE_COLOR, fg=LETTERS_COLORS)
        button.place(relx=BUTTON_X_POS_RATIO, rely=BUTTON_Y_POS_RATIO)
        self.text_box.place(relx=TEXT_BOX_X_POS_RATIO, rely=TEXT_BOX_Y_POS_RATIO)

        self.screen.mainloop()

    def choice(self, error):  # lets the user choose whether to create a room or join a room, if the user chooses to
        # join a room he needs to write the room's name and the function saves the result in the class variables which
        # is used to pass the info to the other file
        if error:
            room_unavailable = Label(self.screen, text=ROOM_UNAVAILABLE_MESSAGE, bg=COLOR_BOXES, fg=ERROR_COLOR)
            room_unavailable.place(relx=ROOM_MESSAGE_X_RATIO, rely=ROOM_MESSAGE_Y_RATIO)

        room_choice = Label(self.screen, text=ROOM_CHOICE, font=(LABEL_FONT, FONT_SIZE), bg=COLOR_BOXES,
                            fg=LETTERS_COLORS)
        room_choice.place(relx=ROOM_CHOICE_X_POS_RATIO, rely=ROOM_CHOICE_Y_POS_RATIO)
        name_message = Label(self.screen, text=ROOM_NAME, bg=COLOR_BOXES, fg=LETTERS_COLORS)
        name_message.place(relx=SECOND_MESSAGE_X_POS_RATIO, rely=SECOND_MESSAGE_Y_POS_RATIO)
        self.text_box = Entry(self.screen, bd=TEXT_BOX_BD, width=TEXT_BOX_WIDTH, bg=COLOR_BOXES, fg=LETTERS_COLORS)
        self.text_box.place(relx=SECOND_TEXTBOX_X_POS_RATIO, rely=SECOND_TEXTBOX_Y_POS_RATIO)
        create_button = Button(self.screen, text=CREATE_GROUP, command=self.signal_create, bg=COLOR_BOXES,
                               fg=LETTERS_COLORS, activebackground=ACTIVE_COLOR)
        create_button.place(relx=CREATE_BUTTON_X_POS_RATIO, rely=CREATE_BUTTON_Y_POS_RATIO)
        join_button = Button(self.screen, text=JOIN_GROUP, command=self.signal_join, bg=COLOR_BOXES, fg=LETTERS_COLORS,
                             activebackground=ACTIVE_COLOR)
        join_button.place(relx=JOIN_BUTTON_X_POS_RATIO, rely=JOIN_BUTTON_Y_POS_RATIO)

        self.screen.mainloop()

    def update_name(self):  # checks if the name the user wants to use fits the requirements, if it does update the name
        if MIN_CHAR <= len(self.text_box.get()) <= MAX_CHAR:
            self.txt = self.text_box.get()
            self.screen.destroy()

    def signal_create(self):  # saves the correct variable if the user wants to create a room and closes program
        self.create = True
        self.screen.destroy()

    def signal_join(self):  # saves the correct variables if the user wants to join a room and closes program
        self.join = True
        self.txt = self.text_box.get()
        self.screen.destroy()


if __name__ == '__main__':
    main()
