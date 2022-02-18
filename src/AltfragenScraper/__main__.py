"""
TODO: Write introduction into Logbox, would be sick as hell. Only thing I'm worried about it is that
users might be confused as to why the instructions suddenly disappear off the screen... Maybe I'll have
to implement a more sophisticated version of print_data lol
TODO: Create custom configuration for how answered/unanswered questions should be displayed in
"""

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s -  %(levelname)s - %(message)s', datefmt='%H:%M:%S')
from traceback import format_exc
from threading import Thread
from itertools import cycle
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from selenium.common.exceptions import WebDriverException
import webbrowser
import scraper
from scraper import data, data_order

class Interface(tk.Tk):
    # Just a couple of strings whose exact states are important
    STR_CLOSE_BROWSER = 'Browser schließen'
    STR_OPEN_BROWSER = 'Browser öffnen'
    def __init__(self):
        """
        Initializes the Tkinter window.
        The window is set up to contain three frames:
        - The browser frame, which allows us to start Selenium and select which browser to start it on.
          Button changes from "Browser starten" to "Browser stoppen"
        - The Logbox frame, which contains information about how to proceed with the program at first, 
          then turns into a visual representation of what's saved in data.
          Also contains a label to make the logbox's name known
        - Save frame contains the "Save to file" button which is to be used after the program is run.
          Also contains a small label at the bottom, which changes text when /mod/quiz/summary is opened in the browser,
          indicating that the exam is over and that the user likely wants to save their progress.

        Attributes not inherited from TK:
        - self.btn_browser (ttk.Button)
        - self.btn_browser_text (StringVar)
        - self.logbox (ttk.Text)
        - self.btn_save (ttk.Button)
        - self.lbl_browser_status_text (StringVar)
        """
        super().__init__()
        self.title = "Altfragen Scraper"

        # Attributes
        self.exam_url = 'http://moodle.univie.ac.at/'

        # Starting strings
        save_text = "Noch keine Fragen"
        browser_status_text = "Browser Status: Nicht gestartet"
        introduction = """Introductory Paragraph 1
Introductory Paragraph 2
Introductory Paragraph 3"""  # Shown in logbox at startup

        # Window
        self.minsize(500, 300)
        self.grid_columnconfigure(1, weight=1)  # Enable horizontal resizing of logbox
        self.grid_rowconfigure(0, weight=1)

        # Browser selection frame
        frm_browser = tk.Frame(self)
        frm_browser.grid(row=0, column=0, sticky='nw', padx=(10, 0), pady=10)

        ttk.Label(frm_browser, text='Wähle Browser'
            ).grid(row=0, column=0, sticky='w', pady=(3,0))

        self.choice_browser = tk.StringVar(frm_browser, 'firefox')

        ttk.Radiobutton(frm_browser, text='Firefox', variable=self.choice_browser, value='firefox', state='normal'
            ).grid(row=1, column=0, pady=(3, 0), sticky='w')
        ttk.Radiobutton(frm_browser, text='Chrome', variable=self.choice_browser, value='chrome'
            ).grid(row=2, column=0, pady=(3, 0), sticky='w')
        
        self.btn_browser_text = tk.StringVar(frm_browser, self.STR_OPEN_BROWSER)
        self.btn_browser = ttk.Button(frm_browser, textvariable=self.btn_browser_text, command=self.on_btn_browser_click)
        self.btn_browser.grid(row=3, rowspan=1, column=0, pady=3, sticky='ew')
        
        # Save Dialogue
        frm_save = tk.Frame(self)
        frm_save.grid(row=1, column=0, padx=(10,0), pady=10, sticky='s')

        self.btn_save = ttk.Button(frm_save, text='Altfragen speichern', command=placeholder)
        self.btn_save.grid(row=1, column=0, sticky='ew')
        
        self.lbl_save_text = tk.StringVar(frm_save, save_text)
        ttk.Label(frm_save, textvariable=self.lbl_save_text, font=('TkTextFont', 8), foreground='#484848'
            ).grid(row=0, column=0, padx=5)

        # Logbox Wrapper containing Label, Browser Status, and Logbox + Scrollbar
        frm_logbox_wrapper = tk.Frame(self)
        frm_logbox_wrapper.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        frm_logbox_wrapper.columnconfigure(1, weight=1)
        frm_logbox_wrapper.rowconfigure(1, weight=1)

        ttk.Label(frm_logbox_wrapper, text='Log/Altfragen'
            ).grid(row=0, column=0, sticky='w', pady=(0, 3))
        
        self.lbl_browser_status_text = tk.StringVar(frm_logbox_wrapper, browser_status_text)
        ttk.Label(frm_logbox_wrapper, textvariable=self.lbl_browser_status_text, foreground=('#505050')
            ).grid(row=0, column=1, padx=20, pady=(0,5), sticky='e')
        
        # Logbox + Scrollbar
        frm_logbox = tk.Frame(frm_logbox_wrapper)
        frm_logbox.grid(row=1, column=0, columnspan=2, sticky='nsew')

        self.logbox = tk.Text(frm_logbox, wrap='word', font=('Helvetica', 10), borderwidth=10, relief=tk.FLAT)  # Border creates illusion of padding inside text box
        self.logbox.grid(row=1, sticky='nsew')
        self.logbox.insert(0.0, introduction)
        self.logbox['state'] = 'disabled'

        logbox_scrollbar = ttk.Scrollbar(frm_logbox, orient='vertical', command=self.logbox.yview)
        self.logbox.configure({'yscrollcommand': logbox_scrollbar.set})
        logbox_scrollbar.grid(column=1, row=1, sticky = 'ns')

        frm_logbox.grid_rowconfigure(0, weight=0)  # Disable resizing of label
        frm_logbox.grid_rowconfigure(1, weight=1)  # Enable vertical resizing of logbox + scrollbar
        frm_logbox.grid_columnconfigure(0, weight=1)  # Enables horizontal resizing of logbox

        self.logbox.mark_set('end_of_questions', 4.0)  # As the Introduction text is replaced by the questions once they're registered
        self.logbox.mark_set('error_log', 5.0)


    def print_data(self):
        """
        Clears the logbox and inserts all gathered questions, then resets the user's position inside the
        logbox to what it had been before clearing it.txt
        Potential TODO: Add different ways of visualizing selected questions vs unselected questions; if
        I wanna go real crazy, maybe even include a config box to add your own syntax.
        """
        string = ''
        ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

        for i, id in enumerate(data_order):
            question = data[id]
            index = i + 1  # Since enumerate starts at 0

            # Prints question
            string += "{}. {}\n".format(index, question['question'])
            
            for i, answer in enumerate(question['answers']):
                # Prints answer as two different strings depending on whether answer was selected or not
                if question['is_selected'][i] is True:
                    string += "{}.*{}\n".format(ALPHABET[i], answer)
                else:
                    string += "{}. {}\n".format(ALPHABET[i], answer)
                
            string += '\n'
        
        # Inserts new string, gets rid of the old, and resets the screen to the same place it was before
        yview = self.logbox.yview()

        self.logbox['state'] = 'normal'
        self.logbox.delete(0.0, 'end_of_questions')
        self.logbox.insert(0.0, string[:-2])  # -2 since last \n is meant to be omitted from string
        self.logbox['state'] = 'disabled'

        self.logbox.yview_moveto(yview[0])


    def log(self, string):
        """Sends a string to self.txt_log; important to note: self.print_data() will overwrite what's in log every time it's run"""
        self.logbox['state'] = 'normal'
        self.logbox.insert(tk.END, return_breakline(self.logbox.winfo_width()) + string)
        self.logbox.yview_moveto(5000.0)  # 'end' doesn't work here for some reason, so I just went for a really high number.
        self.logbox['state'] = 'disabled'

    def log_traceback(self):
        str_traceback = format_exc()
        logging.critical('Webdriver issue:\n' + str_traceback)
        self.status('Fehler')
        self.log(str_traceback)

    
    def status(self, string):
        string = 'Browser Status: ' + string
        self.lbl_browser_status_text.set(string)
        logging.debug(string)
        
        if '...' in string:
            self._animate_trailing_commas_dots = cycle(('   ', '.  ', '.. ', '...'))
            self._animate_trailing_commas(string)

    def _animate_trailing_commas(self, string):
        """Animates trailing commas in the status"""
        if '...' in string:
            string = string[:-3]  # Removes the trailing commas

        dots = next(self._animate_trailing_commas_dots)

        if string in self.lbl_browser_status_text.get():  # Abort the loop when new browser status
            self.lbl_browser_status_text.set(string + dots)
            self.after(750, lambda: self._animate_trailing_commas(string))


    def on_btn_browser_click(self):
        """Figures out which state the browser is in and starts the relevant processes"""
        if self.btn_browser_text.get() == self.STR_OPEN_BROWSER:
            self.selenium_run()
            self.btn_browser_text.set(self.STR_CLOSE_BROWSER)

        elif self.btn_browser_text.get() == self.STR_CLOSE_BROWSER:
            self.driver.quit()
            self.btn_browser_text.set(self.STR_OPEN_BROWSER)


    def selenium_run(self):
        """Starts driver in thread so as to ensure responsiveness of Interface"""
        threadObj = Thread(target=self._selenium_run)
        threadObj.start()

    def _selenium_run(self):
        """Runs selenium, handles errors"""
        try:
            self.status('Startet...')
            self.driver = scraper.get_selenium(self.choice_browser.get())

            scraper.scrape(self.driver, self)
        except:
            # Checks whether Selenium window was closed. Since this is typically done by a user, it returns a less-threatening
            # warning message if so. If the driver is still alive, it returns a more threatening warning message, since the driver
            # isn't logging anything anymore.
            if self.driver_is_alive():
                self.on_driver_crash()
            else:
                self.status("Unerwartet geschlossen")
                self.btn_browser_text.set(self.STR_OPEN_BROWSER)
                logging.critical(format_exc)

    def driver_is_alive(self):
        """Checks whether the Selenium window has been closed"""
        try: 
            self.driver.current_url  # Throws up an exception when browser is closed
        except WebDriverException:
            return False 
        return True

    
    def data_listener(self):
        """Checks whether there are values in data and enables the 'Altfragen Speichern' button if so"""
        if data:
            self.btn_save['state'] = 'normal'
        else:
            self.after(1000, self.data_listener)

    
    def has_finished(self):
        self.status('Bereit zu speichern!')

        self.log(return_breakline(self.logbox.winfo_width()))
        self.log('Nun gerne auf "Altfragen Speichern" klicken; den Browser kannst du ohne Gefahr schließen!', mark='end_of_questions')

    
    def on_driver_crash(self):
        """When selenium throws up an error, quit selenium and ask user whether to continue on Selenium or open in normal browser. 
        If user chooses normal browser, the exact URL of the exam will be opened."""
        self.log_traceback()
        self.driver.quit()

        return_val = messagebox.YESNOCANCEL(text="""Huch! Der Browser ist abgestürzt! Aber keine Panik, alle Antworten sind auf Moodle gespeichert!
Möchtest du's nochmal mit dem AltfragenScraper probieren? (Wenn du auf "Nein" klickst, wird dein Standardbrowser gestartet)""")

        if return_val is True:
            self.selenium_run()
        elif return_val is False:
            webbrowser.open(self.exam_url)


def return_breakline(width):
    """Returns a line of ------- corresponding to the width of the logbox in order to visually break text apart"""
    width = width-24  # 20 since padx=10, 4 because... well, I don't know, some weird default padding in the textbox
    count = round(width/8)  # One - character takes up 8 pixels, hence pixels/8
    return '\n' + '-'*count + '\n'


def placeholder():
    print("This is a placeholder")


def main():
    global root

    root = Interface()
    root.print_data()
    root.mainloop()


if __name__ == '__main__':
    main()
