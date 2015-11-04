from Tkinter import *
import tkSimpleDialog
import tkMessageBox
import sys

def survey():
    tkMessageBox.showwarning(title="SURVEY", message="Please rate each of the following statements on a scale from 1 to 7, with 1 being absolutely not, and 7 being absolutely yes.\n [1    2    3   4   5   6   7]\n[no||prob no||maybe no||maybe yes||prob ye||yes]")

    one = tkSimpleDialog.askinteger(title="enjoyment", prompt="I enjoyed playing Tetris.")
    
    two = tkSimpleDialog.askinteger(title="scared", prompt="I felt scared.")

    three = tkSimpleDialog.askinteger(title="lose track", prompt="I lost track of where I was.")
   
    four = tkSimpleDialog.askinteger(title="different", prompt="I felt different.")

    five = tkSimpleDialog.askinteger(title="time", prompt="Time seemed to stand still or stop.")

    six = tkSimpleDialog.askinteger(title="focus", prompt="I felt spaced out.")

    seven = tkSimpleDialog.askinteger(title="tired", prompt="I couldn't tell if I was getting tired.")

    eight = tkSimpleDialog.askinteger(title="drive", prompt="I felt like I couldn't stop playing.")

    nine = tkSimpleDialog.askinteger(title="real", prompt="The game felt real.")

    ten = tkSimpleDialog.askinteger(title="stress", prompt="I got wound up.")

    eleven = tkSimpleDialog.askinteger(title="auto", prompt="Playing seemed automatic.")

    twelve = tkSimpleDialog.askinteger(title="thought", prompt="I played without thinking how to play.")

    thirteen = tkSimpleDialog.askinteger(title="calm", prompt="Playing made me feel calm.")

    fourteen = tkSimpleDialog.askinteger(title="game auto", prompt="Things seemed to happen automatically.")

    fifteen = tkSimpleDialog.askinteger(title="thoughts", prompt="My thoghts went fast.")

    sixteen = tkSimpleDialog.askinteger(title="time", prompt="I lost track of time.")

    seventeen = tkSimpleDialog.askinteger(title="involvement", prompt="I really got into the game.")

    return([one, two, three, four, five, six, seven, eight, nine, ten, eleven, twelve, thirteen, fourteen, fifteen, sixteen, seventeen])
