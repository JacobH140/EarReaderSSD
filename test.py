from pyo import *
from mido import MidiFile


def working_playback(started_server, midi_file_path):

    # A little audio synth to play the MIDI events.
    mid = Notein()
    amp = MidiAdsr(mid["velocity"])
    pit = MToF(mid["pitch"])
    osc = Osc(SquareTable(), freq=pit, mul=amp).mix(1)
    rev = STRev(osc, revtime=1, cutoff=4000, bal=0.2).out()

    # Opening the MIDI file...
    mid = MidiFile(midi_file_path)

    # ... and reading its content.
    for message in mid.play():
        started_server.addMidiEvent(*message.bytes())


if __name__ == "__main__":
    working_playback()