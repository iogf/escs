import sys

class LogWrapper:
    def __init__(self):
        self.outputs = []        

    def write(self, data):
        sys.__stdout__.write(data)

        for xstr in self.outputs:
            self.pipe_data(xstr, data)

    def pipe_data(self, xstr, data):
        xstr.insert('end', data)
        xstr.see('end')

    def add_chan(self, xstr):
        self.outputs.append(xstr)

    def del_chan(self, xstr):
        self.outputs.remove(xstr)

    def flush(self):
        pass

logwrapper = LogWrapper()
sys.stdout = logwrapper
