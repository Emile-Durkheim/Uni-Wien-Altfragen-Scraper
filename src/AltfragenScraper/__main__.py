"""


"""

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s -  %(levelname)s - %(message)s', datefmt='%H:%M:%S')
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import scraper

data = {}

class Window(tk.Tk):
    def __init__(self):
        """
        Initializes the Tkinter window.
        The window is set up to contain four frames:
        - The title frame to give the window some flavor
        - The browser frame, which allows us to start Selenium and select which browser to start it on.
          Changes from "Browser starten" to "Browser stoppen"
        - The Logbox frame, which contains information about how to proceed with the program at first, 
          then turns into a visual representation of what's saved in data.
          Also contains a label to make the logbox's name known
        - Save frame contains the "Save to file" button which is to be used after the program is run.
          Also contains a small label at the bottom, which changes text when /mod/quiz/summary is opened in the browser,
          indicating that the exam is over and that the user likely wants to save their progress.

        Attributes not inherited from TK:
        - self.btn_browser
        - self.btn_browser_text
        - self.logbox
        - self.btn_save
        """
        super().__init__()
        self.title = "Altfragen Scraper"

        # Attributes


        # Interface
        self.minsize(500, 300)
        self.grid_columnconfigure(1, weight=1)  # Enable horizontal resizing of logbox
        self.grid_rowconfigure(0, weight=1)


        # Browser selection frame
        frm_browser = tk.Frame(self)
        frm_browser.grid(row=0, column=0, sticky='nw', padx=(10, 0), pady=10)

        ttk.Label(frm_browser, text='Wähle Browser').grid(row=0, column=0, sticky='w', pady=(3,0))

        preferred_browser = tk.StringVar(frm_browser, 'firefox')
        ttk.Radiobutton(frm_browser, text='Firefox', variable=preferred_browser, value='firefox', state=True).grid(row=1, column=0, pady=(3, 0), sticky='w')
        ttk.Radiobutton(frm_browser, text='Chrome', variable=preferred_browser, value='chrome').grid(row=2, column=0, pady=(3, 0), sticky='w')
        
        self.btn_browser_text = tk.StringVar(frm_browser, 'Browser starten')
        self.btn_browser = ttk.Button(frm_browser, textvariable=self.btn_browser_text, command=placeholder)
        self.btn_browser.grid(row=3, rowspan=1, column=0, pady=3, sticky='ew')
        
        # Save Dialogue
        frm_save = tk.Frame(self)
        frm_save.grid(row=1, column=0, padx=(10,0), pady=10, sticky='s')

        self.btn_save = ttk.Button(frm_save, text='Altfragen speichern', state='disabled', command=placeholder)
        self.btn_save.grid(row=0, column=0, sticky='ew')
        
        self.lbl_save_text = tk.StringVar(frm_save, "Keine Altfragen vorhanden")
        ttk.Label(frm_save, textvariable=self.lbl_save_text, font=(None, 8), foreground='#484848').grid(row=1, column=0, padx=5)

        # Logbox Wrapper containing Label and Browser Status
        frm_logbox_wrapper = tk.Frame(self)
        frm_logbox_wrapper.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        frm_logbox_wrapper.columnconfigure(1, weight=1)
        frm_logbox_wrapper.rowconfigure(1, weight=1)

        ttk.Label(frm_logbox_wrapper, text='Log/Altfragen').grid(row=0, column=0, sticky='w', pady=(0, 3))
        
        self.lbl_browser_status_text = tk.StringVar(frm_logbox_wrapper, "Browser Status: Lorem Ipsum Dolor Sit Am")
        ttk.Label(frm_logbox_wrapper, textvariable=self.lbl_browser_status_text, foreground=('#505050')).grid(row=0, column=1, padx=20, pady=(0,3), sticky='e')

        # Logbox itself
        frm_logbox = tk.Frame(frm_logbox_wrapper)
        frm_logbox.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.logbox = tk.Text(frm_logbox, state='normal', wrap='word')
        self.logbox.grid(row=1, sticky='nsew')

        logbox_scrollbar = ttk.Scrollbar(frm_logbox, orient='vertical', command=self.logbox.yview)
        self.logbox.configure({'yscrollcommand': logbox_scrollbar.set})
        logbox_scrollbar.grid(column=1, row=1, sticky = 'ns')

        frm_logbox.grid_rowconfigure(0, weight=0)  # Disable resizing of label
        frm_logbox.grid_rowconfigure(1, weight=1)  # Enable vertical resizing of logbox + scrollbar
        frm_logbox.grid_columnconfigure(0, weight=1)  # Enables horizontal resizing of logbox


    def print_data(self):
        pass


    def log(self, string):
        """Sends a string to self.txt_log; important to note: self.print_data() will overwrite what's in log every time it's run"""
        self.logbox.insert('end', ('' if self.logbox.get(0.0, 'end') else '\n') + string)
        self.logbox.yview_moveto(5000.0)  # 'end' doesn't work here for some reason, so I just went for a really high number.


def placeholder():
    print("You triggered a placeholder!")
    return True

def main():
    root = Window()
    root.mainloop()

if __name__ == '__main__':
    main()
