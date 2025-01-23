#!/bin/python3
import curses
import os
import time
import sys
class Vec2:
    def __init__(self):
        self.nestedList = []
        self.length = 0
    def addRow(self):
        self.nestedList.append([])
        self.length += 1
    def addCol(self, item):
        self.nestedList[self.length].append(item)
    def getRow(self, index):
        return self.nestedList[index]
    def getLastRow(self):
        return self.nestedList[self.length]
class Shell:
    def __init__(self):
        self.s = curses.initscr()
        self.s.nodelay(1)
        curses.noecho()
        curses.raw()
        self.textb = []
        curses.start_color()
        curses.init_pair(9, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.username = ""
        self.maxy, self.maxx = self.s.getmaxyx()
        self.curx, self.cury = (0, 0)
        self.accepted = False
        self.comb = []
        self.comStr = ''
        self.scrollOfsset = 0
    def login(self):
        self.s.addstr(0, 0, 'Username: ')
        self.s.addstr(1, 0, 'Password: ')
        self.s.move(0, 10)
        while False == self.accepted:
            userb = []
            passb = []
            passString = ''
            userString = ''
            userFilled = False
            passFilled = False
            while False == userFilled:
                ch = -1
                while -1 == ch:
                    ch = self.s.getch()
                if ord('q') & 0x1f == ch:
                    sys.exit()
                elif '\n' == chr(ch):
                    self.s.move(1, 10)
                    userString = ''.join(userb)
                    userFilled = True
                elif ch in [8, 263]:
                    try:
                        del userb[len(userb)-1]
                        self.s.addstr(0, (10 + len(userb)), ' ')
                        self.s.move(0, (10 + len(userb)))
                    except:
                        pass
                elif ch != (ch & 0x1f) and ch < 128:
                    self.s.addstr(0, (10 + len(userb)), chr(ch))
                    userb.append(chr(ch))
            while False == passFilled:
                ch = -1
                while -1 == ch:
                    ch = self.s.getch()
                if ord('q') & 0x1f == ch:
                    sys.exit()
                elif ch in [8, 263]:
                    try:
                        del passb[len(passb)-1]
                        self.s.addstr(1, (10 + len(passb)), ' ')
                        self.s.move(1, (10 + len(passb)))
                    except:
                        pass
                elif '\n' == chr(ch):
                    passString = ''.join(passb)
                    passFilled = True
                elif ch != (ch & 0x1f) and ch < 128:
                    self.s.addstr(1, (10 + len(passb)), '*')
                    passb.append(chr(ch))
            if 'root' == userString:
                if 'root' == passString:
                    self.username = userString
                    self.accepted = True
                else:
                    self.s.addstr(2, 0, 'Wrong Password')
                    userb = []
                    passb = []
                    self.s.clear()
                    self.s.refresh()
                    self.s.addstr(0, 0, 'Username: ')
                    self.s.addstr(1, 0, 'Password: ')
                    self.s.move(0, 10)
            else:
                self.s.addstr(2, 0, 'no username found')
                userb = []
                passb = []
                self.s.clear()
                self.s.refresh()
                self.s.addstr(0, 0, 'Username: ')
                self.s.addstr(1, 0, 'Password: ')
                self.s.move(0, 10)
    def draw(self):
        self.s.clear()
        self.s.refresh()
        topbar = 'Welcome ' + self.username
        while len(topbar) < (self.maxx - 1):
            topbar += ' '
        commandinput = self.username + '@radon > '
        while len(commandinput) < (self.maxx - 1):
            commandinput += ' '
        self.s.addstr(0, 0, topbar, curses.color_pair(9))
        self.s.addstr((self.maxy - 1), 0, commandinput, curses.color_pair(9))
        drawablex = self.maxx - 2
        drawabley = self.maxy
        ftextlist = ''
        count = 2
        for i in self.textb:
            ftextlist = ''.join(i)
            self.s.addstr(count, 0, ftextlist)
            count += 1
        self.s.addstr(self.maxy-1, len(self.username) + 9, ''.join(self.comb), curses.color_pair(9))
        self.s.move(self.cury, self.curx)
    def handleInput(self):
        ch = -1
        while -1 == ch:
            ch = self.s.getch()
        if (ord('q') & 0x1f) == ch:
            sys.exit()
        elif '\n' == chr(ch):
            self.s.move(1, 10)
            self.comStr = ''.join(self.comb)
            self.comb = []
            self.curx = (len(self.username) + 9)
            self.runCommand(self.comStr)
        elif ch in [8, 263]:
            try:
                del self.comb[self.curx-1-len(self.username)-9]
                self.curx -= 1
            except:
                pass
        elif ch != (ch & 0x1f) and ch < 128:
            self.comb.append(chr(ch))
            self.curx += 1
        elif curses.KEY_RIGHT == ch:
            if self.curx >= (len(self.comb) + len(self.username) + 9):
                '''self.s.move((self.maxy-1), (len(self.username) + 9 + len(self.comb) + 1))'''
                pass
            else:
                self.curx += 1
        elif curses.KEY_LEFT == ch:
            if self.curx <= (len(self.username) + 9):
               '''self.s.move((self.maxy - 1), (len(self.username) + 9))'''
               pass
            else:
               self.curx -= 1
    def runCommand(self, command):
        result = os.popen(command)
        output = result.read().strip()
        templist = output.split('\n')
        for i in templist:
            self.textb.append(list(i))
def main(stdscr):
    shell = Shell()
    #remove this after testing
    shell.username = 'root'
    shell.accepted = True
    #shell.login()
    shell.curx = len(shell.username) + 9
    shell.cury = shell.maxy - 1
    while True:
        shell.draw()
        shell.handleInput()
curses.wrapper(main)
