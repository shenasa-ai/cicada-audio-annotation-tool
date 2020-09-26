# CICADA. This project is forked and I added freatures to use more efficient.
This app is customized to usewith Deep Speech Mozilla Project.

## Cicada - simple GUI for audio annotation 

Cicada is an audio annotation tool which can be used to annotate .wav files and save the annotation in ```Pickle (Python List)``` format (currently). Eventually it can be made it save as JSON, XML format as well.

This is customized for RTL languages. Feel free to change for your own language.

## OS usage : 
Be careful to use this app in windows to use all features. if you use this in Linux you can just use wav files and some buttons may not work.

#### Setting up environment:
```Requires Python 3.5.6```.

###### Following are requiremnts needed to run the tool.
```shell
$ pip install -r requirements.txt
```

you may need to install some more libs too.

#### Things to know before starting tool :
I have disabled the window resizing option just to make sure the spectrogram fits in well within the frame.

You can make changes according to your screen size by changing the following constants in the script ```cicada_tool.py```
```python
HEADER_FONT_STYLE = ("Tahoma", 10, "bold")
FONT_STYLE_BUTTON = ("Arial Bold", 7, "bold")

# On increasing these values window size shrinks
INITIAL_HEIGHT_ADJUST = INT_NUMBER
INITIAL_WIDTH_ADJUST = INT_NUMBER

# On increasing these values window size enlarges
FINAL_HEIGHT_ADJUST = INT_NUMBER
FINAL_WIDTH_ADJUST = INT_NUMBER

#Height and width of buttons
BUTTONS_HEIGHT = INT_NUMBER
BUTTONS_WIDTH = INT_NUMBER
```
You can adjust the button sizes and change your font styles along with frame size.

#### To start annotating:

##### Run this script:
After making sure you have ```python3.5.6``` installed and all the required packages you are good to go.
```shell
$ python cicada_tool.py
```

Note: I have given ```python```and not ```python3``` for running the script because I assume you have virtual environment which has ```python3``` installed

NOTE : I assume you are using Mozilla Deep Speech format for csv files and wav files.
Then choose the csv file for annotations you have. ( wav_filename must be same with the wav file names. )
Then choose folder which contain audio files. 

And It is readu to use. 
If facing any problem feel free to create new issue.

