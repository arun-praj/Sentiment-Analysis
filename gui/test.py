from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import messagebox

window = Tk()
window.geometry("800x600")
window.resizable(0,0)
window.wm_iconbitmap('gui/icon.ico')
window.title('Sentimental Analysis')


# Label
my_label = Label(text='New Label',font=('Arial',24,'bold'))
my_label.grid(column=0,row=0)
# update label
# my_label.config(text='update')

#input Entry()
input_text = Entry(width=26)
input_text.grid(column=0,row=1)

# button
def button_clicked():
    my_label.config(text=input_text.get()) # update mylabel from input Entry()

fred = Button(text='Submit',command=button_clicked,bg='skyblue',fg='black')
# display in screen
#1 fred.pack()
#2 fred.place(x=180,y=36)
fred.grid(column=2,row=1)

# ComboBox
combo = ttk.Combobox();
combo["values"] = (1,2,3,4,5,'Text')
combo.current(3)
print(combo.get())
combo.grid(column=1,row=5)

# Menubutton
def menu_item_selected(*args):
    print(selected_color.get())
    menu_button.config(text=selected_color.get())

selected_color = StringVar()
selected_color.trace("w", menu_item_selected)

menu_button = Menubutton(text='Select a color')
menu = Menu(menu_button,tearoff=0)
menu.add_radiobutton(label='Red',value='Red',variable=selected_color)
menu.add_radiobutton(label='Green',value='Green',variable=selected_color)
menu.add_radiobutton(label='Blue',value='Blue',variable=selected_color)
menu_button['menu'] = menu
menu_button.grid(column=2,row=5)

# Text
text = Text(height=5,width=30)
text.focus()
text.insert(END,'This is a multiline text entry')
print(text.get('1.0',END))
text.grid(row=2,column=0)

# Spinbox -- number input
def spinbox_used():
    print(spinbox.get())

spinbox = Spinbox(from_=0,to=10,width=10,command=spinbox_used)
spinbox.grid(row=3,column=0)

# Scale
def scale_used(value):
    print(value)

scale = Scale(from_=0,to=100,command=scale_used)
scale.grid(row=2,column=2)

# Checkbutton
def checkbutton_used():
    print(check_state.get())

check_state = IntVar() # BoolreanVar() for boolean
checkbutton = Checkbutton(text='is On?',variable=check_state,command=checkbutton_used)
checkbutton.grid(row=3,column=1)

# Radio button
def radio_used():
    print(radio_state.get())

radio_state = IntVar()
Radiobutton1 = Radiobutton(text='Option1',value=1,variable=radio_state,command=radio_used)
Radiobutton2 = Radiobutton(text='Option2',value=2,variable=radio_state,command=radio_used)
Radiobutton3 = Radiobutton(text='Option3',value=3,variable=radio_state,command=radio_used)
Radiobutton1.grid(row=4,column=0)
Radiobutton2.grid(row=4,column=1)
Radiobutton3.grid(row=4,column=2)

#List Box
def list_box(event):
    print(listbox.get(listbox.curselection()))

listbox = Listbox(height=4)
fruits = ['apple','pear','orange','papaya','grapes']
for item in fruits:
    listbox.insert(fruits.index(item),item)
listbox.bind("<<ListboxSelect>>",list_box)
listbox.grid(row=5,column=0)

# Scrolltext
scroll_text = scrolledtext.ScrolledText(width=40,height=10)
scroll_text.grid(row=6,padx=4,pady=4)

# MessageBox
def mseg_box():
    messagebox.showinfo('Message Title','Message Content')

btn_message = Button(text='Message Box',command=mseg_box)
btn_message.grid(row=6,column=1)

# Events Mouse Buttons
def right_fun_bind_btn(event):
    Label(text ='right button clicked').grid(column=1,row=7)

def left_fun_bind_btn(event):
    Label(text ='left button clicked').grid(column=1,row=7)

bind_btn = Button(text='text right click')
bind_btn.bind("<Button-3>",right_fun_bind_btn)
bind_btn.bind("<Button-1>",left_fun_bind_btn)
bind_btn.grid(row=7,column=0)

# Add images
# icon = PhotoImage(file='gui/icon.ico')
# img_label = Label(image=icon)
# img_label.grid(row=8,column=0)


window.mainloop()