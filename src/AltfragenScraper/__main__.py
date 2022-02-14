"""
TODO: Write introduction into Logbox, would be sick as hell. Only thing I'm worried about it is that
users might be confused as to why the instructions suddenly disappear off the screen... Maybe I'll have
to implement a more sophisticated version of print_data lol
TODO: Create custom configuration for how answered/unanswered questions should be displayed in
"""

import logging; logging.basicConfig(level=logging.INFO, format='%(asctime)s -  %(levelname)s - %(message)s', datefmt='%H:%M:%S')
import traceback
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from selenium.common.exceptions import WebDriverException
import scraper
from scraper import data

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


        # Interface
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

        self.btn_save = ttk.Button(frm_save, text='Altfragen speichern', state='disabled', command=placeholder)
        self.btn_save.grid(row=1, column=0, sticky='ew')
        
        self.lbl_save_text = tk.StringVar(frm_save, "Noch keine Fragen")
        ttk.Label(frm_save, textvariable=self.lbl_save_text, font=(None, 8), foreground='#484848'
            ).grid(row=0, column=0, padx=5)

        # Logbox Wrapper containing Label and Browser Status
        frm_logbox_wrapper = tk.Frame(self)
        frm_logbox_wrapper.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='nsew')
        frm_logbox_wrapper.columnconfigure(1, weight=1)
        frm_logbox_wrapper.rowconfigure(1, weight=1)

        ttk.Label(frm_logbox_wrapper, text='Log/Altfragen'
            ).grid(row=0, column=0, sticky='w', pady=(0, 3))
        
        self.lbl_browser_status_text = tk.StringVar(frm_logbox_wrapper)
        ttk.Label(frm_logbox_wrapper, textvariable=self.lbl_browser_status_text, foreground=('#505050')
            ).grid(row=0, column=1, padx=20, pady=(0,5), sticky='e')
        self.set_browser_status('Nicht gestartet')

        # Logbox itself
        frm_logbox = tk.Frame(frm_logbox_wrapper)
        frm_logbox.grid(row=1, column=0, columnspan=2, sticky='nsew')

        ttk.Style().configure('TText', padding='5 1 1 1')

        self.logbox = tk.Text(frm_logbox, state='disabled', wrap='word', font=('Helvetica', 10), borderwidth=10, relief=tk.FLAT)  # Border creates illusion of padding inside text box
        self.logbox.grid(row=1, sticky='nsew')

        logbox_scrollbar = ttk.Scrollbar(frm_logbox, orient='vertical', command=self.logbox.yview)
        self.logbox.configure({'yscrollcommand': logbox_scrollbar.set})
        logbox_scrollbar.grid(column=1, row=1, sticky = 'ns')

        frm_logbox.grid_rowconfigure(0, weight=0)  # Disable resizing of label
        frm_logbox.grid_rowconfigure(1, weight=1)  # Enable vertical resizing of logbox + scrollbar
        frm_logbox.grid_columnconfigure(0, weight=1)  # Enables horizontal resizing of logbox


    def print_data(self):
        """
        Clears the logbox and inserts all gathered questions, then resets the user's position inside the
        logbox to what it had been before clearing it.txt
        Potential TODO: Add different ways of visualizing selected questions vs unselected questions; if
        I wanna go real crazy, maybe even include a config box to add your own syntax.
        """
        string = ''
        ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

        for question in data.values():
            string += "{}. {}\n".format(question['index'], question['question'])
            
            for i, answer in enumerate(question['answers']):
                if question['answers'][answer] is True:  # If answer is selected
                    string += "{}.*{}\n".format(ALPHABET[i], answer)
                else:
                    string += "{}. {}\n".format(ALPHABET[i], answer)
                
            string += '\n'  # So different questions are visually broken apart
        
        yview = self.logbox.yview()

        self.logbox['state'] = 'normal'
        self.logbox.delete(0.0, tk.END)
        self.logbox.insert(0.0, string[:-2])  # -2 since last \n is meant to be omitted from string
        self.logbox['state'] = 'disabled'

        self.logbox.yview_moveto(yview[0])


    def log(self, string):
        """Sends a string to self.txt_log; important to note: self.print_data() will overwrite what's in log every time it's run"""
        self.logbox['state'] = 'normal'
        self.logbox.insert('end', ('' if self.logbox.get(0.0, 'end') else '\n') + string)
        self.logbox.yview_moveto(5000.0)  # 'end' doesn't work here for some reason, so I just went for a really high number.
        self.logbox['state'] = 'disabled'


    def on_btn_browser_click(self):
        """Figures out which state the browser is in and starts the relevant processes"""
        if self.btn_browser_text.get() == self.STR_OPEN_BROWSER:
            self.selenium_run()
            self.btn_browser_text.set(self.STR_CLOSE_BROWSER)

        elif self.btn_browser_text.get() == self.STR_CLOSE_BROWSER:
            self.driver.quit()
            self.btn_browser_text.set(self.STR_OPEN_BROWSER)


    def selenium_run(self):
        """Tries to start Selenium and runs the scraper"""
        try:
            self.set_browser_status('Startet...')
            self.driver = scraper.get_selenium(self.choice_browser.get())
            self.selenium_listener()
        except Exception:
            str_traceback = traceback.format_exc()
            logging.critical('Couldn\'t open webdriver:\n' + str_traceback)
            self.set_browser_status('Fehler')
            self.log('\n\n' + str_traceback)

        scraper.scrape(self.driver, self)


    def selenium_listener(self):
        """Periodically checks that Selenium is still alive. If it died, it changes the text on self.btn_browser_text to 'Browser Schließen'"""
        try: 
            self.driver.current_url  # Throws up an exception when browser is closed
            self.after(250, self.selenium_listener)  # Function recursively calls itself
        except WebDriverException:
            self.set_browser_status('Unerwartet geschlossen')
            self.btn_browser_text.set(self.STR_OPEN_BROWSER)


    def set_browser_status(self, string):
        self.lbl_browser_status_text.set('Browser Status: ' + string)
        logging.debug('Browser Status: ' + string)


def placeholder():
    print("You triggered a placeholder!")
    return True


def main():
    root = Interface()
    root.log("""1. Wie heißt die Logik des Forschungsprozesses? (1)
a. Methodologie
b. Prozessologie
c.*Epistemologie
d. Pragmatologie

2. Was trifft zu? (3)
Laut Émile Durkheim lassen sich soziale Tatbestände durch psychologische Faktoren erklären.
WEIL
Émile Durkheim wollte der Ethnographie zum Durchbruch verhelfen.
a. Die erste Aussage ist richtig.
b.*Die erste Aussage ist falsch.
c.*Die zweite Aussage ist richtig.
d. Die zweite Aussage ist falsch.
e. Die Weil-Verknüpfung ist berechtigt.
f.*Die Weil-Verknüpfung ist falsch.

3. Was trifft zu? (3)
Die Studie „Die Arbeitslosen von Marienthal“ lässt sich als Aktionsforschung bezeichnen.
WEIL
Die Forschenden der Studie „Die Arbeitslosen von Marienthal“ sollten die Rolle eins für die Gemeinschaft nützlichen
Mitglieds einnehmen.
a.*Die erste Aussage ist richtig.
b. Die erste Aussage ist falsch.
c.*Die zweite Aussage ist richtig.
d. Die zweite Aussage ist falsch.
e.*Die Weil-Verknüpfung ist berechtigt.
f. Die Weil-Verknüpfung ist falsch.

4. Wie ist Émile Durkheim in seiner Studie „Der Selbstmord“ vorgegangen? (1)
a. Er hat experimentelle und natürliche Daten kombiniert.
b. Er hat psychologische Tests durchgeführt.
c. Er hat persönliche Dokumente analysiert.
d.*Er hat Hypothesen aufgestellt und überprüft.

5. Welche der folgenden Merkmale stehen für eine erklärende Vorgehensweise in den Sozialwissenschaften? (2)
a.*hypothesentestend
b.*quantitativ
c. situationsbezogen
d. theoriegenerierend
e. qualitativ

6. Das Zusammenfassen mehrerer Variablen zu einer Kennzahl nennt man... (1)
a. Panel.
b. Kausalzusammenhang.
c. Normalverteilung.
d.*Index.

7. Welcher Erkenntnislogik folgt William F. Whytes Studie "Street Corner Society"? (2)
a. deduktiv
b.*idiographisch
c. kausal-erklärend
d. nomothetisch
e.*qualitativ

8. Unter Kausalität versteht man... (1)
a. das Zusammenfassen von mindestens zwei Variablen.
b. das gleichzeitige Auftreten von zwei Phänomenen.
c. die Schlussfolgerung aus einer logischen Ableitung.
d.*einen bekannten Ursache-Wirkung Zusammenhang.

9. Ein Beispiel:
In einem oberösterreichischen Badeort wird die See nahe Landschaft zunehmend durch Zweitwohnsitze verbaut. Um
die daraus entstehenden Konflikte zu untersuchen, wurde ein Schwimmwettbewerb zwischen der örtlichen
Bevölkerung und Personen mit Zweitwohnsitz organisiert und das Verhalten beider Gruppen beobachtet.
Um welchen Typus von Daten würde es sich nach den heuristischen Achsen von Lazarsfeld handeln? (1)
a.*experimentell
b. komplex
c. subjektiv
d. natürlich

10. Schlüsselpersonen spielen eine wichtige Rolle in der Feldforschung, weil sie...(1)
a. die Forschung leiten.
b.*den Zugang zum Feld verschaffen.
c. als Testpersonen fungieren.
d. Forschungsprojekte finanzieren.""")
    root.mainloop()
    

if __name__ == '__main__':
    main()
