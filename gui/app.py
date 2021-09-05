from tkinter import *
from tkinter import ttk,filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import os

window = Tk()
window.geometry("800x500")
window.resizable(0,0)
window.wm_iconbitmap('gui/icon.ico')
window.title('Sentimental Analysis')

# row 0
def mic_clicked():
    print('mic clicked')

mic_icon = PhotoImage(file='gui/mic-4.png')
mic_button = Button(image=mic_icon,command=mic_clicked)
mic_button.grid(column=0,row=0,padx=10,pady=10)

heading = Label(text='Sentiment Analysis\n What it does: Detecting the intentions behind text response',font=(24),width=72)
heading.grid(column=1,row=0)

def folder_clicked():
    files = filedialog.askopenfilenames()
    # print(files[0])
    f = open(files[0], "r")
    f_list = f.readlines()
    f_sentence = ''.join(f_list)
    text_input.insert(END,f_sentence)

folder_icon = PhotoImage(file='gui/folder-6.png')
folder_button = Button(image=folder_icon,command=folder_clicked)
folder_button.grid(column=2,row=0,padx=10,pady=10)

# row 1
text_input = scrolledtext.ScrolledText(width=60,height=5)
# text_input.insert(END,'Hello rabin, This is an awesome application\nPlease let me know when you are available.')
# print(text_input.get('1.0',END))
text_input.grid(row=2,column=1,padx=4,pady=4)

def analyze_clicked():
    print('analyze clicked')

analyze_button = Button(text='  Analyze ',command=analyze_clicked,pady=20)
analyze_button.grid(column=2,row=2)

# row 2
style = ttk.Style()
style.theme_use('clam')

tree = ttk.Treeview( column=("Algorithm", "Accuracy", "Result"), show='headings', height=5)
tree.column("# 1", anchor=CENTER)
tree.heading("# 1", text="Algorithm")
tree.column("# 2", anchor=CENTER)
tree.heading("# 2", text="Accuracy")
tree.column("# 3", anchor=CENTER)
tree.heading("# 3", text="Result")
u1 = ('KNN','86%','Best')
u2 = ('Random Forest','82%','Middle')
u3 = ('Decision Tree','80%','Good')
u4 = ('SVC','72%','Fine')
u5 = ('Naive Bayes','70%','Ok')
tree.insert('', 'end', text="1", values=u1)
tree.insert('', 'end', text="1", values=u2)
tree.insert('', 'end', text="1", values=u3)
tree.insert('', 'end', text="1", values=u4)
tree.insert('', 'end', text="1", values=u5)

tree.grid(row=3,column=1,pady=20)

window.mainloop()