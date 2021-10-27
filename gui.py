#!/usr/bin/env python3
import sys
import ffmpeg

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

#Then we create the widgets that make up the GUI. For example the QLabel object type:

inputFileButton = QPushButton('Input file')




def getInputFile():
    #First we want to get the input file - the '(*.*)' thing is where we could specify a file extension e.g. (*.flac)
    fname = QFileDialog.getOpenFileName(None, 'Open file', './', '(*.*)')
    
    #input and output files need to be globally scoped
    global inputFile
    global outputFileName
    global inputFileLabel
    
    #Grab the relevant part of the tuple
    inputFile = ffmpeg.input(fname[0])

    #Tell the user that we've got their file as well as hiding the old button
    inputFileButton.hide()
    inputFileLabel = QLabel("Selected input file: " + fname[0])
    inputFileLabel.show()
    layout.addWidget(inputFileLabel)

    #Grab the name of the file for the outputs, split it into a list, keep only the last entry - the file
    inputFileName = fname[0].split("/")
    inputFileName = inputFileName[-1]
    #The bin the file extension as we only need the name itself
    inputFileName = inputFileName.split(".")
    outputFileName = inputFileName[0]



    #Now show the output button:
    doStuffButton.show()
    doStuffLabel.show()



doStuffButton = QPushButton('Select the output folder')
doStuffLabel = QLabel('Click the button to output all four formats')

def doStuff():
    doStuffButton.hide()
    doStuffLabel.hide()
        
    #Now we prompt the user for where to save the output
    outputPath = QFileDialog.getExistingDirectory(None,'Select output folder')
    #The output path is a string rather than the tuples we get from getSaveFileName
    

    inputFileLabel.hide()

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

    #Opus first
    stream = ffmpeg.output(inputFile, outputPath + "/" + outputFileName + '.opus', ac=1, audio_bitrate=24000)
    ffmpeg.run(stream)
    #Then MP3
    stream = ffmpeg.output(inputFile, outputPath + "/" + outputFileName + '.mp3', q=5.5)
    ffmpeg.run(stream)
    #Now AAC - we don't actually have libfdk_aac so instead we're using the native implementation which isn't quite as good
    #We'll make do though!
    stream = ffmpeg.output(inputFile, outputPath + "/" + outputFileName + '.m4a', q=0.55)
    ffmpeg.run(stream)
    #Then Vorbis
    stream = ffmpeg.output(inputFile, outputPath + "/" + outputFileName + '.ogg', q=-0.1, ac=1)
    ffmpeg.run(stream)

    stuffDoneLabel = QLabel('Done!')
    layout.addWidget(stuffDoneLabel)



#When the button is clicked run the code
inputFileButton.clicked.connect(getInputFile)
doStuffButton.clicked.connect(doStuff)


#Now we add those widgets to the layout. At present we're using a vertical layout so these are from top to bottom.
layout.addWidget(inputFileButton)
layout.addWidget(doStuffLabel)
layout.addWidget(doStuffButton)

#Add a button that kills the program:
closeButton = QPushButton('Close program')
closeButton.clicked.connect(lambda _: sys.exit())
layout.addWidget(closeButton)

doStuffButton.hide()
doStuffLabel.hide()

#Then we need to actually display it:
window.setLayout(layout)
window.show()

#This one I don't fully understand:
sys.exit(app.exec())