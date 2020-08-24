#!/usr/bin/python

import ctypes
import os
import re
import struct
import sys
import argparse
import datetime
import numpy as np
from config import *

#========================== Display / Color  ==================================#
def ClearTerminal():
  os.system('cls' if os.name=='nt' else 'clear')  

# Required for colored text 
def get_csbi_attributes(handle):
  import struct
  csbi = ctypes.create_string_buffer(22)
  res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
  # assert res
  if res:
    (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    return wattr

# Constants from the Windows API
STD_OUTPUT_HANDLE = -11
COLOR_BLACK       = 0x00
COLOR_DARK_RED    = 0x04
COLOR_GRAY        = 0x08
COLOR_GREEN       = 0x0A
COLOR_CYAN        = 0x0B
COLOR_RED         = 0x0C
COLOR_PINK        = 0x0D
COLOR_YELLOW      = 0x0E
COLOR_WHITE       = 0x0F

if (os.name != "posix"):
  color_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
  color_reset = get_csbi_attributes(color_handle)


# Set background and foreground color  
def setColor(foreground=0xF, background=0x0):
  if (os.name != "posix"):
    ctypes.windll.kernel32.SetConsoleTextAttribute(color_handle, foreground | (background << 4))

  
# Set colors back to normal
def resetColor():
  if (os.name != "posix"):
    ctypes.windll.kernel32.SetConsoleTextAttribute(color_handle, color_reset)

def printError(msg):
  if (os.name == "posix"):
    print("\033[91m"+str(msg)+"\033[0m")
  else:
    setColor(COLOR_RED); print(msg); resetColor()
    
def printComment(msg):
  if (os.name == "posix"):
    print("\033[94m"+str(msg)+"\033[0m")
  else:
    setColor(COLOR_CYAN); print(msg); resetColor()
    
def printGreen(msg):
  if (os.name == "posix"):
    print("\033[92m"+str(msg)+"\033[0m")
  else:
    setColor(COLOR_GREEN); print(msg); resetColor()
    
def printYellow(msg):
  if (os.name == "posix"):
    print("\033[93m"+str(msg)+"\033[0m")
  else:
    setColor(COLOR_YELLOW); print(msg); resetColor()

def printGrayDate(msg):
  try:
    matchObj = None
    matchObj = re.match(r'(\[.*\])(.*)', msg)
  except TypeError as te:
    print("Type Error. Got msg = ",msg)
    
  if not matchObj:
    print("Error in printGrayDate. Expected message of format: [xxx] Message.")
    print(msg)
    return msg
  if matchObj.group(2) == " PING":
    return str(matchObj.group(2))
  if (os.name == "posix"):
    print("\x1b[37;2m"+str(matchObj.group(1))+"\033[0m" + str(matchObj.group(2)))
  else:
    setColor(COLOR_GRAY); sys.stdout.write(str(matchObj.group(1))); resetColor(); print(str(matchObj.group(2)))
  return str(matchObj.group(2))

def console_print(header, msg, method='normal'):
  msg_str = datetime.datetime.now().strftime("[{} %Y-%m-%dT%H:%M:%S] {}".format(header, msg))
  if method == 'normal':
    printGreen(msg_str)
  elif method == 'error':
    printError(msg_str)

#########################
### Utility Functions ###
#########################
def generate_dir(child_dir, dt='now'):
  if dt == 'now':
    dt = datetime.datetime.now()
  dir_dt = dt.strftime('%Y/%m/%d')
  return os.path.join(DIR_DATA_PARENT, dir_dt, child_dir)

def move_file(src, dst):
  dst_dir = os.path.split(dst)[0]
  if not os.path.exist(dst_dir):
    os.makedirs(dst_dir)
  shutil.move(src, dst)

def render_numeric_value(value):
  try:
    num = float(value)

    if num == 0.:
      return ' 0.00'
    sgn = ' ' if np.sign(num) == 1 else ''
    exp = np.floor(np.log10(np.abs(num))/3.)

    if exp == 0:
      return sgn+"{:.2f}".format(num)
    else:
      return sgn+"{:.2f}e{:d}".format(num/(10**(3*exp)), int(3*exp))

  except:
    return str(value)