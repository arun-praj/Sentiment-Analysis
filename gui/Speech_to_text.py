import tkinter as tk
from tkinter import *
import argparse
import os
import ast
import queue
import sounddevice
import vosk
import sys
import _thread
from datetime import datetime

# ui
is_running=True
final_text  =[]
root = Tk()
fls = StringVar()
fls2 = StringVar()
fls3 = StringVar()
fls_diff = StringVar()

##
canvas = Canvas(root, width=800, height=650)
canvas.create_text(100,10,fill="darkblue",font="Times 20 italic bold",
                        text="Click the bubbles that are multiples of two.")
##

fls.set('Start Record') # Update
fls2.set('Your Speech')
fls3.set('')


wrapper = LabelFrame(root,text='Spech to Text')
wrapper.pack(fill="both",expand="yes",padx=10,pady=10)

lbl3 = Label(wrapper,textvariable=fls3)
lbl3.pack()

lbl = Label(wrapper,textvariable=fls)
lbl.pack()

lbl2 = Label(wrapper,textvariable=fls2)
lbl2.pack()

def record():
    global is_running
    is_running=True
    btn1.pack_forget()
    btn2.pack(padx=20)
    fls.set('Recording') # Update
    _thread.start_new_thread(startrecord,())

def stop():
    global is_running,final_text
    is_running = False
    fls.set('Start Recording') 
    btn1.pack(padx=20)
    btn2.pack_forget()
    time_stamp = 'gui/record.txt'
    with open(time_stamp, 'w') as f:
        f.write(' '.join(final_text))
        f.close()

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
            print(status, file=sys.stderr)
        q.put(bytes(indata))

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        '-l', '--list-devices', action='store_true',
        help='show list of audio devices and exit')

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sounddevice.query_devices())
        parser.exit(0)
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[parser])

    parser.add_argument(
        '-f', '--filename', type=str, metavar='FILENAME',
        help='audio file to store recording to')

    parser.add_argument(
        '-m', '--model', type=str, metavar='MODEL_PATH',
        help='Path to the model')

    parser.add_argument(
        '-d', '--device', type=int_or_str,
        help='input device (numeric ID or substring)')

    parser.add_argument(
        '-r', '--samplerate', type=int, help='sampling rate')
    args = parser.parse_args(remaining)
    try:
        if args.model is None:
            args.model = "gui/model"
        if not os.path.exists(args.model):
            print ("Please download a model for your language from https://alphacephei.com/vosk/models")
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
                print('#' * 80)
                print('Press Ctrl+C to stop the recording')
                print('#' * 80)

                rec = vosk.KaldiRecognizer(model, args.samplerate)
                while is_running:
                    data = q.get()
                    if rec.AcceptWaveform(data):
                        fls2.set('Listening..')
                        text = ast.literal_eval(rec.FinalResult())['text']
                        global final_text
                        final_text.append(text)
                        new_text = ' '.join(final_text)
                        new_text = [new_text[i:i+110] for i in range(0, len(new_text), 110)]
                        fls3.set('\n'.join(new_text))
                        # print(new_text)
                        # pass
                    else:
                        # print(rec.PartialResult())
                        text = ast.literal_eval(rec.PartialResult())['partial']
                        text =  [text[i:i+110] for i in range(0, len(text), 110)]
                        fls2.set('\n'.join(text))
                    if dump_fn is not None:
                        print('helooooooooooooooooo')
                        dump_fn.write(data)
                else:
                    fls2.set('')
                    parser.exit(0)

    except KeyboardInterrupt:
        print('\nDone')
        parser.exit(0)
    except Exception as e:
        parser.exit(type(e).__name__ + ': ' + str(e))

# btn3 = Button(wrapper,text="Exit",command=lambda:exit())
# btn3.pack(padx=1)

btn1 = Button(wrapper,text="Record",command=record)
btn1.pack(padx=20)

btn2 = Button(wrapper,text="Stop",command=stop)


root.title('Speech to Text.')
root.geometry("720x600")
root.resizable(False,False)
root.mainloop()