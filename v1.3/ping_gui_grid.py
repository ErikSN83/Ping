# 2022-03-20    ERSN    v.1.0   Ping
# 2022-03-22    ERSN    v.1.1   Code for the .after() function that keeps the status label text updated rewritten.
# 2022-03-23    ERSN    v.1.2   'IP Adresse' -> 'IP Adresse(r)'. Added check that IP list and save path not '' before accepting start().

import tkinter as tk
from tkinter import filedialog
from ping import Ping

class Ping_GUI(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.ping_1 = None

        def browse(var_x):
            filename = filedialog.askdirectory()
            var_x.set(filename)

        def start():
            stop()
            if save_path_var.get() != '' and ip_list_var.get() != '':
                self.ping_1 = Ping(ip_list_var.get(), ping_delay_var.get(), stop_n_pings_var.get(), stop_n_hours_var.get(), save_path_var.get())
                self.ping_1.start_ping_sequence()

        def stop():
            if self.ping_1 != None:
                self.ping_1.stop_ping_sequence()
                del self.ping_1
                self.ping_1 = None

        def status(status_var_x):
            if not self.ping_1:
                status_var_x.set('Status : stoppet')
            elif self.ping_1 and not self.ping_1.ping_sequence_active:
                status_var_x.set('Status : stoppet')
            elif self.ping_1 and self.ping_1.ping_sequence_active:
                status_var_x.set('Status : pinger...')
            self.parent.after(ms=1000, func=lambda n=status_var_x: status(n)) # assigns the .after() function to the root tk.Tk() instance from main class. Best way according to reddit.
            #self.after(ms=1000, func=lambda n=status_var_x: status(n)) # assigns the .after() method to this class(?) instance.

        frame = tk.Frame(self)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=0, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # IP
        tk.Label(frame, text='IP Adresse(r)',font=("Arial", 12)).grid(row=1, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        ip_list_var = tk.StringVar(frame, '8.8.8.8')
        tk.Entry(frame,textvariable=ip_list_var,font=("Arial", 12),width=35).grid(row=1, column=1, ipadx=5, ipady=5, padx=5, pady=5, columnspan=2, sticky=tk.W)

        # Ping delay
        tk.Label(frame, text='Tid mellem ping',font=("Arial", 12)).grid(row=2, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        ping_delay_var = tk.IntVar(frame, 5)
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
        tk.Button(frame, text="Browse", font=("Arial", 12), command = lambda: browse(save_path_var)).grid(row=5, column=1, ipadx=5, ipady=5, padx=5, pady=5)

        tk.Label(frame,textvariable=save_path_var,font=("Arial", 12), wraplength=350, justify=tk.LEFT).grid(row=6, column=0, ipadx=5, ipady=5, padx=5, pady=5, columnspan=3, sticky=tk.W)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=7, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Start, stop
        tk.Button(frame, text="START", font=("Arial", 12), width=12, command = lambda: start()).grid(row=8, column=0, ipadx=5, ipady=5, padx=5, pady=5)
        tk.Button(frame, text="STOP", font=("Arial", 12), width=12, command = lambda: stop()).grid(row=8, column=1, ipadx=5, ipady=5, padx=5, pady=5)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=9, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        # Status
        status_var = tk.StringVar(frame)
        tk.Label(frame,textvariable=status_var,font=("Arial", 12)).grid(row=10, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)
        status(status_var)

        # Empty space
        tk.Label(frame, text='',font=("Arial", 12)).grid(row=11, column=0, ipadx=5, ipady=5, padx=5, pady=5, sticky=tk.W)

        frame.pack()
