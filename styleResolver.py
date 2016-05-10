# http://zetcode.com/gui/tkinter/layout/
# http://www.tkdocs.com/tutorial/grid.html
from Tkinter import Tk, Text, BOTH, W, N, E, S
from ttk import Frame, Button, Label, Style


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.parent = parent
        self.initUI()


    def initUI(self):

        self.parent.title("Style Resolver")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(6, pad=7)

        lbl = Label(self, text="Layer Order")
        lbl.grid(sticky=W, pady=4, padx=5)

        area = Text(self)
        area.grid(column=0, row=1, columnspan=1, rowspan=6,
                  padx=5, sticky=E+W+S+N)

        abtn = Button(self, text="Up")
        abtn.grid(column=1, row=1)

        cbtn = Button(self, text="Down")
        cbtn.grid(column=1, row=2, pady=4)

        hbtn = Button(self, text="Load")
        hbtn.grid(row=4, column=1, padx=5)

        obtn = Button(self, text="Save")
        obtn.grid(row=5, column=1)

        cancel_button = Button(self, text="Cancel")
        cancel_button.grid(row=6, column=1)


def main():

    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()