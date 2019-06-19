from datetime import datetime
import pickle
class FlagIO(object):
    def __init__(self):
        self.READ_MSG = "[{}] {} Flags Read: {}"

    def send_flags(self):
        print("[{}] {} Flags Send: {}".format(datetime.now(), type(self).__name__, self.flags))
        with open(r"/dev/shm/.flags.pkl", "wb") as outfile:
            pickle.dump(self.flags, outfile)


    def read_flags(self):
        with open(r"/dev/shm/.flags.pkl", "rb") as inpfile:
            try:
                flags = pickle.load(inpfile)
            except EOFError:
                print("[{}] Program Flags Busy: Reusing old".format(datetime.now()))
                self.flags = flags
            self.flags = flags
            return self.flags