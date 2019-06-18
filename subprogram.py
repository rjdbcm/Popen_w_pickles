import pickle
from datetime import datetime
import time
import sys
import io


class SubProgram(object):
    def __init__(self):

        while self.read_flags()['progress'] < 1.0:
            time.sleep(.1)
            self.flags['progress'] += .01
            self.io_flags()
        else:
            self.flags['done'] = True
            self.io_flags()

    def io_flags(self):
        self.send_flags()
        self.flags = self.read_flags()

    def send_flags(self):
        print("[{}] SubPrgm Flags Send: {}".format(datetime.now(), self.flags))
        with open(r".flags.pkl", "wb") as outfile:
            pickle.dump(self.flags, outfile)

    def read_flags(self):
        with open(r".flags.pkl", "rb") as inpfile:
            flags = pickle.load(inpfile)
        if flags:
            self.flags = flags
            return (self.flags)


if __name__ == "__main__":
    SubProgram()