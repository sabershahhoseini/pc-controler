# Listens on http://192.168.1.104:8800/{hotkey} and when the url is requested, passes the
# requested hotkey to pressKey to press hotkey using pynput module

import socketserver
import socket
import subprocess
from http.server import BaseHTTPRequestHandler
from pynput.keyboard import Key, Controller
import platform

ip = '192.168.1.104'
port = 8800

# A list of hotkeys and their equal for pynput as dictionary
hotkeys_list = {'volume-up' : Key.media_volume_up, 'volume-down' : Key.media_volume_down,
        'right' : Key.right, 'left': Key.left, 'pause-play-toggle' : Key.media_play_pause,
        'space' : Key.space, 'enter' : Key.enter, 'next-song' : Key.media_next, 'previous-song' : Key.media_previous}

keyboard = Controller()

def pressKey(hotkey):
    # Based on the requested url from user, send hotkey to the pc
    hotkey = hotkey.lstrip('/')
    print(hotkey)
    if hotkey in hotkeys_list.keys():
        keyboard.press(hotkeys_list[hotkey])
        keyboard.release(hotkeys_list[hotkey])
    elif hotkey == 'exit':
        with keyboard.pressed(Key.alt):
            keyboard.press(Key.f4)
            keyboard.release(Key.f4)
    elif hotkey == 'shutdown':
        if platform.system() == 'Linux':
            subprocess.call(['shutdown', 'now'])
        elif platform.system() == 'Windows':
            subprocess.call(['shutdown', '/s'])


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """get url path (hotkey) and send it to pressKey"""
        pressKey(self.path)
        self.send_response(200)

class MyTCPServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
        
"""Start serving on localhost and port 8800"""
httpd = MyTCPServer((ip, port), MyHandler)
print("Serving forever...")
httpd.serve_forever()
