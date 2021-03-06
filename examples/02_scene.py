# encoding: utf-8



import sys
sys.path.append("../..")

from seqzero import Sequencer

import scenes


# Instanciate a sequencer listening on port 12345
# sending osc messages to localhost on port 5555
# with a bpm set to 120
seq = Sequencer(bpm=120, port=12345, target='localhost:5555', scenes=scenes)


# Add a sequence
seq.sequence_add('test',[
    ['/step', 1],
    ['/step', 2],
])

# Enale the sequence
seq.send(':/Sequencer/Sequence/Enable', 'test')

# Start the sequencer
seq.send(':/Sequencer/Play')

seq.start()

# now listen on port 5555 with your favorite tool...
# and send '/Sequencer/Scene/Play a' or '/Sequencer/Scene/Play b' on port 12345
