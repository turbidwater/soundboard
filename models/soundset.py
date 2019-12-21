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
  code = 0

  def __init__(self, obj):
    if (obj):
      self.translate(obj)

  def translate(self, obj):
    self.name = obj['name']
    self.key = obj['key']

    if (bool(obj.get('file'))):
      self.file = obj.get('file')

    if (bool(obj.get('code'))):
      self.code = obj.get('code')

    if (not bool(self.name) and bool(self.file)):
      self.name = self.file.split('.')[0]