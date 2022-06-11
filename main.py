from tkinter.messagebox import askyesno, showerror
import tkinter as tk
import tkinter.ttk as ttk
import sys

# General Settings
title_font = ('Arial', 30, 'bold')
std_font = ('Arial', 14)
big_font = ('Arial', 20)
player_colors = ['#a57dbb', '#4faf4d', '#f8c400', '#fc1d49', '#2c9efe']
symbol_path = '/symbols'


class Gui(tk.Frame):

    # Class variables

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        master.title("TFM Counter")

        # Attributes
        self.player_num = 0
        self.players = []

        # Widgets
        self.menubar = tk.Frame(self, relief=tk.GROOVE, bd=3)  # Makes a Frame for the menubar
        self.menubar.grid(row=0, column=0, columnspan=5, sticky=tk.N + tk.W + tk.E)

        # File Menu
        self.fl_menubutton = tk.Menubutton(self.menubar, text='File', underline=0)
        self.fl_menubutton.grid(row=0, column=0)

        self.fl_menu = tk.Menu(self.fl_menubutton, tearoff=0)
        self.fl_menu.add_command(label="Save")
        self.fl_menu.add_command(label="Save As...")
        self.fl_menu.add_command(label="Quit", command=self.quit)

        # Player Menu
        self.pl_menubutton = tk.Menubutton(self.menubar, text='Players', underline=0)
        self.pl_menubutton.grid(row=0, column=1)

        self.pl_menu = tk.Menu(self.pl_menubutton, tearoff=0)
        self.pl_menu.add_command(label="Add Player...", command=self.add_player)
        self.pl_menu.add_command(label="Remove Player...", command=self.remove_player)
        self.pl_menu.add_command(label="Clear Scores", command=self.clear_scores)

        # About Menu
        self.about_menubutton = tk.Menubutton(self.menubar, text="About", underline=0)
        self.about_menubutton.grid(row=0, column=2)

        self.about_menu = tk.Menu(self.about_menubutton, tearoff=0)
        self.about_menu.add_command(label="About TFM Counter", command=self.show_about)

        # Add sub-menus to the top menu
        self.fl_menubutton.config(menu=self.fl_menu)
        self.pl_menubutton.config(menu=self.pl_menu)
        self.about_menubutton.config(menu=self.about_menu)

        # Geometry Management

        # Binds/Hotkeys
        self.master.bind('<Control-p>', lambda e: self.add_player())  # Assigns "Ctrl+p" to "Add Player".
        self.master.bind('<Control-r>', lambda e: self.remove_player())  # Assigns "Ctrl+r" to "Remove Player".
        self.master.bind('<Control-q>', lambda e: self.clear_scores())  # Assigns "Ctrl+q" to "Clear Scores".
        self.master.bind('<Control-t>', lambda e: self.change_player_focus())

    def add_player(self):
        if self.player_num < 5:
            player_name = 'Player ' + str(self.player_num + 1)
            player = Player(self, player_name)
            player.grid(row=1, column=self.player_num)

            # Append the player to the list of all players
            self.players.append(player)
            self.player_num += 1

            print("Currently playing: {}".format(self.player_num))
            print(self.players)
        else:
            showerror('Maximum amount of players reached!', 'You cannot add more than 5 players.')

    def remove_player(self):
        last_player = self.players[-1]
        if askyesno("Remove Player", "Are you sure you want to remove {}?".format(last_player.name)):
            last_player.destroy()
            print("{} removed!".format(last_player.name))
            self.players.remove(last_player)
            self.player_num -= 1
            print("Currently playing: {}".format(self.player_num))
            print(self.players)
        else:
            pass

    def clear_scores(self):
        if askyesno("Clear Scores", "Are you sure you want clear the scoreboard?"):
            for player in self.players:
                player.var_list[0].set(20)
                for var in player.var_list[1:]:
                    var.set(0)
                player.calculate_sum()
            print("Score values returned to the defaults for all players.")
        else:
            pass

    def show_about(self):
        print("Not implemented yet!")
        pass

    def change_player_focus(self):
        current_focus = self.focus_get()
        print(current_focus.grid_info()['row'])  # Returns the row of the current widget.
        focus_parent = str(current_focus.master)
        focus_index = int(focus_parent.split("Player ")[1])
        if focus_index == self.player_num:
            focus_index_right = 0
        else:
            focus_index_right = focus_index
        self.players[focus_index_right].focus_set()

    def quit(self):
        # Terminate the software
        sys.exit()


class Player(tk.Frame):
    def __init__(self, master, name):
        tk.Frame.__init__(self, master, bd=3, relief=tk.GROOVE)
        self.master = master
        self.number = int(name[-1])
        self.name = name

        # tk Variables
        self.name_var = tk.StringVar(value=self.name)

        self.tr_var = tk.IntVar()
        self.mls_var = tk.IntVar()
        self.awd_var = tk.IntVar()
        self.vp_var = tk.IntVar()
        self.green_var = tk.IntVar()
        self.city_var = tk.IntVar()
        self.sum_var = tk.IntVar()

        self.var_list = [self.tr_var,
                         self.mls_var,
                         self.awd_var,
                         self.vp_var,
                         self.green_var,
                         self.city_var,
                         self.sum_var,
                         ]

        # Images
        self.tr_sbl = tk.PhotoImage(file='./symbols/tr_sbl.gif')
        self.milestones_sbl = tk.PhotoImage(file='./symbols/milestones_sbl.gif')
        self.awards_sbl = tk.PhotoImage(file='./symbols/awards_sbl.gif')
        self.vp_sbl = tk.PhotoImage(file='./symbols/vp_sbl.gif')
        self.city_sbl = tk.PhotoImage(file='./symbols/city_sbl.gif')
        self.greenery_sbl = tk.PhotoImage(file='./symbols/greenery_sbl.gif')

        # Widgets
        # Player name
        self.name_lbl = tk.Label(self, textvariable=self.name_var, fg=player_colors[self.number - 1], font=title_font)

        # Point related widgets
        self.tr_lbl = tk.Label(self, text='TR', image=self.tr_sbl)
        self.tr_spn = tk.Spinbox(self, textvariable=self.tr_var, from_=20, to=100, increment=1, justify=tk.CENTER)
        self.mls_lbl = tk.Label(self, text='Milestones', image=self.milestones_sbl)
        self.mls_spn = tk.Spinbox(self, textvariable=self.mls_var, from_=0, to=15, increment=5, justify=tk.CENTER)
        self.awd_lbl = tk.Label(self, text='Awards', image=self.awards_sbl)
        self.awd_chk = tk.Spinbox(self, textvariable=self.awd_var, values=(0, 2, 4, 5, 6, 7, 9, 10, 12, 15),
                                  justify=tk.CENTER)
        self.vp_lbl = tk.Label(self, text='VP', image=self.vp_sbl)
        self.vp_spn = tk.Spinbox(self, textvariable=self.vp_var, from_=-20, to=120, increment=1, justify=tk.CENTER)
        self.green_lbl = tk.Label(self, text='Greeneries', image=self.greenery_sbl)
        self.green_spn = tk.Spinbox(self, textvariable=self.green_var, from_=0, to=50, increment=1, justify=tk.CENTER)
        self.city_lbl = tk.Label(self, text='Cities', image=self.city_sbl)
        self.city_spn = tk.Spinbox(self, textvariable=self.city_var, from_=0, to=100, increment=1, justify=tk.CENTER)

        # Point sum total
        self.sum_lbl = tk.Label(self, text='Total', font=big_font)
        self.sum_total = tk.Label(self, textvariable=self.sum_var, font=big_font)

        # Store point related widgets in a list for easier management.
        # The labels and spinboxes are separated into different lists.
        self.labels = [self.tr_lbl,
                       self.mls_lbl,
                       self.awd_lbl,
                       self.vp_lbl,
                       self.green_lbl,
                       self.city_lbl, ]

        self.spinboxes = [self.tr_spn,
                          self.mls_spn,
                          self.awd_chk,
                          self.vp_spn,
                          self.green_spn,
                          self.city_spn, ]

        # Separators
        self.sep1 = ttk.Separator(self, orient=tk.HORIZONTAL)
        self.sep2 = ttk.Separator(self, orient=tk.HORIZONTAL)
        # Clear score
        self.clr_score = tk.Button(self, text='Clear Score', command=self.clear_score)

        # Geometry Management
        # Place the player label.
        self.name_lbl.grid(row=0, column=0, columnspan=2)

        self.sep1.grid(row=1, column=0, columnspan=2, padx=3, pady=5, sticky=tk.W + tk.E)  # Separator

        # Place the point related widgets and adjust their font.
        cur_row = 2
        cur_column = 0
        for widget in self.labels:
            widget.config(font=std_font, padx=3)
            widget.grid(row=cur_row, column=cur_column)
            cur_row += 1
        cur_column += 1
        cur_row = 2
        for widget in self.spinboxes:
            widget.config(font=std_font, width=6, command=self.calculate_sum)
            widget.bind('<Return>', self.calculate_sum)
            widget.grid(row=cur_row, column=cur_column, sticky=tk.W)
            cur_row += 1

        self.sep2.grid(row=8, column=0, columnspan=2, padx=3, pady=5, sticky=tk.W + tk.E)  # Separator

        self.sum_lbl.grid(row=9, column=0, sticky=tk.W)
        self.sum_total.grid(row=9, column=1)
        self.clr_score.grid(row=11, column=0, columnspan=2)

        self.calculate_sum()

        # Binds
        self.name_lbl.bind("<Button-1>", lambda event: self.change_player_color())

    def calculate_sum(self):
        total = 0
        for widget in self.spinboxes:
            try:
                total += int(widget.get())
            except ValueError:
                total += 0
        self.sum_var.set(total)

    def change_player_color(self):
        print("You just clicked the label")

    def clear_score(self):
        if askyesno("Clear Score", "Are you sure you want clear {}'s score?".format(self.name)):
            self.var_list[0].set(20)
            for var in self.var_list[1:]:
                var.set(0)
            self.calculate_sum()
            print("Score values returned to the defaults.")
        else:
            pass

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name


if __name__ == '__main__':
    root = tk.Tk()
    app = Gui(root)
    app.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
