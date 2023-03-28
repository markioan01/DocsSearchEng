import tkinter as tk
from tkinter import *
import functionalityScripts as fs

class WinSearchEngineClass:
    def __init__(self, master):

        #variables
        self.file = None
        self.dict1 = None
        self.docs = None
        self.buttons = []
        
        #main window
        self.master = master
        self.master.geometry("1200x700")
        self.master.title('GPD(Greek Parliament Documents) Search Engine')
        self.master.resizable(False, False)
        
        #Create the left and right frames
        self.left_frame = tk.Frame(master, width=266, bg="red")
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.right_frame = tk.Frame(master, width=534, bg="green")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        #Create the top and bottom frames inside the right frame
        self.top_frame = tk.Frame(self.right_frame, height=167, bg="blue", highlightthickness=4, highlightbackground="gray")
        self.top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.right_frame, height=333, bg="yellow", highlightthickness=4, highlightbackground="gray")
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


        #create three vertical frames inside the top frame of the right frame
        #Then we put labels in them, for the characteristics of the docs
        frame1 = tk.Frame(self.top_frame, bg='red')
        frame1.place(relx=0, rely=0, relwidth=0.33, relheight=1)

        self.member_name_label = tk.Label(frame1, text="Member Name:", padx=10, pady=2,font=("Arial", 7))
        self.sitting_date_label = tk.Label(frame1, text="Sitting Date:", padx=10, pady=5,font=("Arial", 7))
        self.parliamentary_period_label = tk.Label(frame1, text="Parliamentary Period:", padx=10, pady=5,font=("Arial", 7))
        self.parliamentary_session_label = tk.Label(frame1, text="Parliamentary Session:", padx=10, pady=5,font=("Arial", 7))

        self.member_name_label.pack(side=tk.TOP, padx=10, pady=5)
        self.sitting_date_label.pack(side=tk.TOP, padx=10, pady=5)
        self.parliamentary_period_label.pack(side=tk.TOP, padx=10, pady=5)
        self.parliamentary_session_label.pack(side=tk.TOP, padx=10, pady=5)


        frame2 = tk.Frame(self.top_frame, bg='green')
        frame2.place(relx=0.33, rely=0, relwidth=0.33, relheight=1)

        self.parliamentary_sitting_label = tk.Label(frame2, text="Parliamentary Sitting:", padx=10, pady=2,font=("Arial", 7))
        self.political_party_label = tk.Label(frame2, text="Political Party:", padx=10, pady=5,font=("Arial", 7))
        self.government_label = tk.Label(frame2, text="Government:", padx=10, pady=5,font=("Arial", 7))
        self.member_region_label = tk.Label(frame2, text="Member Region:", padx=10, pady=5,font=("Arial", 7))

        self.parliamentary_sitting_label.pack(side=tk.TOP, padx=10, pady=5)
        self.political_party_label.pack(side=tk.TOP, padx=10, pady=5)
        self.government_label.pack(side=tk.TOP, padx=10, pady=5)
        self.member_region_label.pack(side=tk.TOP, padx=10, pady=5)


        frame3 = tk.Frame(self.top_frame, bg='yellow')
        frame3.place(relx=0.66, rely=0, relwidth=0.34, relheight=1)

        self.roles_label = tk.Label(frame3, text="Roles:", padx=10, pady=2,font=("Arial", 7))
        self.member_gender_label = tk.Label(frame3, text="Member Gender:", padx=10, pady=5,font=("Arial", 7))

        self.roles_label.pack(side=tk.TOP, padx=10, pady=5)
        self.member_gender_label.pack(side=tk.TOP, padx=10, pady=5)


        
        #create frames and entries for the load of the files
        self.label_frame = tk.Frame(self.left_frame, pady=10)
        self.label_frame.pack(side=tk.TOP, fill=tk.X)
        self.label = tk.Label(self.label_frame, text='Φόρτωσε τα αρχεία από-έως:')
        self.label.pack(side=tk.TOP, fill=tk.X)
        self.entry_frame = tk.Frame(self.label_frame)
        self.entry_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        self.entry1 = tk.Entry(self.entry_frame)
        self.entry1.pack(side=tk.LEFT, padx=10)
        self.entry2 = tk.Entry(self.entry_frame)
        self.entry2.pack(side=tk.LEFT, padx=10)
        self.enter_button = tk.Button(self.label_frame, text='Load', command=self.loadFiles)
        self.enter_button.pack(side=tk.TOP, padx=10)
    

        #create frame and entry for the search bar
        self.search_frame = tk.Frame(self.left_frame)
        self.search_frame.pack(side=tk.TOP, fill=tk.X)
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var)
        self.search_entry.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.X)

        #create frame and button for the search button
        self.search_button_frame = tk.Frame(self.left_frame)
        self.search_button_frame.pack(side=tk.TOP, fill=tk.X)
        self.search_button = tk.Button(self.search_button_frame, text='Search', command=self.search)
        self.search_button_frame.columnconfigure(0, weight=1)
        self.search_button_frame.columnconfigure(1, weight=1)
        self.search_button_frame.columnconfigure(2, weight=1)
        self.search_button.pack(side=tk.LEFT, padx=10)
        self.search_button_frame.bind('<Configure>', self.center_search_button)

        #create scrollbar and result box for results of the searching
        self.scrollbar = tk.Scrollbar(self.left_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_listbox = tk.Listbox(self.left_frame, yscrollcommand=self.scrollbar.set)
        self.results_listbox.pack(side=tk.BOTTOM, padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.scrollbar.config(command=self.results_listbox.yview)

        #create scrollbar for the text frame where we appear the document
        self.scrollbar2 = tk.Scrollbar(self.bottom_frame, orient=tk.VERTICAL)
        self.scrollbar2.pack(side=tk.RIGHT, fill=tk.Y)
        self.labelDoc = tk.Text(self.bottom_frame, yscrollcommand=self.scrollbar2.set, wrap=tk.WORD)
        self.labelDoc.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill=tk.BOTH)
        self.scrollbar2.config(command=self.labelDoc.yview)
        self.labelDoc.config(state=DISABLED)

        
        
    #Search function that call the functions that we have already create
    def search(self):
        search_term = self.search_var.get()
        queryLabel = tk.Label(self.results_listbox, text=str("Q:" + search_term)).pack(side=tk.TOP, fill=tk.X)
        search_term = fs.clearQuery(search_term,self.file)
        
        self.results_listbox.delete(0, tk.END)
        
        results = fs.topK(search_term,self.dict1,5,self.file)

        selected_indices = self.results_listbox.curselection()
        for i in range(self.results_listbox.size()):
            button_text = self.results_listbox.get(i)
            button = self.buttons_dict.get(button_text)
            if button:
                button.destroy()
                del self.buttons_dict[button_text]
        self.results_listbox.delete(0, tk.END)
        
        self.buttons = []
        bs = []
        
        #print(results)
        for f in results:
            bs.append(f)
            
            self.b = Button(self.results_listbox, text=f, command=lambda r=f: self.showDoc(r)).pack(side=tk.TOP, fill=tk.X)
            self.buttons.append(self.b)
            
        #print(self.buttons)

    #Function that calls the dunction to load the files    
    def loadFiles(self):
        value1 = self.entry1.get()
        value2 = self.entry2.get()
        self.file, self.dict1, self.docs = fs.readDocuments(int(float(value1)),int(float(value2)))

    #It centers the search button in it's frame   
    def center_search_button(self, event):
        self.search_button_frame.update()
        search_button_x = (self.search_button_frame.winfo_width() - self.search_button.winfo_reqwidth()) / 2
        self.search_button.place(x=search_button_x, y=0)

    #It centers a label in its frame
    def center_label(self, event):
        self.label_frame.update()
        label_x = (self.label_frame.winfo_width() - self.label.winfo_reqwidth()) / 2
        label_y = (self.label_frame.winfo_height() - self.label.winfo_reqheight()) / 2
        self.label.place(x=label_x, y=label_y)

    #Shows the informations of the doc and the doc itself
    def showDoc(self,arg):
        arg = int(float(arg))
        txt = self.docs.loc[arg]["speech"]
        self.labelDoc.config(state=NORMAL)
        self.labelDoc.delete('1.0', tk.END)
        self.labelDoc.insert(tk.END,txt)
        self.labelDoc.config(state=DISABLED)

        
        self.member_name_label.config(text = str("Member Name:\n" + self.docs.loc[arg]["member_name"]))
        self.sitting_date_label.config(text = str("Sitting Date:\n" + self.docs.loc[arg]["sitting_date"]))
        self.parliamentary_period_label.config(text = str("Parliamentary Period:\n" + self.docs.loc[arg]["parliamentary_period"]))
        self.parliamentary_session_label.config(text = str("Parliamentary Session:\n" + self.docs.loc[arg]["parliamentary_session"]))
        self.parliamentary_sitting_label.config(text = str("Parliamentary Sitting:\n" + self.docs.loc[arg]["parliamentary_sitting"]))
        self.political_party_label.config(text = str("Political Party:\n" + self.docs.loc[arg]["political_party"]))
        self.government_label.config(text = str("Government:\n" + self.docs.loc[arg]["government"]))
        self.member_region_label.config(text = str("Member Region:\n" + self.docs.loc[arg]["member_region"]))
        self.roles_label.config(text = str("Roles:\n" + self.docs.loc[arg]["roles"]))
        self.member_gender_label.config(text = str("Member Gender:\n" + self.docs.loc[arg]["member_gender"]))



if __name__ == '__main__':
    root = tk.Tk()
    app = WinSearchEngineClass(root)
    root.mainloop()






