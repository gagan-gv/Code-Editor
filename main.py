from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
from idlelib.percolator import Percolator
from idlelib.colorizer import ColorDelegator
import subprocess, os

file_path = ''

def set_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('All Files', '*.*'), ('Python Files', '*.py'), ('Java Files', '*.java'), ('R files', '*.r'), ('C Files', '*.c'), ('C++ Files', '*.cpp'), ('Go Files', '*.go')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_path(path)

def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('All Files', '*.*'), ('Python Files', '*.py'), ('Java Files', '*.java'), ('R files', '*.r'), ('C Files', '*.c'), ('C++ Files', '*.cpp'), ('Go Files', '*.go')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_path(path)

def exec(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    output, error = process.communicate()

    code_output.insert('1.0', output)
    code_output.insert('1.0', error)

def run():
    if file_path == '':
        messagebox.showwarning('Editor Warning', 'Please save the code')
        return
    
    fn, file_extension = os.path.splitext(file_path)
    file_name = os.path.basename(file_path)
    if file_extension == '.py':
        command = f'py {file_name}'
        exec(command)
    elif file_extension == '.java':
        command = f'javac {file_name}'
        exec(command)
        command = 'java {fn}'
        exec(command)
    elif file_extension == '.r':
        command = f'Rscript {file_name}'
        exec(command)
    elif file_extension == '.c' or file_extension == '.cpp':
        command = f'g++ {file_name}'
        exec(command)
    elif file_extension == '.go':
        command = f'go run {file_name}'
        exec(command)

tk = Tk()
tk.title("Codon")
tk.iconbitmap('logo.ico')

menu_bar = Menu(tk)

menu = Menu(menu_bar, tearoff=0)
menu.add_command(label='Open', command=open_file)
menu.add_command(label='Save', command=save_as)
menu.add_command(label='Exit', command=exit)

menu_bar.add_cascade(label='File', menu=menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run', command=run)
menu_bar.add_cascade(label='Run File', menu=run_bar)

tk.config(menu=menu_bar)

editor = Text(height=35, width=200, fg='#f5f5f5', bg='#303030', insertbackground='#f5f5f5')
editor.pack()
Percolator(editor).insertfilter(ColorDelegator())

code_output = Text(height=15, width=200, fg='#f5f5f5', bg='#303030', insertbackground='#f5f5f5')
code_output.pack()

tk.mainloop()