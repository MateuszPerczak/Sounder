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
# Zmienne globalne
Try = 0
PlayLabelText = StringVar()
DirectoryLabelText = StringVar()
GenreLabelText = StringVar()
BitrateLabelText = StringVar()
VolumeValue = StringVar()
ListOfSongs = []
MaxSong = 0
State = 0
SongNumber = 0
PlayButtonState = 0
# ikony
PlayPhotoimg = PhotoImage(file="musicicon.png")
Playimg = PhotoImage(file="play.png")
Pauseimg = PhotoImage(file="pause.png")
Forwardimg = PhotoImage(file="forward.png")
Previousimg = PhotoImage(file="previous.png")
Fileimg = PhotoImage(file="file-directory.png")
MusicLabelimg = PhotoImage(file="sounder.png")


def MusicScan():
    global directory
    global MaxSong
    global ListOfSongs
    global PlayButtonState
    global State
    global SongNumber
    State = 0
    SongNumber = 0
    os.chdir(directory)
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            MaxSong += 1
            State = 1
            ListOfSongs.append(file)
    if State == 1 and PlayButtonState == 0:
        mixer.music.load(ListOfSongs[SongNumber])


def FirstStart():
    print("Hello from Mateusz Perczak and Krzysztof Zawisła")
    global directory
    global ListOfSongs
    global SongNumber
    global State
    directory = askdirectory()
    if directory == "" or None:
        exit("Directory is empty!!")
    mixer.init()
    MusicScan()


def ChangeDirectory(event):
    global directory
    global State
    global MaxSong
    global ListOfSongs
    global DirectoryLabelText
    newdirectory = askdirectory()
    if directory != newdirectory and newdirectory != "" or None:
        ListOfSongs = []
        for file in range(MaxSong + 1):
            MusicListBox.delete(0)
        directory = newdirectory
        DirectoryLabelText.set(directory)
        MusicScan()
        Update(State)


def Update(state):
    global ListOfSongs
    global MaxSong
    if state == 1:
        ListOfSongs.reverse()
        for file in ListOfSongs:
            MusicListBox.insert(0, file)
        ListOfSongs.reverse()
    elif state == 0:
        MusicListBox.delete(0, END)
        MaxSong = 0
        ListOfSongs = []


def Play(event):
    global PlayButtonState
    global PlayedState
    global SongNumber
    global ListOfSongs
    global State
    global Curent
    if State == 1:
        if PlayButtonState == 1:
            mixer.music.stop()
            time.sleep(0.1)
            PlayButton.configure(image=Playimg)
            PlayButtonState = 0
        elif PlayButtonState == 0:
            mixer.music.load(ListOfSongs[SongNumber])
            PlayLabelText.set(ListOfSongs[SongNumber])
            mixer.music.play()
            PlayButton.configure(image=Pauseimg)
            PlayButtonState = 1
            ProgressUpdate()
    elif State == 0:
        if PlayButtonState == 1:
            mixer.music.stop()
            time.sleep(0.1)
            PlayLabelText.set("")
            PlayButton.configure(image=Playimg)
            PlayButtonState = 0


def Next(event):
    global PlayButtonState
    global SongNumber
    global State
    global MaxSong
    if State == 1:
        if PlayButtonState == 1:
            if SongNumber < MaxSong - 1:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButton.configure(image=Pauseimg)
                PlayButtonState = 1
                SongNumber += 1
                mixer.music.load(ListOfSongs[SongNumber])
                mixer.music.play()
                PlayLabelText.set(ListOfSongs[SongNumber])
                ProgressUpdate()
        if PlayButtonState == 0:
            if SongNumber < MaxSong - 1:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButtonState = 1
                PlayButton.configure(image=Pauseimg)
                SongNumber += 1
                mixer.music.load(ListOfSongs[SongNumber])
                mixer.music.play()
                PlayLabelText.set(ListOfSongs[SongNumber])
                ProgressUpdate()


def Previous(event):
    global PlayButtonState
    global SongNumber
    global State
    global PlayingStatus
    global MaxSong
    if State == 1:
        if PlayButtonState == 1:
            if SongNumber > 0:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButton.configure(image=Pauseimg)
                SongNumber -= 1
                mixer.music.load(ListOfSongs[SongNumber])
                mixer.music.play()
                PlayLabelText.set(ListOfSongs[SongNumber])
                ProgressUpdate()
        if PlayButtonState == 0:
            if SongNumber > 0:
                mixer.music.stop()
                time.sleep(0.1)
                PlayButtonState = 1
                PlayButton.configure(image=Pauseimg)
                SongNumber -= 1
                mixer.music.load(ListOfSongs[SongNumber])
                mixer.music.play()
                PlayLabelText.set(ListOfSongs[SongNumber])
                ProgressUpdate()


def MusicListBoxPointer(event):
    global Try
    global Selected
    global Curent
    global State
    global SongNumber
    global PlayButtonState
    Try += 1
    if Try == 2:
        mixer.music.stop()
        time.sleep(0.1)
        if State == 1:
            Selected = MusicListBox.curselection()
            if Selected != ():
                mixer.music.stop()
                time.sleep(0.1)
                for Song in Selected:
                    Curent = MusicListBox.get(Song)
                for nr, Song in enumerate(ListOfSongs):
                    if Song == Curent:
                        mixer.music.load(ListOfSongs[nr])
                        SongNumber = nr
                        mixer.music.play()
                        if PlayButtonState == 0:
                            PlayButtonState = 1
                            PlayButton.configure(image=Pauseimg)
                        PlayLabelText.set(ListOfSongs[SongNumber])
                        ProgressUpdate()
                        Try = 0


def Volume(value):
    global VolumeValue
    value = float(value)
    value = round(value, 0)
    value = int(value)
    VolumeValue.set("{}%".format(value))
    value = value / 100
    mixer.music.set_volume(value)


def ProgressUpdate():
    global ListOfSongs
    global SongNumber
    global PlayButtonState
    File = MP3(ListOfSongs[SongNumber])
    BitrateVar = File.info.bitrate
    BitrateVar = BitrateVar /1000
    BitrateVar = int(BitrateVar)
    BitrateLabelText.set("{}kbps".format(BitrateVar))
    try:
        FileInfo = File.tags['TCON']
        GenreLabelText.set(FileInfo)
    except:
        GenreLabelText.set("None")
    ProgressValue = round(File.info.length, 1)
    ProgressValue = ProgressValue * 10
    ProgressValue = int(ProgressValue)
    if PlayButtonState == 0:
        PlayButton.configure(image=Pauseimg)
    PBF = threading.Thread(target=ProgressBarFill, args=(ProgressValue,))
    PBF.daemon = True
    PBF.start()


def ProgressBarFill(TotalLength):
    global PlayButtonState
    Target = 0
    MusicProgressBar["maximum"] = TotalLength
    Elapsed = 1
    while Elapsed <= TotalLength and mixer.music.get_busy():
        Elapsed += 1
        MusicProgressBar["value"] = Elapsed
        if Elapsed == TotalLength - 15 and Target != 1:
            Target = 1
            PlayButton.configure(image=Playimg)
            PlayButtonState = 0
        time.sleep(0.1)


def Close():
    mixer.music.stop()
    PlayerForm.destroy()


FirstStart()
MusicProgressBar = ttk.Progressbar(PlayerForm, orient=HORIZONTAL, length=200, mode="determinate", style="G.Horizontal.TProgressbar")
PlayLabel = ttk.Label(PlayerForm, textvariable=PlayLabelText, font="Calibri", style="W.TLabel")
GenreLabel = ttk.Label(PlayerForm, textvariable=GenreLabelText, font="Calibri", style="W.TLabel")
PlayBitrate = ttk.Label(PlayerForm, textvariable=BitrateLabelText, font="Calibri", style="W.TLabel")
VerLabel = ttk.Label(PlayerForm, text="Ver. 02.02.2019", font="Calibri", style="W.TLabel")
DirectoryChangeButton = ttk.Button(PlayerForm, image=Fileimg, cursor="hand2", takefocus=0)
DirectoryLabel = ttk.Label(PlayerForm, font="Calibri",textvariable=DirectoryLabelText,  style="W.TLabel")
PlayButton = ttk.Button(PlayerForm, image=Pauseimg, cursor="hand2", takefocus=0)
NextButton = ttk.Button(PlayerForm, image=Forwardimg, cursor="hand2", takefocus=0)
PreviousButton = ttk.Button(PlayerForm, image=Previousimg, cursor="hand2", takefocus=0)
MusicListBox = Listbox(PlayerForm, font="Calibri", cursor="hand2", bd=0, activestyle="none", selectbackground="#8bc34a", takefocus=0)
PlayImg = ttk.Label(PlayerForm, image=PlayPhotoimg, style="W.TLabel")
VolumeSlider = ttk.Scale(PlayerForm, from_=0, to=100, orient=HORIZONTAL, command=Volume, cursor="hand2")
VolumeLabel = ttk.Label(PlayerForm, textvariable=VolumeValue, font="Calibri", style="W.TLabel")
MusicLabel = ttk.Label(PlayerForm, image=MusicLabelimg, style="W.TLabel")
mixer.music.set_volume(0.50)
VolumeSlider.set(50)
VolumeValue.set("50{}".format("%"))
GenreLabelText.set("")
PlayLabelText.set("No song is playing!")
BitrateLabelText.set("")
DirectoryLabelText.set(directory)
Update(State)
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
PlayButton.bind("<Button-1>", Play)
PreviousButton.bind("<Button-1>", Previous)
NextButton.bind("<Button-1>", Next)
MusicListBox.bind("<Button-1>", MusicListBoxPointer)
DirectoryChangeButton.bind("<Button-1>", ChangeDirectory)
PlayerForm.protocol("WM_DELETE_WINDOW", Close)
PlayerForm.mainloop()
