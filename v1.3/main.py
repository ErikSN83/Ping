# 2022-03-20    ERSN    v.1.0   Ping
# 2022-03-22    ERSN    v.1.1   Ping and Ping_Gui classes changed.
# 2022-03-23    ERSN    v.1.2   Ping and Ping_Gui classes changed.
# 2022-03-24    ERSN    v.1.3   Ping class changed.

from ping_gui_grid import Ping_GUI
import tkinter as tk

if __name__ == "__main__":
    # configure the root window
    root = tk.Tk()
    root.title('Ping v1.3')
    root.resizable(False,False)

    # add GUI parts to root window
    #Ping_GUI(root).pack(side="top", fill="both", expand=True)
    Ping_GUI(root).pack()

    # run root window  mainloop
    root.mainloop()
