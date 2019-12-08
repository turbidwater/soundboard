import json
import assets.data.soundmap as soundmap
from models.soundset import SoundSet, SoundKey 
from camelcase import CamelCase
from pydub import AudioSegment
from pydub.playback import play
import keyboard

class Soundboard:
  soundDir = ''
  sets = []
  currentSetIndex = 0
  volumeModifier = 5
  maxVol = 20
  minVol = 0
  reverse = False


  def __init__(self):
    self.loadSoundMap()
    print('Soundboard initialized')
    self.addListeners()


  def addListeners(self):
    keyboard.add_hotkey( 'shift+left', lambda: self.changeSet(-1) )
    keyboard.add_hotkey( 'shift+right', lambda: self.changeSet(1) )
    keyboard.add_hotkey( 'shift+up', lambda: self.changeVolume(1) )
    keyboard.add_hotkey( 'ctrl+down', lambda: self.toggleReverse(False) )
    keyboard.add_hotkey( 'ctrl+up', lambda: self.toggleReverse(True) )


  def loadSoundMap(self):
    with open('./assets/data/soundmap.json', 'r') as file:
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
      keyboard.add_hotkey(sound.key, self.playSound, args=[self.buildFileName(soundSet.name, sound.file)]) 


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
    print( self.volumeModifier )


  def toggleReverse( self, reverseOn ):
    self.reverse = reverseOn


  def buildFileName( self, setName, filename ):
    return self.soundDir + setName + '/' + filename


  def playSound( self, filename ): 
    if '.wav' in filename:
      sound = AudioSegment.from_wav(filename)
    else:
      sound = AudioSegment.from_mp3(filename)

    sound = sound.apply_gain(self.volumeModifier)

    if self.reverse:
      sound = sound.reverse()

    play( sound )
