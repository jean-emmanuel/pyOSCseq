from time import sleep 
import liblo as _liblo
import threading
from scenes import scenes_list

class pyOSCseq(object):
    def __init__(self,bpm,port,target):
        self.bpm = bpm
        self.port = port
        self.target = target.split(' ')
        self.cursor = 0
        self.is_playing = 0
        self.sequences = {}
        self.scenes = {}
         
        self.server = _liblo.ServerThread(self.port)
        self.server.register_methods(self)
        self.server.start()
        
    @_liblo.make_method('/Sequencer/Play', 'f')
    def play(self):
        self.is_playing = 1
        self.cursor = 0
        while self.is_playing:
            for name in self.sequences:
                self.parseOscArgs(self.sequences[name].getArgs(self.cursor))
            self.cursor += 1
            sleep(60./self.bpm)
            
    @_liblo.make_method('/Sequencer/Stop', 'f')
    def stop(self):
        self.is_playing = 0
        
    @_liblo.make_method('/Sequencer/Sequence/Play', 's')
    def play_sequence(self,path,args):
        self.sequences[args[0]].play()
        
    @_liblo.make_method('/Sequencer/Sequence/Stop', 's')
    def stop_sequence(self,path,args):
        self.sequences[args[0]].stop()
    
    @_liblo.make_method('/Sequencer/Scene/Play', 's')
    def play_scene(self,path,args):
        if not args[0] in self.scenes:   
            self.scenes[args[0]] = threading.Thread(target=scenes_list, args=([self.parseOscArgs,args[0]]))
            self.scenes[args[0]].start()
        if not self.scenes[args[0]].is_alive():
            self.scenes[args[0]] = threading.Thread(target=scenes_list, args=([self.parseOscArgs,args[0]]))
            self.scenes[args[0]].start()

        
    @_liblo.make_method('/Sequence/Clip/Stop', 's')
    def stop_clip(self,path,args):
        self.clips[args[0]].stop()
        
    @_liblo.make_method('/test', None)
    def test(self,path,args):
        print args
            
    def addSequence(self,name,events):
        self.sequences[name] = self.sequence(self,name,events)
        
    def addClip(self,name,events):
        self.clips[name] = self.clip(self,name,events)
        
    def parseOscArgs(self,args):

        if not args:
            return

        if type(args[0]) is list:
            for i in range(len(args)):
                self.sendOsc(args[i])
        else:
            self.sendOsc(args)
                
    def sendOsc(self,args):
        path = str(args[0])
        if path[0]== ':':
            _liblo.send('osc.udp://localhost:'+str(self.port), path[1:], *args[1:])

        else:
            for i in range(len(self.target)):
                _liblo.send('osc.udp://'+self.target[i], path, *args[1:])


    """
    Sequence subclass : event loop synchronized by the sequencer's tempo
    """
    class sequence(object):
        def __init__(self,parent=None,name=None,events=None):
            self.name = name
            self.events = events
            self.beats = len(self.events)
            self.is_playing = True
            
        def getArgs(self,cursor):
            if not self.is_playing:
                return False
            return self.events[cursor%self.beats]
                
        def play(self):
            self.is_playing = True
        def stop(self):
            self.is_playing = False



seq = pyOSCseq(640,123451,'192.168.1.82:56418 192.168.1.82:7770 localhost:5555')



seq.addSequence('aa',[

    [':/Sequencer/Scene/Play', 'Intro_generique'],
    [':/Sequencer/Sequence/Stop', 'aa']

])

seq.play()
