import pygame
import paramiko
import select
from midiutil.MidiFile import MIDIFile

MUSIC_FILENAME = 'goldengate.mid'
LOGFILE = 'goldengate.log'

MAJOR = "ttsttts"
MINOR = "tsttstt"

CLIENT = paramiko.SSHClient()
CLIENT.set_missing_host_key_policy(paramiko.AutoAddPolicy())
rsa = paramiko.RSAKey.from_private_key_file('/home/franhp/.ssh/id_rsa')
CLIENT.connect('localhost',username='franhp',pkey=rsa)
transport = CLIENT.get_transport()
CHANNEL = transport.open_session()
CHANNEL.exec_command('tail -f /home/franhp/code/logs2music/goldengate.log')


def make_scale(definition):
  val = 0
  i = 0
  scale = []
  while len(scale) < 256:
    scale.append(val)
    val += 2 if definition[i] == "t" else 1
    i = (i + 1) % len(definition)
  return scale


def addTrack(midi, track_number, track_name, tempo):
    midi.addTrackName(track_number, 1, track_name)

    # tempo in beats per minute
    midi.addTempo(track_number, 0, tempo)

def writeFile(midi, filename):
    binfile = open(filename, 'wb')
    midi.writeFile(binfile)
    binfile.close()

def addNotes(midi, fileText):
    """
        Arguments:
            track: The track to which the note is added.
            channel: the MIDI channel to assign to the note. [Integer, 0-15]
            pitch: the MIDI pitch number [Integer, 0-127].
            time: the time (in beats) at which the note sounds [Float].
            duration: the duration of the note (in beats) [Float].
            volume: the volume (velocity) of the note. [Integer, 0-127].
    """

    minimum = ord('A')
    maximum = ord('z')
    scale = make_scale(MAJOR)
    x = 0
    for lines in fileText:
        
        for letter in lines:
                pitch = ord(letter)-minimum
                #print "Letter:",letter,"pitch:",pitch
                if pitch < 127 and pitch > 0:
                        #print "Adding note", scale[pitch]
                        midi.addNote(0, 0, scale[pitch], x, 5, 100)
                        midi.addNote(0, 0, scale[pitch + (3 if letter in "aeiouAEIOU" else 2)], x, 5, 100)
                x += 1

def generate_midi(logfile):
    myMidi = MIDIFile(2)

    addTrack(myMidi, 0, 'track-1', 350)
    addTrack(myMidi, 1, 'track-2', 350)

    addNotes(myMidi, logfile)

    writeFile(myMidi, MUSIC_FILENAME)

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)


try:
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(1.0)

    while True:
        rl, wl, xl = select.select([CHANNEL],[],[],0.0)
        if len(rl) > 0:
            tail = CHANNEL.recv(1024)
            print tail
            generate_midi(tail)
            play_music(MUSIC_FILENAME)
except KeyboardInterrupt:
    # if user hits Ctrl/C then exit
    # (works only in console mode)
    pygame.mixer.music.fadeout(1000)
    pygame.mixer.music.stop()
    raise SystemExit