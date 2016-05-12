# http://zetcode.com/gui/tkinter/layout/
# http://www.tkdocs.com/tutorial/grid.html
# http://tkinter.unpythonic.net/wiki/tkFileDialog
from Tkinter import Tk, Text, BOTH, END, W, N, E, S
from tkFileDialog import askopenfilename, asksaveasfilename
from ttk import Frame, Button, Label, Style
import anime

root = None
anime_file = None

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.self = None
        self.parent = parent
        self.initUI()


    def Load(self):
        global anime_file
        anime_file = askopenfilename(filetypes=[('Anime Studio Files', '.anime')])
        my_list = anime.top_level_layer_names(anime.get_data(anime_file)['layers'])
        self.area.delete("1.0", END)
        for x in my_list:
            self.area.insert(END, x + '\n')


    def Save(self):
        layer_names = self.area.get("1.0", END).split('\n')
        anime.process_named_layers(anime_file, layer_names)
        output_file = asksaveasfilename(defaultextension='.anime',filetypes=[('Anime Studio Files', '.anime')])
        anime.write_anime_file(output_file)


    def cancel(self):
        root.destroy()

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
        self.area.grid(column=0, row=1, columnspan=1, rowspan=6, padx=5, pady=7, sticky=E+W+S+N)

        hbtn = Button(self, text="Select Anime File", command=self.Load)
        hbtn.grid(row=4, column=1, padx=5, sticky='EW')

        obtn = Button(self, text="Resolve Layers", command=self.Save)
        obtn.grid(row=5, column=1, pady=7, padx=5, sticky='WE')

        cancel_button = Button(self, text="Exit", command=self.cancel)
        cancel_button.grid(row=6, column=1, padx=5, sticky='WE')


def main():
    global root
    root = Tk()
    root.geometry("350x300+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()