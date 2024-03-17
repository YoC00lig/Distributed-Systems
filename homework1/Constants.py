HOST = '127.0.0.1'
PORT = 8888

GROUP = '224.1.1.1'
MULTICAST_PORT = 8888

TIME_TO_LIVE = 2

ENCODING = 'utf-8'
BUFFER_SIZE = 1024
TIMEOUT_DURATION = 0.01

PINK = '\033[38;2;255;20;147m'  
DEFAULT = '\033[0m'
GREEN = '\033[38;2;0;255;0m'  
RED = '\033[38;2;255;0;0m'  
BLUE = '\033[38;2;0;0;255m'  

WELCOME_MESSAGE = f'{DEFAULT} Hello! Please, choose your nick (Remember, it will be visible to all participants. Later, you will not be able to edit it) : '
CLIENT_JOIN_MESSAGE = f'{BLUE} Hello! Read the chat rules carefully. \n -> Sending "Q" message will cause you to leave the chat.\n -> Sending "U" message will send ASCII art picture to other chat participants.\n -> Sending "M" message will send ASCII art picture via multicast.\n -> To send a message, you need to press ENTER.\n I wish you a pleasant conversation.:)\n'

PICTURE_U = """
 _( o)>
 \ <_. )
  `---'
"""

PICTURE_M = """
 /\_/\  
( o.o ) 
 > ^ <
"""