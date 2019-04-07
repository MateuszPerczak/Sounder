import os
import time
import threading
from mutagen.mp3 import MP3
from pygame import mixer
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
import tkinter.messagebox
# dir
sounderdir = os.path.dirname(sys.executable)
userdir = os.path.expanduser('~')
# end
PlayerForm = Tk()
PlayerForm.geometry('800x500')
PlayerForm.title("Sounder!")
PlayerForm.resizable(width=FALSE, height=FALSE)
PlayerForm.iconbitmap(sounderdir + "\\Soundericon.ico")
s = ttk.Style()
s.theme_use('clam')
# variables
PlayLabelText = StringVar()
DirectoryLabelText = StringVar()
GenreLabelText = StringVar()
BitrateLabelText = StringVar()
VolumeValue = StringVar()
YearLabelText = StringVar()
TimeLabelText = StringVar()
SampleLabelText = StringVar()
NowYear = StringVar()
Avtime = StringVar()
TSongs = StringVar()
TVol = StringVar()
ETimeVar = StringVar()
maxsong = 0
playbuttonstate = 0
mode = 0
themeset = "Light"
infoframe = None
threads = 0
totallength = 0.0
# end
# images
PlayPhotoimg = PhotoImage(file=sounderdir + "\\musicicon.png")
Playimg = PhotoImage(file=sounderdir + "\\play.png")
Pauseimg = PhotoImage(file=sounderdir + "\\pause.png")
Forwardimg = PhotoImage(file=sounderdir + "\\forward.png")
Previousimg = PhotoImage(file=sounderdir + "\\previous.png")
Fileimg = PhotoImage(file=sounderdir + "\\file-directory.png")
RefreshLabelimg = PhotoImage(file=sounderdir + "\\refresh.png")
RepeatNone = PhotoImage(file=sounderdir + "\\repeatnone.png")
RepeatAll = PhotoImage(file=sounderdir + "\\repeatall.png")
RepeatOne = PhotoImage(file=sounderdir + "\\repeatone.png")
Info = PhotoImage(file=sounderdir + "\\info.png")
InfoMusic = PhotoImage(file=sounderdir + "\\musicinfo.png")
Copyright = PhotoImage(file=sounderdir + "\\copyright.png")
Fork = PhotoImage(file=sounderdir + "\\fork.png")
Theme = PhotoImage(file=sounderdir + "\\theme.png")
PlayPhotoimgD = PhotoImage(file=sounderdir + "\\musicicond.png")
PlayimgD = PhotoImage(file=sounderdir + "\\playd.png")
PauseimgD = PhotoImage(file=sounderdir + "\\paused.png")
ForwardimgD = PhotoImage(file=sounderdir + "\\forwardd.png")
PreviousimgD = PhotoImage(file=sounderdir + "\\previousd.png")
FileimgD = PhotoImage(file=sounderdir + "\\file-directoryd.png")
RefreshLabelimgD = PhotoImage(file=sounderdir + "\\refreshd.png")
RepeatNoneD = PhotoImage(file=sounderdir + "\\repeatnoned.png")
RepeatAllD = PhotoImage(file=sounderdir + "\\repeatalld.png")
RepeatOneD = PhotoImage(file=sounderdir + "\\repeatoned.png")
InfoD = PhotoImage(file=sounderdir + "\\infod.png")
InfoMusicD = PhotoImage(file=sounderdir + "\\musicinfod.png")
CopyrightD = PhotoImage(file=sounderdir + "\\copyrightd.png")
ForkD = PhotoImage(file=sounderdir + "\\forkd.png")
ThemeD = PhotoImage(file=sounderdir + "\\themed.png")
# end
# year
NowYear.set("Copyright 2018-{}".format(time.strftime("%Y")))
# end


def musicscan():
    global directory, maxsong, listofsongs, state, songnumber
    directory = directory.rstrip('\n')
    state = 0
    songnumber = 0
    maxsong = -1
    listofsongs = []
    try:
        os.chdir(directory)
        for file in os.listdir(directory):
            if file.endswith(".mp3"):
                maxsong += 1
                state = 1
                listofsongs.append(file)
    except:
        tkinter.messagebox.showwarning('Settings', 'Your settings file was corrupted!')
        os.chdir(sounderdir)
        os.remove('settings.ini')
        firststart()


def firststart():
    global directory, themeset
    if os.path.exists('settings.ini'):
        with open('settings.ini', 'r') as data:
            directory = data.readline()
            theme = data.readline()
            if theme != "" or None:
                if theme == "Dark" or theme == "Light":
                    themeset = theme.rstrip('\n')
                    themechange()
                    themechange()
                else:
                    themeset = "Dark"
                    themechange()
            else:
                themeset = "Dark"
                themechange()
        if directory == "" or None:
            directory = askdirectory()
            if directory == "" or None:
                directory = userdir + '\\Music'
                with open('settings.ini', 'a') as file:
                    file.write(directory)
                mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                mixer.init()
                musicscan()
            elif directory != "" or None:
                with open('settings.ini', 'a') as file:
                    file.write(directory)
                mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
                mixer.init()
                musicscan()
        elif directory != "" or None:
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
            mixer.init()
            musicscan()
    elif not os.path.exists('settings.ini'):
        directory = askdirectory()
        themeset = "Dark"
        themechange()
        if directory == "" or None:
            directory = userdir + '\\Music'
            with open('settings.ini', 'a') as file:
                file.write(directory)
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
            mixer.init()
            musicscan()
        elif directory != "" or None:
            with open('settings.ini', 'a') as file:
                file.write(directory)
            mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=4096)
            mixer.init()
            musicscan()


def changedirectory():
    global directory, sounderdir, state
    newdirectory = askdirectory()
    if directory != newdirectory and newdirectory != "" or None:
        os.chdir(sounderdir)
        with open('settings.ini', 'w') as data:
            data.write(newdirectory)
        MusicListBox.delete(0, END)
        directory = newdirectory
        DirectoryLabelText.set(directory)
        musicscan()
        update(state)


def update(cstate):
    global listofsongs, maxsong, songnumber
    try:
        if cstate == 1:
            if maxsong == 0:
                TSongs.set("Song: {}".format(maxsong + 1))
            elif maxsong > 0:
                TSongs.set("Songs: {}".format(maxsong + 1))
            listofsongs.reverse()
            for file in listofsongs:
                file = file.rstrip('.mp3')
                MusicListBox.insert(0, file)
            listofsongs.reverse()
            if mixer.music.get_busy():
                MusicListBox.selection_clear(0, END)
                MusicListBox.select_set(songnumber)
        elif cstate == 0:
            MusicListBox.delete(0, END)
            maxsong = -1
            listofsongs = []
            TSongs.set("Songs: 0")
            ETimeVar.set("0:00")
    except:
        pass


def refreshdirectory():
    global directory, maxsong, listofsongs, state
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
    time.sleep(0.2)


def playsong():
    global playbuttonstate, songnumber, listofsongs, state, themeset
    if state == 1:
        if playbuttonstate == 1:
            mixer.music.pause()
            if themeset == "Light":
                PlayButton.configure(image=Playimg)
            elif themeset == "Dark":
                PlayButton.configure(image=PlayimgD)
            playbuttonstate = 0
        elif playbuttonstate == 0:
            if mixer.music.get_busy():
                mixer.music.unpause()
                if themeset == "Light":
                    PlayButton.configure(image=Pauseimg)
                elif themeset == "Dark":
                    PlayButton.configure(image=PauseimgD)
                playbuttonstate = 1
            else:
                mixer.music.load(listofsongs[songnumber])
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60])
                else:
                    PlayLabelText.set(str(listofsongs[songnumber]).rstrip('.mp3'))
                mixer.music.play()
                if themeset == "Light":
                    PlayButton.configure(image=Pauseimg)
                elif themeset == "Dark":
                    PlayButton.configure(image=PauseimgD)
                playbuttonstate = 1
                preapir()
    elif state == 0:
        if playbuttonstate == 1:
            mixer.music.stop()
            PlayLabelText.set("")
            ETimeVar.set("0:00")
            if themeset == "Light":
                PlayButton.configure(image=Playimg)
            elif themeset == "Dark":
                PlayButton.configure(image=PlayimgD)
            playbuttonstate = 0


def nextsong():
    global playbuttonstate, songnumber, state, maxsong, themeset
    if state == 1:
        if playbuttonstate == 1:
            if songnumber < maxsong:
                mixer.music.stop()
                if themeset == "Light":
                    PlayButton.configure(image=Pauseimg)
                elif themeset == "Dark":
                    PlayButton.configure(image=PauseimgD)
                playbuttonstate = 1
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60])
                else:
                    PlayLabelText.set(str(listofsongs[songnumber]).rstrip('.mp3'))
                preapir()
        if playbuttonstate == 0:
            if songnumber < maxsong:
                mixer.music.stop()
                playbuttonstate = 1
                if themeset == "Light":
                    PlayButton.configure(image=Pauseimg)
                elif themeset == "Dark":
                    PlayButton.configure(image=PauseimgD)
                songnumber += 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 60:
                    PlayLabelText.set(listofsongs[songnumber][0:60])
                else:
                    PlayLabelText.set(str(listofsongs[songnumber]).rstrip('.mp3'))
                preapir()


def previoussong():
    global playbuttonstate, songnumber, state, themeset
    if state == 1:
        if playbuttonstate == 1:
            if songnumber > 0:
                mixer.music.stop()
                if themeset == "Light":
                    PlayButton.configure(image=Pauseimg)
                elif themeset == "Dark":
                    PlayButton.configure(image=PauseimgD)
                songnumber -= 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 50:
                    PlayLabelText.set(listofsongs[songnumber][0:50])
                else:
                    PlayLabelText.set(str(listofsongs[songnumber]).rstrip('.mp3'))
                preapir()
        if playbuttonstate == 0:
            if songnumber > 0:
                mixer.music.stop()
                playbuttonstate = 1
                if themeset == "Light":
                    PlayButton.configure(image=Pauseimg)
                elif themeset == "Dark":
                    PlayButton.configure(image=PauseimgD)
                songnumber -= 1
                mixer.music.load(listofsongs[songnumber])
                mixer.music.play()
                if len(listofsongs[songnumber]) > 50:
                    PlayLabelText.set(listofsongs[songnumber][0:50])
                else:
                    PlayLabelText.set(str(listofsongs[songnumber]).rstrip('.mp3'))
                preapir()


def musiclistboxpointer(e):
    global selected, curent, state, songnumber, playbuttonstate, listofsongs, themeset
    if state == 1:
        selected = MusicListBox.curselection()
        if selected != ():
            mixer.music.stop()
            for Song in selected:
                curent = MusicListBox.get(Song)
            for nr, Song in enumerate(listofsongs):
                if Song.rstrip('.mp3') == curent:
                    mixer.music.load(listofsongs[nr])
                    songnumber = nr
                    mixer.music.play()
                    if playbuttonstate == 0:
                        playbuttonstate = 1
                        if themeset == "Light":
                            PlayButton.configure(image=Pauseimg)
                        elif themeset == "Dark":
                            PlayButton.configure(image=PauseimgD)
                    if len(listofsongs[songnumber]) > 50:
                        PlayLabelText.set(listofsongs[songnumber][0:50].rstrip('.mp3'))
                    else:
                        PlayLabelText.set(str(listofsongs[songnumber]).rstrip('.mp3'))
                    preapir()


def volume(value):
    value = float(value)
    value = value / 100
    if value == 0.99:
        TVol.set("Volume: 100%")
    else:
        TVol.set("Volume: {}%".format(int(value * 100)))
    mixer.music.set_volume(value)


def preapir():
    global listofsongs, songnumber, playbuttonstate, totallength
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
    MusicProgressBar["value"] = 0
    MusicProgressBar["maximum"] = totallength
    if playbuttonstate == 0:
        PlayButton.configure(image=Pauseimg)
    if not threads > 0:
        music_progress = threading.Thread(target=progressbarfill,)
        music_progress.daemon = True
        music_progress.start()


def progressbarfill():
    global playbuttonstate, themeset, threads, totallength
    wait = False
    threads += 1
    activtime = 0
    while mixer.music.get_busy() == 1 and activtime <= totallength - 0.11:
        # time smoothing
        if playbuttonstate == 1 and wait:
            time.sleep(0.15)
            wait = False
        elif playbuttonstate == 1 and not wait:
            activtime = mixer.music.get_pos() / 1000
            MusicProgressBar["value"] = activtime
            emin, esec = divmod(activtime, 60)
            ETimeVar.set(str(int(emin)) + ":" + str(int(esec)).zfill(2))
        elif playbuttonstate == 0 and not wait:
            wait = True
        # end
        time.sleep(0.2)
    threads -= 1
    if activtime >= totallength - 0.5:
        mixer.music.stop()
        if themeset == "Light":
            PlayButton.configure(image=Playimg)
        elif themeset == "Dark":
            PlayButton.configure(image=PlayimgD)
        playbuttonstate = 0
        playmode()


def playmode():
    global mode, songnumber, maxsong, state
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
    global mode, themeset
    if mode == 0:
        mode = 1
        if themeset == "Light":
            ModeButton.configure(image=RepeatAll)
        elif themeset == "Dark":
            ModeButton.configure(image=RepeatAllD)
    elif mode == 1:
        mode = 2
        if themeset == "Light":
            ModeButton.configure(image=RepeatOne)
        elif themeset == "Dark":
            ModeButton.configure(image=RepeatOneD)
    else:
        mode = 0
        if themeset == "Light":
            ModeButton.configure(image=RepeatNone)
        elif themeset == "Dark":
            ModeButton.configure(image=RepeatNoneD)


def close():
    global themeset, playbuttonstate
    if playbuttonstate == 1:
        check = tkinter.messagebox.askquestion('Sounder!', 'Are you sure you want to quit?')
        if check == 'yes':
            os.chdir(sounderdir)
            with open('settings.ini', 'w') as file:
                file.write(directory)
                file.write('\n')
                file.write(themeset)
            mixer.music.stop()
            PlayerForm.destroy()
        else:
            pass
    else:
        os.chdir(sounderdir)
        with open('settings.ini', 'w') as file:
            file.write(directory)
            file.write('\n')
            file.write(themeset)
        mixer.music.stop()
        PlayerForm.destroy()


def info():
    global themeset, infoframe
    infoframe = Toplevel(PlayerForm)
    infoframe.geometry("300x220")
    infoframe.resizable(width=False, height=False)
    infoframe.title("Sounder Info")
    infoframe.iconbitmap(sounderdir + "\\Soundericon.ico")
    infoframe.grab_set()
    verlabel = ttk.Label(infoframe, text="Version 2.8.1", font='Bahnschrift 11', style="W.TLabel")
    authorlabel = ttk.Label(infoframe, text="By: Mateusz Perczak", font='Bahnschrift 11', style="W.TLabel")
    musiclabel = ttk.Label(infoframe, image=InfoMusic, style="W.TLabel")
    copylabel = ttk.Label(infoframe, image=Copyright, style="W.TLabel")
    infolabel = ttk.Label(infoframe, textvariable=NowYear, font='Bahnschrift 11', style="W.TLabel")
    atlabel = ttk.Label(infoframe, textvariable=Avtime, font='Bahnschrift 11', style="W.TLabel")
    themebutton = ttk.Button(infoframe, image=Theme, cursor="hand2", takefocus=0, command=themechange)
    forknutton = ttk.Button(infoframe, image=Fork, cursor="hand2", takefocus=0, command=lambda: os.system("start \"\" "
                                                                                                          "https"
                                                                                                          "://github"
                                                                                                          ".com/losek1"
                                                                                                          "/Sounder"))
    if themeset == "Dark":
        infoframe.configure(background='#000')
        musiclabel.configure(image=InfoMusicD)
        copylabel.configure(image=CopyrightD)
        themebutton.configure(image=ThemeD)
        forknutton.configure(image=ForkD)
    elif themeset == "Light":
        infoframe.configure(background='#fff')
    musiclabel.place(x=90, y=15)
    verlabel.place(x=110, y=94)
    authorlabel.place(x=86, y=120)
    copylabel.place(x=2, y=190)
    infolabel.place(x=32, y=192)
    atlabel.place(x=42, y=140)
    forknutton.place(x=268, y=186)
    themebutton.place(x=230, y=186)


def themechange():
    global themeset, playbuttonstate, infoframe, mode
    if infoframe is not None:
        infoframe.destroy()
    if themeset == "Dark":
        themeset = "Light"
        PlayerForm.configure(background='#fff')
        MusicListBox.configure(selectbackground="#000", foreground='#000', background='#fff')
        s.configure("G.Horizontal.TProgressbar", foreground='#000', background='#000', lightcolor='#000',
                    darkcolor='#fff', bordercolor='#fff', troughcolor='#fff')
        s.configure("W.TLabel", background='#fff', foreground='#000', border='0')
        s.configure("TButton", background='#fff', relief="flat")
        s.configure("TScale", troughcolor='#fff', background='#fff', relief="flat")
        VerButton.configure(image=Info)
        DirectoryChangeButton.configure(image=Fileimg)
        RefreshButton.configure(image=RefreshLabelimg)
        NextButton.configure(image=Forwardimg)
        PreviousButton.configure(image=Previousimg)
        PlayImg.configure(image=PlayPhotoimg)
        if playbuttonstate == 1:
            PlayButton.configure(image=Pauseimg)
        elif playbuttonstate == 0:
            PlayButton.configure(image=Playimg)
        if mode == 0:
            ModeButton.configure(image=RepeatNone)
        elif mode == 1:
            ModeButton.configure(image=RepeatAll)
        else:
            ModeButton.configure(image=RepeatOne)
        if infoframe is not None:
            info()
    elif themeset == "Light":
        themeset = "Dark"
        PlayerForm.configure(background='#000')
        MusicListBox.configure(selectbackground="#1e88e5", foreground='#fff', background='#000')
        s.configure("G.Horizontal.TProgressbar", foreground='#1e88e5', background='#1e88e5', lightcolor='#1e88e5',
                    darkcolor='#1e88e5', bordercolor='#000', troughcolor='#000')
        s.configure("W.TLabel", foreground='#fff', background='#000', border='0')
        s.configure("TButton", background='#000', relief="flat")
        s.configure("TScale", troughcolor='#000', background='#1e88e5', relief="FLAT")
        VerButton.configure(image=InfoD)
        DirectoryChangeButton.configure(image=FileimgD)
        RefreshButton.configure(image=RefreshLabelimgD)
        NextButton.configure(image=ForwardimgD)
        PreviousButton.configure(image=PreviousimgD)
        PlayImg.configure(image=PlayPhotoimgD)
        if playbuttonstate == 1:
            PlayButton.configure(image=PauseimgD)
        elif playbuttonstate == 0:
            PlayButton.configure(image=PlayimgD)
        if mode == 0:
            ModeButton.configure(image=RepeatNoneD)
        elif mode == 1:
            ModeButton.configure(image=RepeatAllD)
        else:
            ModeButton.configure(image=RepeatOneD)
        if infoframe is not None:
            info()


def soundertime():
    asec = 0
    amin = 0
    while True:
        time.sleep(1)
        asec += 1
        if asec == 60:
            amin += 1
            asec = 0
        Avtime.set("Sounder has been running for {}:{}".format(str(amin), str(asec).zfill(2)))


MusicProgressBar = ttk.Progressbar(PlayerForm, orient=HORIZONTAL, length=200, mode="determinate", style="G.Horizontal"
                                                                                                        ".TProgressbar")
PlayLabel = ttk.Label(PlayerForm, textvariable=PlayLabelText, font='Bahnschrift 11', style="W.TLabel")
GenreLabel = ttk.Label(PlayerForm, textvariable=GenreLabelText, font='Bahnschrift 11', style="W.TLabel")
PlayBitrate = ttk.Label(PlayerForm, textvariable=BitrateLabelText, font='Bahnschrift 11', style="W.TLabel")
VerButton = ttk.Button(PlayerForm, image=Info, cursor="hand2", takefocus=0, command=info)
DirectoryChangeButton = ttk.Button(PlayerForm, image=Fileimg, cursor="hand2", takefocus=0, command=changedirectory)
RefreshButton = ttk.Button(PlayerForm, image=RefreshLabelimg, cursor="hand2", takefocus=0, command=refreshdirectory)
DirectoryLabel = ttk.Label(PlayerForm, font='Bahnschrift 11', textvariable=DirectoryLabelText, style="W.TLabel")
PlayButton = ttk.Button(PlayerForm, image=Playimg, cursor="hand2", takefocus=0, command=playsong)
NextButton = ttk.Button(PlayerForm, image=Forwardimg, cursor="hand2", takefocus=0, command=nextsong)
PreviousButton = ttk.Button(PlayerForm, image=Previousimg, cursor="hand2", takefocus=0, command=previoussong)
MusicListBox = Listbox(PlayerForm, font='Bahnschrift 11', cursor="hand2", bd=0, activestyle="none",
                       selectbackground="#000", takefocus=0)
PlayImg = ttk.Label(PlayerForm, image=PlayPhotoimg, style="W.TLabel")
VolumeSlider = ttk.Scale(PlayerForm, from_=0, to=99, orient=HORIZONTAL, command=volume, cursor="hand2")
ModeButton = ttk.Button(PlayerForm, image=RepeatNone, cursor="hand2", takefocus=0, command=switchmode)
InfoLabel = ttk.Label(PlayerForm, text="File Info", font='Bahnschrift 11', style="W.TLabel")
YearLabel = ttk.Label(PlayerForm, textvariable=YearLabelText, font='Bahnschrift 11', style="W.TLabel")
TimeLabel = ttk.Label(PlayerForm, textvariable=TimeLabelText, font='Bahnschrift 11', style="W.TLabel")
SampleLabel = ttk.Label(PlayerForm, textvariable=SampleLabelText, font='Bahnschrift 11', style="W.TLabel")
InfoSeparator = ttk.Separator(PlayerForm, orient=HORIZONTAL)
SouInfo = ttk.Label(PlayerForm, text="Info", font='Bahnschrift 11', style="W.TLabel")
SouSeperator = ttk.Separator(PlayerForm, orient=HORIZONTAL)
TotalSongs = ttk.Label(PlayerForm, textvariable=TSongs, font='Bahnschrift 11', style="W.TLabel")
VolumeInfo = ttk.Label(PlayerForm, textvariable=TVol, font='Bahnschrift 11', style="W.TLabel")
ElapsedTime = ttk.Label(PlayerForm, textvariable=ETimeVar, font='Bahnschrift 10', style="W.TLabel")
# init ui
firststart()
mixer.music.set_volume(0.50)
VolumeSlider.set(50)
Avtime.set("It has been running for 0:00")
GenreLabelText.set("Genre: ")
if themeset == "Dark":
    PlayLabelText.set("I'm blue da ba dee da ba daa")
else:
    PlayLabelText.set("Never gonna give you up")
BitrateLabelText.set("Bitrate: ")
YearLabelText.set("Year: ")
TimeLabelText.set("Time: ")
SampleLabelText.set("Sample Rate: ")
ETimeVar.set("0:00")
DirectoryLabelText.set(directory)
update(state)
activetime = threading.Thread(target=soundertime, args=())
activetime.daemon = True
activetime.start()
# end
MusicProgressBar.place(x=1, y=492, width=800, height=9)
DirectoryChangeButton.place(x=32, y=0)
RefreshButton.place(x=1, y=0)
DirectoryLabel.place(x=66, y=2, width=651, height=28)
MusicListBox.place(x=1, y=32, width=550, height=388)
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
VerButton.place(x=763, y=0)
InfoSeparator.place(x=592, y=80, width=170, height=2)
SouInfo.place(x=666, y=250)
SouSeperator.place(x=592, y=280, width=170, height=2)
TotalSongs.place(x=592, y=285)
VolumeInfo.place(x=592, y=315)
PlayLabel.place(x=62, y=442)
ElapsedTime.place(x=62, y=462)
MusicListBox.bind("<<ListboxSelect>>", musiclistboxpointer)
PlayerForm.protocol("WM_DELETE_WINDOW", close)
PlayerForm.mainloop()
