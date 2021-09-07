from tkinter import *
from typing import Sized
from stopword import removing_stopwords
from tkinter import ttk,filedialog
from tkinter import scrolledtext
from tkinter import messagebox
from cleaner import cleaner
import pandas as pd
import sounddevice
import argparse
import _thread
import queue
import vosk
import sys
import ast
import os

window = Tk()
window.geometry("826x500")
# window.resizable(0,0)
window.wm_iconbitmap('gui/icon.ico')
window.title('Sentimental Analysis')

style = ttk.Style()
style.theme_use('vista')
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

# global variables
is_recording = False
final_text = []
cleaned_text = []
current_text = StringVar()
current_text.set('What it does: Detecting the intentions behind text response')

# row 0
first_frame = ttk.Frame(window)
first_frame.columnconfigure(0, weight=1)
first_frame.grid(row=0,column=0)

def startrecord():
    # recorder
    q = queue.Queue()
    def int_or_str(text):
        """Helper function for argument parsing."""
        try:
            return int(text)
        except ValueError:
            return text

    def callback(indata, frames, time, status):
        """This is called (from a separate thread) for each audio block."""
        if status:
            # print(status, file=sys.stderr)
            pass
        q.put(bytes(indata))

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        # print(sounddevice.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])

    parser.add_argument('-f', '--filename', type=str, metavar='FILENAME',help='audio file to store recording to')
    parser.add_argument('-m', '--model', type=str, metavar='MODEL_PATH',help='Path to the model')
    parser.add_argument('-d', '--device', type=int_or_str,help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)
    try:
        if args.model is None:
            args.model = "gui/model"
        if not os.path.exists(args.model):
            print ("Download model from https://alphacephei.com/vosk/models")
            print ("and unpack as 'model' in the current folder.")
            parser.exit(0)
        if args.samplerate is None:
            device_info = sounddevice.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])

        model = vosk.Model(args.model)
        if args.filename:
            dump_fn = open(args.filename, "wb")
        else:
            dump_fn = None

        with sounddevice.RawInputStream(samplerate=args.samplerate, blocksize = 8000, device=args.device, dtype='int16',
                                channels=1, callback=callback):
                rec = vosk.KaldiRecognizer(model, args.samplerate)
                while is_recording:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        text = ast.literal_eval(rec.FinalResult())['text']
                        global final_text
                        final_text.append(text)
                        text_input.insert(END,final_text[-1]+'\n')
                        current_text.set('Listening ...')
                    else:
                        text = ast.literal_eval(rec.PartialResult())['partial']
                        text =  [text[i:i+110] for i in range(0, len(text), 50)]
                        if len(text) ==0:
                            current_text.set('Listening ...')
                        else:
                            current_text.set('\n'.join(text))
                        
                    if dump_fn is not None:
                        dump_fn.write(data)
                else:
                    current_text.set('What it does: Detecting the intentions behind text response')
                    textfile = open("gui/record.txt", "w")
                    for element in final_text:
                        textfile.write(element + "\n")
                    textfile.close()
                    parser.exit(0)

    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

def mic_clicked():
    global is_recording
    if is_recording:
        heading2.grid(row=1)
        heading1.config(text='Sentiment Analysis')
        is_recording = False
        mic_button.config(image=mic_icon)
        second_frame.config(text='Input Text')
    else:
        heading2.grid(row=0)
        heading1.config(text='')
        is_recording = True
        mic_button.config(image=mic_rec)
        text_input.delete('0.0', END)
        second_frame.config(text='Recording ...')
        _thread.start_new_thread(startrecord,())
    
mic_icon = PhotoImage(file='gui/mic-4.png')
mic_rec = PhotoImage(file='gui/mic-44.png')
mic_button = Button(first_frame,image=mic_icon,command=mic_clicked,borderwidth=1,relief=RIDGE,width=60,height=60)
mic_button.grid(column=0,row=0,padx=5,pady=5)

first_sub_frame = ttk.Frame(first_frame)
first_frame.columnconfigure(0, weight=1)
first_sub_frame.grid(row=0,column=1)

heading1 = Label(first_sub_frame,text='Sentiment Analysis',font=("Comic Sans MS",24,"normal"))
heading1.grid(column=0,row=0)
heading2 = Label(first_sub_frame,textvariable=current_text,font=('Candara Light',12),width=72)
heading2.grid(column=0,row=1)

def folder_clicked():
    files = filedialog.askopenfilenames()
    # print(files[0])
    f = open(files[0], "r")
    f_list = f.readlines()
    f_sentence = ''.join(f_list)
    text_input.delete('0.0', END)
    text_input.insert(END,f_sentence)

folder_icon = PhotoImage(file='gui/folder-6.png')
folder_button = Button(first_frame,image=folder_icon,command=folder_clicked,borderwidth=1,relief=RIDGE,width=60,height=60)
folder_button.grid(column=2,row=0,padx=10,pady=10)

# row 1
second_frame = LabelFrame(window,text='Input Text')
second_frame.columnconfigure(0, weight=1)
second_frame.grid(row=1,column=0,ipadx=4)


text_input = scrolledtext.ScrolledText(second_frame,width=72,height=8)
# text_input.insert(END,'Hello rabin, This is an awesome application\nPlease let me know when you are available.')
# print(text_input.get('1.0',END))
text_input.grid(row=0,column=0,padx=0,pady=4)

def analyze_clicked():
    global cleaned_text
    list_sentence = text_input.get('1.0',END).split('\n')
    list_sentence = [removing_stopwords(cleaner(sentence)) for sentence in list_sentence if len(sentence)!=0]
    text_input.delete('0.0', END)
    text_input.insert(END,'\n'.join(list_sentence))
    cleaned_text = list_sentence
    ############################

analyze_button = Button(second_frame,text='  Analyze ',font=('Comic Sans MS',18,'normal'),command=analyze_clicked,borderwidth=1,relief=RAISED ,pady=10)
analyze_button.grid(column=1,row=0)

# row 2
third_frame = Frame(window)
third_frame.columnconfigure(0, weight=1)
third_frame.grid(row=2,column=0,padx=5,pady=8)

# Tabs notbook
third_notebook = ttk.Notebook(third_frame)
third_notebook.grid(row=0,column=0)

tree = ttk.Treeview(third_notebook,column=("Algorithm",'Accuracy', "F1 Score", "Recall","Precision"), show='headings', height=9)
tree.column("# 1", anchor=CENTER,width=200)
tree.heading("#1", text="Algorithm")
tree.column("# 2", anchor=CENTER,width=150)
tree.heading("#2", text="Accuracy")
tree.column("# 3", anchor=CENTER,width=150)
tree.heading("#3", text="F1 Score")
tree.column("# 4", anchor=CENTER,width=150)
tree.heading("#4", text="Recall")
tree.column("# 5", anchor=CENTER,width=150)
tree.heading("#5", text="Precision")

tree.insert('', 'end', text="1", values=('Logestic',0.89,89.5,91.4,88.1))
tree.insert('', 'end', text="1", values=('SVC',0.88,88.2,89.4,86.9))
tree.insert('', 'end', text="1", values=('Multinomial NB',0.86,86.4,86.4,86.4))
tree.insert('', 'end', text="1", values=('Random Forest',0.85,84.9,84.3,85.6))
tree.insert('', 'end', text="1", values=('Bernoulli NB',0.84,83.6,81.6,86.2))
tree.insert('', 'end', text="1", values=('KNN',0.78,79.1,84.2,74.5))
tree.insert('', 'end', text="1", values=('Gaussain NB',0.76,74.9,72.64,77.3))
tree.insert('', 'end', text="1", values=('Decision Tree',0.72,71.7,71.1,71.9))
tree.grid(row=0,column=0,pady=10,padx=5)

tree2 = ttk.Treeview(third_notebook,column=("Sentence/Algorithm",'Logestic', "SVC","Multinomial NB","Random Forest","Bernoulli NB","KNN","Gaussain NB","Decision Tree"), show='headings', height=9)
tree2.column("# 1", anchor=CENTER)
tree2.heading("#1", text="Sentence/Algorithm")
tree2.column("# 2", anchor=CENTER,width=38)
tree2.heading("#2", text="Logestic")
tree2.column("# 3", anchor=CENTER,width=14)
tree2.heading("#3", text="SVC")
tree2.column("# 4", anchor=CENTER,width=78)
tree2.heading("#4", text="Multinomial NB")
tree2.column("# 5", anchor=CENTER,width=78)
tree2.heading("#5", text="Random Forest")
tree2.column("# 6", anchor=CENTER,width=62)
tree2.heading("#6", text="Bernoulli NB")
tree2.column("# 7", anchor=CENTER,width=18)
tree2.heading("#7", text="KNN")
tree2.column("# 8", anchor=CENTER,width=60)
tree2.heading("#8", text="Gaussain NB")
tree2.column("# 9", anchor=CENTER,width=66)
tree2.heading("#9", text="Decision Tree")

tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN1 Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN2 Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN3 Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN4 Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.insert('', 'end', text="1", values=('KNN5 Random Forest Random Forest Random Forest Random Forest','86%','Best'))
tree2.grid(row=0,column=0,pady=10,padx=5)

third_notebook.add(tree2,text='Sentiment')
third_notebook.add(tree,text='Result')

window.mainloop()