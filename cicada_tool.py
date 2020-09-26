# -*- coding: UTF-8 -*-
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import glob
import os
import csv
import pandas as pd
import subprocess
from pygame import mixer
from tkinter import messagebox
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
import glob
import matplotlib
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pickle
import numpy as np
import matplotlib.animation as animation
# original annotation imports was here
import arabic_reshaper
import pandas as pd
import os
from tkinter import messagebox
from bidi.algorithm import get_display

###############################################################
              #Constants defined#
###############################################################

HEADER_FONT_STYLE = ("Tahoma", 10, "bold")
FONT_STYLE_BUTTON = ("Arial Bold", 7, "bold")
FONT_STYLE_ANNOTATION = ("Arial", 20)


# On increasing these values window size shrinks
INITIAL_HEIGHT_ADJUST = 1600
INITIAL_WIDTH_ADJUST = 1200

# On increasing these values window size enlarges
FINAL_HEIGHT_ADJUST = 1600
FINAL_WIDTH_ADJUST = 1200

#Height and width of buttons
BUTTONS_HEIGHT = 2
BUTTONS_WIDTH = 15

CSV_FILENAME = "ANNOTATIONS_FILE.csv"
CSV_ORIGINAL_ANNOTATIONS_NAME = ''

# # ==================================================== ADDED ===============================
def _onKeyRelease(event):
    ctrl  = (event.state & 0x4) != 0
    if event.keycode==88 and  ctrl and event.keysym.lower() != "x": 
        event.widget.event_generate("<<Cut>>")

    if event.keycode==86 and  ctrl and event.keysym.lower() != "v": 
        event.widget.event_generate("<<Paste>>")

    if event.keycode==67 and  ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")


###############################################################
           #Initaliazing Tkinter  Window#
###############################################################
# -*- coding: UTF-8 -*-
root = tk.Tk()

proc = subprocess.Popen(["xrandr  | grep \* | cut -d' ' -f4"], stdout=subprocess.PIPE, shell=True)
(OUT, ERR) = proc.communicate()
OUT = str(OUT).split("x")
# HEIGHT_SIZE = str(int(int(OUT[0])/2)-INITIAL_HEIGHT_ADJUST)
# WIDTH_SIZE = str(int(int(OUT[1])/2)-INITIAL_WIDTH_ADJUST)
root.geometry(str(INITIAL_HEIGHT_ADJUST)+"x"+str(INITIAL_WIDTH_ADJUST))
root.bind_all("<Key>", _onKeyRelease, "+")
root.title("Annotation Tool")
root.resizable(1,1)

HEADER = Label(root,text="نرمافزار ساخت زیر نویس برای فایل های صوتی کوتاه ده ثانیه ای",
 underline=0, font=HEADER_FONT_STYLE).grid(row=0, column=10, pady=10)
CURRENT_INDEX = 0
CURRENT_SECOND = 0
LONGEST_AUDIO_MS = 10000
ANNOTATION_ENTRY_VAR = StringVar(root)
mixer.init(16000)



###############################################################
               #Audio Files Folder#
###############################################################
def browse_wav_files():
    """
	Get the folder path of .wav files
	"""
    filename = filedialog.askdirectory()
    global FOLDER_WAV_FILES
    # NOTE : I changed next line to just detect one 
    FOLDER_WAV_FILES = glob.glob(filename+"/*.mp3") 
    if os.path.exists(CSV_FILENAME):
        # ['E:/SUBTITLE TOOLS/cicada-audio-annotation-tool/annotator_wav_to_mp3', 'radio-goftego-98_07_06-08_30.mp3chunk10.mp3']
        starter_string_for_folder_wav_files = FOLDER_WAV_FILES[2].split('\\')[0] 
        annotated_files = pd.read_csv(CSV_FILENAME, error_bad_lines=False)
        annotated_files = annotated_files['Filename'].values.tolist()
        print(FOLDER_WAV_FILES[0:2])
        # for i in FOLDER_WAV_FILES:
        #     if i.split("/")[-1].split('\\')[-1] in annotated_files:
        #         FOLDER_WAV_FILES.remove(i)
        for i in list(set(annotated_files)):
            file_to_remove = starter_string_for_folder_wav_files + '\\' + i
            print("==================================")
            print(f'i am searching for {i} in folderWavFile')
            if file_to_remove in FOLDER_WAV_FILES:
                print(file_to_remove)
                FOLDER_WAV_FILES.remove(file_to_remove)
            print("==================================")
    else:
        pass   
    if len(FOLDER_WAV_FILES) == 0:
        messagebox.showerror("Error", "No Wav Files in Given path")
    else:

        Label(root, text=FOLDER_WAV_FILES[0].split("/")[-1], font=FONT_STYLE_BUTTON).grid(row=4, column=10, sticky=(N, S, W, E), pady=10)
ASK_FOR_WAVFILE_DIR = Button(root, text="Audio Files Folder", fg="green", bd=3, relief="raised",
	                            command=browse_wav_files, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH,
	                            font=FONT_STYLE_BUTTON)
ASK_FOR_WAVFILE_DIR.grid(row=3, column=12, pady=2)


###############################################################
               # Wehre IS Annotation of Audios # 
###############################################################

def browse_folder_to_save_annotations():
    global CSV_ORIGINAL_ANNOTATIONS_NAME
    filename = filedialog.askopenfilename()
    CSV_ORIGINAL_ANNOTATIONS_NAME = filename

ASK_FOR_ANNOTATION_DIR = Button(root, text="Annotatios File", bd=3, relief="raised", fg="green",
	                               command=browse_folder_to_save_annotations, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH,
	                               font=FONT_STYLE_BUTTON)
ASK_FOR_ANNOTATION_DIR.grid(row=2, column=12, pady=10)


###############################################################
                    # QUIT #
###############################################################
def _quit():
    offset = 15.0
    popooz = 12.0
    mixer.music.load(FOLDER_WAV_FILES[CURRENT_INDEX])
    mixer.music.play(loops=0, start=offset + popooz) #  seconds from beginning

# quit_button = Button(root, text="Quit", bd=3, fg="green", relief="raised", command= _quit,
# 	                    font=FONT_STYLE_BUTTON, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
# quit_button.grid(row=2, column=12, pady=10)

###############################################################
                 #Details Button#
###############################################################
def get_details():
    try:
        # print(FOLDER_WAV_FILES[CURRENT_INDEX].split('/')[-1])
        # total_annotations = len(glob.glob(FOLDER_TO_SAVE_ANNOTATIONS+"/*.pkl"))
        total_annotations = pd.read_csv(CSV_FILENAME, error_bad_lines=False)
        total_annotations = len(list(set(total_annotations['Filename'].values)))
        remaining_files = len(FOLDER_WAV_FILES) - (total_annotations)
        messagebox.showinfo("Details", "Total Annotations : " +str(total_annotations)+
                            "\n Total Remaining wav files: "+str(remaining_files))
    except (NameError, FileNotFoundError):
        messagebox.showerror("Path not specified", "Give path for saving annotations")


DETAILS_BUTTON = Button(root, text="Details", bd=3, relief="raised", fg="green", command=get_details,
	                       font=FONT_STYLE_BUTTON, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
DETAILS_BUTTON.grid(row=4, column=12, pady=10)



###############################################################
               #FIND original annotation#
###############################################################

def show_original_annotation():
    ab = os.getcwd()
    CSV_ORIGINAL_ANNOTATIONS_DATAFRAME = pd.read_csv(CSV_ORIGINAL_ANNOTATIONS_NAME)
    text_to_be_reshaped = CSV_ORIGINAL_ANNOTATIONS_DATAFRAME[
        CSV_ORIGINAL_ANNOTATIONS_DATAFRAME['wav_filename'] == FOLDER_WAV_FILES[CURRENT_INDEX].split('\\')[-1] ]['transcript']
    reshaped_text = arabic_reshaper.reshape(text_to_be_reshaped.values[0])
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text_to_be_reshaped.values[0])
    Label(root, text="",
            	     font=("Arial", 20)).grid(row=10, column=10,
            	                                           sticky=(N, S, W, E), pady=10)    
    return get_display(reshaped_text)
     

###############################################################
               #Previous Audio Button#
###############################################################
def previous_audio_update_index():
    try:
        check_folder = len(FOLDER_WAV_FILES)
        global CURRENT_INDEX
        if CURRENT_INDEX == 0:
            return CURRENT_INDEX
        else:
            CURRENT_INDEX = CURRENT_INDEX - 1
            ANNOTATION_ENTRY_VAR.set("")
            Label(root, text=FOLDER_WAV_FILES[CURRENT_INDEX].split("/")[-1],
            	     font=FONT_STYLE_BUTTON).grid(row=4, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
            Label(root, text=show_original_annotation(),
            	     font=FONT_STYLE_BUTTON).grid(row=3, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
        if mixer.music.get_busy():
            mixer.music.stop()
        play_audio(CURRENT_INDEX)

    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")



previous_audio_button = Button(root, text="<< Previous",bd=3,relief="raised",fg="green",
	                              command=previous_audio_update_index, font=FONT_STYLE_BUTTON,
	                              height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
previous_audio_button.grid(row=7, column=0, pady=10)



###############################################################
               #Next Audio Button
###############################################################
def next_audio_update_index():
    """
	Loop over the next audio if the directory
	"""
    try:
        global CURRENT_INDEX
        print(len(FOLDER_WAV_FILES))
        if CURRENT_INDEX == len(FOLDER_WAV_FILES)-1:
            return CURRENT_INDEX
        else:
            CURRENT_INDEX = CURRENT_INDEX + 1
            ANNOTATION_ENTRY_VAR.set("")
            Label(root, text=FOLDER_WAV_FILES[CURRENT_INDEX].split("/")[-1],
            	     font=FONT_STYLE_BUTTON).grid(row=4, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
            Label(root, text=show_original_annotation(),
            	     font=FONT_STYLE_BUTTON).grid(row=3, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
        if mixer.music.get_busy():
            mixer.music.stop()
        play_audio(CURRENT_INDEX)


    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")

NEXT_AUDIO_BUTTON = Button(root, text="Next >>", bd=3, relief="raised", fg="green",
	                          command=next_audio_update_index, font=FONT_STYLE_BUTTON,
	                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
NEXT_AUDIO_BUTTON.grid(row=6, column=0, pady=10)


###############################################################
               # Pause Audio
###############################################################
def pause():
    """
    TODO : write a function to pause unpause with one function. 
    Initialize A VAR and Zero it when next and prev.
	"""
    try:
        if mixer.music.get_busy():
            mixer.music.pause()
            # print("======================  dasht ye chizi pakhsh mishod ======================")
    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")

NEXT_AUDIO_BUTTON = Button(root, text="Pause", bd=3, relief="raised", fg="green",
	                          command=pause, font=FONT_STYLE_BUTTON,
	                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
NEXT_AUDIO_BUTTON.grid(row=2, column=0, pady=10)


###############################################################
               # Resume Audio
###############################################################
def resume():
    """
    TODO : write a function to pause unpause with one function. 
    Initialize A VAR and Zero it when next and prev.
	"""
    try:
        global CURRENT_SECOND
        if mixer.music.get_busy():
            mixer.music.unpause()
    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")

NEXT_AUDIO_BUTTON = Button(root, text="Resume", bd=3, relief="raised", fg="green",
	                          command=resume, font=FONT_STYLE_BUTTON,
	                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
NEXT_AUDIO_BUTTON.grid(row=1, column=0, pady=10)


###############################################################
               # 2sec forward Audio
###############################################################
def secForward():
    """
	Loop over the next audio if the directory
	"""
    try:
        global CURRENT_SECOND
        global LONGEST_AUDIO_MS
        if mixer.music.get_busy():
            if CURRENT_SECOND + mixer.music.get_pos() + 2000 < LONGEST_AUDIO_MS:
                CURRENT_SECOND = CURRENT_SECOND + mixer.music.get_pos()
                mixer.music.rewind()
                CURRENT_SECOND = CURRENT_SECOND + 2000
                mixer.music.play(loops=0, start = CURRENT_SECOND/1000)
                # print(CURRENT_SECOND)
    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")

NEXT_AUDIO_BUTTON = Button(root, text="2 SEC Forward", bd=3, relief="raised", fg="green",
	                          command=secForward, font=FONT_STYLE_BUTTON,
	                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
NEXT_AUDIO_BUTTON.grid(row=3, column=0, pady=10)


###############################################################
               # 2sec backward Audio
###############################################################
def secBack():
    """
	Loop over the next audio if the directory
	"""
    try:
        global CURRENT_SECOND
        global LONGEST_AUDIO_MS
        if mixer.music.get_busy():
            if CURRENT_SECOND + mixer.music.get_pos() - 2000 > 0:
                CURRENT_SECOND = CURRENT_SECOND + mixer.music.get_pos()
                mixer.music.rewind()
                CURRENT_SECOND = CURRENT_SECOND - 2000
                mixer.music.play(loops=0, start = CURRENT_SECOND/1000)
                # print(CURRENT_SECOND)
    except NameError:
        messagebox.showinfo("File Path", "No Wav Files Path Given")

NEXT_AUDIO_BUTTON = Button(root, text="2 SEC Backward", bd=3, relief="raised", fg="green",
	                          command=secBack, font=FONT_STYLE_BUTTON,
	                          height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
NEXT_AUDIO_BUTTON.grid(row=4, column=0, pady=10)



###############################################################
               #Play Audio Button#
###############################################################
def play_audio(index_value):
    """
	Play audio
	"""
    try:
        mixer.music.load(FOLDER_WAV_FILES[index_value])
        mixer.music.play()
    except NameError:
        messagebox.showerror("No Wav file", "No audio file to Play")

PLAY_BUTTON = Button(root, text="Start Audio", bd=3, fg="green",
	                    command=lambda: play_audio(CURRENT_INDEX), font=FONT_STYLE_BUTTON,
	                    height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
PLAY_BUTTON.grid(row=5, column=0, pady=10)


###############################################################
               #Annotation Entry Field#
###############################################################
ANNOTATIONS_ENTRY = Entry(root, width = 100,textvariable=ANNOTATION_ENTRY_VAR, bd=5, relief="raised",
	                         font=("Arial", 15)).grid(row=9, column=10, ipady = 10, ipadx = 10)
# Label(root, text="Spectrogram Type: ", fg="green",
# 	     font=FONT_STYLE_BUTTON).grid(row=7, column=12, sticky=(N, S, W, E), pady=10)


###############################################################
               #Save Annotations#
###############################################################
def save_annotations(index_value):
    """
	Function to save the annotations
	"""
    try:
        if os.path.exists(CSV_FILENAME):
            with open(CSV_FILENAME, "a", encoding='utf-8') as file_object:
                wavfile_information_object = csv.writer(file_object)
                wavfile_information_object.writerow([FOLDER_WAV_FILES[index_value].split("\\")[-1]] + ANNOTATION_ENTRY_VAR.get().split(","))
                # print(FOLDER_WAV_FILES[index_value].split("/")[-1]+" - " '{}'.format(ANNOTATION_ENTRY_VAR.get().split(",")))

        # with open(FOLDER_TO_SAVE_ANNOTATIONS+"/"+FOLDER_WAV_FILES[index_value].split("/")[-1][:-4]+".pkl", "wb") as file_obj:
        #     pickle.dump(ANNOTATION_ENTRY_VAR.get().split(","), file_obj)
        # next_audio_update_index()
        else:
            with open(CSV_FILENAME, "w", encoding='utf-8') as file_object:
                wavfile_information_object = csv.writer(file_object)
                wavfile_information_object.writerow(["Filename","Label1","Label2","Label3","Label4"])
                wavfile_information_object.writerow([FOLDER_WAV_FILES[index_value].split("\\")[-1]]+ANNOTATION_ENTRY_VAR.get().split(","))
        Label(root, text="SUBMITTED",
            	     font=FONT_STYLE_BUTTON).grid(row=11, column=10,
            	                                           sticky=(N, S, W, E), pady=10)
    except NameError:
        messagebox.showerror("No Path", "Specify path to save annotations!")


def save_and_next_audio(event):
    """
	Binding the submit button to <Return> key
	"""
    save_annotations(CURRENT_INDEX)
    next_audio_update_index()
    play_audio(CURRENT_INDEX)

SUBMIT_BUTTON = Button(root, text="Submit", bd=3, relief="raised", fg="green",
	                      command=lambda: save_annotations(CURRENT_INDEX),
	                      font=FONT_STYLE_BUTTON, height=BUTTONS_HEIGHT, width=BUTTONS_WIDTH)
SUBMIT_BUTTON.grid(row=5, column=12, pady=10)
root.bind('<Return>', save_and_next_audio)

root.mainloop()