import os
import shlex
import time

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QComboBox, QFileDialog, QFrame,
                             QHBoxLayout, QLineEdit, QMainWindow, QMenu,
                             QProgressBar, QPushButton, QTabWidget,
                             QToolButton, QTreeWidget, QTreeWidgetItem)

from appsgen import genapplist
from res.ui.qoptirun import Ui_MainWindow
from signalledprogram import SignalledProgram
from configfile import ConfigFile


class MainWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        Ui_MainWindow().setupUi(self)
        self.app = app

        self.conf = ConfigFile(os.path.join(os.path.expanduser("~"), ".config/qoptirun/config.json"), "r+")

        terminate_btnmenu = QMenu()
        terminate_btnmenu.addAction('Kill', self.killProgram)
        self.findChild(QToolButton, "program_terminate").setMenu(
            terminate_btnmenu)

        tabs = {"applications" : 0, "presets" : 1}
        tab = self.conf.get_option("last_tab").lower()
        if tab in tabs:
            self.findChild(QTabWidget, "programs_tabwidget").setCurrentIndex(tabs[tab])

        bridges = {"default" : 0, "none" : 1, "virtualgl" : 2, "primus" : 3}
        bridge = self.conf.get_option("last_bridge").lower()
        if bridge in bridges:
            self.findChild(QComboBox, "optirun_bridge").setCurrentIndex(bridges[bridge])

        compressmethods = {"default" : 0, "proxy" : 1, "rgb" : 2, "yuv" : 3,
                           "xv" : 4, "jpeg" : 5}
        compress = self.conf.get_option("last_vglcompress").lower()
        if compress in compressmethods:
            self.findChild(QComboBox, "optirun_vglcompress").setCurrentIndex(compressmethods[compress])

        self.populateAppList()

    def populateAppList(self):
        apps = genapplist()

        itemlist = []
        extensions = ["jpg", "jpeg", "png", "bmp", "gif", "xpm", "svg"]

        for i in apps:
            item = QTreeWidgetItem([i[0], i[1], i[2]])
            if ("/" in i[3]):
                print("Path:", i[3])
                item.setIcon(0, QIcon(i[3]))
            elif i[3].split(".")[-1] in extensions:
                print("Pixmap:", i[3])
                item.setIcon(0, QIcon("/usr/share/pixmaps/" + i[3]))
            else:
                print("Theme:", i[3])
                # TODO: Fix theme icons in /usr/share/pixmaps/ not being picked
                # up by QIcon.fromTheme()
                item.setIcon(0, QIcon.fromTheme(i[3]))

            itemlist.append(item)

        appList = self.findChild(QTreeWidget, "applications_list")
        appList.clear()
        appList.insertTopLevelItems(0, itemlist)
        appList.setCurrentItem(appList.topLevelItem(0))

    def appListSelect(self):
        appList = self.findChild(QTreeWidget, "applications_list")
        current = appList.currentItem()

        progpath = self.findChild(QLineEdit, "program_path")
        progargs = self.findChild(QLineEdit, "program_args")

        progpath.setText(current.text(1))
        progargs.setText(current.text(2))

    def presetListSelect(self):
        pass

    def runProgram(self):
        progpath = self.findChild(QLineEdit, "program_path")
        progargs = self.findChild(QLineEdit, "program_args")
        optirunbridge = self.findChild(QComboBox, "optirun_bridge")
        optirunvglcompress = self.findChild(QComboBox, "optirun_vglcompress")

        self.runningprogram = SignalledProgram("", progpath.text(), shlex.split(
            progargs.text()), optirunbridge.currentText(), optirunvglcompress.currentText())
        self.runningprogram.program_closed.connect(self.stub)
        self.blockUi()
        self.runningprogram.start()

    def termProgram(self):
        self.runningprogram.end(False)

    def killProgram(self):
        self.runningprogram.end(True)

    def blockUi(self):
        self.findChild(QTabWidget, "programs_tabwidget").setEnabled(False)
        self.findChild(QPushButton, "preset_save").setEnabled(False)
        self.findChild(QPushButton, "preset_load").setEnabled(False)
        self.findChild(QPushButton, "preset_delete").setEnabled(False)
        self.findChild(QPushButton, "program_path_browse").setEnabled(False)
        self.findChild(QLineEdit, "program_path").setEnabled(False)
        self.findChild(QLineEdit, "program_args").setEnabled(False)
        self.findChild(QComboBox, "optirun_bridge").setEnabled(False)
        self.findChild(QComboBox, "optirun_vglcompress").setEnabled(False)
        self.findChild(QPushButton, "program_run").setEnabled(False)
        self.findChild(QToolButton, "program_terminate").setEnabled(True)

    def unblockUi(self):
        self.findChild(QTabWidget, "programs_tabwidget").setEnabled(True)
        self.findChild(QPushButton, "preset_save").setEnabled(True)
        self.findChild(QPushButton, "preset_load").setEnabled(True)
        self.findChild(QPushButton, "preset_delete").setEnabled(True)
        self.findChild(QPushButton, "program_path_browse").setEnabled(True)
        self.findChild(QLineEdit, "program_path").setEnabled(True)
        self.findChild(QLineEdit, "program_args").setEnabled(True)
        self.findChild(QComboBox, "optirun_bridge").setEnabled(True)
        self.findChild(QComboBox, "optirun_vglcompress").setEnabled(True)
        self.findChild(QPushButton, "program_run").setEnabled(True)
        self.findChild(QToolButton, "program_terminate").setEnabled(False)

    def closeEvent(self, event):
        self.save_config()
        self.app.quit()
    
    def save_config(self):
        tab = self.findChild(QTabWidget, "programs_tabwidget").currentIndex()
        tabs = ["applications", "presets"]
        self.conf.set_option("last_tab", tabs[tab])
        
        bindex = self.findChild(QComboBox, "optirun_bridge").currentIndex()
        bridges = ["Default", "None", "VirtualGL", "Primus"]
        self.conf.set_option("last_bridge", bridges[bindex])

        vindex = self.findChild(QComboBox, "optirun_vglcompress").currentIndex()
        compressmethods = ["Default", "Proxy", "RGB", "YUV", "XV", "JPEG"]
        self.conf.set_option("last_vglcompress", compressmethods[vindex])

        self.conf.close()

    def stub(self):
        self.unblockUi()
