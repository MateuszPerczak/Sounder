import os
import time
import threading
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory

PlayerForm = Tk()
PlayerForm.geometry('800x500')
PlayerForm.title("Sounder!")
PlayerForm.resizable(width=FALSE, height=FALSE)
PlayerForm.iconbitmap("Soundericon.ico")
PlayerForm.configure(background='#ffffff')
s = ttk.Style()
s.theme_use('clam')
s.configure("G.Horizontal.TProgressbar", foreground='#8bc34a', background='#8bc34a', lightcolor='#8bc34a',
            darkcolor='#8bc34a', bordercolor='#ffffff', troughcolor='#ffffff')
s.configure("W.TLabel", background='#ffffff', border='0')
tryv = 0
PlayLabelText = StringVar()
DirectoryLabelText = StringVar()
GenreLabelText = StringVar()
BitrateLabelText = StringVar()
VolumeValue = StringVar()
listofsongs = []
maxsong = 0
state = 0
songnumber = 0
playbuttonstate = 0
# ikony
PlayPhotoimg = PhotoImage(file="musicicon.png")
Playimg = PhotoImage(file="play.png")
Pauseimg = PhotoImage(file="pause.png")
Forwardimg = PhotoImage(file="forward.png")
Previousimg = PhotoImage(file="previous.png")
Fileimg = PhotoImage(file="file-directory.png")
MusicLabelimg = PhotoImage(file="sounder.png")
sounderdirectory = os.getcwd()


def musicscan():
    global directory
    global maxsong
    global listofsongs
    global playbuttonstate
    global state
    global songnumber
    state = 0
    songnumber = 0
    try:
        os.chdir(directory)
    except:
        os.chdir(sounderdirectory)
        os.remove('Data.sou')
        directory = askdirectory()
        if directory == "" or None:
            exit("Directory is empty!!")
        with open('Data.sou', 'a')as data:
            data.write(directory)
        os.chdir(directory)
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            maxsong += 1
            state = 1
            listofsongs.append(file)
    if state == 1 and playbuttonstate == 0:
        mixer.music.load(listofsongs[songnumber])


def firststart():
    print("Hello from Mateusz Perczak and Krzysztof Zawisła")
    global directory
    if os.path.exists('Data.sou'):
        with open('Data.sou', 'r') as data:
            directory = data.readline()
    elif not os.path.exists('Data.sou'):
        directory = askdirectory()
        with open('Data.sou', 'a')as data:
            data.write(directory)
    if directory == "" or None:
        exit("Directory is empty!!")
    mixer.init()
    musicscan()


def changedirectory(event):
    print(event)
    global directory
    global sounderdirectory
    global state
    global maxsong
    global listofsongs
    newdirectory = askdirectory()
    if directory != newdirectory and newdirectory != "" or None:
        os.chdir(sounderdirectory)
        with open('Data.sou', 'w') as data:
            data.write(newdirectory)
        listofsongs = []
        for file in range(maxsong + 1):
            MusicListBox.delete(0)
        directory = newdirectory
        DirectoryLabelText.set(directory)
        musicscan()
        update(state)


def update(cstate):
    global listofsongs
    global maxsong
    if cstate == 1:
        listofsongs.reverse()
        for file in listofsongs:
            MusicListBox.insert(0, file)
        listofsongs.reverse()
    elif cstate == 0:
        MusicListBox.delete(0, END)
        maxsong = 0
        listofsongs = []


def playsong(event):
    print(event)
    global playbuttonstate
    global songnumber
    global listofsongs
    global state
    if state == 1:
        if playbuttonstate == 1:
            mixer.music.stop()
            time.sleep(0.1)
            PlayButton.configure(image=Playimg)
            playbuttonstate = 0
        elif playbuttonstate == 0:
            mixer.music.load(listofsongs[songnumber])
            PlayLabelText.set(listofsongs[songnumber])
            mixer.music.play()
            PlayButton.configure(image=Pauseimg)
            playbuttonstate = 1
            progressupdate()
    elif state == 0:
        if playbuttonstate == 1:
            mixer.music.stop()
            time.sleep(0.1)
            PlayLabelText.set("")
            PlayButton.configure(image=Playimg)
            playbuttonstate = 0


def nextsong(event):
    print(event)
    global playbuttonstate
    global songnumber
    global state
    global maxsong
    if state == 1:
        if playbuttonstate == 1:
            if songnumber < maxsong - 1:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButton.configure(image=Pauseimg)
                playbuttonstate = 1
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                PlayLabelText.set(listofsongs[songnumber])
                progressupdate()
        if playbuttonstate == 0:
            if songnumber < maxsong - 1:
                mixer.music.stop()
                time.sleep(0.1)
                playbuttonstate = 1
                PlayButton.configure(image=Pauseimg)
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                PlayLabelText.set(listofsongs[songnumber])
                progressupdate()


def previoussong(event):
    print(event)
    global playbuttonstate
    global songnumber
    global state
    if state == 1:
        if playbuttonstate == 1:
            if songnumber > 0:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButton.configure(image=Pauseimg)
                songnumber -= 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                PlayLabelText.set(listofsongs[songnumber])
                progressupdate()
        if playbuttonstate == 0:
            if songnumber > 0:
                mixer.music.stop()
                time.sleep(0.1)
                playbuttonstate = 1
                PlayButton.configure(image=Pauseimg)
                songnumber -= 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                PlayLabelText.set(listofsongs[songnumber])
                progressupdate()


def musiclistboxpointer(event):
    print(event)
    global tryv
    global selected
    global curent
    global state
    global songnumber
    global playbuttonstate
    global listofsongs
    tryv += 1
    if tryv == 2:
        mixer.music.stop()
        time.sleep(0.1)
        if state == 1:
            selected = MusicListBox.curselection()
            if selected != ():
                mixer.music.stop()
                time.sleep(0.1)
                for Song in selected:
                    curent = MusicListBox.get(Song)
                for nr, Song in enumerate(listofsongs):
                    if Song == curent:
                        mixer.music.load(listofsongs[nr])
                        songnumber = nr
                        mixer.music.play()
                        if playbuttonstate == 0:
                            playbuttonstate = 1
                            PlayButton.configure(image=Pauseimg)
                        PlayLabelText.set(listofsongs[songnumber])
                        progressupdate()
                        tryv = 0


def volume(value):
    global VolumeValue
    value = float(value)
    value = round(value, 0)
    value = int(value)
    VolumeValue.set("{}%".format(value))
    value = value / 100
    mixer.music.set_volume(value)


def progressupdate():
    global listofsongs
    global songnumber
    global playbuttonstate
    file = MP3(listofsongs[songnumber])
    bitratevar = file.info.bitrate
    bitratevar = bitratevar / 1000
    bitratevar = int(bitratevar)
    BitrateLabelText.set("{}kbps".format(bitratevar))
    try:
        fileinfo = file.tags['TCON']
        GenreLabelText.set(fileinfo)
    except:
        GenreLabelText.set("None")
    progressvalue = round(file.info.length, 1)
    progressvalue = progressvalue * 10
    progressvalue = int(progressvalue)
    if playbuttonstate == 0:
        PlayButton.configure(image=Pauseimg)
    pbf = threading.Thread(target=progressbarfill, args=(progressvalue,))
    pbf.daemon = True
    pbf.start()


def progressbarfill(totallength):
    global playbuttonstate
    MusicProgressBar["maximum"] = totallength
    elapsed = 0
    while elapsed <= totallength and mixer.music.get_busy():
        elapsed += 1
        MusicProgressBar["value"] = elapsed
        time.sleep(0.1)
    if elapsed > totallength - 30:
        PlayButton.configure(image=Playimg)
        playbuttonstate = 0


def close():
    mixer.music.stop()
    PlayerForm.destroy()


firststart()
MusicProgressBar = ttk.Progressbar(PlayerForm, orient=HORIZONTAL, length=200, mode="determinate",
                                   style="G.Horizontal.TProgressbar")
PlayLabel = ttk.Label(PlayerForm, textvariable=PlayLabelText, font="Calibri", style="W.TLabel")
GenreLabel = ttk.Label(PlayerForm, textvariable=GenreLabelText, font="Calibri", style="W.TLabel")
PlayBitrate = ttk.Label(PlayerForm, textvariable=BitrateLabelText, font="Calibri", style="W.TLabel")
VerLabel = ttk.Label(PlayerForm, text="Ver. 03.02.2019", font="Calibri", style="W.TLabel")
DirectoryChangeButton = ttk.Button(PlayerForm, image=Fileimg, cursor="hand2", takefocus=0)
DirectoryLabel = ttk.Label(PlayerForm, font="Calibri", textvariable=DirectoryLabelText, style="W.TLabel")
PlayButton = ttk.Button(PlayerForm, image=Pauseimg, cursor="hand2", takefocus=0)
NextButton = ttk.Button(PlayerForm, image=Forwardimg, cursor="hand2", takefocus=0)
PreviousButton = ttk.Button(PlayerForm, image=Previousimg, cursor="hand2", takefocus=0)
MusicListBox = Listbox(PlayerForm, font="Calibri", cursor="hand2", bd=0, activestyle="none", selectbackground="#8bc34a",
                       takefocus=0)
PlayImg = ttk.Label(PlayerForm, image=PlayPhotoimg, style="W.TLabel")
VolumeSlider = ttk.Scale(PlayerForm, from_=0, to=100, orient=HORIZONTAL, command=volume, cursor="hand2")
VolumeLabel = ttk.Label(PlayerForm, textvariable=VolumeValue, font="Calibri", style="W.TLabel")
MusicLabel = ttk.Label(PlayerForm, image=MusicLabelimg, style="W.TLabel")
mixer.music.set_volume(0.50)
VolumeSlider.set(50)
VolumeValue.set("50{}".format("%"))
GenreLabelText.set("")
PlayLabelText.set("No song is playing!")
BitrateLabelText.set("")
DirectoryLabelText.set(directory)
update(state)
PlayButton.configure(image=Playimg)
MusicProgressBar.place(x=1, y=492, width=803, height=9)
DirectoryChangeButton.place(x=0, y=0)
MusicLabel.place(x=560, y=180)
DirectoryLabel.place(x=32, y=2, width=651, height=28)
MusicListBox.place(x=0, y=32, width=400, height=380)
PlayLabel.place(x=62, y=436)
PlayBitrate.place(x=62, y=460)
GenreLabel.place(x=121, y=460)
PreviousButton.place(x=490, y=442)
PlayButton.place(x=535, y=438)
NextButton.place(x=590, y=442)
PlayImg.place(x=4, y=435)
VolumeSlider.place(x=650, y=454)
VolumeLabel.place(x=756, y=449)
VerLabel.place(x=690, y=2)
PlayButton.bind("<Button-1>", playsong)
PreviousButton.bind("<Button-1>", previoussong)
NextButton.bind("<Button-1>", nextsong)
MusicListBox.bind("<Button-1>", musiclistboxpointer)
DirectoryChangeButton.bind("<Button-1>", changedirectory)
PlayerForm.protocol("WM_DELETE_WINDOW", close)
PlayerForm.mainloop()
