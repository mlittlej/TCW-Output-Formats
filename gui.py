#!/usr/bin/env python3
import sys
import tcw_transcode_tools as tcw_tools

#Every time Jenny finishes editing an episode she needs to create multiple versions of the podcast's audio files
#Each serves a different purpose - mostly to allow people who need different formats and filesizes to get them
#Admittedly I doubt anyone actually uses these but I know I've been stuck in a situation with barely any bandwidth
#and nothing to listen to!

#I've used my previous GUI code as a starting point so some of the comments may look familiar!

# 1. Import `QApplication` and all the required widgets
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QVBoxLayout
from PyQt5 import QtGui 
from PyQt5.QtGui import QIcon

#QApplication is an object that we fiddle with. I think. We pass it the command line arguments, for some as-yet-obscure reason.
app = QApplication(sys.argv)

#Now we create the GUI
#Window is an object of the type QWidget. Then we do the usual object-orientated stuff to mess with it.
window = QWidget()
window.setWindowTitle('Audio exporter')

#Also I don't want the default icon (whether that's the window or the tray)
icon = QIcon('icon.png')
app.setWindowIcon(QIcon(icon))

#The first two parameters are the x and y coordinates at which the window will be placed on the screen. 
#The third and fourth parameters are the width and height of the window.
window.setGeometry(100, 100, 480, 200)
window.move(260, 215)

#Let's lay things out vertically
layout = QVBoxLayout()


def get_input_file():
    
    #input and output files need to be globally scoped
    global input_file
    global output_file_name
    global input_file_label
    global file_name

    #First we want to get the input file - the '(*.*)' thing is where we could specify a file extension e.g. (*.flac)
    file_name = QFileDialog.getOpenFileName(None, 'Open file', './', '(*.*)')
    
    #Grab the relevant part of the tuple and pass it to ffmpeg in a way it understands
    input_file = file_name[0]

    #flatten the list into a string (if the filename has full stops in it then input_file_name[0] alone won't work)
    output_file_name = tcw_tools.output_filename_sanitiser(file_name[0])

    #Tell the user that we've got their file as well as hiding the old button
    input_file_button.hide()
    input_file_label = QLabel(f"Selected input file: {file_name[0]}")
    input_file_label.show()
    layout.addWidget(input_file_label)

    #Now show the output button:
    output_button.show()

def output_directory_selection():
    output_button.hide()
    
    global output_path
    #Now we prompt the user for where to save the output
    output_path = QFileDialog.getExistingDirectory(None,'Select output folder')
    #The output path is a string rather than the tuples we get from getSaveFileName
    input_file_label.hide()
    transcode_all_button.show()
    transcode_mp3_button.show()

def transcode_all():
    # The parameters for the various The C Word release formats are as follows:
    # Opus, 24kbps VBR mono
    # MP3 V5.5 ~125kbps
    # M4A Q3 ~96kbps
    # Ogg Vorbis Q-0.1 mono ~48kbps
    #
    # Translated into ffmpeg command line commands that's: 
    # ffmpeg -i [input] -c:a libopus -b:a 24k -ac 1 -frame_duration 60 [output.opus]
    # ffmpeg -i [input] -c:a libmp3lame -q 5.5 -compression_level 0 [output.mp3]
    # ffmpeg -i [input] -c:a libvorbis -q -0.1 -ac 1 [output.ogg]
    # ffmpeg -i [input] -c:a libfdk_aac -vbr 3 [output.m4a]
    #
    # If you'd like to add more variants they can go in here.
    # If you're adding a new file extension then you'll need to tinker with the tcw_transcode_tools module
    # Mainly because I've not looked up the specific eccentricities of every conceivable audio codec!
    
    # The last number is the channel count (1 for mono, 2 for stereo)
    # Also the numbers should be strings
    tcw_tools.ffmpeg_audio_transcode(input_file, output_path, output_file_name, "opus", "24000", "1")
    tcw_tools.ffmpeg_audio_transcode(input_file, output_path, output_file_name, "mp3", "5.5", "2")
    tcw_tools.ffmpeg_audio_transcode(input_file, output_path, output_file_name, "m4a", "3", "2")
    tcw_tools.ffmpeg_audio_transcode(input_file, output_path, output_file_name, "ogg", "-0.1", "1")
    transcode_all_button.hide()
    transcode_mp3_button.hide()
    transcoding_complete_label.show()

def transcode_mp3():
    tcw_tools.ffmpeg_audio_transcode(input_file, output_path, output_file_name, "mp3", "5.5", "2")
    transcode_all_button.hide()
    transcode_mp3_button.hide()
    transcoding_complete_label.show()

#Add the buttons and labels but hide them initially
input_file_button = QPushButton('Select input file')
output_button = QPushButton('Select the output folder')
transcode_all_button = QPushButton('Transcode to all formats')
transcode_mp3_button = QPushButton('Transcode to MP3 only')
transcoding_complete_label = QLabel('Done!')

output_button.hide()
transcode_all_button.hide()
transcode_mp3_button.hide()
transcoding_complete_label.hide()

#When a button is clicked run the code
input_file_button.clicked.connect(get_input_file)
output_button.clicked.connect(output_directory_selection)
transcode_all_button.clicked.connect(transcode_all)
transcode_mp3_button.clicked.connect(transcode_mp3)

#Now we add those widgets to the layout. At present we're using a vertical layout so these are from top to bottom.
layout.addWidget(input_file_button)
layout.addWidget(output_button)
layout.addWidget(transcode_all_button)
layout.addWidget(transcode_mp3_button)
layout.addWidget(transcoding_complete_label)

#Add a button that kills the program:
closeButton = QPushButton('Close program')
closeButton.clicked.connect(lambda _: sys.exit())
layout.addWidget(closeButton)

#Then we need to actually display it:
window.setLayout(layout)
window.show()

#This one I don't fully understand:
sys.exit(app.exec())
