from tkinter import *
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
window.resizable(0,0)
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
                        current_text.set('Listening ...')
                        text = ast.literal_eval(rec.FinalResult())['text']
                        global final_text
                        final_text.append(text)
                        text_input.insert(END,final_text[-1]+'\n')
                    else:
                        text = ast.literal_eval(rec.PartialResult())['partial']
                        text =  [text[i:i+110] for i in range(0, len(text), 50)]
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
        is_recording = False
        mic_button.config(image=mic_icon)
        second_frame.config(text='Input Text')
    else:
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

analyze_button = Button(second_frame,text='  Analyze ',font=('Comic Sans MS',18,'normal'),command=analyze_clicked,borderwidth=1,relief=RAISED ,pady=20,padx=0)
analyze_button.grid(column=1,row=0)

# row 2
third_frame = Frame(window)
third_frame.columnconfigure(0, weight=1)
third_frame.grid(row=2,column=0,padx=5,pady=8)

# Tabs notbook
third_notebook = ttk.Notebook(third_frame)
third_notebook.grid(row=0,column=0)

tree = ttk.Treeview(third_notebook,column=("Algorithm",'Accuracy', "F1 Score", "Result"), show='headings', height=5)
tree.column("# 1", anchor=CENTER)
tree.heading("#1", text="Algorithm")
tree.column("# 2", anchor=CENTER)
tree.heading("#2", text="Accuracy")
tree.column("# 3", anchor=CENTER)
tree.heading("#3", text="F1 Score")
tree.column("# 4", anchor=CENTER)
tree.heading("#4", text="Result")
u1 = ('Logestic',0.89,89.5,'Best')
u2 = ('SVC',0.88,88.2,'Middle')
u3 = ('Multinomial NB',0.86,86.4,'Good')
u4 = ('Random Forest',0.85,84.9,'Fine')
u5 = ('Bernoulli NB',0.84,83.6,'Ok')
u6 = ('KNN',0.78,79.1,'Ok')
u7 = ('Gaussain NB',0.76,74.9,'Ok')
u8 = ('Decision Tree',0.72,71.7,'Ok')
tree.insert('', 'end', text="1", values=u1)
tree.insert('', 'end', text="1", values=u2)
tree.insert('', 'end', text="1", values=u3)
tree.insert('', 'end', text="1", values=u4)
tree.insert('', 'end', text="1", values=u5)
tree.insert('', 'end', text="1", values=u6)
tree.insert('', 'end', text="1", values=u7)
tree.insert('', 'end', text="1", values=u8)
tree.grid(row=0,column=0,pady=10,padx=5)

tree2 = ttk.Treeview(third_notebook,column=("Sentence",'Algorithm', "Sentiment"), show='headings', height=8)
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