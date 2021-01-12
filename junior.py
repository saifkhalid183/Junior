import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import requests
import json
import random
from pygame import mixer
import pygame
from tkinter import *
import sys
from functools import partial
import cv2
import dlib
import face_recognition
import numpy as np
import csv
import warnings
mixer.init()

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
# face recognition


def attendance(imgname, to):
    global filename
    try:
        while True:
            grabbed, img1 = webcam.read()
            # img1=face_recognition.load_image_file(frame)
            # if grabbed==True:
            if os.path.exists(f"images\\{imgname}.jpg"):
                img2 = face_recognition.load_image_file(
                    f'images\\{imgname}.jpg')
                img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
                faceLocation2 = face_recognition.face_locations(img2)[0]
                encodeimg2 = face_recognition.face_encodings(img2)[0]
                cv2.rectangle(img2, (faceLocation2[3], faceLocation2[0]), (
                    faceLocation2[1], faceLocation2[2]), (0, 255, 0), 2)
                img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
                faceLocation1 = face_recognition.face_locations(img1)[0]
                # print(faceLocation1)
                encodeimg1 = face_recognition.face_encodings(img1)[0]
                cv2.rectangle(img1, (faceLocation1[3], faceLocation1[0]), (
                    faceLocation1[1], faceLocation1[2]), (0, 255, 0), 2)
                result = face_recognition.compare_faces(
                    [encodeimg1], encodeimg2)  # compare the face encodings
                facedistance = face_recognition.face_distance(
                    [encodeimg1], encodeimg2)  # lower distance higher accuracy
                # print(result,facedistance)
                cv2.putText(img1, f'{result} {round(facedistance[0],2)}', (
                    50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
                cv2.imshow('img1', img1)
                # cv2.imshow('img2',img2)
                keyy = cv2.waitKey(1)
                temp = 1
                if key == 27 or keyy == 27:
                    break
                if facedistance < .45:
                    rows = [[imgname]]
                    print(
                        f"Attendance of {imgname} marked successfully...................................")
                    speak(
                        f"Attendance of {imgname} marked successfully...................................")
                    print()
                    while temp:
                        try:
                            sendEmail(
                                to, f"{imgname} your Attendance is marked")
                            temp = 0
                        except:
                            print("Some error occurred")
                            print("Please type the correct address")
                            speak("Some error occurred")
                            speak("Please type the correct address")
                            to = input()
                    speak("Mail sent")
                    # writing to csv file
                    with open(filename, 'a', newline='') as csvfile:
                        # creating a csv writer object
                        csvwriter = csv.writer(csvfile)
                        # writing the data rows
                        csvwriter.writerows(rows)
                    break
                else:
                    print("Bring the right person here!!!!!!!!!!!!!!!!")
                    speak("Bring the right person here!!!!!!!!!!!!!!!!")
            else:
                print("Type your name it was not clear")
                speak("Type your name it was not clear")
                imgname = input()
    except:
        attendance(imgname, to)


# face recognition end
# snake game
player_name = ""
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0 \n")
        f.write(player_name)
with open("highscore.txt", "r") as f:
    highscore = f.readline()
    name = f.readline()
    highscore = int(highscore)
pygame.mixer.init()
pygame.init()
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 128, 0)
blue = (0, 0, 255)
screen_width = 900
screen_height = 600
n = 0
k = 0
j = 0
level = 1
window = ""
bgimg = ""
welcomeimg = ""
outimg = ""
snake_x = 50
snake_y = 55
snake_size = 10
food_size = 10
score = 0
velocity_x = 0
velocity_y = 0
food_x = random.randint(30, screen_width/2)
food_y = random.randint(30, screen_height/2)
exit = False
over = False
FPS = 32
snk_list = []
snk_length = 1
initial_speed = 4
FPSCLOCK = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)


def func(root, fnamevalue):
    global player_name
    global window
    global bgimg
    global welcomeimg
    global outimg
    player_name = fnamevalue.get()
    root.destroy()
    window = pygame.display.set_mode((screen_width, screen_height))
    bgimg = pygame.image.load("snake_img.jpg")
    bgimg = pygame.transform.scale(
        bgimg, (screen_width, screen_height)).convert_alpha()
    welcomeimg = pygame.image.load(
        "welcome_img.jpg")
    welcomeimg = pygame.transform.scale(
        welcomeimg, (screen_width, screen_height)).convert_alpha()
    outimg = pygame.image.load("out_img.jpg")
    outimg = pygame.transform.scale(
        outimg, (screen_width, screen_height)).convert_alpha()
    pygame.display.set_caption("Snake")
    pygame.display.update()
    # return player_name


def banao_snake(window, color, snk_list, snake_size):
    for snake_x, snake_y in snk_list:
        pygame.draw.rect(
            window, black, [snake_x, snake_y, snake_size, snake_size])


def score_on_screen(score, color, x, y):
    score_text = font.render(score, True, color)
    window.blit(score_text, [x, y])


def welcome():
    global exit
    pygame.mixer.music.load('snake_song.mp3')
    pygame.mixer.music.play()
    while not exit:
        window.fill(white)
        window.blit(welcomeimg, (0, 0))
        score_on_screen("Welcome to the Snakes game", black, 200, 200)
        score_on_screen("To play press spacebar", black, 200, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def levelup():
    global level
    global exit
    window.fill(green)
    if level == 1:
        score_on_screen("Level "+str(level), red, 200, 200)
    else:
        score_on_screen("Level "+str(level)+" increasing speed", red, 200, 200)
    score_on_screen("To play press spacebar", black, 200, 300)
    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def pause():
    global exit
    pygame.mixer.music.load('snake_song.mp3')
    pygame.mixer.music.play()
    while not exit:
        window.fill(white)
        window.blit(welcomeimg, (0, 0))
        score_on_screen("Snakes game has been paused", black, 200, 200)
        score_on_screen("To resume press escape", black, 200, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        pygame.display.update()
        FPSCLOCK.tick(FPS)


# snake_game_chalao = 0


def snake_game_chalao():
    root = Tk()
    root.geometry("500x400")
    Label(root, text="Enter Your Name", fg="green",
          font="verdana 24 bold").grid(row=0, column=1, pady=5)
    fname = Label(root, text="First Name")
    fname.grid(row=1, pady=5)
    fnamevalue = StringVar()
    fnameentry = Entry(root, textvariable=fnamevalue)
    fnameentry.grid(row=1, column=1, pady=5, padx=10)
    Button(text="Submit", bg="grey", command=partial(
        func, root, fnamevalue)).grid(pady=5)
    root.mainloop()


# snake game ends
# tic_tac_toe
board = ["-", "-", "-",
         "-", "-", "-",
         "-", "-", "-"]
current_player = "X"
if not os.path.exists("tic_tac.txt"):
    with open("tic_tac.txt", "w") as tt:
        tt.write("Initial board: "+str(board)+"\n")
        tt.write("Current player: "+current_player)
        tt.write("\n")
else:
    with open("tic_tac.txt", "a") as tt:
        tt.write("Initial board: "+str(board)+"\n")
        tt.write("Current player: "+current_player)
        tt.write("\n")
game_still_going = True


winner = None


value_to_speak = 1


def play_game():

    display_board()

    while game_still_going:

        handle_turn(current_player)

        check_if_game_over()

        flip_player()

    if winner == "X" or winner == "O":
        print(winner + " won.")
        speak(winner + " won.")
        tt.write(winner + " won." + "\n")
    elif winner == None:
        print("Tie.")
        speak("Tie.")
        tt.write(winner + " won." + "\n")


def display_board():
    print("\n")
    print(board[0] + " | " + board[1] + " | " + board[2] + "     1 | 2 | 3")
    print(board[3] + " | " + board[4] + " | " + board[5] + "     4 | 5 | 6")
    print(board[6] + " | " + board[7] + " | " + board[8] + "     7 | 8 | 9")
    print("\n")
    tt.write("\n")
    tt.write("Current board: \n")
    tt.write(board[0] + " | " + board[1] +
             " | " + board[2] + "     1 | 2 | 3\n")
    tt.write(board[3] + " | " + board[4] +
             " | " + board[5] + "     4 | 5 | 6\n")
    tt.write(board[6] + " | " + board[7] +
             " | " + board[8] + "     7 | 8 | 9\n")
    tt.write("\n")


def handle_turn(player):
    global value_to_speak
    print(player + "'s turn.")
    speak(player + "'s turn.")
    tt.write(player + "'s turn."+"\n")
    if (value_to_speak == 1):
        print("Speak a position from 1-9: ")
        speak("Speak a position from 1-9: ")
        position = (Command())
        tt.write("Speak a position from 1-9: \n")
        tt.write("Position selected: "+position+"\n")
        valid = False
    elif value_to_speak == 0:
        print("Choose a position from 1-9: ")
        speak("Choose a position from 1-9: ")
        position = input()
        tt.write("Choose a position from 1-9: \n")
        tt.write("Position selected: "+position+"\n")
        valid = False
    while not valid:

        while position not in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            if (value_to_speak == 1):
                print("Speak a position from 1-9: ")
                speak("Speak a position from 1-9: ")
                position = (Command())
                tt.write("Speak a position from 1-9: \n")
                tt.write("Position selected: "+position+"\n")
            elif value_to_speak == 0:
                print("Choose a position from 1-9: ")
                speak("Choose a position from 1-9: ")
                position = input()
                tt.write("Choose a position from 1-9: \n")
                tt.write("Position selected: "+position+"\n")

        position = int(position) - 1

        if board[position] == "-":
            valid = True
        else:
            print("You can't go there. Go again.")
            speak("You can't go there. Go again.")
            tt.write("You can't go there. Go again.\n")

    board[position] = player

    display_board()


def check_if_game_over():
    check_for_winner()
    check_for_tie()


def check_for_winner():
    global winner
    row_winner = check_rows()
    column_winner = check_columns()
    diagonal_winner = check_diagonals()
    if row_winner:
        winner = row_winner
    elif column_winner:
        winner = column_winner
    elif diagonal_winner:
        winner = diagonal_winner
    else:
        winner = None


def check_rows():
    global game_still_going
    row_1 = board[0] == board[1] == board[2] != "-"
    row_2 = board[3] == board[4] == board[5] != "-"
    row_3 = board[6] == board[7] == board[8] != "-"
    if row_1 or row_2 or row_3:
        game_still_going = False
    if row_1:
        return board[0]
    elif row_2:
        return board[3]
    elif row_3:
        return board[6]
    else:
        return None


def check_columns():
    global game_still_going
    column_1 = board[0] == board[3] == board[6] != "-"
    column_2 = board[1] == board[4] == board[7] != "-"
    column_3 = board[2] == board[5] == board[8] != "-"
    if column_1 or column_2 or column_3:
        game_still_going = False
    if column_1:
        return board[0]
    elif column_2:
        return board[1]
    elif column_3:
        return board[2]
    else:
        return None


def check_diagonals():
    global game_still_going
    diagonal_1 = board[0] == board[4] == board[8] != "-"
    diagonal_2 = board[2] == board[4] == board[6] != "-"
    if diagonal_1 or diagonal_2:
        game_still_going = False
    if diagonal_1:
        return board[0]
    elif diagonal_2:
        return board[2]
    else:
        return None


def check_for_tie():
    global game_still_going
    if "-" not in board:
        game_still_going = False
        return True
    else:
        return False


def flip_player():
    global current_player
    if current_player == "X":
        current_player = "O"
        tt.write("Current player: "+current_player+"\n")
    elif current_player == "O":
        current_player = "X"
        tt.write("Current player: "+current_player+"\n")
# tic_tac_toe ends

# sudoku solver


def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r, c
    return None, None


def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False

    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    row_start = (row//3)*3
    col_start = (col//3)*3

    for r in range(row_start, row_start+3):
        for c in range(col_start, col_start+3):
            if puzzle[r][c] == guess:
                return False
    return True


def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)
    if row is None:
        return True

    for guess in range(1, 10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True
        puzzle[row][col] = -1
    return False
# sudoku solver ends


def speaknews(str):
    from win32com.client import Dispatch
    speak = Dispatch("SAPI.SpVoice")
    speak.Speak(str)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def greetMe():
    hour = int(datetime.datetime.now().hour)
    if(hour >= 0 and hour < 12):
        speak("Good Morning!")
    elif(hour >= 12 and hour < 18):
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hi Sir! I am JUNIOR. How may I help you?")


def Command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 0.5
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print("Try Again!!!!!!!!!!!!!!!!!!")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('sender_gmail_address', "sender_gmail_password")
    server.sendmail('sender_gmail_address', to, content)
    server.close()
    return


if not os.path.exists("sports_news.txt"):
    with open("sports_news.txt", "w") as sn:
        sn.write("News: \n")
if not os.path.exists("jokes.txt"):
    with open("jokes.txt", "w") as joke:
        joke.write("Jokes: \n")
if not os.path.exists("india_news.txt"):
    with open("india_news.txt", "w") as inn:
        inn.write("News: \n")
if not os.path.exists("news.txt"):
    with open("news.txt", "w") as n:
        n.write("News: \n")
if not os.path.exists("mail.txt"):
    with open("mail.txt", "w") as g:
        g.write("Mails: \n")

if(__name__ == "__main__"):
    greetMe()
    print()
    print("Welcome to the assistant!")
    speak("Welcome to the assistant!")
    print("To use the basic features, try saying the basic commands in readme file!")
    speak("To use the basic features, try saying the basic commands in readme file!")
    print("To use the cool Face-Recognition Attendance System just say Face Recognition!")
    speak("To use the cool Face-Recognition Attendance System just say Face Recognition!")
    print("We have a Sudoku Solver, which gives the solution to your Sudoku. Just say Sudoku solver!")
    speak("We have a Sudoku Solver, which gives the solution to your Sudoku. Just say Sudoku solver!")
    print("If you are bored, you can play Tic Tac Toe with your friend or anyone else :) . Just say Tic Tac Toe!")
    speak("If you are bored, you can play Tic Tac Toe with your friend or anyone else :) . Just say Tic Tac Toe!")
    print("There is a Snake game which we play in mobiles, but it isn't that bad in desktop or pc. To enjoy just say Snake game!")
    speak("There is a Snake game which we play in mobiles, but it isn't that bad in desktop or pc. To enjoy just say Snake game!")
    print("To exit, simply say Exit!")
    speak("To exit, simply say Exit!")
    print()
    while True:
        query = Command().lower()
        if not os.path.exists("queries.txt"):
            with open("queries.txt", "w") as ff:
                ff.write(query)
                ff.write("\n")
        else:
            with open("queries.txt", "a") as ff:
                ff.write(query)
                ff.write("\n")
        if 'wikipedia' in query:
            try:
                speak('Searching the WIKIPEDIA....')
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=3)
                speak("According to WIKIPEDIA")
                print(results)
                speak(results)
            except:
                print("Some error occurred. Please try again!")
                speak("Some error occurred. Please try again!")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")

        elif 'play music' in query or 'play song' in query:
            try:
                music = 'C:\\Users\\Saif Khalid\\Music\\music'
                songs = os.listdir(music)
                for song in songs:
                    print(song)
                nn = len(songs)
                print(nn)
                i = random.randint(0, nn-1)
                print(f"Playing : {songs[i]}")
                gaana = os.path.join(music, songs[i])
                mixer.music.load(gaana)
                mixer.music.set_volume(0.7)
                mixer.music.play()
                while(True):
                    print(
                        "To pause type p, to resume again type r, n for next random song, to exit type e and enter:\n")
                    h = input()
                    if(h == 'p'):
                        mixer.music.pause()
                    elif(h == 'r'):
                        mixer.music.unpause()
                    elif(h == 'e'):
                        mixer.music.stop()
                        break
                    elif(h == 'n'):
                        i = random.randint(0, nn-1)
                        print(f"Playing : {songs[i]}")
                        gaana = os.path.join(music, songs[i])
                        mixer.music.load(gaana)
                        mixer.music.set_volume(0.7)
                        mixer.music.play()
            except:
                print(
                    "Your location of music folder is not specified or specified wrong")
                speak(
                    "Your location of music folder is not specified or specified wrong")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Hey! the time is {strTime}")

        elif 'date' in query:
            tdate = datetime.datetime.now().strftime("%d:%B:%Y:%A")
            speak(f"today's date is : {tdate}")

        elif 'open code' in query:
            try:
                path1 = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
                os.startfile(path1)
            except:
                print("Your location of code exe is not specified or specified wrong")
                speak("Your location of code exe is not specified or specified wrong")

        elif 'open chrome' in query:
            try:
                path2 = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(path2)
            except:
                print("Your location of chrome exe is not specified or specified wrong")
                speak("Your location of chrome exe is not specified or specified wrong")

        elif 'what is your name' in query or "who are you" in query:
            print("Hi! I am JUNIOR.")
            speak("Hi! I am JUNIOR.")

        elif 'who am i' in query:
            print("You are Saif Khalid.")
            speak("You are Saif Khalid.")

        elif 'gmail' in query or "mail" in query:
            with open("mail.txt", "a") as g:
                try:
                    temp = 1
                    speak("Sure, to type message say 1 or to use voice say 0")
                    print("Sure, to type message say 1 or to use voice say 0")
                    n = Command()
                    g.write("Sure, to type message say 1 or to use voice say 0\n")
                    g.write(f"User input to say message or type {n}\n")
                    # if "1" not in n or "0" not in n:
                    while True:
                        if '0' in n:
                            speak("What is the message?")
                            content = Command()
                            g.write("What is the message?\n")
                            g.write(f"User said: {content}\n")
                            break
                        elif '1' in n:
                            speak("Please type the message")
                            content = input()
                            g.write("Please type the message\n")
                            g.write(f"User said: {content}\n")
                            break
                        else:
                            print("Enter your choice")
                            speak("Enter your choice")
                            n = input()
                            g.write("Enter your choice\n")
                            g.write(f"User input {n}\n")
                    speak("Type the receivers mail address")
                    print("Type the receivers mail address")
                    to = input()
                    g.write("Type the receivers mail address\n")
                    g.write(f"User gave: {to}\n")
                    while temp:
                        try:
                            sendEmail(to, content)
                            temp = 0
                        except:
                            print("Some error occurred")
                            print("Please type the correct address")
                            speak("Some error occurred")
                            speak("Please type the correct address")
                            to = input()
                            g.write("Some error occurred\n")
                            g.write("Please type the correct address\n")
                            g.write(f"User gave: {to}\n")
                    # print(qwer)
                    print("Done.")
                    speak("Done.")
                    g.write("Done.\n")
                except Exception as e:
                    # print(e)
                    print("Sorry some error occurred.")
                    g.write("Sorry some error occurred.\n")

        elif 'sports news' in query or 'sports' in query:
            url = ('http://newsapi.org/v2/top-headlines?'
                   'country=in&'
                   'category=sports&'
                   'apiKey=a14fc394cf6f46f3a452842b4288d4f0')
            r = requests.get(url)
            news = r.text
            parsednews = json.loads(news)
            if not os.path.exists("sports_news.txt"):
                with open("sports_news.txt", "w") as sn:
                    i = 0
                    listt = ["first", "second", "third", "fourth", "fifth",
                             "sixth", "seventh", "eighth", "ninth", "tenth"]
                    v = len(parsednews)
                    if v != 0:
                        for i in range(v):
                            speaknews(f"{listt[i]} news is:")
                            sn.write(f"{listt[i]} news is:\n")
                            print(parsednews['articles'][i]['title'])
                            speaknews(parsednews['articles'][i]['title'])
                            sn.write(parsednews['articles'][i]['title']+"\n")
                    else:
                        speaknews("no new update for news")
                        print("no new update for news")
                        sn.write("no new update for news\n")
            else:
                with open("sports_news.txt", "a") as sn:
                    i = 0
                    listt = ["first", "second", "third", "fourth", "fifth",
                             "sixth", "seventh", "eighth", "ninth", "tenth"]
                    v = len(parsednews)
                    if v != 0:
                        for i in range(v):
                            speaknews(f"{listt[i]} news is:")
                            sn.write(f"{listt[i]} news is:\n")
                            print(parsednews['articles'][i]['title'])
                            speaknews(parsednews['articles'][i]['title'])
                            sn.write(parsednews['articles'][i]['title']+"\n")
                    else:
                        speaknews("no new update for news")
                        print("no new update for news")
                        sn.write("no new update for news\n")

        elif 'joke' in query or 'jokes' in query:
            url = "https://official-joke-api.appspot.com/random_joke"
            r = requests.get(url)
            texts = r.text
            parsedjoke = json.loads(texts)
            n = len(parsedjoke)
            with open("jokes.txt", "a") as joke:
                if n != 0:
                    print(parsedjoke["setup"])
                    speak(parsedjoke["setup"])
                    joke.write(parsedjoke["setup"]+"\n")
                    print(parsedjoke["punchline"])
                    speak(parsedjoke["punchline"])
                    joke.write(parsedjoke["punchline"]+"\n")
                else:
                    print("No joke for now!")
                    speak("No joke for now!")
                    joke.write("No joke for now!\n")

        elif 'india news' in query or 'news from india' in query or 'news of india' in query:
            url = ('http://newsapi.org/v2/top-headlines?'
                   'country=in&'
                   'apiKey=a14fc394cf6f46f3a452842b4288d4f0')
            r = requests.get(url)
            news = r.text
            parsednews = json.loads(news)
            if not os.path.exists("india_news.txt"):
                with open("india_news.txt", "w") as inn:
                    i = 0
                    listt = ["first", "second", "third", "fourth", "fifth",
                             "sixth", "seventh", "eighth", "ninth", "tenth"]
                    v = len(parsednews)
                    if v != 0:
                        for i in range(v):
                            speaknews(f"{listt[i]} news is:")
                            inn.write(f"{listt[i]} news is:\n")
                            print(parsednews['articles'][i]['title'])
                            speaknews(parsednews['articles'][i]['title'])
                            inn.write(parsednews['articles'][i]['title']+"\n")
                    else:
                        speaknews("no new update for news")
                        print("no new update for news")
                        inn.write("no new update for news\n")
            else:
                with open("india_news.txt", "a") as inn:
                    i = 0
                    listt = ["first", "second", "third", "fourth", "fifth",
                             "sixth", "seventh", "eighth", "ninth", "tenth"]
                    v = len(parsednews)
                    if v != 0:
                        for i in range(v):
                            speaknews(f"{listt[i]} news is:")
                            inn.write(f"{listt[i]} news is:\n")
                            print(parsednews['articles'][i]['title'])
                            speaknews(parsednews['articles'][i]['title'])
                            inn.write(parsednews['articles'][i]['title']+"\n")
                    else:
                        speaknews("no new update for news")
                        print("no new update for news")
                        inn.write("no new update for news\n")

        elif 'news' in query:
            url = ('http://newsapi.org/v2/top-headlines?'
                   'sources=bbc-news&'
                   'apiKey=a14fc394cf6f46f3a452842b4288d4f0')
            r = requests.get(url)
            news = r.text
            parsednews = json.loads(news)
            newss = parsednews['articles']
            if not os.path.exists("news.txt"):
                with open("news.txt", "w") as n:
                    i = 0
                    listt = ["first", "second", "third", "fourth", "fifth",
                             "sixth", "seventh", "eighth", "ninth", "tenth"]
                    v = len(newss)
                    if v != 0:
                        for i in range(v):
                            speaknews(f"{listt[i]} news is:")
                            n.write(f"{listt[i]} news is:\n")
                            print(parsednews['articles'][i]['title'])
                            speaknews(parsednews['articles'][i]['title'])
                            n.write(parsednews['articles'][i]['title']+"\n")
                    else:
                        speaknews("no new update for news")
                        print("no new update for news")
                        n.write("no new update for news\n")
            else:
                with open("news.txt", "a") as n:
                    i = 0
                    listt = ["first", "second", "third", "fourth", "fifth",
                             "sixth", "seventh", "eighth", "ninth", "tenth"]
                    v = len(newss)
                    if v != 0:
                        for i in range(v):
                            speaknews(f"{listt[i]} news is:")
                            n.write(f"{listt[i]} news is:\n")
                            print(parsednews['articles'][i]['title'])
                            speaknews(parsednews['articles'][i]['title'])
                            n.write(parsednews['articles'][i]['title']+"\n")
                    else:
                        speaknews("no new update for news")
                        print("no new update for news")
                        n.write("no new update for news\n")

        elif 'exit' in query:
            speak("Thank you and gooooooood to work with you.")
            print("Thank you and gooooooood to work with you.")
            sys.exit()

        elif 'hi' in query or 'hello' in query:
            speak("hello and welcome!")

        elif 'sudoku' in query:
            speak("Welcome to the Sudoku Solver")
            grid_length = 9
            example_board = []
            b = []
            print(
                "If you want to type the values of your puzzle say 1 or if you want to speak them say 0")
            speak(
                "If you want to type the values of your puzzle say 1 or if you want to speak them say 0")
            val = (Command())
            while True:
                if "1" in val:
                    print(
                        "Enter your puzzle, if there is an empty space type -1 and if not type the value")
                    speak(
                        "Enter your puzzle, if there is an empty space type -1 and if not type the value")
                    for i in range(grid_length):
                        b = list(map(int, input().split()))
                        example_board.append(b)
                    break
                elif "0" in val:
                    print(
                        "Enter your puzzle, if there is an empty space say -1 and if not say the value")
                    speak(
                        "Enter your puzzle, if there is an empty space say -1 and if not say the value")
                    for i in range(grid_length):
                        for j in range(grid_length):
                            print(f"Say the value at {i} , {j}")
                            speak(f"Say the value at {i} , {j}")
                            try:
                                c = int(Command())
                            except:
                                print("Please type it. It was not clear.")
                                speak("Please type it. It was not clear.")
                                c = int(input())
                            b.append(c)
                        # print(b)
                        example_board.append(b)
                        b = []
                    break
                else:
                    print("Please type your choice")
                    speak("Please type your choice")
                    val = input()
            print(solve_sudoku(example_board))
            print("The Solution to your Sudoku is:")
            speak("The Solution to your Sudoku is:")
            print(example_board)
            speak(example_board)
        elif "tic tac toe" in query or "tic tac" in query or "tic_tac_toe" in query:
            print("if you want speak the values of position say 1 else to type say 0")
            speak("if you want speak the values of position say 1 else to type say 0")
            inp = (Command())
            with open("tic_tac.txt", "a") as tt:
                tt.write("User input to type or say: "+inp+"\n")
                if "1" in inp:
                    value_to_speak = 1
                    play_game()
                elif "0" in inp:
                    value_to_speak = 0
                    play_game()
                else:
                    print("Please input your choice it is not clear")
                    speak("Please input your choice it is not clear")
                    inpu = input()
                    tt.write("Please input your choice it is not clear\n")
                    tt.write("Input of user: "+inpu+"\n")
                    value_to_speak = inpu
                    play_game()
                board = ["-", "-", "-",
                         "-", "-", "-",
                         "-", "-", "-"]
                game_still_going = True

                winner = None

                current_player = "X"
                tt.write(str(board)+"\n")
                tt.write(current_player+"\n")

                value_to_speak = 1
        elif "snake" in query:
            snake_game_chalao()
            welcome()
            levelup()
            while not exit:
                # if exit == False:
                #     break
                if highscore <= score:
                    highscore = score
                if(j >= 10):
                    initial_speed += 2
                    level += 1
                    levelup()
                    j = 0
                if over:
                    window.fill(white)
                    window.blit(outimg, (0, 0))
                    if highscore <= score:
                        highscore = score
                        with open("highscore.txt", "w") as f:
                            hiscore = str(highscore)
                            f.write(hiscore+"\n")
                            f.write(player_name)
                    score_on_screen(
                        "Game Over!!!!!!!!!!!!!!!!Press Enter to continue", red, 100, 250)
                    score_on_screen("Score : "+str(score), red, 350, 350)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                exit = False
                                over = False
                                snake_x = 50
                                snake_y = 55
                                snake_size = 10
                                food_size = 10
                                score = 0
                                velocity_x = 0
                                velocity_y = 0
                                snk_list = []
                                snk_length = 1
                                j = 0
                                n = 0
                                k = 0
                                initial_speed = 4
                                level = 1
                                with open("highscore.txt", "r") as f:
                                    highscore = f.readline()
                                    name = f.readline()
                                    highscore = int(highscore)
                                welcome()
                                levelup()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                velocity_x = initial_speed
                                velocity_y = 0
                            if event.key == pygame.K_LEFT:
                                velocity_x = -initial_speed
                                velocity_y = 0
                            if event.key == pygame.K_UP:
                                velocity_y = -initial_speed
                                velocity_x = 0
                            if event.key == pygame.K_DOWN:
                                velocity_y = initial_speed
                                velocity_x = 0
                            if event.key == pygame.K_ESCAPE:
                                pause()
                    snake_x += velocity_x
                    snake_y += velocity_y
                    if abs(snake_x-food_x) < 8 and abs(snake_y-food_y) < 8:
                        j += 1
                        pygame.mixer.music.load(
                            'food.mp3')
                        pygame.mixer.music.play()
                        score += 10
                        if n >= 5:
                            n = 0
                            k = 1
                        n += 1
                        food_x = random.randint(30, screen_width/1.5)
                        food_y = random.randint(30, screen_height/1.5)
                        snk_length += 5
                    window.fill(white)
                    window.blit(bgimg, (0, 0))
                    score_on_screen("Score : "+str(score), red, 5, 5)
                    score_on_screen("HighScore : "+str(highscore), red, 550, 5)
                    score_on_screen("Made By : "+name, red, 550, 35)
                    score_on_screen("To pause press escape", red, 5, 550)
                    if n >= 5:
                        pygame.draw.rect(window, red, [food_x, food_y, 15, 15])
                    else:
                        pygame.draw.rect(
                            window, blue, [food_x, food_y, food_size, food_size])
                    if k != 0:
                        h = random.randint(50, 100)
                        score += h
                        k = 0
                    head = []
                    head.append(snake_x)
                    head.append(snake_y)
                    snk_list.append(head)
                    if(len(snk_list) > snk_length):
                        del snk_list[0]
                    if(head in snk_list[:-1]):
                        over = True
                        pygame.mixer.music.set_volume(2.0)
                        pygame.mixer.music.load(
                            'hit.wav')
                        pygame.mixer.music.play()
                    if(snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height):
                        over = True
                        pygame.mixer.music.set_volume(2.0)
                        pygame.mixer.music.load(
                            'hit.wav')
                        pygame.mixer.music.play()
                    banao_snake(window, black, snk_list, snake_size)
                pygame.display.update()
                FPSCLOCK.tick(FPS)
            pygame.display.quit()
            pygame.quit()

        elif "face recognition" in query:
            imgname = ""
            # putting 0 will select default camera
            webcam = cv2.VideoCapture(0)
            key = cv2.waitKey(1)
            webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 800)
            # greetMe()
            print("Enter classname")
            speak("Enter classname")
            CLASSNAME = input()
            print()
            tdate = datetime.datetime.now().strftime("%d:%B:%Y:%A")
            fields = [f"{CLASSNAME} {tdate}"]
            filename = f"images\\{CLASSNAME}_attendance_records.csv"
            # writing to csv file
            with open(filename, 'a') as csvfile:
                # creating a csv writer object
                csvwriter = csv.writer(csvfile)
                # writing the fields
                csvwriter.writerow(fields)
            if not webcam.isOpened():
                print("nhi hua open")
            while True:
                count = 1
                print(
                    "If you want to speak your name say YES and if you want to type your name say NO. To exit say EXIT.")
                speak(
                    "If you want to speak your name say YES and if you want to type your name say NO.  To exit say EXIT.")
                ask = Command().lower()
                # print(ask)
                if "exit" in ask:
                    speak("THANK YOU and it was good working with the class")
                    break
                elif "no" in ask:
                    print("Enter your name....................................")
                    speak("Enter your name....................................")
                    imgname = input()
                    if 'exit' in imgname:
                        speak("THANK YOU and it was good working with the class")
                        break
                    while count:
                        if os.path.exists(f"images\\{imgname}.jpg"):
                            print("Enter your mail address")
                            speak("Enter your mail address")
                            to = input()
                            attendance(imgname, to)
                            count = 0
                        else:
                            print("Please type your name. You are not a student.")
                            speak("Please type your name. You are not a student.")
                            imgname = input()
                elif "yes" in ask:
                    print("Speak your name....................................")
                    speak("Speak your name....................................")
                    imgname = Command().lower()
                    if 'exit' in imgname:
                        speak("THANK YOU and it was good working with the class")
                        break
                    while count:
                        if os.path.exists(f"images\\{imgname}.jpg"):
                            print("Enter your mail address")
                            speak("Enter your mail address")
                            to = input()
                            attendance(imgname, to)
                            count = 0
                        else:
                            print("Please type your name. You are not a student.")
                            speak("Please type your name. You are not a student.")
                            imgname = input()
                else:
                    speak(f"{ask} matt bol sirf haa ya naa bol")
            webcam.release()
warnings.filterwarnings("ignore")
