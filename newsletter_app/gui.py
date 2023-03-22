import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from send_newsletter import Newsletter



def temporary_text(textbox):
    textbox.delete(0,"end")

class EntryDefaultText(tk.Entry):
    def __init__(self, default_text, textvariable=None):
        super().__init__(self, textvariable=textvariable)
        self.default_text = default_text
        self.insert(0, self.default_text)

    def delete_text_when_focus(self):
        self.bind("<FocusIn>", self.delete(0,"end"))

class DemoWidget(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.filename = []
        self.champs = {
            'username': tk.StringVar(),
            'password': tk.StringVar(),
            'sender_email': tk.StringVar(),
            'recipient': tk.StringVar(),
            'images': tk.StringVar(),
            'subject': tk.StringVar(),
        }
        self._create_gui()
        self.pack()

    def upload_file(self):
        f_types = [('Jpg Files', '*.jpg'),('PNG Files','*.png')]
        self.filename = list(filedialog.askopenfilename(multiple=True,filetypes=f_types))
        print(self.filename)


    def _create_gui(self):
        username_label = tk.Label(self, text="Username")
        username_label.grid(column=0, row=0)

        # self.champs['username'].set("Default Text")
        #username_text = EntryDefaultText("Default", textvariable=self.champs['username'])
        #username_text.grid(column=1, row=0, columnspan=2)
        #username_text.delete_text_when_focus()
        username_text = tk.Entry(self, textvariable=self.champs['username'])
        username_text.grid(column=1, row=0, columnspan=2)
        # #username_text.insert(0, "This is Temporary Text...")
        # username_text.bind("<FocusIn>", self.delete())

        password_label = tk.Label(self, text="Password")
        password_label.grid(column=0, row=1)

        password_text = ttk.Entry(self, show="*", textvariable=self.champs['password'])
        password_text.grid(column=1, row=1, columnspan=2)


        sender_label = tk.Label(self, text="Sender email")
        sender_label.grid(column=0, row=2)

        sender_text = ttk.Entry(self, textvariable=self.champs['sender_email'])
        sender_text.grid(column=1, row=2, columnspan=2)

        recipient_label = tk.Label(self, text="Recipient")
        recipient_label.grid(column=0,row=3)

        recipient_text = ttk.Entry(self, textvariable=self.champs["recipient"])
        recipient_text.grid(column=1, row=3,  columnspan=2)

        subject_label = tk.Label(self, text="Subject")
        subject_label.grid(column=0,row=4)

        subject_text = ttk.Entry(self, textvariable=self.champs["subject"])
        subject_text.grid(column=1, row=4,  columnspan=2)


        upload_button = tk.Button(self, text='Upload File',  width=20,command = lambda: self.upload_file())
        upload_button.grid(column=1, row=5,columnspan=2)


        button = tk.Button(self, text="Send", command=self.valider)
        button.grid(column=1, row=7, pady=20)

        button = tk.Button(self, text="Close", command=app.quit)
        button.grid(column=2, row=7, pady=20)

    def valider(self):
        newsletter = Newsletter()
        newsletter.initialise_email_sender(self.champs['username'].get(), self.champs['password'].get(), smtp_email_adress=self.champs['sender_email'].get())
        print(self.champs["recipient"].get())
        newsletter.add_receiver(self.champs["recipient"].get())
        newsletter.set_subject(self.champs["subject"].get())
        newsletter.set_images(self.filename)
        newsletter.find_smtp_server()
        newsletter.send_email()



app = tk.Tk()
app.title("Demo Widgets")
DemoWidget(app)
app.mainloop()