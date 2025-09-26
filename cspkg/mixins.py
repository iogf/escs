class IdleEvent:
    def __init__(self, widget):
        self.widget.bind('<<Data>>', self.on_data, add=True)
        self.widget  = widget
        self.timeout = 1200
        self.funcid  = ''

    def on_data(self, event):
        # Make sure self.funcid is initialized before calling after_cancel.
        # The idea here it is to have <<idle>> spawned once when the user
        # stopped typing.

        if self.funcid:
            self.widget.after_cancel(self.funcid)
        self.funcid = self.widget.after(self.timeout, self.send_idle)

    def send_idle(self):
        self.widget.event_generate('<<Idle>>')

class DataEvent:
    def __init__(self, widget):
        self.widget = widget
        self.widget.bind('<Key>', self.dispatch_data, add=True)

    def dispatch_data(self, event):
        if event.char:
            self.widget.event_generate('<<Data>>')


