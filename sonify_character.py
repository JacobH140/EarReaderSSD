import pandas as pd
import pyfiglet
from music21 import stream, chord

import playback


def sonify_character(character, c, pan_ratio, num_timesteps=-1, num_freq_bands=-1, audio_on=True):
    """Given a character and chord, RETURNS: a music21 stream object of music21
    chords corresponding to the character's sonification. current implementation (pyfiglet)
    doesn't use num_timesteps or num_freq_bands, but later versions might use different rendering
    strategies which would"""

    output = stream.Stream()

    df = make_character_array(character, font="univers")
    df = flip_character_array(df)  # flip the character aray to make indexing more intuitive

    possible_voices = enumerate_possible_voices(df, c)

    for timestep in range(len(df.iloc[0])):
        print(timestep)
        voicing = choose_voices(df, timestep, possible_voices)
        print(voicing.pitches)
        output.append(voicing)

    # output.show()

    if audio_on:
        s = playback.init()
        adjusted_output = playback.scale_stream_tempo(output, 0.25)
        fp = playback.stream_to_midi_file(adjusted_output)
        playback.synthesize_midi_test_1(s, fp, pan_ratio)

    return output


def choose_voices(df, timestep, possible_voices):
    """given a character dataframe, timestep, and possible notes,
    decides with respect to the freq band content of dataframe @ t-step
    which voices to write to output. RETURNS: a new chord object — this
    one being the one we'd like to sonify"""

    # NOTE: notes and frequency_bands are coindexed

    output_chord = chord.Chord()
    frequency_bands = df.iloc[:, timestep]

    for band_index in range(len(frequency_bands)):
        if frequency_bands[band_index] != '0':
            output_chord.add(possible_voices[band_index])

    return output_chord


def enumerate_possible_voices(df, c):
    """for the given timestep, returns ascending list of notes which are based off of spelling out the
    input chord c with respect to the number of freq bands"""
    # print(df)

    frequency_bands = df.iloc[:, 0]  # the timestep shouldn't matter, chose 0 arbitrarily
    chord_notes = [n for n in c]
    upper_voices = [octavate(chord_notes[(i + len(chord_notes)) % len(chord_notes)], (i + len(chord_notes)) // len(chord_notes)) for i in range(len(frequency_bands) - len(chord_notes))]
    chord_notes_enumerated = [*chord_notes, *upper_voices]

    return chord_notes_enumerated


def octavate(n, x):
    """transposes input up x octaves"""
    i = 0
    while i < x:
        n = n.transpose('P8')
        i += 1
    return n


def make_character_array(character, font="univers"):
    # helper function that uses pyfiglet to make a numpy array out of the input character
    figlet_string = pyfiglet.figlet_format(character, font=font)
    # print(figlet_string)

    output = [list(item.replace(' ', '0')) for item in figlet_string.splitlines()]
    df = pd.DataFrame(output)

    # now clean up the leading and trailing rows of all zeros in dataframe
    df = clean_leading_0_rows(df)
    df = clean_trailing_0_rows(df)

    return df


def clean_trailing_0_rows(df):
    index = 0
    num_rows = len(df[0])  # number of entries in first col is number of rows
    for ind, row in df[::-1].iterrows():
        if all([v == '0' for v in row.values]):  # i.e., if row has at least one nonzero element
            index += 1
        else:
            break
    return df.iloc[:(num_rows-index)].reset_index(drop=True)


def clean_leading_0_rows(df):
    index = 0
    for ind, row in df.iterrows():
        if all([v == '0' for v in row.values]):  # i.e., if row has at least one nonzero element
            index += 1
        else:
            break
    return df.iloc[index:].reset_index(drop=True)


def flip_character_array(df):
    print("before flip: ")
    print(df)
    for col_index in range(len(df.iloc[0])):
        df[col_index] = df[col_index].values[::-1]
    print("after flip: ")
    print(df)
    return df


if __name__ == "__main__":
    sonify_character('A', chord.Chord(['C4', 'E4', 'G4']), 5, 5)
    # sonify_character('B', chord.Chord(['C4', 'E4', 'G4']), 5, 5).show()
    # sonify_character('C', chord.Chord(['C4', 'E4', 'G4']), 5, 5).show()
