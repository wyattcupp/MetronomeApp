"""
Wyatt Cupp
wyattcupp@gmail.com

"""

from tkinter import *
from winsound import Beep


class Metronome:
    """
    Class representing a Metronome object.

    Attributes:
        root (Tk): The Tk() instance object (root frame)
        time_sig (tuple): the tuple used to store the various time signatures
        start (bool): the boolean used to specify an on / off state of the metronome
        bpm (int): beats per minute attribute of the metronome
        beats_per_measure (int): the amount of beats for each measure
        time_interval (int): the ms between metronome beeps
        _beat_count (int): how many current beats have taken place in a given measure
        s_var (StringVar): variable string that references the counter label (used to update counter label)
    """

    def __init__(self, root, time_sig):
        """
        Constructor - sets up default attribute values and calls the _app_interface method to create the GUI.
        :param root: the root panel (Tk)
        :param time_sig: the tuple containing valid time signatures
        """
        self.root = root
        self.time_sig = time_sig
        self.start = False
        self.bpm = 0
        self.beats_per_measure = 0
        self.time_interval = 0  # in ms
        self._beat_count = 0
        self.s_var = StringVar()
        self.s_var.set(self._beat_count)

        self._app_interface()

    def _app_interface(self):
        """
        Sets up the tkinter GUI interface for the app
        :return: void
        """
        frame = Frame(self.root)
        frame.pack()

        bpm_entry = Entry(frame, width=8, justify=CENTER)
        bpm_entry.grid(row=0, column=0, padx=10, sticky='E')
        bpm_entry.insert(0, '60')

        bpm_label = Label(frame, text='BPM:')
        bpm_label.grid(row=0, column=0, sticky='W')

        spinbox = Spinbox(frame, width=6, values=self.time_sig, wrap=True)
        spinbox.grid(row=0, column=1, sticky='E')

        spin_label = Label(frame, text='Time:')
        spin_label.grid(row=0, column=1, sticky='W')

        counter_lbl = Label(frame, textvariable=self.s_var, font=('Arial', 34))
        counter_lbl.grid(row=1, columnspan=2)

        start_button = Button(frame, text='Start', font=('Arial', 12), width=8, height=2,
                              command=lambda: self.check_start(bpm_entry, spinbox))
        start_button.grid(row=2, column=0, padx=5, pady=5, sticky='W')

        stop_button = Button(frame, text='Stop', font=('Arial', 12), width=8, height=2,
                             command=lambda: self._stop_metronome())
        stop_button.grid(row=2, column=1, padx=5, pady=5, sticky='E')

    def check_start(self, entry: Entry, spinbox: Spinbox):
        """
        Command linked to the 'Start' button. Checks if start boolean is false, if so,
        invokes the self._start_metronome command to invoke counter
        :param entry:
        :param spinbox:
        :return: void
        """
        if not self.start:
            try:
                self.bpm = int(entry.get())
                if self.bpm > 300 and (int(spinbox.get()[0])) != 6:
                    self.bpm = 300
                    entry.delete(0, last=END)
                    entry.insert(0, '300')
                elif self.bpm > 200 and (int(spinbox.get()[0])) == 6:
                    self.bpm = 200
                    entry.delete(0, last=END)
                    entry.insert(0, '200')
            except ValueError:
                self.bpm = 60  # default bpm is set
            self.start = True
            self._start_metronome(spinbox)

    def _start_metronome(self, spinbox: Spinbox):
        """
        Starts the metronome, calculates the beats per measure for each call, in the case that the
        time_signature spinbox tuple is changed while running. This method may be updated in the future to
        avoid over-calculating the time intervals.
        :param spinbox:
        :return:
        """
        if self.start:

            self.beats_per_measure = int(spinbox.get()[0])

            if self.beats_per_measure == 6:
                self.time_interval = int((60 / (self.bpm * 2) - 0.1) * 1000)
            else:
                self.time_interval = int((60 / self.bpm - 0.1) * 1000)

            self._beat_count += 1
            self.s_var.set(self._beat_count)
            if self._beat_count == 1:  # on-beat
                Beep(900, 100)  # 100ms -> must subtract 100ms delay from time_interval
            elif self._beat_count >= self.beats_per_measure:
                self._beat_count = 0
                Beep(440, 100)
            else:
                Beep(440, 100)
            self.root.after(self.time_interval, lambda: self._start_metronome(spinbox))

    def _stop_metronome(self):
        self.start = False


def main():
    root = Tk()
    root.title('Metronome')
    # root.geometry('{}x{}'.format(220, 120))

    time_signatures = ('4/4', '2/4', '3/4', '6/8')  # tuple with valid time signatures
    Metronome(root, time_signatures)

    root.mainloop()


if __name__ == '__main__':
    main()
