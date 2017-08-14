#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# http://cmusphinx.sourceforge.net/wiki/tutorialadapt
# http://cmusphinx.sourceforge.net/wiki/tutorialtuning

# you probably need the file /acoustic-model/mixture_weights to get better results in adaptation. Just check that you have it.


import time
from os import path
import speech_recognition as sr
import sys
import shutil
import os
import select
import subprocess


import pyaudio
import wave



language = "en-US"

inst_dir = "/usr/local/lib/python3.5/dist-packages/speech_recognition/pocketsphinx-data/"

libdir = "/usr/lib/"
bindir = "/usr/bin/"


FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024


AUDIO_FILE = ""




for (i, item) in enumerate(sys.argv):
    if item == "-h":
        print("Options:\n -l specify language\n -f specify file to recognize\n -t tune speech recognition voice model \n -r do recognize audio input (from microphone or file)")
        
    if item == "-l":
        language = sys.argv[i+1]
        print("LANGUAGE: " + language)
        
    if item == "-f":
        AUDIO_FILE = sys.argv[i+1]
        #we could build a telegram bot and let it recognize the wav files it gets as vocal messages
        
    if item == "-r":
        r = sr.Recognizer()
        m = sr.Microphone()
        try:
            print("Noise calibration. A moment of silence, please...")
            with m as source: r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            runrecognition = True
            while runrecognition:
                if AUDIO_FILE!="":
                    with sr.AudioFile(AUDIO_FILE) as fsource:
                        audio = r.record(fsource)  # read the entire audio file
                else:
                    print("Listening...") #Please, try to speak with you usual voice: if you talk too slow sphinx will not identify words boundaries
                    with m as source: audio = r.listen(source)
                print("Wait...")
                try:
                    # recognize speech using Google Speech Recognition
                    #value = r.recognize_google(audio) #https://cloud.google.com/speech/pricing
                    value = r.recognize_sphinx(audio, language)
                    print("You: {}".format(value))
                    if AUDIO_FILE!="":
                        runrecognition = False
                    os.system(os.path.abspath(os.path.dirname(sys.argv[0])) + "/zorba-cmd.py -p \"" + value + "\"")
                except sr.UnknownValueError:
                    print("???")
                except sr.RequestError as e:
                    print("Error; {0}".format(e))
        except KeyboardInterrupt:
            pass
        
    if item == "-t":
        #TODO: -copy immediately original language model in current_pwd and work only on the copy -edit if needed the feat.params file on the copy
        
        #we start to adapt the model
        current_pwd = os.getcwd() + "/training" #os.getcwd is probably a directory we can write without root permission, while this script folder probably not
        shutil.rmtree(current_pwd, ignore_errors=True)
        os.makedirs(current_pwd)
        
        fparams = inst_dir + language + "/acoustic-model/feat.params"
        params = open(fparams, 'r')
        paramscont = params.readlines()
        params.close()
        found = False
        for line in paramscont:
            if "-cmn current" in line:
                print("Found '-cmn current' in feat.params file. Good.")
                found = True

        if not found:
            print("Please take note that training MAY FAIL, since the file " + fparams + " does not contain the '-cmn current' line.")
        

        ph = []
        f = open(os.path.abspath(os.path.dirname(sys.argv[0])) + '/lang/' + language + '/sphinxadapt.txt','r')
        for line in f:
            ph.append(line.strip())
        f.close()
        
        audio = pyaudio.PyAudio()
        f1 = open(current_pwd + "/test.fileids", 'w')
        f2 = open(current_pwd + "/test.transcription", 'w')
        for (n, itemn) in enumerate(ph):
            f1.write("test" + str(n) + "\n")
            f2.write(itemn + " (test" + str(n) + ")\n")
            
            stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
            print("Please say: " + itemn + " And press ENTER.")
            frames = []
 
            runrecord = True
            while runrecord:
                data = stream.read(CHUNK)
                frames.append(data)
                if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
                    line = input()
                    runrecord = False
            
            stream.stop_stream()
            stream.close()

            waveFile = wave.open(current_pwd + "/test" + str(n) +".wav", 'wb')
            waveFile.setnchannels(CHANNELS)
            waveFile.setsampwidth(audio.get_sample_size(FORMAT))
            waveFile.setframerate(RATE)
            waveFile.writeframes(b''.join(frames))
            waveFile.close()
            
        f1.close()
        f2.close()
        audio.terminate()
        
        # verify accuracy
        command = bindir + "pocketsphinx_batch -adcin yes -cepdir " + current_pwd + " -cepext .wav -ctl " + current_pwd + "/test.fileids -lm " + inst_dir + language + "/language-model.lm.bin -dict " + inst_dir + language + "/pronounciation-dictionary.dict -hmm " + inst_dir + language + "/acoustic-model -hyp " + current_pwd + "/test.hyp"
        os.system(command)
        
        command = libdir + "sphinxtrain/scripts/decode/word_align.pl " + current_pwd + "/test.transcription " + current_pwd + "/test.hyp"
        os.system(command)
        ##
        
        #now build new language model
        shutil.copytree(inst_dir + language, current_pwd + "/" + language)

        command = bindir + "sphinx_fe -argfile " + current_pwd + "/" + language + "/acoustic-model/feat.params -samprate 16000 -c " + current_pwd + "/test.fileids -di " + current_pwd + " -do " + current_pwd + " -ei wav -eo mfc -mswav yes"
        os.system(command)
        
        command = bindir + "pocketsphinx_mdef_convert -text " + current_pwd + "/" + language + "/acoustic-model/mdef " + current_pwd + "/" + language + "/acoustic-model/mdef.txt"
        os.system(command)
        
        command = libdir + "sphinxtrain/bw -hmmdir " + inst_dir + language + "/acoustic-model -moddeffn " + current_pwd + "/" + language + "/acoustic-model/mdef.txt -ts2cbfn .cont. -feat 1s_c_d_dd -cmn current -agc none -dictfn " + inst_dir + language + "/pronounciation-dictionary.dict -ctlfn " + current_pwd + "/test.fileids -lsnfn " + current_pwd + "/test.transcription -accumdir" + current_pwd + " -lda " + current_pwd + "/" + language + "/acoustic-model/feature_transform"
        os.system(command)
        
        command = libdir + "sphinxtrain/mllr_solve -meanfn " + current_pwd + "/" + language + "/acoustic-model/means -varfn " + current_pwd + "/" + language + "/acoustic-model/variances -outmllrfn mllr_matrix -accumdir" + current_pwd
        os.system(command)
        
        shutil.copytree(current_pwd + "/" + language, current_pwd + "/" + language + "-adapt")
        
        command = libdir + "sphinxtrain/map_adapt -moddeffn " + current_pwd + "/" + language + "/acoustic-model/mdef.txt -ts2cbfn .cont. -meanfn " + current_pwd + "/" + language + "/acoustic-model/means -varfn " + current_pwd + "/" + language + "/acoustic-model/variances -mixwfn " + current_pwd + "/" + language + "/acoustic-model/mixture_weights -tmatfn " + current_pwd + "/" + language + "/acoustic-model/transition_matrices -accumdir" + current_pwd + " -mapmeanfn " + current_pwd + "/" + language + "-adapt/acoustic-model/means -mapvarfn " + current_pwd + "/" + language + "-adapt/acoustic-model/variances -mapmixwfn " + current_pwd + "/" + language + "-adapt/acoustic-model/mixture_weights -maptmatfn " + current_pwd + "/" + language + "-adapt/acoustic-model/transition_matrices"
        os.system(command)
        
        command = libdir + "sphinxtrain/mk_s2sendump -pocketsphinx yes -moddeffn " + current_pwd + "/" + language + "-adapt/acoustic-model/mdef.txt -mixwfn " + current_pwd + "/" + language + "-adapt/acoustic-model/mixture_weights -sendumpfn " + current_pwd + "/" + language + "-adapt/acoustic-model/sendump"
        os.system(command)
        
        # verify accuracy of new model
        command = bindir + "pocketsphinx_batch -adcin yes -cepdir " + current_pwd + " -cepext .wav -ctl " + current_pwd + "/test.fileids -lm " + inst_dir + language + "-adapt/language-model.lm.bin -dict " + inst_dir + language + "-adapt/pronounciation-dictionary.dict -hmm " + inst_dir + language + "-adapt/acoustic-model -hyp " + current_pwd + "/test-adapt.hyp"
        os.system(command)
        
        command = libdir + "sphinxtrain/scripts/decode/word_align.pl " + current_pwd + "/test.transcription " + current_pwd + "/test-adapt.hyp"
        os.system(command)
        ##
        
        
       
        yes = set(['yes','y', 'ye'])
        no = set(['no','n', ''])

        choice = ''
        if "linux" in sys.platform:
            print("Do you want to INSTALL the new voice model? [y/N]")
            choice = input().lower()
            #if you are not on a GNU/Linux system, you may install manually the new voice model
   
        if choice in yes:
            subprocess.call(['sudo','/bin/rm','-r', inst_dir + language + '-adapt'])
            subprocess.call(['sudo','/bin/cp','-r', current_pwd + '/' + language + '-adapt', inst_dir + language + '-adapt'])
            print("Installed in " + inst_dir + language + '-adapt')
            print("To use the new model just run this program with the following option: -l " + language + '-adapt')
        else:
            print("You can find the new model files in " + current_pwd + '/' + language + '-adapt')
