import os
import time
import threading
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import tkinter.messagebox
PlayerForm = Tk()
PlayerForm.geometry('800x500')
PlayerForm.title("Sounder!")
PlayerForm.resizable(width=FALSE, height=FALSE)
PlayerForm.iconbitmap("Soundericon.ico")
PlayerForm.configure(background='#ffffff')
s = ttk.Style()
s.theme_use('clam')
s.configure("G.Horizontal.TProgressbar", foreground='#00000', background='#000000', lightcolor='#000000',
            darkcolor='#ffffff', bordercolor='#ffffff', troughcolor='#ffffff')
s.configure("W.TLabel", background='#ffffff', border='0')
s.configure("TButton", background='#ffffff', relief="flat")
s.configure("TScale", troughcolor='#ffffff', background='#ffffff')
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
RepeatNone = PhotoImage(file="repeatnone.png")
RepeatAll = PhotoImage(file="repeatall.png")
RepeatOne = PhotoImage(file="repeatone.png")
sounderdirectory = os.getcwd()


def musicscan():
    global directory
    global maxsong
    global listofsongs
    global state
    global songnumber
    state = 0
    songnumber = 0
    maxsong = -1
    listofsongs = []
    try:
        os.chdir(directory)
    except:
        tkinter.messagebox.showwarning('Settings', 'Your settings file was corrupted!')
        os.chdir(sounderdirectory)
        os.remove('.settings')
        firststart()
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
        if directory == "" or None:
            directory = askdirectory()
            if directory == "" or None:
                firststart()
            elif directory != "" or None:
                mixer.init()
                musicscan()
        elif directory != "" or None:
            mixer.init()
            musicscan()
    elif not os.path.exists('.settings'):
        directory = askdirectory()
        if directory == "" or None:
            firststart()
        elif directory != "" or None:
            with open('.settings', 'a') as file:
                file.write(directory)
            mixer.init()
            musicscan()


def changedirectory():
    global directory
    global sounderdirectory
    global state
    newdirectory = askdirectory()
    if directory != newdirectory and newdirectory != "" or None:
        os.chdir(sounderdirectory)
        with open('.settings', 'w') as data:
            data.write(newdirectory)
        MusicListBox.delete(0, END)
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
            maxsong = -1
            listofsongs = []
    except:
        print("Unexpected char")


def refreshdirectory():
    global directory
    global maxsong
    global listofsongs
    global state
    state = 0
    maxsong = -1
    listofsongs = []
    MusicListBox.delete(0, END)
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            maxsong += 1
            state = 1
            listofsongs.append(file)
    update(state)
    time.sleep(0.07)


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
            if len(listofsongs[songnumber]) > 60:
                PlayLabelText.set(listofsongs[songnumber][0:60] + "...mp3")
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
            if songnumber < maxsong:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButton.configure(image=Pauseimg)
                playbuttonstate = 1
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60] + "...mp3")
                else:
                    PlayLabelText.set(listofsongs[songnumber])
                preapir()
        if playbuttonstate == 0:
            if songnumber < maxsong:
                mixer.music.stop()
                time.sleep(0.1)
                playbuttonstate = 1
                PlayButton.configure(image=Pauseimg)
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60] + "...mp3")
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
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60] + "...mp3")
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
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60] + "...mp3")
                else:
                    PlayLabelText.set(listofsongs[songnumber])
                preapir()


def musiclistboxpointer(event):
    print(event)
    global selected
    global curent
    global state
    global songnumber
    global playbuttonstate
    global listofsongs
    if state == 1:
        mixer.music.stop()
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
                    if len(listofsongs[songnumber]) > 60:
                        PlayLabelText.set(listofsongs[songnumber][0:60] + "...mp3")
                    else:
                        PlayLabelText.set(listofsongs[songnumber])
                    preapir()


def volume(value):
    value = float(value)
    value = round(value, 0)
    value = int(value) / 100
    mixer.music.set_volume(value)


def preapir():
    global listofsongs
    global songnumber
    global playbuttonstate
    MusicListBox.selection_clear(0, END)
    MusicListBox.select_set(songnumber)
    file = MP3(listofsongs[songnumber])
    bitratevar = int(file.info.bitrate / 1000)
    samplerate = file.info.sample_rate
    BitrateLabelText.set("Bitrate: " + str(bitratevar) + "kbps")
    SampleLabelText.set("Sample Rate: " + str(samplerate) + "kHz")
    try:
        fileinfo = file.tags['TCON']
        if len(str(fileinfo)) > 13:
            GenreLabelText.set("Genre: " + str(fileinfo)[0:15])
        else:
            GenreLabelText.set("Genre: " + str(fileinfo))
    except:
        GenreLabelText.set("Genre: Unknown")
    try:
        fileyear = file.tags['TDRC']
        YearLabelText.set("Year: " + str(fileyear))
    except:
        YearLabelText.set("Year: Unknown")
    mins, secs = divmod(file.info.length, 60)
    mins = int(mins)
    secs = int(secs)
    TimeLabelText.set("Time: " + str(mins) + ":" + str(secs).zfill(2))
    totallength = round(file.info.length, 1)
    if playbuttonstate == 0:
        PlayButton.configure(image=Pauseimg)
    pbf = threading.Thread(target=progressbarfill, args=(totallength,))
    pbf.daemon = True
    pbf.start()


def progressbarfill(totallength):
    global playbuttonstate
    MusicProgressBar["maximum"] = totallength
    elapsed = 1.4
    while round(elapsed, 1) <= totallength and mixer.music.get_busy():
        elapsed += 0.1
        MusicProgressBar["value"] = elapsed
        time.sleep(0.1)
    if round(elapsed, 1) >= totallength - 4:
        MusicProgressBar["value"] = totallength
        PlayButton.configure(image=Playimg)
        playbuttonstate = 0
        playmode()


def playmode():
    global mode
    global songnumber
    global maxsong
    global state
    if state == 1:
        time.sleep(0.5)
        if mode == 0:
            if songnumber < maxsong:
                nextsong()
        elif mode == 1:
            if songnumber < maxsong:
                nextsong()
            elif songnumber == maxsong:
                songnumber = 0
                playsong()
        elif mode == 2:
            playsong()


def switchmode():
    global mode
    if mode == 0:
        mode = 1
        ModeButton.configure(image=RepeatAll)
    elif mode == 1:
        mode = 2
        ModeButton.configure(image=RepeatOne)
    else:
        mode = 0
        ModeButton.configure(image=RepeatNone)


def close():
    if mixer.music.get_busy():
        check = tkinter.messagebox.askquestion('Sounder!', 'Are you sure you want to quit?')
        if check == 'yes':
            mixer.music.stop()
            PlayerForm.destroy()
        else:
            pass
    else:
        mixer.music.stop()
        PlayerForm.destroy()


firststart()
MusicProgressBar = ttk.Progressbar(PlayerForm, orient=HORIZONTAL, length=200, mode="determinate", style="G.Horizontal"
                                                                                                        ".TProgressbar")
PlayLabel = ttk.Label(PlayerForm, textvariable=PlayLabelText, font='Bahnschrift 11', style="W.TLabel")
GenreLabel = ttk.Label(PlayerForm, textvariable=GenreLabelText, font='Bahnschrift 11', style="W.TLabel")
PlayBitrate = ttk.Label(PlayerForm, textvariable=BitrateLabelText, font='Bahnschrift 11', style="W.TLabel")
VerLabel = ttk.Label(PlayerForm, text="Ver. 2.6.8", font='Bahnschrift 11', style="W.TLabel")
DirectoryChangeButton = ttk.Button(PlayerForm, image=Fileimg, cursor="hand2", takefocus=0, command=changedirectory)
RefreshButton = ttk.Button(PlayerForm, image=RefreshLabelimg, cursor="hand2", takefocus=0, command=refreshdirectory)
DirectoryLabel = ttk.Label(PlayerForm, font='Bahnschrift 11', textvariable=DirectoryLabelText, style="W.TLabel")
PlayButton = ttk.Button(PlayerForm, image=Playimg, cursor="hand2", takefocus=0, command=playsong)
NextButton = ttk.Button(PlayerForm, image=Forwardimg, cursor="hand2", takefocus=0, command=nextsong)
PreviousButton = ttk.Button(PlayerForm, image=Previousimg, cursor="hand2", takefocus=0, command=previoussong)
MusicListBox = Listbox(PlayerForm, font='Bahnschrift 11', cursor="hand2", bd=0, activestyle="none",
                       selectbackground="#000", takefocus=0)
PlayImg = ttk.Label(PlayerForm, image=PlayPhotoimg, style="W.TLabel")
VolumeSlider = ttk.Scale(PlayerForm, from_=0, to=100, orient=HORIZONTAL, command=volume, cursor="hand2")
ModeButton = ttk.Button(PlayerForm, image=RepeatNone, cursor="hand2", takefocus=0, command=switchmode)
InfoLabel = ttk.Label(PlayerForm, text="File Info", font='Bahnschrift 11', style="W.TLabel")
YearLabel = ttk.Label(PlayerForm, textvariable=YearLabelText, font='Bahnschrift 11', style="W.TLabel")
TimeLabel = ttk.Label(PlayerForm, textvariable=TimeLabelText, font='Bahnschrift 11', style="W.TLabel")
SampleLabel = ttk.Label(PlayerForm, textvariable=SampleLabelText, font='Bahnschrift 11', style="W.TLabel")
Separator = ttk.Separator(PlayerForm, orient=HORIZONTAL)
mixer.music.set_volume(0.35)
VolumeSlider.set(35)
GenreLabelText.set("Genre: ")
PlayLabelText.set("No song is playing!")
BitrateLabelText.set("Bitrate: ")
YearLabelText.set("Year: ")
TimeLabelText.set("Time: ")
SampleLabelText.set("Sample Rate: ")
DirectoryLabelText.set(directory)
update(state)
MusicProgressBar.place(x=1, y=492, width=800, height=9)
DirectoryChangeButton.place(x=32, y=0)
RefreshButton.place(x=1, y=0)
DirectoryLabel.place(x=66, y=2, width=651, height=28)
MusicListBox.place(x=1, y=32, width=550, height=388)
PlayLabel.place(x=62, y=450)
SampleLabel.place(x=597, y=145)
PlayBitrate.place(x=597, y=115)
GenreLabel.place(x=597, y=85)
InfoLabel.place(x=652, y=50)
YearLabel.place(x=597, y=175)
TimeLabel.place(x=597, y=205)
PlayImg.place(x=6, y=438)
PreviousButton.place(x=530, y=442)
PlayButton.place(x=574, y=442)
NextButton.place(x=618, y=442)
ModeButton.place(x=494, y=445)
VolumeSlider.place(x=670, y=454)
VerLabel.place(x=730, y=4)
Separator.place(x=592, y=80, width=170, height=2)
MusicListBox.bind("<<ListboxSelect>>", musiclistboxpointer)
PlayerForm.protocol("WM_DELETE_WINDOW", close)
PlayerForm.mainloop()
