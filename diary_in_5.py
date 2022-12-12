#!/usr/bin/env python3
import curses
import os
import regex as re
import sys
import datetime
import time

logfile = open(sys.argv[1], 'w') if len(sys.argv) > 1 else None

def log(log_line):
    if logfile:
        logfile.write(log_line + "\n")
        logfile.flush()

def logf(log_line):
    if logfile:
        logfile.write(log_line)
        logfile.flush()

def writequit(text):
        date = datetime.datetime.now()
        day = date.strftime("%d")
        month = date.strftime("%m")
        year = date.strftime("%Y")

        path = initializePath(month, year) 

        with open(os.path.join(path, day), 'a') as file:
            file.write(text)

def initializePath(m, y):
    date = [str(y),str(m)]
    home = os.path.expanduser("~")
    path = os.path.join(home, ".diary")
    for num in date:
        path = os.path.join(path,num)
        testPath(path)
    return path 

def testPath(path):
    if not os.path.exists(path):
        os.makedirs(path)

def mainLoop(text, timer):
    time1 = time.perf_counter()
    entry = ""
    while True:
        time2 = time.perf_counter()
        delta = time2-time1
        if delta >= 5:
            break
        else:
            drawTimer(timer, delta)
        c = text.getch()
        if(c != -1):
            c = vetChar(c)
            if c:
                if c == "bs":
                    entry = backspace(entry, text)
                else:
                    entry += c
                    text.addch(c)
                    time1 = time.perf_counter()
            else:
                pass
    finish(entry)

def backspace(entry, tb):
    if len(entry) > 0:
        y,x = getAmbiguousCursor(entry, tb)
        tb.delch(y,x)
        entry = entry[0:len(entry)-1]
    return entry

def getAmbiguousCursor(entry, tb):
    lines, cols = tb.getmaxyx()
    y = 0
    entryLength = len(entry)
    while entryLength > cols :
        entryLength -= cols
        y+=1
    x=entryLength
    return y,x-1

def drawTimer(timer, delta):
    timer.clear()
    lines, cols = timer.getmaxyx()
    timeToWrite = 5
    secsPerChar = lines/timeToWrite
    numChars = int(delta*secsPerChar)
    for i in range(numChars):
        timer.addch("|")
    timer.refresh()

def finish(text):
    writequit(text)
    curses.endwin()
    exit

def start(stdscr):
    curses.echo(False)
    lines, cols = stdscr.getmaxyx()
    textBox = curses.newwin(lines, cols-1, 0, 0)
    textBox.nodelay(True)
    textBox.keypad(True)
    timer = curses.newwin(lines, 1, 0, cols-1)
    mainLoop(textBox, timer)

def vetChar(char):
    bannedKeys = [curses.KEY_LEFT, curses.KEY_SLEFT, curses.KEY_RIGHT, curses.KEY_SRIGHT, curses.KEY_UP, curses.KEY_DOWN]
    if char in bannedKeys:
        return None

    strChar = str(chr(char))
    m = re.match(r"(\w)", strChar)
    if m:
        return strChar
    else:
        m = re.match(r"(\r?\n)",strChar)
        if m:
            return strChar
        else:
            m = re.match(r"\p{Punctuation}", strChar)
            if m:
                return strChar
            else:
                if strChar == " ":
                    return strChar
                else:
                    if char == 127:
                        return "bs"
    return None

curses.wrapper(start)