These .UI files can be edited in QT Designer

Once they are modified, run the script in this folder to convert them to .py files.
Place the .py files in the ui folder within the project's root directory before building.

pyuic5 -x mainWindow.ui -o mainWindow.py