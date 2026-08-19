import datetime
import os
import random
import threading
import time
import webbrowser
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import pyttsx3
import speech_recognition as sr
import wikipedia
from pypdf import PdfReader


# CONFIGURATION

ASSISTANT_NAME = "VIPRA"
NAME_FILE = Path("name.txt")


# TEXT TO SPEECH

engine = pyttsx3.init()

voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)


def speak(text: str) -> None:
    """Convert text to speech and print it to the terminal."""
    print(f"{ASSISTANT_NAME}: {text}")

    engine.say(text)
    engine.runAndWait()


# USER NAME

def get_username() -> str:
    """Read the user's name from name.txt."""
    try:
        if NAME_FILE.exists():
            name = NAME_FILE.read_text(encoding="utf-8").strip()

            if name:
                return name

    except OSError:
        pass

    return ""


def save_username(name: str) -> None:
    """Save the user's name."""
    NAME_FILE.write_text(name.strip(), encoding="utf-8")


def change_name() -> None:
    """Ask the user for a new name and save it."""
    speak("Okay. What should I call you?")

    name = input("Enter your name: ").strip()

    if not name:
        speak("That doesn't look like a valid name.")
        return

    save_username(name)
    speak(f"Okay, I will remember that, {name}.")



# GREETING

def wish_me(username: str) -> None:
    """Give a greeting depending on the current time."""
    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good morning"
    elif 12 <= hour < 18:
        greeting = "Good afternoon"
    elif 18 <= hour < 22:
        greeting = "Good evening"
    else:
        greeting = "Good night"

    speak(
        f"{greeting} {username}, "
        f"please tell me how may I help you."
    )


# SPEECH RECOGNITION

def take_command() -> str:
    """Listen through the microphone and return recognized text."""
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("\nListening...")

        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            print("No speech detected.")
            return ""

    try:
        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print(f"You said: {query}")
        return query.lower().strip()

    except sr.UnknownValueError:
        speak("Sorry, I didn't understand that.")
        return ""

    except sr.RequestError:
        speak("The speech recognition service is currently unavailable.")
        return ""


# WIKIPEDIA

def search_wikipedia(query: str) -> None:
    """Search Wikipedia and read a short summary."""
    search_term = query.replace("wikipedia", "").strip()

    if not search_term:
        speak("What should I search for on Wikipedia?")
        return

    try:
        speak("Searching Wikipedia.")

        result = wikipedia.summary(
            search_term,
            sentences=2,
            auto_suggest=True
        )

        print(f"\n{result}\n")
        speak(result)

    except wikipedia.exceptions.DisambiguationError as error:
        options = ", ".join(error.options[:5])

        speak(
            f"There are multiple results for that topic. "
            f"Some options are: {options}"
        )

    except wikipedia.exceptions.PageError:
        speak("I couldn't find a Wikipedia page for that.")

    except Exception as error:
        print(f"Wikipedia error: {error}")
        speak("Sorry, something went wrong while searching Wikipedia.")


# NUMBER GUESSING GAME

def guess_the_number() -> None:
    """Play a number guessing game."""
    number = random.randint(1, 100)
    guesses = 0

    speak("I have chosen a number between 1 and 100.")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            guesses += 1

            if guess == number:
                speak(
                    f"Correct! You guessed the number "
                    f"in {guesses} guesses."
                )
                break

            if guess > number:
                speak("Too high. Try a smaller number.")
            else:
                speak("Too low. Try a larger number.")

        except ValueError:
            speak("Please enter a valid number.")



# TIC TAC TOE

def display_board(board: list[str]) -> None:
    """Display the Tic-Tac-Toe board."""
    print()
    print(f" {board[7]} | {board[8]} | {board[9]} ")
    print("---+---+---")
    print(f" {board[4]} | {board[5]} | {board[6]} ")
    print("---+---+---")
    print(f" {board[1]} | {board[2]} | {board[3]} ")
    print()


def choose_marker() -> tuple[str, str]:
    """Choose X or O for Player 1."""
    while True:
        marker = input(
            "Player 1, choose X or O: "
        ).strip().upper()

        if marker == "X":
            return "X", "O"

        if marker == "O":
            return "O", "X"

        print("Please choose X or O.")


def place_marker(
    board: list[str],
    marker: str,
    position: int
) -> None:
    """Place a marker on the board."""
    board[position] = marker


def win_check(
    board: list[str],
    marker: str
) -> bool:
    """Check whether a player has won."""
    winning_positions = [
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
        (1, 4, 7),
        (2, 5, 8),
        (3, 6, 9),
        (1, 5, 9),
        (3, 5, 7),
    ]

    return any(
        all(board[position] == marker for position in combination)
        for combination in winning_positions
    )


def board_full(board: list[str]) -> bool:
    """Check whether the board is full."""
    return all(board[position] != " " for position in range(1, 10))


def get_position(board: list[str]) -> int:
    """Get a valid empty position from the player."""
    while True:
        try:
            position = int(
                input("Choose your position (1-9): ")
            )

            if position not in range(1, 10):
                print("Choose a number from 1 to 9.")
                continue

            if board[position] != " ":
                print("That position is already occupied.")
                continue

            return position

        except ValueError:
            print("Please enter a number.")


def tic_tac_toe() -> None:
    """Run a two-player Tic-Tac-Toe game."""
    speak("Welcome to Tic-Tac-Toe.")

    while True:
        board = [" "] * 10

        player1, player2 = choose_marker()

        current_player = random.choice(["Player 1", "Player 2"])

        print(f"{current_player} will go first.")

        ready = input(
            "Are you ready to play? (yes/no): "
        ).strip().lower()

        if not ready.startswith("y"):
            speak("Okay, maybe later.")
            return

        game_running = True

        while game_running:

            display_board(board)

            if current_player == "Player 1":
                marker = player1
            else:
                marker = player2

            print(f"{current_player}'s turn.")

            position = get_position(board)

            place_marker(board, marker, position)

            if win_check(board, marker):
                display_board(board)
                speak(f"{current_player} wins!")
                game_running = False

            elif board_full(board):
                display_board(board)
                speak("The game is a draw!")
                game_running = False

            else:
                current_player = (
                    "Player 2"
                    if current_player == "Player 1"
                    else "Player 1"
                )

        replay = input(
            "Do you want to play again? (y/n): "
        ).strip().lower()

        if not replay.startswith("y"):
            break


# OPEN WEBSITES

def open_website(url: str, name: str) -> None:
    """Open a website in the default browser."""
    speak(f"Opening {name}.")
    webbrowser.open_new_tab(url)


# OPEN WINDOWS APPLICATIONS

def open_windows_app(
    shortcut_path: str,
    app_name: str
) -> None:
    """
    Open a Windows application using its shortcut.

    Update the shortcut_path if the application is installed
    somewhere else on your computer.
    """

    path = Path(shortcut_path)

    if not path.exists():
        speak(
            f"I couldn't find the shortcut for {app_name}. "
            f"Please update its path in the code."
        )
        return

    speak(f"Opening {app_name}.")

    try:
        os.startfile(path)

    except OSError as error:
        print(f"Application error: {error}")
        speak(f"I couldn't open {app_name}.")


# PDF READER

def read_pdf() -> None:
    """Open a PDF and read it aloud."""
    speak("Opening the PDF reader.")

    try:
        root = Tk()
        root.withdraw()

        file_path = askopenfilename(
            title="Select a PDF",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )

        root.destroy()

        if not file_path:
            speak("No PDF was selected.")
            return

        reader = PdfReader(file_path)

        total_pages = len(reader.pages)

        print(f"\nPDF: {Path(file_path).name}")
        print(f"Total pages: {total_pages}")

        page_number = int(
            input(
                f"Enter the starting page "
                f"(1-{total_pages}): "
            )
        )

        if not 1 <= page_number <= total_pages:
            speak("That page number is invalid.")
            return

        speak("Starting the audiobook.")

        for page_index in range(page_number - 1, total_pages):

            page = reader.pages[page_index]

            text = page.extract_text() or ""

            if not text.strip():
                continue

            print(
                f"\n--- Page {page_index + 1} ---\n"
            )

            print(text)

            speak(text)

    except ValueError:
        speak("Please enter a valid page number.")

    except Exception as error:
        print(f"PDF error: {error}")
        speak("Sorry, I couldn't read that PDF.")


# ALARM

def alarm_worker(
    alarm_time: datetime.datetime,
    message: str
) -> None:
    """Wait until the alarm time without blocking VIPRA."""
    while datetime.datetime.now() < alarm_time:
        time.sleep(1)

    speak(message)

    print("\n🔔 ALARM 🔔")
    print(message)


def set_alarm() -> None:
    """Create an alarm."""
    speak("Tell me the alarm date and time.")

    try:
        year = int(input("Year: "))
        month = int(input("Month: "))
        day = int(input("Day: "))
        hour = int(input("Hour (0-23): "))
        minute = int(input("Minute (0-59): "))

        message = input("Alarm message: ").strip()

        if not message:
            message = "Your alarm is ringing."

        alarm_time = datetime.datetime(
            year,
            month,
            day,
            hour,
            minute
        )

        if alarm_time <= datetime.datetime.now():
            speak("That time has already passed.")
            return

        alarm_thread = threading.Thread(
            target=alarm_worker,
            args=(alarm_time, message),
            daemon=True
        )

        alarm_thread.start()

        formatted_time = alarm_time.strftime(
            "%d %B %Y at %I:%M %p"
        )

        speak(
            f"Alarm set for {formatted_time}."
        )

    except ValueError:
        speak("Invalid date or time.")


# COMMAND HANDLER

def handle_command(
    query: str,
    username: str
) -> tuple[bool, str]:
    """
    Process a voice command.

    Returns:
        (continue_running, updated_username)
    """

    # EXIT

    if query in {"exit", "quit", "shutdown", "terminate"}:
        speak("Okay, I will terminate the program.")
        return False, username

    # SLEEP

    if "go to sleep" in query:
        speak(
            "Okay, I will go to sleep. "
            "Wake me up when you need my help."
        )
        return False, username

    # NAME
    

    if "change my name" in query:
        change_name()
        username = get_username()
        return True, username

    if query in {"my name", "what is my name", "what's my name"}:
        if username:
            speak(f"Your name is {username}.")
        else:
            speak("I don't know your name yet.")

        return True, username

    if "your name" in query:
        speak(f"My name is {ASSISTANT_NAME}.")
        return True, username

    # WIKIPEDIA

    if "wikipedia" in query:
        search_wikipedia(query)
        return True, username

    # GAMES

    if "guess the number" in query:
        guess_the_number()
        return True, username

    if query in {"game 1", "tic tac toe", "play tic tac toe"}:
        tic_tac_toe()
        return True, username

    if "play game" in query or "play games" in query:
        speak(
            "You can play Guess the Number "
            "or Tic-Tac-Toe."
        )
        return True, username

    # WEBSITES

    if "open youtube" in query:
        open_website(
            "https://www.youtube.com/",
            "YouTube"
        )
        return True, username

    if "open google" in query:
        open_website(
            "https://www.google.com/",
            "Google"
        )
        return True, username

    if "open maps" in query:
        open_website(
            "https://www.google.com/maps/",
            "Google Maps"
        )
        return True, username

    if "open whatsapp" in query:
        open_website(
            "https://web.whatsapp.com/",
            "WhatsApp Web"
        )
        return True, username

    if "open instagram" in query:
        open_website(
            "https://www.instagram.com/",
            "Instagram"
        )
        return True, username

    if "songs" in query or "open spotify" in query:
        open_website(
            "https://open.spotify.com/",
            "Spotify"
        )
        return True, username

    # WINDOWS APPLICATIONS

    if "open brave" in query:
        open_windows_app(
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Brave.lnk",
            "Brave"
        )
        return True, username

    if "open chrome" in query:
        open_windows_app(
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
            "Google Chrome"
        )
        return True, username

    if "open excel" in query:
        open_windows_app(
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Excel.lnk",
            "Microsoft Excel"
        )
        return True, username

    if "open powerpoint" in query:
        open_windows_app(
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\PowerPoint.lnk",
            "Microsoft PowerPoint"
        )
        return True, username

    if "open word" in query:
        open_windows_app(
            r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Word.lnk",
            "Microsoft Word"
        )
        return True, username

    # ALARM

    if "set alarm" in query:
        set_alarm()
        return True, username

    # PDF
    

    if "read me a book" in query or "read pdf" in query:
        read_pdf()
        return True, username

    # BORED

    if "bored" in query:
        speak(
            "You can play games, read a book, "
            "or listen to music with me."
        )
        return True, username

    # UNKNOWN COMMAND

    speak(
        "I don't know how to do that yet."
    )

    return True, username


# MAIN PROGRAM

def main() -> None:
    """Start VIPRA."""
    username = get_username()

    if not username:
        speak("How may I call you?")

        username = input(
            "Enter your name: "
        ).strip()

        if not username:
            username = "Sir"

        save_username(username)

    wish_me(username)

    speak(
        f"You can tell me 'exit' anytime to shut me down, "
        f"{username}."
    )

    running = True

    while running:
        try:
            query = take_command()

            if not query:
                continue

            running, username = handle_command(
                query,
                username
            )

        except KeyboardInterrupt:
            print("\nVIPRA stopped by user.")
            break

        except Exception as error:
            print(f"Unexpected error: {error}")
            speak(
                "Something went wrong, "
                "but I am still running."
            )


# PROGRAM ENTRY POINT

if __name__ == "__main__":
    main()
