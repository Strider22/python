# http://zetcode.com/gui/tkinter/layout/
# http://www.tkdocs.com/tutorial/grid.html
from Tkinter import Tk, Text, BOTH, END, W, N, E, S
from tkFileDialog import askopenfilename
from ttk import Frame, Button, Label, Style
import anime


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.self = None
        self.parent = parent
        self.initUI()


    def Load(self):
        filename = askopenfilename()
        print(filename)
        my_list = anime.top_level_layer_names(anime.get_data(filename)['layers'])
        for x in my_list:
            self.area.insert(END, x + '\n')



    def initUI(self):

        self.parent.title("Style Resolver")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, pad=7)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(6, pad=7)

        lbl = Label(self, text="Layer Order")
        lbl.grid(sticky=W, pady=4, padx=5)

        self.area = Text(self)
        self.area.grid(column=0, row=1, columnspan=1, rowspan=6,
                  padx=5, sticky=E+W+S+N)

        abtn = Button(self, text="Up", command = self.move_up)
        abtn.grid(column=1, row=1)

        cbtn = Button(self, text="Down", command = self.move_down)
        cbtn.grid(column=1, row=2, pady=4)

        hbtn = Button(self, text="Load", command = self.Load)
        hbtn.grid(row=4, column=1, padx=5)

        obtn = Button(self, text="Save")
        obtn.grid(row=5, column=1)

        cancel_button = Button(self, text="Cancel")
        cancel_button.grid(row=6, column=1)


    # swap this line with the line above it
    def move_up(self):
        self.area.config(state='normal')
        # get text on current and previous lines
        lineText = self.area.get("insert linestart", "insert lineend")
        prevLineText = self.area.get("insert linestart -1 line", "insert -1 line lineend")

        # delete the old lines
        self.area.delete("insert linestart -1 line", "insert -1 line lineend")
        self.area.delete("insert linestart", "insert lineend")

        # insert lines in swapped order
        self.area.insert("insert linestart -1 line", lineText)
        self.area.insert("insert linestart", prevLineText)
        #text.config(state='disabled')


    # swap this line with the line below it
    def move_down(self):
        self.area.config(state='normal')
        # get text on current and next lines
        lineText = self.area.get("insert linestart", "insert lineend")
        nextLineText = self.area.get("insert +1 line linestart", "insert +1 line lineend")

        # delete text on current and next lines
        self.area.delete("insert linestart", "insert lineend")
        self.area.delete("insert +1 line linestart", "insert +1 line lineend")

        # insert text in swapped order
        self.area.insert("insert linestart", nextLineText)
        self.area.insert("insert linestart + 1 line", lineText)
        #text.config(state='disabled')

def main():

    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()