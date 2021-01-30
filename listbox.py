from tkinter import * # for python 2.7 use Tkinter

root = Tk()


frame1 = Frame(root, bg="red", height=20)
frame1.grid(row=0,column=0, sticky=W+E)

frame3 = Frame(root, bg="blue", height=20)
frame3.grid(row=0,column=1, sticky=W+E)

frame2 = Frame(root, bg="green",  height=20)
frame2.grid(row=1,column=0, sticky=W+E)



frame4 = Frame(root)
frame4.grid(row=2,columnspan=2, sticky=E+W)

l5 = Label(frame4, text="Output:", bg="orange").grid(row=0, column=0, sticky=E+W)
output = Listbox(frame4, height=5, width=50)
output.grid(row=1,column=0)
#output.pack(side=LEFT,  fill=BOTH, expand=1)

root.mainloop()