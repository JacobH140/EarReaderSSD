from music21 import midi
from mido import MidiFile
from pyo import *


def init():
    return Server().boot().start()


def set_stream_tempo(note_stream, tempo=0.5):
    return note_stream.augmentOrDiminish(tempo)


def stream_to_midi_experiment(note_stream):
    """used to take the stream of chords for a character and make it into midi event sequence"""

    full_event_list = []

    for c in note_stream:
        partial_event_list = midi.translate.chordToMidiEvents(c)
        full_event_list = [*full_event_list, *partial_event_list]

    # print(full_event_list)
    return full_event_list


def stream_to_midi_file(note_stream):
    """writes stream to temp midi file to be 'picked up' by other libs; returns the filepath"""
    fp = note_stream.write('midi', fp='/Users/jacobhume/PycharmProjects/EarReaderSSD/midifile.mid')
    return fp


def mido_to_pyo_demo(started_server, midi_file_path):
    """reads in a midi file with mido and sends the events to pyo"""

    # ALSO not necessary later, just a little audio synth to play the MIDI events.
    mid = Notein()  # i think this listens for midi events
    amp = MidiAdsr(mid["velocity"])
    pit = MToF(mid["pitch"])
    osc = Osc(SquareTable(), freq=pit, mul=amp).mix(1)
    rev = STRev(osc, revtime=1, cutoff=4000, bal=0.2)

    # Opening the MIDI file...
    mid = MidiFile(midi_file_path)
    print(mid.type)

    # ... and reading its content.

    # binaural_pan = Binaural(rev, azimuth=90, elevation=15).out()
    # binaural_pan.ctrl()
    #pan = Pan(rev, outs=2, pan=0.1, spread=0.1)

    # print(mid.play())
    # print(Sine())
    # started_server.gui(locals())
    for message in mid.play():
        # For each message, we convert it to integer data with the bytes()
        # method and send the values to pyo's Server with the addMidiEvent()
        # method. This method programmatically adds a MIDI message to the
        # server's internal MIDI event buffer.

        started_server.addMidiEvent(*message.bytes())

        # playback_midi_message(started_server, message, -90, 60) # arbitrarily chosen for now; later make into parameters


def playback_midi_message(started_server, message, azi, ele):
    """plays back the midi event with relevant panning parameters"""
    example(Binaural)
    binaural_pan = Binaural(*message.bytes(), azimuth=azi, elevation=ele).out()
    started_server.addMidiEvent(binaural_pan)


def basic_playback_draft(note_stream):
    player = midi.realtime.StreamPlayer(note_stream)
    player.play()


def pyoExample():
    s = Server().boot()
    s.start()
    a = Sine(mul=0.01).out()
    s.gui(locals())

# pyoExample()
