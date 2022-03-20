from ping_gui_grid import Ping_GUI
import tkinter as tk

if __name__ == "__main__":
    # configure the root window
    root = tk.Tk()
    root.title('Ping v1.0')
    root.resizable(False,False)

    # add GUI parts to root window
    Ping_GUI(root).pack(side="top", fill="both", expand=True)

    # run root window  mainloop
    root.mainloop()