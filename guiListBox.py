from Tkinter import *
import tkMessageBox
import Tkinter
# http://stackoverflow.com/questions/13091222/changing-order-of-items-in-tkinter-listbox

def move_up(self, pos):
    """ Moves the item at position pos up by one """

    if pos == 0:
        return

    text = self.fileListSorted.get(pos)
    self.fileListSorted.delete(pos)
    self.fileListSorted.insert(pos-1, text)

top = Tk()

Lb1 = Listbox(top)
Lb1.insert(1, "Python")
Lb1.insert(2, "Perl")
Lb1.insert(3, "C")
Lb1.insert(4, "PHP")
Lb1.insert(5, "JSP")
Lb1.insert(6, "Ruby")

Lb1.pack()
top.mainloop()