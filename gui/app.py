from tkinter import *
from tkinter import ttk,filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import os

window = Tk()
window.geometry("826x500")
window.resizable(0,0)
window.wm_iconbitmap('gui/icon.ico')
window.title('Sentimental Analysis')

style = ttk.Style()
style.theme_use('vista')
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

# global variables
is_recording = False

# row 0
first_frame = ttk.Frame(window)
first_frame.columnconfigure(0, weight=1)
first_frame.grid(row=0,column=0)


def mic_clicked():
    print('mic clicked')
    global is_recording
    if is_recording:
        is_recording = False
        mic_button.config(image=mic_icon)
        second_frame.config(text='Input Text')
    else:
        is_recording = True
        mic_button.config(image=mic_rec)
        second_frame.config(text='Recording ...')
    
mic_icon = PhotoImage(file='gui/mic-4.png')
mic_rec = PhotoImage(file='gui/mic-44.png')
mic_button = Button(first_frame,image=mic_icon,command=mic_clicked,borderwidth=1,relief=RIDGE,width=60,height=60)
mic_button.grid(column=0,row=0,padx=5,pady=5)

first_sub_frame = ttk.Frame(first_frame)
first_frame.columnconfigure(0, weight=1)
first_sub_frame.grid(row=0,column=1)

heading1 = Label(first_sub_frame,text='Sentiment Analysis',font=("Comic Sans MS",24,"normal"),width=33)
heading1.grid(column=0,row=0)
heading2 = Label(first_sub_frame,text='What it does: Detecting the intentions behind text response',font=('Candara Light',18))
heading2.grid(column=0,row=1)

def folder_clicked():
    files = filedialog.askopenfilenames()
    # print(files[0])
    f = open(files[0], "r")
    f_list = f.readlines()
    f_sentence = ''.join(f_list)
    text_input.insert(END,f_sentence)

folder_icon = PhotoImage(file='gui/folder-6.png')
folder_button = Button(first_frame,image=folder_icon,command=folder_clicked,borderwidth=1,relief=RIDGE,width=60,height=60)
folder_button.grid(column=2,row=0,padx=10,pady=10)

# row 1
second_frame = LabelFrame(window,text='Input Text')
second_frame.columnconfigure(0, weight=1)
second_frame.grid(row=1,column=0,ipadx=4)


text_input = scrolledtext.ScrolledText(second_frame,width=72,height=6)
# text_input.insert(END,'Hello rabin, This is an awesome application\nPlease let me know when you are available.')
# print(text_input.get('1.0',END))
text_input.grid(row=0,column=0,padx=0,pady=4)

def analyze_clicked():
    print('analyze clicked')

analyze_button = Button(second_frame,text='  Analyze ',font=('Comic Sans MS',18,'normal'),command=analyze_clicked,borderwidth=1,relief=RAISED ,pady=20,padx=0)
analyze_button.grid(column=1,row=0)

# row 2
third_frame = Frame(window)
third_frame.columnconfigure(0, weight=1)
third_frame.grid(row=2,column=0,padx=5,pady=8)

# Tabs notbook
third_notebook = ttk.Notebook(third_frame)
third_notebook.grid(row=0,column=0)

tree = ttk.Treeview(third_notebook,column=("Algorithm",'test', "Accuracy", "Result"), show='headings', height=5)
tree.column("# 1", anchor=CENTER)
tree.heading("#1", text="Algorithm")
tree.column("# 2", anchor=CENTER)
tree.heading("#2", text="Accuracy")
tree.column("# 3", anchor=CENTER)
tree.heading("#3", text="text1")
tree.column("# 4", anchor=CENTER)
tree.heading("#4", text="Result")
u1 = ('KNN',1,'86%','Best')
u2 = ('Random Forest',1,'82%','Middle')
u3 = ('Decision Tree',1,'80%','Good')
u4 = ('SVC',1,'72%','Fine')
u5 = ('Naive Bayes',1,'70%','Ok')
tree.insert('', 'end', text="1", values=u1)
tree.insert('', 'end', text="1", values=u2)
tree.insert('', 'end', text="1", values=u3)
tree.insert('', 'end', text="1", values=u4)
tree.insert('', 'end', text="1", values=u5)
tree.grid(row=0,column=0,pady=10,padx=5)

tree2 = ttk.Treeview(third_notebook,column=("Sentence",'Algorithm', "Sentiment"), show='headings', height=5)
tree2.column("# 1", anchor=CENTER)
tree2.heading("#1", text="Sentence")
tree2.column("# 2", anchor=CENTER)
tree2.heading("#2", text="Algorithm")
tree2.column("# 3", anchor=CENTER)
tree2.heading("#3", text="Sentiment")
tree2.insert('', 'end', text="1", values=('KNN','86%','Best'))
tree2.insert('', 'end', text="1", values=('Random Forest','82%','Middle'))
tree2.insert('', 'end', text="1", values=('Decision Tree','80%','Good'))
tree2.insert('', 'end', text="1", values=('SVC','72%','Fine'))
tree2.insert('', 'end', text="1", values=('Naive Bayes','70%','Ok'))
tree2.grid(row=0,column=0,pady=10,padx=5)

third_notebook.add(tree,text='Result')
third_notebook.add(tree2,text='Sentiment')

window.mainloop()