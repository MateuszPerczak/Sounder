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
s.configure("G.Horizontal.TProgressbar", foreground='#8bc34a', background='#8bc34a', lightcolor='#8bc34a', darkcolor='#8bc34a', bordercolor='#ffffff', troughcolor='#ffffff')
s.configure("W.TLabel", background='#ffffff', border='0')
tryv = 0
PlayLabelText = StringVar()
DirectoryLabelText = StringVar()
GenreLabelText = StringVar()
BitrateLabelText = StringVar()
VolumeValue = StringVar()
listofsongs = []
maxsong = 0
playbuttonstate = 0
# ikony
PlayPhotoimg = PhotoImage(file="musicicon.png")
Playimg = PhotoImage(file="play.png")
Pauseimg = PhotoImage(file="pause.png")
Forwardimg = PhotoImage(file="forward.png")
Previousimg = PhotoImage(file="previous.png")
Fileimg = PhotoImage(file="file-directory.png")
RefreshLabelimg = PhotoImage(file="refresh.png")
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
        os.remove('.settings')
        directory = askdirectory()
        if directory == "" or None:
            exit("Directory is empty!!")
        with open('.settings', 'a')as data:
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
    global directory
    if os.path.exists('.settings'):
        with open('.settings', 'r') as data:
            directory = data.readline()
    elif not os.path.exists('Data.sou'):
        directory = askdirectory()
        with open('.settings', 'a')as data:
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
        with open('.settings', 'w') as data:
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
    try:
        if cstate == 1:
            listofsongs.reverse()
            for file in listofsongs:
                MusicListBox.insert(0, file)
            listofsongs.reverse()
        elif cstate == 0:
            MusicListBox.delete(0, END)
            maxsong = 0
            listofsongs = []
    except:
        print("Unexpected char")


def refreshdirectory(event):
    print(event)
    global directory
    global maxsong
    global listofsongs
    global state
    state = 0
    maxsong = 0
    listofsongs = []
    MusicListBox.delete(0, END)
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            maxsong += 1
            state = 1
            listofsongs.append(file)
    listofsongs.reverse()
    for song in listofsongs:
        MusicListBox.insert(0, song)
    listofsongs.reverse()


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
    progressvalue = round(file.info.length, 2)
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
    elapsed = 18
    while elapsed <= totallength and mixer.music.get_busy():
        elapsed += 1
        MusicProgressBar["value"] = elapsed
        time.sleep(0.1)
    if elapsed >= totallength - 50:
        PlayButton.configure(image=Playimg)
        playbuttonstate = 0


def close():
    mixer.music.stop()
    PlayerForm.destroy()


firststart()
MusicProgressBar = ttk.Progressbar(PlayerForm, orient=HORIZONTAL, length=200, mode="determinate", style="G.Horizontal.TProgressbar")
PlayLabel = ttk.Label(PlayerForm, textvariable=PlayLabelText, font="Calibri", style="W.TLabel")
GenreLabel = ttk.Label(PlayerForm, textvariable=GenreLabelText, font="Calibri", style="W.TLabel")
PlayBitrate = ttk.Label(PlayerForm, textvariable=BitrateLabelText, font="Calibri", style="W.TLabel")
VerLabel = ttk.Label(PlayerForm, text="Ver. 05.02.2019", font="Calibri", style="W.TLabel")
DirectoryChangeButton = ttk.Button(PlayerForm, image=Fileimg, cursor="hand2", takefocus=0)
RefreshButton = ttk.Button(PlayerForm, image=RefreshLabelimg, cursor="hand2", takefocus=0)
DirectoryLabel = ttk.Label(PlayerForm, font="Calibri", textvariable=DirectoryLabelText, style="W.TLabel")
PlayButton = ttk.Button(PlayerForm, image=Pauseimg, cursor="hand2", takefocus=0)
NextButton = ttk.Button(PlayerForm, image=Forwardimg, cursor="hand2", takefocus=0)
PreviousButton = ttk.Button(PlayerForm, image=Previousimg, cursor="hand2", takefocus=0)
MusicListBox = Listbox(PlayerForm, font="Calibri", cursor="hand2", bd=0, activestyle="none", selectbackground="#8bc34a", takefocus=0)
PlayImg = ttk.Label(PlayerForm, image=PlayPhotoimg, style="W.TLabel")
VolumeSlider = ttk.Scale(PlayerForm, from_=0, to=100, orient=HORIZONTAL, command=volume, cursor="hand2")
VolumeLabel = ttk.Label(PlayerForm, textvariable=VolumeValue, font="Calibri", style="W.TLabel")
# SetUp
mixer.music.set_volume(0.50)
VolumeSlider.set(50)
VolumeValue.set("50{}".format("%"))
GenreLabelText.set("")
PlayLabelText.set("No song is playing!")
BitrateLabelText.set("")
DirectoryLabelText.set(directory)
update(state)
PlayButton.configure(image=Playimg)
# End
#Coordinates
MusicProgressBar.place(x=1, y=492, width=800, height=9)
DirectoryChangeButton.place(x=32, y=0)
RefreshButton.place(x=0, y=0)
DirectoryLabel.place(x=66, y=2, width=651, height=28)
MusicListBox.place(x=1, y=32, width=798, height=388)
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
#binds
PlayButton.bind("<Button-1>", playsong)
PreviousButton.bind("<Button-1>", previoussong)
NextButton.bind("<Button-1>", nextsong)
MusicListBox.bind("<Button-1>", musiclistboxpointer)
DirectoryChangeButton.bind("<Button-1>", changedirectory)
RefreshButton.bind("<Button-1>", refreshdirectory)
PlayerForm.protocol("WM_DELETE_WINDOW", close)
PlayerForm.mainloop()
