import json
import assets.data.soundmap as soundmap
from models.soundset import SoundSet, SoundKey 
from camelcase import CamelCase
from pydub import AudioSegment
from pydub.playback import play

class Soundboard:
  soundDir = ''
  sets = [];

  def __init__(self):
    print('Soundboard initialized')
    self.loadSoundMap()

  def loadSoundMap(self):
    with open('assets/data/soundmap.json', 'r') as file:
      soundMap = json.load(file)

    soundDir = soundMap['soundDir']
    for soundSet in soundMap['sets']:
      self.sets.append( SoundSet(soundSet) )

    for soundSet in self.sets:
      print( soundSet.name + ' ' + str(len(soundSet.soundKeys)) );

  def playSound( self, filename ): 
    sound = AudioSegment.from_wav( soundDir + filename );
    play( sound )
