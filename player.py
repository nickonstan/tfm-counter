from tkinter.messagebox import askyesno
import settings
import tkinter as tk
import tkinter.ttk as ttk


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
        # Player Name
        self.name_lbl = tk.Label(self, textvariable=self.name_var, fg=settings.player_colors[self.number - 1],
                                 font=settings.title_font)

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
        self.sum_lbl = tk.Label(self, text='Total', font=settings.big_font)
        self.sum_total = tk.Label(self, textvariable=self.sum_var, font=settings.big_font)

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
            widget.config(font=settings.std_font, padx=3)
            widget.grid(row=cur_row, column=cur_column)
            cur_row += 1
        cur_column += 1
        cur_row = 2
        for widget in self.spinboxes:
            widget.config(font=settings.std_font, width=6, command=self.calculate_sum)
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
        if not PlayerEdit.editor_on:
            PlayerEdit(self)
            PlayerEdit.editor_on = True

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


class PlayerEdit(tk.Toplevel):
    editor_on = False

    def __init__(self, player):
        tk.Toplevel.__init__(self)
        self.protocol('WM_DELETE_WINDOW', self.set_editor_off)

        self.title('Edit Player')
        self.player = player
        self.player_name = tk.StringVar(value=player.name)

        self.picker_size = 32
        self.padding_size = 3

        self.pl_name_lbl = tk.Label(self, text='Player Name')
        self.pl_name = tk.Entry(self, textvariable=self.player_name)
        self.pl_color_lbl = tk.Label(self, text='Player Color')
        self.pl_color_canvas = tk.Canvas(self, width=self.picker_size * 5 + self.padding_size * 4,
                                         height=self.picker_size, relief=tk.GROOVE)

        self.create_color_picker(self.picker_size, self.padding_size)

        # Geometry Management
        self.pl_name_lbl.grid(row=0, column=0, sticky=tk.W)
        self.pl_name.grid(row=0, column=1)
        self.pl_color_lbl.grid(row=1, column=0, sticky=tk.W)
        self.pl_color_canvas.grid(row=1, column=1, sticky=tk.W)

        # Binds
        self.bind('<Return>', lambda e: self.change_player_name(self.player))
        self.bind('<ButtonPress-1>', lambda e: self.change_player_color(self.player))

    def create_color_picker(self, size, padding):
        x = 0
        for i in range(5):
            self.pl_color_canvas.create_rectangle(x, 0, x + size, size, width=0, fill=settings.player_colors[i])
            x += (size + padding)

    def change_player_name(self, player):
        player.name_var.set(self.pl_name.get())

    def change_player_color(self, player):
        """ Changes the player color when clicking on one of the color tiles."""
        color_tile = self.pl_color_canvas.find_withtag('current')
        if color_tile:
            player.name_lbl.configure(fg=self.pl_color_canvas.itemcget(color_tile, 'fill'))

    def set_editor_off(self):
        """ Sets the editor as "off" and destroys the window."""
        PlayerEdit.editor_on = False
        self.destroy()
