# encoding: utf-8

"""
OSC Feeds

Args:
    sequencer (Sequencer)

Returns:
    Useful data in a dictionnary, that will be serialized and sent to the
    subscribers by the sequencer
"""

def transport(sequencer):
    return {
        'bpm': sequencer.bpm,
        'cursor': sequencer.cursor,
        'playing': sequencer.playing
    }

def sequences(sequencer):
    data = {}

    for name in sequencer.sequences:
        data[name] = {
            'steps': sequencer.sequences[name].steps,
            'playing': sequencer.sequences[name].playing
        }

    return data

def scenes(sequencer):
    data = {}

    for name in sequencer.scenes_list:
        data[name] = {
            'playing': name in sequencer.scenes and sequencer.scenes[name].is_alive()
        }

    return data
