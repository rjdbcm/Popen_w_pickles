import pickle
import time
import sys
import io


class SubProgram(object):
    def __init__(self):
        self.flags = self.read_flags()
        self.flags['flt'] = .25
        self.io_flags()
        time.sleep(3)
        self.flags['flt'] = .5
        self.io_flags()
        time.sleep(3)
        self.flags['flt'] = .75
        self.io_flags()
        time.sleep(3)
        self.flags['flt'] = 1.0
        self.flags['done'] = True
        self.io_flags()
        time.sleep(3)

        self.flags = self.read_flags()


    def io_flags(self):
        self.send_flags()
        self.flags = self.read_flags()

    def speak_flags(self, flags):
        sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='latin-1')
        d = pickle.dumps(flags)
        print(d.decode('latin-1'), end='', flush=True)

    def send_flags(self):
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