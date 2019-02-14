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
YearLabelText = StringVar()
TimeLabelText = StringVar()
SampleLabelText = StringVar()
maxsong = 0
playbuttonstate = 0
mode = 0
PlayPhotoimg = PhotoImage(file="musicicon.png")
Playimg = PhotoImage(file="play.png")
Pauseimg = PhotoImage(file="pause.png")
Forwardimg = PhotoImage(file="forward.png")
Previousimg = PhotoImage(file="previous.png")
Fileimg = PhotoImage(file="file-directory.png")
RefreshLabelimg = PhotoImage(file="refresh.png")
Scuffle = PhotoImage(file="shuffle.png")
Repeat = PhotoImage(file="repeat.png")
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
    listofsongs = []
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


def firststart():
    global directory
    if os.path.exists('.settings'):
        with open('.settings', 'r') as data:
            directory = data.readline()
    elif not os.path.exists('.settings'):
        directory = askdirectory()
        with open('.settings', 'a')as data:
            data.write(directory)
    if directory == "" or None:
        exit("Directory is empty!!")
    mixer.init()
    musicscan()


def changedirectory():
    global directory
    global sounderdirectory
    global state
    global maxsong
    newdirectory = askdirectory()
    if directory != newdirectory and newdirectory != "" or None:
        os.chdir(sounderdirectory)
        with open('.settings', 'w') as data:
            data.write(newdirectory)
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


def refreshdirectory():
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
    update(state)


def playsong():
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
            if len(listofsongs[songnumber]) > 50:
                PlayLabelText.set(listofsongs[songnumber][0:50] + "...mp3")
            else:
                PlayLabelText.set(listofsongs[songnumber])
            mixer.music.play()
            PlayButton.configure(image=Pauseimg)
            playbuttonstate = 1
            preapir()
    elif state == 0:
        if playbuttonstate == 1:
            mixer.music.stop()
            time.sleep(0.1)
            PlayLabelText.set("")
            PlayButton.configure(image=Playimg)
            playbuttonstate = 0


def nextsong():
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
                if len(listofsongs[songnumber]) > 50:
                    PlayLabelText.set(listofsongs[songnumber][0:50] + "...mp3")
                else:
                    PlayLabelText.set(listofsongs[songnumber])
                preapir()
        if playbuttonstate == 0:
            if songnumber < maxsong - 1:
                mixer.music.stop()
                time.sleep(0.1)
                playbuttonstate = 1
                PlayButton.configure(image=Pauseimg)
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 50:
                    PlayLabelText.set(listofsongs[songnumber][0:50] + "...mp3")
                else:
                    PlayLabelText.set(listofsongs[songnumber])
                preapir()


def previoussong():
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
                if len(listofsongs[songnumber]) > 50:
                    PlayLabelText.set(listofsongs[songnumber][0:50] + "...mp3")
                else:
                    PlayLabelText.set(listofsongs[songnumber])
                preapir()
        if playbuttonstate == 0:
            if songnumber > 0:
                mixer.music.stop()
                time.sleep(0.1)
                playbuttonstate = 1
                PlayButton.configure(image=Pauseimg)
                songnumber -= 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 50:
                    PlayLabelText.set(listofsongs[songnumber][0:50] + "...mp3")
                else:
                    PlayLabelText.set(listofsongs[songnumber])
                preapir()


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
                        if len(listofsongs[songnumber]) > 50:
                            PlayLabelText.set(listofsongs[songnumber][0:50] + "...mp3")
                        else:
                            PlayLabelText.set(listofsongs[songnumber])
                        preapir()
                        tryv = 0


def volume(value):
    global VolumeValue
    value = float(value)
    value = round(value, 0)
    value = int(value)
    VolumeValue.set("{}%".format(value))
    value = value / 100
    mixer.music.set_volume(value)


def preapir():
    global listofsongs
    global songnumber
    global playbuttonstate
    file = MP3(listofsongs[songnumber])
    bitratevar = int(file.info.bitrate / 1000)
    samplerate = file.info.sample_rate
    BitrateLabelText.set("Bitrate: {}kbps".format(bitratevar))
    SampleLabelText.set("Sample Rate: {}kHz".format(samplerate))
    try:
        fileinfo = file.tags['TCON']
        GenreLabelText.set("Genre:  {}".format(fileinfo))
    except:
        GenreLabelText.set("Genre: Unknown")
    try:
        fileyear = file.tags['TDRC']
        YearLabelText.set("Year: {}".format(fileyear))
    except:
        YearLabelText.set("Year: Unknown")
    mins, secs = divmod(file.info.length, 60)
    mins = int(mins)
    secs = int(secs)
    if secs < 10:
        TimeLabelText.set("Time: {}:0{}".format(mins, secs))
    else:
        TimeLabelText.set("Time: {}:{}".format(mins, secs))
    progressvalue = round(file.info.length, 1)
    if playbuttonstate == 0:
        PlayButton.configure(image=Pauseimg)
    pbf = threading.Thread(target=progressbarfill, args=(progressvalue,))
    pbf.daemon = True
    pbf.start()


def progressbarfill(totallength):
    global playbuttonstate
    MusicProgressBar["maximum"] = totallength
    elapsed = 1.0
    while elapsed <= totallength and mixer.music.get_busy():
        elapsed += 0.1
        MusicProgressBar["value"] = elapsed
        time.sleep(0.1)
    if elapsed >= totallength - 15:
        MusicProgressBar["value"] = totallength
        PlayButton.configure(image=Playimg)
        playbuttonstate = 0
        playmode()


def playmode():
    global mode
    global playbuttonstate
    global songnumber
    global maxsong
    global listofsongs
    global state
    if state == 1:
        time.sleep(1)
        if mode == 0:
            if songnumber < maxsong:
                nextsong()
        elif mode == 1:
            playsong()


def switchmode():
    global mode
    if mode == 0:
        mode = 1
        ModeButton.configure(image=Repeat)
    else:
        mode = 0
        ModeButton.configure(image=Scuffle)


def close():
    mixer.music.stop()
    PlayerForm.destroy()


firststart()
MusicProgressBar = ttk.Progressbar(PlayerForm, orient=HORIZONTAL, length=200, mode="determinate", style="G.Horizontal"
                                                                                                        ".TProgressbar")
PlayLabel = ttk.Label(PlayerForm, textvariable=PlayLabelText, font="Calibri", style="W.TLabel")
GenreLabel = ttk.Label(PlayerForm, textvariable=GenreLabelText, font="Calibri", style="W.TLabel")
PlayBitrate = ttk.Label(PlayerForm, textvariable=BitrateLabelText, font="Calibri", style="W.TLabel")
VerLabel = ttk.Label(PlayerForm, text="Ver. 2.6.1", font="Calibri", style="W.TLabel")
DirectoryChangeButton = ttk.Button(PlayerForm, image=Fileimg, cursor="hand2", takefocus=0, command=changedirectory)
RefreshButton = ttk.Button(PlayerForm, image=RefreshLabelimg, cursor="hand2", takefocus=0, command=refreshdirectory)
DirectoryLabel = ttk.Label(PlayerForm, font="Calibri", textvariable=DirectoryLabelText, style="W.TLabel")
PlayButton = ttk.Button(PlayerForm, image=Playimg, cursor="hand2", takefocus=0, command=playsong)
NextButton = ttk.Button(PlayerForm, image=Forwardimg, cursor="hand2", takefocus=0, command=nextsong)
PreviousButton = ttk.Button(PlayerForm, image=Previousimg, cursor="hand2", takefocus=0, command=previoussong)
MusicListBox = Listbox(PlayerForm, font="Calibri", cursor="hand2", bd=0, activestyle="none", selectbackground="#8bc34a",
                       takefocus=0)
PlayImg = ttk.Label(PlayerForm, image=PlayPhotoimg, style="W.TLabel")
VolumeSlider = ttk.Scale(PlayerForm, from_=0, to=100, orient=HORIZONTAL, command=volume, cursor="hand2")
VolumeLabel = ttk.Label(PlayerForm, textvariable=VolumeValue, font="Calibri", style="W.TLabel")
ModeButton = ttk.Button(PlayerForm, image=Scuffle, cursor="hand2", takefocus=0, command=switchmode)
InfoLabel = ttk.Label(PlayerForm, text="File Info", font="Calibri", style="W.TLabel")
YearLabel = ttk.Label(PlayerForm, textvariable=YearLabelText, font="Calibri", style="W.TLabel")
TimeLabel = ttk.Label(PlayerForm, textvariable=TimeLabelText, font="Calibri", style="W.TLabel")
SampleLabel = ttk.Label(PlayerForm, textvariable=SampleLabelText, font="Calibri", style="W.TLabel")
Separator = ttk.Separator(PlayerForm, orient=HORIZONTAL)
mixer.music.set_volume(0.50)
VolumeSlider.set(50)
VolumeValue.set("50{}".format("%"))
GenreLabelText.set("Genre: ")
PlayLabelText.set("No song is playing!")
BitrateLabelText.set("Bitrate: ")
YearLabelText.set("Year: ")
TimeLabelText.set("Time: ")
SampleLabelText.set("Sample Rate: ")
DirectoryLabelText.set(directory)
update(state)
MusicProgressBar.place(x=1, y=492, width=800, height=9)
DirectoryChangeButton.place(x=32, y=2, height=27)
RefreshButton.place(x=2, y=2)
DirectoryLabel.place(x=66, y=2, width=651, height=28)
MusicListBox.place(x=1, y=32, width=550, height=388)
PlayLabel.place(x=62, y=450)
SampleLabel.place(x=605, y=145)
PlayBitrate.place(x=605, y=115)
GenreLabel.place(x=605, y=85)
InfoLabel.place(x=660, y=50)
YearLabel.place(x=605, y=175)
TimeLabel.place(x=605, y=205)
PreviousButton.place(x=504, y=444)
PlayButton.place(x=548, y=441)
NextButton.place(x=598, y=444)
PlayImg.place(x=4, y=435)
VolumeSlider.place(x=650, y=454)
VolumeLabel.place(x=756, y=449)
VerLabel.place(x=730, y=4)
ModeButton.place(x=467, y=447)
Separator.place(x=600, y=80, width=170)
MusicListBox.bind("<Button-1>", musiclistboxpointer)
PlayerForm.protocol("WM_DELETE_WINDOW", close)
PlayerForm.mainloop()
