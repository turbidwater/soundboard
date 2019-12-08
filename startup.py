from soundboard import Soundboard
import keyboard
import threading


sound = Soundboard()

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
  sound.playSound('assets/sounds/goodbye.mp3')

if __name__ == '__main__':
  main()