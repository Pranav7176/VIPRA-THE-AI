import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import random
import os
import webbrowser
import re

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# engine.setProperty('voice', voices[1].id)for female voice

# defining speak function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# defining wishme function
def wishMe(username):
    hour = int(datetime.datetime.now().hour)

    if hour >= 0 and hour <= 12:
        speak(f"Good Morning {username}, please tell me how may I help you")
    elif hour > 12 and hour <= 18:
        speak(f"Good Afternoon {username}, please tell me how may I help you")
    elif hour > 18 and hour <= 21:
        speak(f"Good Evening {username}, please tell me how may I help you")
    elif hour > 21 and hour < 0:
        speak(f"Good Night {username}, please tell me how may I help you")


# defining take command function
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognising")
            query = r.recognize_google(audio, language='eg-in')
            query.lower()
            print(f"User said {query}")
        except Exception as e:
            speak("Can you say that again")
            return None
        return query

def change_name(new_name):
    with open('name.txt', 'w') as na:
        na.write(new_name)
        username=new_name


if __name__ == '__main__':
    print("do you want  to speak with Sneha or VIPRA")
    print("Enter 2 for Sneha and 1 for Vipra")
    ai = int(input("Enter here: "))





    if ai == 1:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)
    elif ai == 2:
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[2].id)
    else:
        exit()

        # defining speak function

    filesize = os.path.getsize("name.txt")
    if filesize==0:

        speak('plaese Tell me your name')
        name_user=str(input("Enter here: "))
        with open('name.txt', 'w') as n:
            n.write(name_user)
        wishMe(name_user)

    else:
        wname=open('name.txt')
        wishname=wname.read()
        wishMe(wishname)
    speak("you can tell exit anywhere to exit VIPRA")

    # query=takeCommand()
    try:
        while True:
            query = takeCommand().lower()
            if 'wikipedia' in query:
                speak("Searching wikipedia")
                query = query.replace("wikipedia", "")
                speak("According to wikipedia")
                results = wikipedia.summary(query, sentences=2)
                print(results)
                speak(results)

            if 'your name' in query:
                speak(f"My name is Vipra")

            if 'exit' in query:
                speak(f"Thank u for using VIPRA or Sneha ")
                exit()
            if "play game" in query:
                speak("Which game you want to play. Guess the number or tic tac toe or 3 cup Monty")
            if "game 1" in query:
                try:
                    randNumber = random.randint(1, 100)
                    userGuess = None
                    guesses = 0

                    while (userGuess != randNumber):
                        userGuess = int(input("Enter your guess: "))
                        guesses += 1
                        if (userGuess == randNumber):
                            print("You guessed it right!")
                        else:
                            if (userGuess > randNumber):
                                speak("You guessed it wrong! Enter a smaller number")
                            else:
                                speak("You guessed it wrong! Enter a larger number")

                    speak(f"You guessed the number in {guesses} guesses")
                except Exception as e:
                    speak("Sorry an error occered")
            if "change my name" in query:
                speak('okay! what should I call you')
                name=input("Please Enter here: ")
                change_name(name)
                speak(f"okay I will remember that, {name}")

            if "game 2" in query:
                try:
                    from IPython.display import clear_output


                    def display_board(board):
                        print(board[7] + '|' + board[8] + '|' + board[9])
                        print(board[4] + '|' + board[5] + '|' + board[6])
                        print(board[1] + '|' + board[2] + '|' + board[3])


                    def player_input():

                        marker = ''

                        while not (marker == 'X' or marker == 'O'):
                            marker = input('Player 1: Do you want to be X or O? ').upper()

                        if marker == 'X':
                            return ('X', 'O')
                        else:
                            return ('O', 'X')


                    def place_marker(board, marker, position):

                        board[position] = marker


                    def win_check(board, mark):
                        return ((board[1] == mark and board[2] == mark and board[3] == mark) or
                                (board[4] == mark and board[5] == mark and board[6] == mark) or
                                (board[7] == mark and board[8] == mark and board[9] == mark) or
                                (board[1] == mark and board[4] == mark and board[7] == mark) or
                                (board[2] == mark and board[5] == mark and board[8] == mark) or
                                (board[3] == mark and board[6] == mark and board[9] == mark) or
                                (board[1] == mark and board[5] == mark and board[9] == mark) or
                                (board[3] == mark and board[5] == mark and board[7] == mark))


                    import random


                    def choose_first():
                        if random.randint(0, 1) == 0:
                            return 'Player 2'
                        else:
                            return 'Player 1'


                    def space_check(board, position):

                        return board[position] == ' '


                    def full_board_check(board):
                        for i in range(1, 10):
                            if space_check(board, i):
                                return False
                        return True


                    def player_choice(board):
                        position = 0

                        while position not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                            position = int(input('Choose your next position: (1-9) '))

                        return position


                    def replay():
                        y = input('Do you want to continue? [Y/N]')

                        y = y.lower()
                        if y == 'y':
                            return True
                        else:
                            return False


                    print('Welcome to Tic Tac Toe!')

                    while True:
                        # Reset the board
                        theBoard = [' '] * 10
                        player1_marker, player2_marker = player_input()
                        turn = choose_first()
                        print(turn + ' will go first.')

                        play_game = input('Are you ready to play? Enter Yes or No.')

                        if play_game.lower()[0] == 'y':
                            game_on = True

                        else:

                            game_on = False

                        while game_on:
                            if turn == 'Player 1':
                                # Player1's turn.

                                display_board(theBoard)

                                position = player_choice(theBoard)

                                place_marker(theBoard, player1_marker, position)

                                if win_check(theBoard, player1_marker):

                                    display_board(theBoard)
                                    print('Player 1 has won!')

                                    game_on = False
                                else:

                                    if full_board_check(theBoard):

                                        display_board(theBoard)
                                        print('The game is a draw!')
                                        game_on = False
                                    else:
                                        turn = 'Player 2'

                            else:
                                # Player2's turn.

                                display_board(theBoard)
                                position = player_choice(theBoard)
                                place_marker(theBoard, player2_marker, position)

                                if win_check(theBoard, player2_marker):

                                    display_board(theBoard)
                                    print('Player 2 has won!')
                                    game_on = False
                                else:
                                    if full_board_check(theBoard):

                                        display_board(theBoard)
                                        print('The game is a draw!')
                                        game_on = False
                                    else:
                                        turn = 'Player 1'

                        if not replay():
                            break
                except Exception as e:
                    speak("Error")
            if "open youtube" in query:
                webbrowser.open('https://www.youtube.com/')
                speak("opening youtube")
            if "open google" in query:
                webbrowser.open('https://www.google.com/')
                speak("opening google")
            if "open browser" in query:
                webbrowser.open_new('https://www.google.com/')
                speak("opening google")
            if "open google maps" in query:
                webbrowser.open_new_tab("https://www.google.co.in/maps/")
                speak("opening googlemaps")
            if "open whatsapp in browser" in query:
                webbrowser.open_new_tab("https://web.whatsapp.com/")
                speak("opening instagram")

            if "open instagram" in query:
                webbrowser.open_new_tab('https://www.instagram.com/')
                speak("opening instagram")

            if "open brave browser" in query:
                path1 = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk"
                speak("opening brave browser")
                os.startfile(path1)
            if "open excel" in query:
                path1 = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk"
                speak("opening excel")
                os.startfile(path1)
            if "open powerpoint" in query:
                path1 = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk"
                speak("opening powerpoint")
                os.startfile(path1)
            if "open microsoft word" in query:
                path1 = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk"
                speak("opening word")
                os.startfile(path1)
            if "open chrome" in query:
                path1 = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk"
                speak("opening chrome")
                os.startfile(path1)
            # facts


            if 'my name' in query:
                a=open('name.txt')
                s1=a.read()
                speak(s1)


            if "game 3" in query:
                pass
            if "set alarm" in query:
                try:
                    import pyttsx3
                    import datetime
                    from pygame import mixer

                    # https://klingeltonemp3.info/ding-dong-clock.htm

                    engine = pyttsx3.init('sapi5')
                    voices = engine.getProperty('voices')
                    # print(voices[1].id)
                    engine.setProperty('voice', voices[0].id)


                    def speak(audio):
                        engine.say(audio)
                        engine.runAndWait()


                    def wishMe():
                        hour = int(datetime.datetime.now().hour)
                        if hour >= 0 and hour < 12:
                            speak("Good Morning sir")

                        elif hour >= 12 and hour < 18:
                            speak("Good Afternoon sir")

                        else:
                            speak("Good Evening sir")


                    def alarm(file, stopper):
                        mixer.init()
                        mixer.music.load(file)
                        mixer.music.play()

                        if stopper == "stop":
                            mixer.music.stop()


                    if __name__ == '__main__':
                        while True:
                            wishMe()
                            speak('I am alarm ai sir. Please tell me ur alarm')

                            break

                        speak("tell me the year")
                        year = int(input("Enter here\n"))

                        speak("tell me the month")
                        month = int(input("Enter here\n"))

                        speak("tell me the day")
                        day = int(input("Enter here\n"))

                        speak("tell me the hour")
                        hour = int(input("Enter here\n"))

                        speak("tell me the minute")
                        minutes = int(input("Enter here\n"))

                        speak("can u tell me what's your message")
                        message = str(input("Enter here\n"))

                        speak("Remember done is the stopper")
                        print("Remember done is the stopper")

                        speak("thank u sir the alarm will ring when its time")
                        while True:
                            stopper1 = ""
                            if year == datetime.datetime.now().year and month == datetime.datetime.now().month and day == datetime.datetime.now().day and hour == datetime.datetime.now().hour and minutes == datetime.datetime.now().minute:
                                speak(f"{message}")
                                # speak("please enter 'done' to stop alarm")
                                # print("please enter 'done' to stop alarm")

                                alarm("Ding Dong Clock.mp3", stopper1)
                                stopper1 = input("Enter here: ")
                                if stopper1 == "done":
                                    break

                except Exception as e:
                    speak("sorry There was an error")

            # if "open spotify" in query:
    except Exception as e:
        pass
