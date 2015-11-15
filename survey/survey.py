from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import sys

def survey():
    tkMessageBox.showinfo(title="SURVEY", message="Please rate each of the following statements on a scale from 1 to 7, with 1 being absolutely not, and 7 being absolutely yes.\n [1|2|3|4|5|6|7]")

    one = tkSimpleDialog.askinteger(title="enjoyment", prompt="I enjoyed playing Tetris.")


    two = tkSimpleDialog.askinteger(title="time", prompt="Time seemed to stand still or stop.")


    three = tkSimpleDialog.askinteger(title="tired", prompt="I couldn't tell if I was getting tired.")

    four = tkSimpleDialog.askinteger(title="drive", prompt="I felt like I couldn't stop playing.")


    five = tkSimpleDialog.askinteger(title="stress", prompt="I got wound up.")

    six = tkSimpleDialog.askinteger(title="auto", prompt="Playing seemed automatic.")

    seven = tkSimpleDialog.askinteger(title="thought", prompt="I played without thinking how to play.")

    eight = tkSimpleDialog.askinteger(title="calm", prompt="Playing made me feel calm.")



    nine = tkSimpleDialog.askinteger(title="time", prompt="I lost track of time.")

    ten = tkSimpleDialog.askinteger(title="involvement", prompt="I really got into the game.")

    return([one, two, three, four, five, six, seven, eight, nine, ten])
