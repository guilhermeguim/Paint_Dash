import subprocess
import tkinter as tk
import requests
from time import sleep
import threading

class App:
    def __init__(self):
        self.flask_process = None
        self.starting = 0
        
        self.root = tk.Tk()
        

        self.create_gui()
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Lança a thread para verificar o status do sistema
        self.status_thread = threading.Thread(target=self.check_flask_status_thread)
        self.status_thread.daemon = True  # Define a thread como um daemon para que ela termine com o programa principal
        self.status_thread.start()
        
        self.root.mainloop()

    def create_gui(self):
        self.root.resizable(False,False)
        self.root.title("Sealer App - Manager")
        
        self.root.iconbitmap("d.ico")
        
        self.root.configure(background='#053266')
        self.root.geometry('300x100')
        
        title_text = tk.Label(text="Sealer App - Manager", bg='#053266', fg='#ffffff',font=("Arial", 18,'bold'))
        title_text.place(relx = 0.02, rely = 0.08, relwidth = 0.96, relheight = 0.30)
        
        lbl_text = tk.Label(text="App:", bg='#053266', fg='#ffffff',font=("Arial", 12,'bold'))
        lbl_text.place(relx = 0.01, rely = 0.55, relwidth = 0.20, relheight = 0.30)
        
        self.play_button = tk.Button(self.root, text="Start", command=self.play_button_callback)
        self.play_button.place(relx = 0.20, rely = 0.55, relwidth = 0.20, relheight = 0.30)

        self.pause_button = tk.Button(self.root, text="Stop", command=self.pause_button_callback)
        self.pause_button.place(relx = 0.43, rely = 0.55, relwidth = 0.20, relheight = 0.30)

        self.status_label = tk.Label(self.root, text="Status da Aplicação", bg='#053266')
        self.status_label.place(relx = 0.66, rely = 0.55, relwidth = 0.3, relheight = 0.30)
        
        self.status_label.config(text="Stopped", bg="red",font=("Arial", 12,'bold'))
        self.root.update()


    def check_flask_status_thread(self):
        while True:
            if self.is_flask_running():
                self.status_label.config(text="Running", bg="green",font=("Arial", 12,'bold'))
                self.starting = 0
                self.root.update()
            else:
                if self.starting == 1:
                    self.status_label.config(text="Starting", bg="yellow",font=("Arial", 12,'bold'))
                    self.root.update()
                else:
                    self.status_label.config(text="Stopped", bg="red",font=("Arial", 12,'bold'))
                    self.root.update()
            sleep(1)  # Aguarda 1 segundo antes de verificar novamente o status
            self.root.update()


    def is_flask_running(self):
        try:
            response = requests.get('http://127.0.0.1:5000')
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    def start_flask(self):
        
        self.flask_process = subprocess.Popen(['python', 'app.py'], creationflags=subprocess.CREATE_NO_WINDOW)
        self.root.update()

    def stop_flask(self):
        if self.flask_process:
            self.flask_process.kill()
            self.root.update()
        else:
            return 0

    def play_button_callback(self):
        if not self.is_flask_running():
            self.starting = 1
            self.start_flask()

    def pause_button_callback(self):
        self.stop_flask()

    def on_closing(self):
        # Calcula as coordenadas para centralizar a janela de confirmação
        
        
        newWindow = tk.Toplevel(self.root)
        newWindow.title("CLOSE")
        newWindow.iconbitmap("d.ico")
        newWindow.configure(background='white')
        wn = 340 # width for the Tk root
        hn = 90 # height for the Tk root
        
        x = self.root.winfo_x() + (self.root.winfo_width())
        y = self.root.winfo_y() + (self.root.winfo_height())
        
        # and where it is placed
        newWindow.geometry('%dx%d+%d+%d' % (wn, hn, x-320, y-45))
        newWindow.resizable(False,False)
        
        #newWindow.attributes("-toolwindow", True)
        newWindow.grab_set()
        newWindow.focus_set()

        def closeNew():
            newWindow.destroy()
    
        newWindow.protocol("WM_DELETE_WINDOW", self.disable_new_event)
        text = tk.Label(newWindow, text ='Closing this window would crash the application. \nAre you sure you want to continue?',bg='white',font=("Arial", 11))
        text.place(relx=0.02,rely=0.1, relwidth = 0.96, relheight = 0.40)
        exit_button = tk.Button(newWindow,text='YES',command=self.close_win)
        exit_button.place(relx=0.15,rely=0.6, relwidth = 0.30, relheight = 0.3)
        exit_button2 = tk.Button(newWindow,text='CANCEL',command=closeNew)
        exit_button2.place(relx=0.5,rely=0.6, relwidth = 0.30, relheight = 0.3)
        
    def close_win(self):
        self.stop_flask()
        self.root.destroy()
        
    def disable_new_event(self):
        pass
        


if __name__ == "__main__":
    app = App()