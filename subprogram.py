import pickle
from datetime import datetime
import time
from flags import FlagIO
import sys
import io


class SubProgram(FlagIO):
    def __init__(self):
        FlagIO.__init__(self)  # Old-school inheritance

        self.flags = self.read_flags()
        while self.flags['progress'] < 1.0 and self.flags['kill'] == False:
            time.sleep(.1)
            self.io_flags()
            self.flags['progress'] += .01
        else:
            self.flags['done'] = True
            self.io_flags()

    def io_flags(self):
        self.send_flags()
        self.flags = self.read_flags()
        print(self.READ_MSG.format(datetime.now(), type(self).__name__, self.read_flags()))

if __name__ == "__main__":
    SubProgram()