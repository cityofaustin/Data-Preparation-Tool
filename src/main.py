'''
DataCleanTool - 2022
author: SappI
'''
from distutils import errors
from email import header
import os, sys, pickle, platform, io
from turtle import update
import pandas as pd
import updateCheck
import webbrowser
from PyQt5 import QtWidgets, QtGui, QtCore

# Import UI files
from ui.mainWindow import Ui_MainWindow
from ui.diag import Ui_aboutWindow
from ui.pageSelect import Ui_pageWindow
from ui.trimWindow import Ui_trimWindow
from ui.nullWindow2 import Ui_nullValueWin
from ui.renameColWindow import Ui_renameColumnWindow
from ui.desc_info import Ui_desc_infoWindow
from ui.typeWindow import Ui_typeWindow

# Update this with each release
appName = "Data Preparation Tool"
versionNumber = "1.0.0"
appPath = os.path.dirname(__file__)
platName = platform.system()
dataLoc = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DataLocation)[0] + f'/{appName}'
desktopLoc = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.DesktopLocation)[0]

try:
    resPath = sys._MEIPASS
except Exception:
    resPath = os.path.dirname(__file__)

# Window classes
class mainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)        
        self.act_quit.triggered.connect(quitApp)
        self.act_open.triggered.connect(openFile)
        self.act_about.triggered.connect(showAbout)
        self.tableWidget.cellPressed.connect(self.cell_was_clicked)
        self.tableWidget.horizontalHeader().sectionClicked.connect(self.headerClick)
        self.tableWidget.verticalHeader().sectionClicked.connect(self.rowClick)
        self.actionTrim_digits.triggered.connect(showTrimWindow)
        self.actionClear_Null_Values.triggered.connect(openNullWindow)
        self.menu_save.triggered.connect(saveFile)
        self.btnRename.clicked.connect(lambda: uiRenameCol.displayWindow())
        self.btnDropCol.clicked.connect(lambda: confirmDrop("Do you want to delete the currently selected column?", "Confirm Drop"))
        self.menu_openFile.triggered.connect(openFile)        
        self.menu_trim.triggered.connect(showTrimWindow)
        self.menu_nullVals.triggered.connect(openNullWindow)
        self.menu_undo.triggered.connect(lambda: doUndo())
        self.menu_redo.triggered.connect(lambda: doRedo())
        self.tableWidget.cellChanged.connect(self.updateTable)
        self.menu_desc.triggered.connect(lambda: uiDesc_Info.openWindow(True))
        self.menu_info.triggered.connect(lambda: uiDesc_Info.openWindow(False))
        self.menu_help.triggered.connect(lambda: self.launchHelp())
        #self.btnSort.clicked.connect(lambda: self.sort())
        self.btnChangeType.clicked.connect(lambda: uiTypeWindow.confirmTypeChange())
    def cell_was_clicked(self, row, column):
        global activeColumn
        print(activeColumn)
        print(f"Row {row} and Column {column} was clicked")
        trimInfo.trimText = self.tableWidget.item(row, column).text()
        activeColumn = column

    def headerClick(self, colNum: int):
        global activeColumn
        activeColumn = colNum
        trimInfo.trimText = ui.tableWidget.item(0, activeColumn).text()
    
    def rowClick(self, rowNum: int):
        global activeColumn
        activeColumn = 0
        trimInfo.trimText = ui.tableWidget.item(rowNum, activeColumn).text()

    def updateTable(self):
        global df
        global table
        global fileLoaded

        if fileLoaded:
            try:
                print("cell changed")
                col = self.tableWidget.currentColumn()
                row = self.tableWidget.currentRow()
                tableItem = self.tableWidget.item(row, col).text()
                setUndo(df, undoRedoInfo.undoDF)
                df.iloc[row, col] = tableItem
                write_dt_to_qTable(df, table)
            except:
                pass
    
    def launchHelp(self):
        webbrowser.open('https://github.com/cityofaustin/Data-Preparation-Tool/blob/main/userguide/README.md', new=2)

    def sort(self):
        global df
        global sortInfo

        if sortInfo.headerData[activeColumn] == 0:
            setUndo(df, undoRedoInfo.undoDF)
            headerName = str(list(df)[activeColumn])
            df.loc[pd.to_numeric(df[headerName], errors='coerce').sort_values().index]
            #df.sort_values(by=[headerName], inplace=True)
            sortInfo.headerData[activeColumn] = 1
            write_dt_to_qTable(df, table)
            print(sortInfo.headerData)
        else:
            setUndo(df, undoRedoInfo.undoDF)
            headerName = str(list(df)[activeColumn])
            df.sort_values(by=[headerName], ascending=False, inplace=True)
            sortInfo.headerData[activeColumn] = 0
            write_dt_to_qTable(df, table)
            print(sortInfo.headerData)



class aboutWindow(QtWidgets.QMainWindow, Ui_aboutWindow):
    def __init__(self):
        super(aboutWindow, self).__init__()
        self.setupUi(self)
        self.btnOk.clicked.connect(closeAbout)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        self.lblVersion.setText(f'Version {versionNumber}')

class desc_infoWindow(QtWidgets.QMainWindow, Ui_desc_infoWindow):
    def __init__(self):
        super(desc_infoWindow, self).__init__()
        self.setupUi(self)
        self.btnClose.clicked.connect(lambda: self.closeWindow())
        self.btnExport.clicked.connect(lambda: self.exportCSV())

    def openWindow(self, isDesc: bool):
        global df
        if isDesc:
            self.btnExport.setVisible(True)
            self.txtInfo.setText("")
            self.setWindowTitle("Describe")
            descText = str(df.describe())
            print(df.describe())
            self.txtInfo.setText(descText)
            self.show()
        else:
            self.btnExport.setVisible(False)
            self.txtInfo.setText("")
            self.setWindowTitle("Info")
            buffer = io.StringIO()
            df.info(buf=buffer)
            s = buffer.getvalue()
            sSplit = s.split("\n")
            print(sSplit[3].split())

            #print(str(s.split("\n")))
            self.txtInfo.setText(str(s))
            self.show()

    def closeWindow(self):
        self.close()

    def exportCSV(self):
        global df
        try:
            filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', desktopLoc, "CSV Files(*.csv)")[0]
            df.describe().to_csv(str(filename), index=True)
        except:
            pass


class nullWindow(QtWidgets.QMainWindow, Ui_nullValueWin):
    def __init__(self):
        super(nullWindow, self).__init__()
        self.setupUi(self)
        self.radioIgnore.clicked.connect(self.ignoreSelected)
        self.radioEmpty.clicked.connect(self.emptySelected)
        self.radioZero.clicked.connect(self.zeroSelected)
        self.radioNull.clicked.connect(self.nullSelected)
        self.radioCustom.clicked.connect(self.customSelected)

        self.radioIgnore2.clicked.connect(self.ignoreSelected2)
        self.radioEmpty2.clicked.connect(self.empty2Selected)
        self.radioZero2.clicked.connect(self.zeroSelected2)
        self.radioNull2.clicked.connect(self.nullSelected2)
        self.radioCustom2.clicked.connect(self.customSelected2)

        self.btnCancel.clicked.connect(closeNullWindow)
        self.btnOkay.clicked.connect(commitNullValues)

    def ignoreSelected(self, selected):
        if selected:
            nullInfo.isIgnore1 = True
            self.txtCustom.setEnabled(False)

    def ignoreSelected2(self, selected):
        if selected:
            nullInfo.isIgnore2 = True
            self.txtCustom2.setEnabled(False)

    def emptySelected(self, selected):
        if selected:
            nullInfo.nullVal1 = ""
            nullInfo.isIgnore1 = False
            nullInfo.isCustom1 = False
            self.txtCustom.setEnabled(False)

    def empty2Selected(self, selected):
        if selected:
            nullInfo.nullVal2 = ""
            nullInfo.isIgnore2 = False
            nullInfo.isCustom2 = False
            self.txtCustom2.setEnabled(False)

    def zeroSelected(self, selected):
        if selected:
            nullInfo.nullVal1 = "0"
            nullInfo.isIgnore1 = False
            nullInfo.isCustom2 = False
            self.txtCustom.setEnabled(False)
    
    def zeroSelected2(self, selected):
        if selected:
            nullInfo.nullVal2 = "0"
            nullInfo.isIgnore2 = False
            nullInfo.isCustom2 = False
            self.txtCustom2.setEnabled(False)

    def nullSelected(self, selected):
        if selected:
            nullInfo.nullVal1 = "null"
            nullInfo.isIgnore1 = False
            nullInfo.isCustom2 = False
            self.txtCustom.setEnabled(False)

    def nullSelected2(self, selected):
        if selected:
            nullInfo.nullVal2 = "null"
            nullInfo.isIgnore2 = False
            nullInfo.isCustom2 = False
            self.txtCustom2.setEnabled(False)
    
    def customSelected(self, selected):
        if selected:
            nullInfo.isCustom1 = True
            nullInfo.isIgnore1 = False
            self.txtCustom.setEnabled(True)

    def customSelected2(self, selected):
        if selected:
            nullInfo.isCustom2 = True
            nullInfo.isIgnore2 = False
            self.txtCustom2.setEnabled(True)

class trimWindow(QtWidgets.QMainWindow, Ui_trimWindow):
    def __init__(self):
        super(trimWindow, self).__init__()
        self.setupUi(self)
        self.horizontalSlider.valueChanged.connect(lambda: slideChange(trimInfo.trimTextShort, trimSlider.value()))
        self.radioLeft.toggled.connect(self.leftSelected)
        self.radioRight.toggled.connect(self.rightSelected)
        self.btnCancel.clicked.connect(closeTrimWindow)
        self.btnOkay.clicked.connect(lambda: commitTrim(trimSlider.value()))
    
    def updateInterface(self):
        if trimInfo.isRight == True:
            trimSlider.setRange(-len(trimInfo.trimTextShort), 0)
            trimSlider.setValue(0)
            print("Right pressed")
        else:
            trimSlider.setRange(0, len(trimInfo.trimTextShort))
            trimSlider.setValue(0)
            print("Left pressed")

    def leftSelected(self, selected):
        if selected:
            if len(trimInfo.trimText) > 20:
                trimInfo.trimTextShort = trimInfo.trimText[:20]
                trimLabel.setText(f"<span style='color: black'>{trimInfo.trimTextShort}...</span>")
            else:
                trimInfo.trimTextShort = trimInfo.trimText
                trimLabel.setText(f"<span style='color: black'>{trimInfo.trimTextShort}</span>")

            trimInfo.isRight = False
            self.updateInterface()

    def rightSelected(self, selected):
        if selected:
            if len(trimInfo.trimText) > 20:
                trimInfo.trimTextShort = trimInfo.trimText[-20:]
                trimLabel.setText(f"...<span style='color: black'>{trimInfo.trimTextShort}</span>")
            else:
                trimInfo.trimTextShort = trimInfo.trimText
                trimLabel.setText(f"<span style='color: black'>{trimInfo.trimTextShort}</span>")
            trimInfo.isRight = True
            self.updateInterface()

class pageSelect(QtWidgets.QMainWindow, Ui_pageWindow):
    def __init__(self):
        super(pageSelect, self).__init__()
        self.setupUi(self)
        self.btnForward.clicked.connect(lambda: changePage(False))
        self.btnBack.clicked.connect(lambda: changePage(True))
        self.btnOpen.clicked.connect(openPage)


class typeWindow(QtWidgets.QMainWindow, Ui_typeWindow):
    def __init__(self):
        super(typeWindow, self).__init__()
        self.setupUi(self)
        self.btnCancel.clicked.connect(lambda: self.closeWindow())

    def closeWindow(self):
        self.close()

    def confirmTypeChange(self):
        global df
        headers = list(df)
        selectedColumn = headers[activeColumn]

        try:
            df[selectedColumn] = df[selectedColumn].astype(float).astype('int64')
        except Exception as ex:
            print(ex)

class renameColumn(QtWidgets.QMainWindow, Ui_renameColumnWindow):
    def __init__(self):
        super(renameColumn, self).__init__()
        self.setupUi(self)
        self.btnCancel.clicked.connect(lambda: self.closeWindow())
        self.btnOkay.clicked.connect(lambda: self.renameCol(df))

    def displayWindow(self):
        txt = list(df)[activeColumn]
        self.txtRename.setText(txt)
        self.show()

    def closeWindow(self):
        self.close()

    def renameCol(self, df):
        global table
        text = self.txtRename.text()
        if len(text) < 0:
            print("Can't be empty")
        else:
            setUndo(df, undoRedoInfo.undoDF)
            df.rename(columns={df.columns[activeColumn]: text}, inplace=True)
            write_dt_to_qTable(df, table)
            self.close()

# TRIM CLASS
class trimData:
    def __init__(self):
        self.trimText = ""
        self.trimTextShort = ""
        self.isRight = False

# NULL CLASS
class nullData:
    def __init__(self):
        self.nullVal1 = ""
        self.isCustom1 = False
        self.nullVal2 = ""
        self.isCustom2 = False
        self.isIgnore1 = True
        self.isIgnore2 = True

# UNDO/REDO CLASS
class undoRedo:
    def __init__(self):
        self.undoDF = pd.DataFrame()
        self.redoDF = pd.DataFrame()

class sortData:
    def __init__(self):
        self.headerData = []
        self.redoheaderData = []
        self.undoheaderData = []
    
    def populateLists(self, headers):
        # Run this when loading in a file. Create a list that is the length of
        # the number of headers in the DF. It is intially populated with 0s
        # but are changed to 1 when sorting. This keeps track of each columns
        # sort status (0 = ascending or 1 = descending)
        self.headerData.clear()
        for header in headers:
            self.headerData.append(0)

# Globals
df = pd.DataFrame
dfNew = pd.DataFrame
dfPage = pd.DataFrame
fileLoaded = False
activeColumn = 0
pageNum = 0
numberOfPages = 0
excelFile = ''

# Classes
trimInfo = trimData()
nullInfo = nullData()
undoRedoInfo = undoRedo()
sortInfo = sortData()

# Data from res.dat will be stored in this dictionary
iconDict = {}

# Initialize the app
app = QtWidgets.QApplication([])
app.setStyle("Fusion")

# Create a DF
def createDF(fName: str) -> pd.DataFrame:
    if ".csv" in fName:
        df = pd.read_csv(fName)
        return df
    elif ".xlsx" in fName:
        df = pd.read_excel(fName)
        return df

def readDat(datFile: str):
    # Reads resource data packed in the res.dat file
    global iconDict
    f=open(datFile, 'rb')
    iconDict = pickle.load(f)
    f.close()

def setUndo(origDF: pd.DataFrame, UndoDF: pd.DataFrame):
    global df
    undoRedoInfo.undoDF = df.copy()
    sortInfo.undoheaderData = list(sortInfo.headerData)
    ui.menu_undo.setEnabled(True)
    ui.menu_redo.setEnabled(False)

def doUndo():
    global df
    global table
    undoRedoInfo.redoDF = df.copy()
    sortInfo.redoheaderData = list(sortInfo.headerData)
    df = undoRedoInfo.undoDF
    print(sortInfo.headerData)
    sortInfo.headerData = list(sortInfo.undoheaderData)
    print(sortInfo.headerData)
    write_dt_to_qTable(df, table)
    ui.menu_undo.setEnabled(False)
    ui.menu_redo.setEnabled(True)

def doRedo():
    global df
    global table
    undoRedoInfo.undoDF = df.copy()
    sortInfo.undoheaderData = list(sortInfo.headerData)
    df = undoRedoInfo.redoDF
    sortInfo.headerData = list(sortInfo.undoheaderData)
    write_dt_to_qTable(df, table)
    ui.menu_undo.setEnabled(True)
    ui.menu_redo.setEnabled(False)

def showAbout():
    uiDiag.show()

# Show error message
def errorMessage(text: str, title: str):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    retval = msg.exec()

def confirmDrop(text: str, title: str):
    global df
    global table
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setText(text)
    msg.setWindowTitle(title)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)    
    retval = msg.exec()
    if retval == 1024:
        try:
            setUndo(df, undoRedoInfo.undoDF)
            df.drop(columns=[df.columns[activeColumn]], inplace=True)
            write_dt_to_qTable(df, table)
            sortInfo.headerData.pop(activeColumn)
        except:
            pass

def showTrimWindow():
    uiTrimWindow.show()

    if len(trimInfo.trimText) > 20:
        trimInfo.trimTextShort = trimInfo.trimText[:20]
        trimLabel.setText(trimInfo.trimTextShort + "...")
    else:
        trimInfo.trimTextShort = trimInfo.trimText
        trimLabel.setText(trimInfo.trimTextShort)

    
    trimSlider.setRange(0, len(trimInfo.trimTextShort))
    trimSlider.setValue(0)
    trimInfo.isRight = False
    trimRadioLeft.setChecked(True)

def slideChange(text: str, value: int):
    txt = text
    if trimInfo.isRight == False:
        txtTail = text[value:]
        txtHead = text[:-len(text) + value]
        print(value)
    elif trimInfo.isRight == True:
        txtTail = text[value:]
        txtHead = text[:len(text) + value]
        print(value)

    if trimInfo.isRight == False:
        if value == len(text):
            if len(trimInfo.trimText) > 20:
                trimLabel.setText(f"<span style='color: red'>{text}</span>...")
            else:
                trimLabel.setText(f"<span style='color: red'>{text}</span>")
        else:
            if len(trimInfo.trimText) > 20:
                trimLabel.setText(f"<span style='color: red'>{txtHead}</span>{txtTail}...")
            else:
                trimLabel.setText(f"<span style='color: red'>{txtHead}</span>{txtTail}")
    elif trimInfo.isRight == True:
        if value == -len(text):
            if len(trimInfo.trimText) > 20:
                trimLabel.setText(f"...<span style='color: red'>{text}</span>")
            else:
                trimLabel.setText(f"<span style='color: red'>{text}</span>")
        elif value == 0:
            if len(trimInfo.trimText) > 20:
                trimLabel.setText(f"...<span style='color: black'>{text}</span>")
            else:
                trimLabel.setText(f"<span style='color: black'>{text}</span>")
        else:
            if len(trimInfo.trimText) > 20:
                trimLabel.setText(f"...<span style='color: black'>{txtHead}</span><span style='color: red'>{txtTail}</span>")
            else:
                trimLabel.setText(f"<span style='color: black'>{txtHead}</span><span style='color: red'>{txtTail}</span>")

def commitTrim(value: int):
    global activeColumn
    global df
    if trimInfo.isRight == False:
        setUndo(df, undoRedoInfo.undoDF)
        trimCol = df.iloc[:,activeColumn].astype(str)
        df.iloc[:,activeColumn] = trimCol.str[value:]
        write_dt_to_qTable(df, table)
        uiTrimWindow.close()
        print(trimInfo.trimText[value:])
    elif trimInfo.isRight == True:
        setUndo(df, undoRedoInfo.undoDF)
        trimCol = df.iloc[:,activeColumn].astype(str)
        df.iloc[:,activeColumn] = trimCol.str[:value]
        write_dt_to_qTable(df, table)
        uiTrimWindow.close()
        print(trimInfo.trimText[value:])

def closeTrimWindow():
    uiTrimWindow.close()

def openNullWindow():
    uiNullWindow.show()

def closeNullWindow():
    uiNullWindow.close()

def commitNullValues():
    global df
    setUndo(df, undoRedoInfo.undoDF)
    if nullInfo.isCustom1 == True:        
        if not nullInfo.isIgnore1:
            for col in df:
                if df[col].dtypes in ("int", "float"):
                    df[col] = df[col].fillna(int(uiNullWindow.txtCustom.text()))
                    df[col] = df[col].astype('float64', copy=False, errors='ignore')
    elif nullInfo.isCustom1 == False:
        if not nullInfo.isIgnore1:
            for col in df:
                if df[col].dtypes in ("int", "float"):
                    df[col] = df[col].fillna(str(nullInfo.nullVal1))
                    df[col] = df[col].astype('float64', copy=False, errors='ignore')
    if nullInfo.isCustom2 == True:
        if not nullInfo.isIgnore2:
            for col in df:
                if df[col].dtypes in ("str", "object"):
                    df[col] = df[col].fillna(str(uiNullWindow.txtCustom2.text()))

    elif nullInfo.isCustom2 == False:
        if not nullInfo.isIgnore2:
            for col in df:
                if df[col].dtypes in ("str", "object"):
                    df[col] = df[col].fillna(str(nullInfo.nullVal2))

    write_dt_to_qTable(df, table)
    uiNullWindow.close()

def quitApp():
    sys.exit(0)

def selectPage(fName: str):
    global dfPage
    global pageTable
    global pageNum
    global numberOfPages
    global excelFile
    pageNum = 0
    uiPageSelect.show()
    # Store the excel filename as a global var
    excelFile = fName
    xls = pd.ExcelFile(excelFile)
    numberOfPages = len(xls.sheet_names)
    # Read in the excel file and get the sheet name based off
    # xls's index to pageNum
    dfPage = pd.read_excel(excelFile, sheet_name=xls.sheet_names[pageNum])
    write_dt_to_pageSelect(dfPage, pageTable)
    uiPageSelect.lblPageNum.setText(f"Page {pageNum + 1}")

def changePage(isBack: bool = False):
    global pageNum
    global dfPage
    global numberOfPages
    global excelFile
    try:
        if isBack == False:
            if pageNum < numberOfPages - 1:
                pageNum = pageNum + 1
                # Have to create a new xls item here
                # so we can access page names.
                xls = pd.ExcelFile(excelFile)
                dfPage = pd.read_excel(excelFile, sheet_name=xls.sheet_names[pageNum])
                dfPage.fillna('', inplace=True)
                write_dt_to_pageSelect(dfPage, pageTable)
                uiPageSelect.lblPageNum.setText(f"Page {pageNum + 1}")
        else:
            if pageNum > 0:
                pageNum = pageNum - 1
                # Have to create a new xls item here
                # so we can access page names.
                xls = pd.ExcelFile(excelFile)
                dfPage = pd.read_excel(excelFile, sheet_name=xls.sheet_names[pageNum])
                dfPage.fillna('', inplace=True)
                write_dt_to_pageSelect(dfPage, pageTable)
                uiPageSelect.lblPageNum.setText(f"Page {pageNum + 1}")
    except:
        print("null value")

def openPage():
    global df
    global dfPage
    uiPageSelect.close()
    # Store the contents of dfPage into the primary
    # df object and write it to the table.
    df = dfPage
    write_dt_to_qTable(df, table)
    toggleItems(True)
    headers = list(df)
    sortInfo.populateLists(headers)
    trimInfo.trimText = ui.tableWidget.item(0, activeColumn).text()
    
    ui.btnRename.setEnabled(True)

def openFile():
    global table
    global df
    global fileLoaded
    try:
        filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Dir', desktopLoc, "CSV or Excel files (*.csv *.xlsx)")[0]
    except:
        print("No file found")
    if filename:
        if ".csv" in filename:
            try:
                df = createDF(filename)
                write_dt_to_qTable(df, table)
                fileLoaded = True
                toggleItems(True)
                headers = list(df)
                sortInfo.populateLists(headers)
                trimInfo.trimText = ui.tableWidget.item(0, activeColumn).text()
            except:
                errorMessage("Error opening file", "Error")
        if ".xlsx" in filename:
            xls = pd.ExcelFile(filename)
            # If the length of the excel file is 1 just
            # load that into the DF
            if len(xls.sheet_names) == 1:
                df = createDF(filename)
                df.fillna('', inplace=True)
                write_dt_to_qTable(df, table)
                fileLoaded = True
                toggleItems(True)
                headers = list(df)
                sortInfo.populateLists(headers)
                trimInfo.trimText = ui.tableWidget.item(0, activeColumn).text()
            # If there are more than 1 page in the excel file
            # we then run it through the select page screen
            elif len(xls.sheet_names) > 1:
                selectPage(filename)
            else:
                print("Empty Excel file")
    else:
        print("Empty filename")

def write_dt_to_qTable(df: pd.DataFrame, table: QtWidgets.QTableWidgetItem):
    global fileLoaded
    fileLoaded = False
    headers = list(df)    
    table.setRowCount(df.shape[0])
    table.setColumnCount(df.shape[1])
    table.setHorizontalHeaderLabels(headers)

    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            table.setItem(row, col, QtWidgets.QTableWidgetItem(str(df_array[row,col])))
    fileLoaded = True

def write_dt_to_pageSelect(df: pd.DataFrame, pageTable: QtWidgets.QTableWidgetItem):
    headers = list(df)
    pageTable.setRowCount(df.shape[0])
    pageTable.setColumnCount(df.shape[1])
    pageTable.setHorizontalHeaderLabels(headers)
    df_array = df.values
    for row in range(df.shape[0]):
        for col in range(df.shape[1]):
            pageTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(df_array[row,col])))
    
def saveFile():
    global dfNew
    try:
        filename = QtWidgets.QFileDialog.getSaveFileName(None, 'Save File', desktopLoc, "CSV Files(*.csv)")[0]
        print(filename)
        df.to_csv(str(filename), index=False)
    except:
        pass

def checkForUpdates():
    check = updateCheck.checkUpdates(versionNumber)
    if not check:
        #ui.lblUpdate.setText('<a href="https://github.com/cityofaustin/Data-Preparation-Tool/releases">New Version Available. Click here to download.</a>')
        ui.lblUpdate.setText("<a href=\"https://github.com/cityofaustin/Data-Preparation-Tool/releases\">New Version Available. Click here to download.</a>")
def iconFromBase64(base64: bytes) -> QtGui.QIcon:
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    icon = QtGui.QIcon(pixmap)
    return icon

def imageFromBase64(base64: bytes) -> QtGui.QPixmap:
    pixmap = QtGui.QPixmap()
    pixmap.loadFromData(QtCore.QByteArray.fromBase64(base64))
    return pixmap

def closeAbout():
    uiDiag.close()
    
def toggleItems(bool: bool):
    uiToggleItems = [ui.menu_save, ui.menu_trim,
    ui.actionTrim_digits, ui.menu_nullVals,
    ui.btnDropCol, ui.btnRename, ui.menu_desc, ui.menu_info]

    if bool:
        for item in uiToggleItems:
            item.setEnabled(True)
    else:
        for item in uiToggleItems:
            item.setEnabled(False)

def loadData():
    try:
        if platName == 'Darwin':
            readDat(f'{appPath}/res.dat')
        else:
            readDat(f'{resPath}/res.dat')
        
        app.setWindowIcon(iconFromBase64(bytes(iconDict['icon.png'], encoding='utf8')))
        ui.menu_openFile.setIcon(iconFromBase64(bytes(iconDict['folder.png'], encoding='utf8')))
        ui.menu_trim.setIcon(iconFromBase64(bytes(iconDict['trimIcon.svg'], encoding='utf8')))
        ui.menu_save.setIcon(iconFromBase64(bytes(iconDict['saveIcon.svg'], encoding='utf8')))
        ui.menu_undo.setIcon(iconFromBase64(bytes(iconDict['undo.png'], encoding='utf8')))
        ui.menu_redo.setIcon(iconFromBase64(bytes(iconDict['redo.png'], encoding='utf8')))
        uiDiag.pixLogo.setPixmap(imageFromBase64(bytes(iconDict['logo.png'], encoding='utf8')))
        ui.menu_nullVals.setIcon(iconFromBase64(bytes(iconDict['null.png'], encoding='utf8')))
        ui.menu_help.setIcon(iconFromBase64(bytes(iconDict['help.png'], encoding='utf8')))
        ui.menu_desc.setIcon(iconFromBase64(bytes(iconDict['desc.png'], encoding='utf8')))
        ui.menu_info.setIcon(iconFromBase64(bytes(iconDict['info.png'], encoding='utf8')))
        ui.btnSort.setIcon(iconFromBase64(bytes(iconDict['sort.png'], encoding='utf8')))
    except:
        errorMessage('Could not load res.dat\nApplication will still run without graphical icons and logos.', 'Error')
        uiDiag.pixLogo.setText("Data Preparation Tool")

# Set up the window objects        
ui = mainWindow()
uiDiag = aboutWindow()
uiPageSelect = pageSelect()
uiTrimWindow = trimWindow()
uiNullWindow = nullWindow()
uiRenameCol = renameColumn()
uiDesc_Info = desc_infoWindow()
uiTypeWindow = typeWindow()

# Variables
table = ui.tableWidget
pageTable = uiPageSelect.tblPage
trimSlider = uiTrimWindow.horizontalSlider
trimLabel = uiTrimWindow.label
trimRadioLeft = uiTrimWindow.radioLeft

# Load in the image data from res.dat
loadData()
# Do an update check
checkForUpdates()

ui.tableWidget.horizontalHeader().setDefaultAlignment(QtCore.Qt.AlignLeft)
# Show main window and exec the program
toggleItems(False)
ui.show()
app.exec()