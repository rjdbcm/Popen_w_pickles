from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import subprocess
import pickle
import time
import sys



# Subclassing QThread
# http://qt-project.org/doc/latest/qthread.html
class AThread(QThread):
    def __init__(self, proc, flags):
        super(AThread, self).__init__()
        self.flags = flags
        self.send_flags()
        self.proc = proc

    def send_flags(self):
        print("Flags Send:\n{}".format(self.flags))
        with open(r".flags.pkl", "wb") as outfile:
            pickle.dump(self.flags, outfile)

    def read_flags(self):
        with open(r".flags.pkl", "rb") as inpfile:
            flags = pickle.load(inpfile)
        if flags:
            self.flags = flags
            return(self.flags)

    def run(self):
        count = 0
        while self.proc.poll() is None:  # While the process is running read flags
            if not self.read_flags()['done'] or self.read_flags()['killed']:
                time.sleep(1)
                print("{}. Flags Read:".format(count))
                print(self.read_flags())
                count += 1


def using_q_thread():
    app = QCoreApplication([])
    o = {'kill': False, 'done': False, 'killed': False, "flt": 0.2}
    p = subprocess.Popen([sys.executable, "subprogram.py"], stdout=subprocess.PIPE)
    thread = AThread(p, o)
    thread.finished.connect(app.exit)
    thread.start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    using_q_thread()

