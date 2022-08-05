from tkinter.messagebox import askyesno, showerror, showinfo
from player import Player
import tkinter as tk
import sys


class Gui(tk.Frame):

    # Class variables

    def __init__(self, master):
        tk.Frame.__init__(self, master)

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
        # self.fl_menu.add_command(label="Save")
        # self.fl_menu.add_command(label="Save As...")
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
        self.master.bind('<Control-a>', lambda e: self.add_player())  # Assigns "Ctrl+a" to "Add Player".
        self.master.bind('<Control-A>', lambda e: self.add_player())  # Assigns "Ctrl+A" to "Add Player".
        self.master.bind('<Control-r>', lambda e: self.remove_player())  # Assigns "Ctrl+r" to "Remove Player".
        self.master.bind('<Control-R>', lambda e: self.remove_player())  # Assigns "Ctrl+r" to "Remove Player".
        self.master.bind('<Control-q>', lambda e: self.clear_scores())  # Assigns "Ctrl+q" to "Clear Scores".
        self.master.bind('<Control-Q>', lambda e: self.clear_scores())  # Assigns "Ctrl+Q" to "Clear Scores".
        self.master.bind('<Right>', lambda e: self.focus_right())  # Use the right arrow to shift focus right.
        self.master.bind('<Left>', lambda e: self.focus_left())  # Use the left arrow to shift the focus left.

        # Add the first player automatically when the window is created.
        self.add_player()

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
        content = "TMF Counter\nVersion: 1.0\nDeveloped by Nick Konstantinidis\nnickonstan@gmail.com"
        showinfo('About', content, parent=self)

    def focus_right(self):
        current_focus = self.focus_get()
        focus_parent = str(current_focus.master)
        player_index = int(focus_parent.split("Player ")[1]) - 1
        target_widget = str(current_focus).split('.')[3]
        if player_index == len(self.players) - 1:
            target_index = 0
            self.players[target_index].children[f'{target_widget}'].focus_set()
        else:
            target_index = player_index + 1
            self.players[target_index].children[f'{target_widget}'].focus_set()

    def focus_left(self):
        current_focus = self.focus_get()
        focus_parent = str(current_focus.master)
        player_index = int(focus_parent.split("Player ")[1]) - 1
        target_widget = str(current_focus).split('.')[3]
        if player_index == 0:
            target_index = len(self.players) - 1
            self.players[target_index].children[f'{target_widget}'].focus_set()
        else:
            target_index = player_index - 1
            self.players[target_index].children[f'{target_widget}'].focus_set()

    def quit(self):
        # Terminate the software
        sys.exit()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("TFM Counter")
    root.minsize(163, 480)
    root.resizable(False, False)
    app = Gui(root)
    app.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()
