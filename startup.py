from soundboard import Soundboard
import keyboard
import threading
import os


# TODO uncomment sound = Soundboard()

programEndRequested = threading.Event()

def listenForKeys():
  keyboard.on_release_key('enter', endProgram )

def endProgram(keyboardEvent):
  if (keyboard.is_pressed('ctrl')): 
    programEndRequested.set()

def main():
  thread = threading.Thread(target=listenForKeys)
  thread.start()
  programEndRequested.wait()
  # TODO uncomment sound.playSound(os.path.dirname(os.path.realpath(__file__)) + '/assets/sounds/goodbye.mp3')

if __name__ == '__main__':
  # TODO uncomment main()