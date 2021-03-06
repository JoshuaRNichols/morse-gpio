###############################################################################
# This is a morse code program designed for the Raspberry PI 
# Python 3.2
# morse_gpio.py 
# Written in 2015 by https://github.com/JoshuaRNichols/ 
#
# To the extent possible under law, the author(s) have dedicated all 
#   copyright and related and neighboring rights to this software to the
#   public domain worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication
#   along with this software. If not, 
#   see <http://creativecommons.org/publicdomain/zero/1.0/>. 
#
# ** Any imported libraries may have different licences. 
#    The author(s) claim no rights to those dependencies. 
#
###############################################################################
# 
# Thanks to user techthatinterest on YouTube for a tutorial on how to
# wire the GIPO:  https://youtu.be/R6s_7UaOSKA
# 
###############################################################################
# Prompts for user input
#  translates input through a morse code dictionary 
#  sends that code as dots '.' and dashes '_'
#   into the GPIO at position GPIO_NUM
#
# Possible applications: LEDs, piezzo buzzers, electric bells, etc.
###############################################################################

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

###############################################################################
# USER VARIABLES
###############################################################################
# What GPIO number do you want to output to?
GPIO_NUM = 17

# How many words per minute? 
# WPM_ = 2.4 * (dots per second)
WPM_ = 25 #words per minute 

# If you want the dots and dashes on the console
# Change this variable to True 
verbose_bool = False

# By default: calculated based on the WPM_ variable above.
# Set them manually if you prefer. 
DOT_LENGTH_ = (2.4 * (1 / WPM_))
DSH_LENGTH_ = (DOT_LENGTH_ * 3)
ELEM_PAUSE_ = (DOT_LENGTH_)
CHAR_PAUSE_ = (DOT_LENGTH_ * 3)
WORD_PAUSE_ = (DOT_LENGTH_ * 7)

###############################################################################
# END USER VARIABLES
###############################################################################




GPIO.setup(GPIO_NUM,GPIO.OUT)

# Implementing this as strings for readablity
MORSE_CODE = \
   {'A': '.-',     'B': '-...',   'C': '-.-.', 
    'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',
    'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',
    'P': '.--.',   'Q': '--.-',   'R': '.-.',
 	'S': '...',    'T': '-',      'U': '..-',
    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..',
        
    '0': '-----',  '1': '.----',  '2': '..---',
    '3': '...--',  '4': '....-',  '5': '.....',
    '6': '-....',  '7': '--...',  '8': '---..',
    '9': '----.' 
        }

def dot():
    GPIO.output(GPIO_NUM, True)
    time.sleep(DOT_LENGTH_)
    GPIO.output(GPIO_NUM, False)
    time.sleep(ELEM_PAUSE_)
    
def dash():
    GPIO.output(GPIO_NUM, True)
    time.sleep(DSH_LENGTH_)
    GPIO.output(GPIO_NUM, False)
    time.sleep(ELEM_PAUSE_)
    return
    
def char_pause():
    time.sleep(CHAR_PAUSE_)
    return
    
def word_pause():
    time.sleep(WORD_PAUSE_)
    return
    
def char_to_morse(m = ''):
    """
    parameter m is a single character. 
    if character is alphanumeric:
     return that character's morse string 
    else 
     return empty
    """

    if m.isalnum():
        return (MORSE_CODE[m.upper()]);
    else:
        return '';
    
def morse_char_to_GPIO(morse_char):
    """
    iterate though each element in a character's morse string
    do a character pause at the end of this character
    """
    for c in morse_char:
        if c == '-':
            dash()
        if c == '.':
            dot()
    char_pause()
    return

def morse_str_list_to_GPIO(word_list, verbose_bool = False):
    """ 
    Parameters: list of strings and verbose_bool
     Iterate through each word in the list
      for each character in the word, look up its morse_code_string 
      pass that morse_code_string into the GPIO
     pause at the end of every word 
    """

    for word in word_list:
        if verbose_bool: 
            print(word, "\n")

        morse_code_string = ""
        for c in word:
            morse_code_string = char_to_morse(c)
            if verbose_bool:
                print(c, ": ", morse_code_string)
            morse_char_to_GPIO(morse_code_string)
        
        word_pause()

    if verbose_bool:
        print()
    return;   

def main(verbose_bool = False):
    continue_bool = True
    print("Phrase to send (Enter to quit)")
    while continue_bool:
        phrase = input(": ")
        if phrase == "":
            continue_bool = False
            continue
        
        #create list of all words inputted by user, strip whitespace
        word_list = phrase.strip().split()

        #pass that list as an argument
        morse_str_list_to_GPIO(word_list, verbose_bool)
    
    print("\nCleaning up...")
    GPIO.cleanup()
    print("Exiting...")
    return 0;

main(verbose_bool)

