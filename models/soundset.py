class SoundSet:
  name = ''
  soundKeys = []

  def __init__(self, obj):
    if obj:
      self.translate(obj)

  def translate(self, obj):
    self.name = obj['name']

    if obj['sounds']:
      self.soundKeys = []
      for sound in obj['sounds']:
        self.soundKeys.append( SoundKey(sound) )


class SoundKey:
  name = ''
  key = ''
  file = ''

  def __init__(self, obj):
    if (obj):
      self.translate(obj)

  def translate(self, obj):
    self.name = obj['name']
    self.key = obj['key']

    if (bool(obj.get('file'))):
      self.file = obj.get('file')