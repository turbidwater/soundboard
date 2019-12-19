from soundboard import Soundboard
import keyboard
import threading
import os


sound = Soundboard()

programEndRequested = threading.Event()

def listenForKeys():
  keyboard.on_release_key('enter', endProgram )
  keyboard.on_release(onKey)

def onKey(keyboardEvent):
  print('{"name":"","key":"' + keyboardEvent.name + '", "code": "' + str(keyboardEvent.scan_code) + '"},')

def endProgram(keyboardEvent):
  if (keyboard.is_pressed('ctrl')): 
    programEndRequested.set()

def main():
  thread = threading.Thread(target=listenForKeys)
  thread.start()
  programEndRequested.wait()
  
  sound.cleanUp()

if __name__ == '__main__':
  main()
