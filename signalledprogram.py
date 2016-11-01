import os
import subprocess

from PyQt5.QtCore import QThread, pyqtSignal


class SignalledProgram(QThread):

    #program_closed = pyqtSignal(object, object, object, object)
    program_closed = pyqtSignal()

    def __init__(self, program_name, program_path, program_args, optirun_bridge, optirun_vglcompress):
        QThread.__init__(self)

        self.program_name = program_name
        self.program_path = program_path
        self.program_args = program_args
        self.optirun_bridge = optirun_bridge
        self.optirun_vglcompress = optirun_vglcompress

    def run(self):
        progarr = [self.program_path] + self.program_args
        progstr = " ".join(str(x) for x in progarr)

        optiarr = ["optirun"]

        if self.optirun_bridge != "Default":
            optiarr.append("-b")
            optiarr.append(self.optirun_bridge.lower())

        if self.optirun_vglcompress != "Default":
            optiarr.append("-c")
            optiarr.append(self.optirun_vglcompress.lower())

        optirunprogarr = optiarr + progarr
        print(optirunprogarr)

        print("Attempting to run program: {}".format(progstr))
        print("Optirun bridge:", self.optirun_bridge)
        print("VirtualGL compression method (if available):",
              self.optirun_vglcompress)
        self.proc = subprocess.Popen(optirunprogarr)
        signal = self.proc.wait()
        if signal == -9:  # SIGKILL
            print("Process terminated with extreme prejudice: {}".format(progstr))
        else:
            print("Process ended: {}".format(progstr))
        self.program_closed.emit()

    def end(self, kill=False):
        if kill:
            self.proc.kill()
        else:
            self.proc.terminate()
