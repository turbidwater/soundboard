import json
import keyboard
import pyttsx3
from pydub import AudioSegment
from pydub.playback import play

import assets.data.soundmap as soundmap
from models.soundset import SoundSet, SoundKey 

class Soundboard:
  tts = pyttsx3.init('sapi5', True) ### change to espeak or empty

  soundDir = ''
  sets = []
  currentSetIndex = 0
  volumeModifier = 5
  maxVol = 20
  minVol = 0
  altMode = False


  def __init__(self):
    self.loadSoundMap()

    self.tts.setProperty('volume', self.volumeModifier / self.maxVol)
    self.tts.connect( 'error', self.onTTSError)

    self.tts.connect('started-utterance', self.onTTSStartUtterance)
    self.tts.connect('started-word', self.onTTSStartWord)
    self.tts.connect('finished-utterance', self.onTTSFinishedUtterance)
    
    print('Soundboard initialized')
    self.addListeners()


  def addListeners(self):
    keyboard.add_hotkey( 'shift+left', lambda: self.changeSet(-1) )
    keyboard.add_hotkey( 'shift+right', lambda: self.changeSet(1) )
    keyboard.add_hotkey( 'shift+up', lambda: self.changeVolume(1) )
    keyboard.add_hotkey( 'shift+down', lambda: self.changeVolume(-1) )
    keyboard.add_hotkey( 'ctrl+down', lambda: self.toggleAltMode(False) )
    keyboard.add_hotkey( 'ctrl+up', lambda: self.toggleAltMode(True) )


  def loadSoundMap(self):
    with open('assets/data/soundmap.json', 'r') as file:
      soundMap = json.load(file)

    self.soundDir = soundMap['soundDir']
    for soundSet in soundMap['sets']:
      self.sets.append( SoundSet(soundSet) )

    self.loadSoundSet(self.sets[self.currentSetIndex])


  def loadSoundSet( self, soundSet ):
    print( 'loading ' + soundSet.name )
    self.playSound( self.soundDir + 'loading.mp3' )
    self.playSound( self.buildFileName(soundSet.name, soundSet.name + '.mp3'))
    for sound in soundSet.soundKeys:
      if len(sound.file) > 0:
        keyboard.add_hotkey(sound.key, self.playSound, args=[self.buildFileName(soundSet.name, sound.file)]) 
      else:  
        keyboard.add_hotkey(sound.key, self.speakWord, args=[sound.name]) 


  def unloadSoundSet(self):
    keyboard.remove_all_hotkeys()
    self.addListeners()


  def changeSet( self, dir ):
    self.unloadSoundSet()
    self.currentSetIndex += dir
    if (self.currentSetIndex < 0):
      self.currentSetIndex = len(self.sets) - 1
    elif (self.currentSetIndex >= len(self.sets)):
      self.currentSetIndex = 0

    self.loadSoundSet( self.sets[self.currentSetIndex] )


  def changeVolume( self, dir ):
    self.volumeModifier += dir
    if (self.volumeModifier < self.minVol):
      self.volumeModifier = self.minVol
    elif (self.volumeModifier > self.maxVol):
      self.volumeModifier = self.maxVol

    self.tts.setProperty('volume', self.volumeModifier / self.maxVol)

  def toggleAltMode( self, altModeOn ):
    self.altMode = altModeOn

    voices = self.tts.getProperty('voices')
    voice = voices[1].id if altModeOn else voices[0].id
    self.tts.setProperty('voice', voice)


  def buildFileName( self, setName, filename ):
    return self.soundDir + setName + '/' + filename


  def speakWord(self, word):
    print('### speak ' + word)
    self.tts.say(word, word)
    self.tts.runAndWait()
    print('### complete')
    self.tts.stop()

  def playSound( self, filename ): 
    if '.wav' in filename:
      sound = AudioSegment.from_wav(filename)
    else:
      sound = AudioSegment.from_mp3(filename)

    sound = sound.apply_gain(self.volumeModifier)
    if self.altMode:
      sound = sound.reverse()

    play( sound )


  def cleanUp(self):
    self.playSound('assets/sounds/goodbye.mp3')
    self.tts.stop()

  def onTTSStartUtterance( self, name ):
    print('### started ' + name)
  def onTTSStartWord( self, name, location, length ):
    print('### started word ' + str(location) + ' of ' + name)
  def onTTSFinishedUtterance( self, name, completed ):
    print('### finished ' + name + '? ' + str(completed))

  def onTTSError( self, name, exception ):
    print( 'Error for ' + name )
    print( str(exception) ) 
