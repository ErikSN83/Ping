import tkinter as tk
from tkinter import filedialog
from ping import Ping

class Ping_GUI(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.ping_1 = None

        def browse_button(var_x):
            filename = filedialog.askdirectory()
            var_x.set(filename)

        def start(status_var):
            stop(status_var)
            #status_var.set('Status : pinger...')
            self.ping_1 = Ping(ip_list_var.get(), ping_delay_var.get(), stop_n_pings_var.get(), stop_n_hours_var.get(), save_path_var.get())
            self.ping_1.start_ping_sequence()

        def stop(status_var):
            if self.ping_1 != None:
                #status_var.set('Status : stop')
                self.ping_1.stop_ping_sequence()
                del self.ping_1
                self.ping_1 = None

        frame = tk.Frame(self)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # IP
        tk.Label(frame, text='IP Adresse',font=("Arial", 12)).grid(row=1, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        ip_list_var = tk.StringVar(frame, '')
        tk.Entry(frame,textvariable=ip_list_var,font=("Arial", 12)).grid(row=1, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Ping delay
        tk.Label(frame, text='Tid mellem ping',font=("Arial", 12)).grid(row=2, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        ping_delay_var = tk.IntVar(frame, 10)
        tk.Entry(frame,textvariable=ping_delay_var,font=("Arial", 12)).grid(row=2, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        tk.Label(frame, text='sek. (5 - 3600)',font=("Arial", 12)).grid(row=2, column=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Stop after n ping
        tk.Label(frame, text='Stop efter antal ping',font=("Arial", 12)).grid(row=3, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        stop_n_pings_var = tk.IntVar(frame, 0)
        tk.Entry(frame,textvariable=stop_n_pings_var,font=("Arial", 12)).grid(row=3, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        tk.Label(frame, text='0 = stopper ikke',font=("Arial", 12)).grid(row=3, column=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Stop efter n hours
        tk.Label(frame, text='Stop efter antal timer',font=("Arial", 12)).grid(row=4, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        stop_n_hours_var = tk.IntVar(frame, 0)
        tk.Entry(frame,textvariable=stop_n_hours_var,font=("Arial", 12)).grid(row=4, column=1, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        tk.Label(frame, text='0 = stopper ikke',font=("Arial", 12)).grid(row=4, column=2, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Save files path
        tk.Label(frame, text='Sti gem fil',font=("Arial", 12)).grid(row=5, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        save_path_var = tk.StringVar(frame, '')
        tk.Button(frame, text="Browse", font=("Arial", 12), command = lambda: browse_button(save_path_var)).grid(row=5, column=1, ipadx=5, ipady=5, padx=5, pady=5)

        tk.Label(frame,textvariable=save_path_var,font=("Arial", 12), wraplength=350, justify=tk.LEFT).grid(row=6, column=0, ipadx=5, ipady=5, padx=5, pady=5, columnspan=3, sticky=tk.W)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=7, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Start, stop
        tk.Button(frame, text="START", font=("Arial", 12), width=12, command = lambda: start(status_var)).grid(row=8, column=0, ipadx=5, ipady=5, padx=5, pady=5)
        tk.Button(frame, text="STOP", font=("Arial", 12), width=12, command = lambda: stop(status_var)).grid(row=8, column=1, ipadx=5, ipady=5, padx=5, pady=5)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=9, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Status
        status_var = tk.StringVar(frame)
        tk.Label(frame,textvariable=status_var,font=("Arial", 12)).grid(row=10, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)
        if self.ping_1 == None:
            status_var.set('Status : stoppet')
        elif self.ping_1 != None and self.ping_1.ping_sequence_active == False:
            status_var.set('Status : stoppet')
        elif self.ping_1 != None and self.ping_1.ping_sequence_active == True:
            status_var.set('Status : pinger...')

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=11, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        frame.pack()