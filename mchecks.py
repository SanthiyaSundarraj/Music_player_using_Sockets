import socket
import pyaudio
import wave
import os
from _thread import *
from pydub import AudioSegment
import fnmatch
#import glob

AudioSegment.converter = r"C:\ffmpeg-N-99544-gf7fd205f11-win64-gpl-shared\ffmpeg-N-99544-gf7fd205f11-win64-gpl-shared\bin\ffmpeg.exe"


def clientthread(conn, address):
    print("<", address, ">  connected ")
    while True:

        resource = os.listdir(r"C:\Users\Home\Documents\pyMusic")
        #mp3_files = glob.iglob('**/*.mp3', recursive=True)
        pattern = "*.mp3"
        ss = "\n\n\n\n \t\t Media Player \n"
        for i in range(len(resource)):
            if fnmatch.fnmatch(resource[i], pattern):
                if i % 2 == 0:
                    ss += "\n"
                resource[i] = resource[i][:-4]
                ss = ss+"\t"+resource[i]+"\t"
        conn.send(ss.encode())
        x = conn.recv(1024).decode()
        for i in resource:
            if x.lower() == i.lower():
                print("song found")
                conn.send("1".encode())
                x = i
                break
        else:
            conn.send("0".encode())
            continue
        x = r"C:\Users\Home\Documents\pyMusic/"+x+".mp3"
        sound = AudioSegment.from_mp3(x)
        sound.export("file.wav", format="wav")
        print(x)
        wf = wave.open("file.wav", 'rb')

        p = pyaudio.PyAudio()

        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)

        data = 1
        while data:
            data = wf.readframes(CHUNK)
            conn.send(data)


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("192.168.43.103", 2244))

server_socket.listen(10)
while True:
    conn, address = server_socket.accept()
    start_new_thread(clientthread, (conn, address))