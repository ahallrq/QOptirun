#!/usr/bin/python3

import sys, os, subprocess

from PyQt5.QtWidgets import QApplication

from ui.mainwin import MainWindow

def main():
    mw = MainWindow(app)
    mw.show()
    return app.exec_()

def error_message(msg, error = True):
    if os.path.isfile("/usr/bin/kdialog"):
        if (error):
            errtype = "--error"
        else:
            errtype = "--sorry"
        subprocess.call(['/usr/bin/kdialog', errtype, msg])
    elif os.path.isfile("/usr/bin/zenity"):
        if (error):
            errtype = "--error"
        else:
            errtype = "--warning"
        subprocess.call(['/usr/bin/zenity', errtype, "--text=" + msg])
    else:
        if (error):
            errtype = "ERROR:"
        else:
            errtype = "WARN:"
        print(errtype, msg)

if __name__ == "__main__":
    
    if sys.platform != "linux" and sys.platform != "linux2":
        error_message("This application is only useful on Linux-based operating systems. It will not work on Mac OSX or Windows.")
        sys.exit()
    optirun_available = False
    for path in ["/usr/bin/optirun", "/usr/local/bin/optirun", "/bin/optirun", "/opt/bin/optirun", "/sbin/optirun"]:
        if os.path.isfile(path):
            optirun_available = True
    if optirun_available == False:
        error_message("Optirun must be installed for this application to work. It is usually in the \"bumblebee\" package in most distros.")
        sys.exit()
    app = QApplication(sys.argv)
    main()
    sys.exit()

# TODO:
# x Add check for Windows/Mac
# x Add check for optirun
# x Complete config file
# * Complete presets
# * Possibly add nohup support
# * Fix that weird pixmap issue
# * Add custom binaries for applications without a .desktop file