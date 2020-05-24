import tkinter as tk
from tkinter import ttk
import numpy as np
import scipy.special as sc

class StartCombobox:
    def __init__(self, label, values, column, width, initial_state, bg='SystemButtonFace'):
        self.frame = tk.Frame(start_columns[column], pady= 5, padx= 0)
        self.frame.pack(side= tk.TOP, fill="x")

        self.label = tk.Label(self.frame, text=label, bg= bg)
        self.combobox = ttk.Combobox(self.frame, values=values, width=width, text= label)
        self.combobox.pack(side=tk.RIGHT)
        self.label.pack(side=tk.LEFT)

        self.combobox.current(initial_state)

class ElectionRound:
    def __init__(self, round, red, blu, pres):
        self.round = round
        self.frame = tk.Frame(elections_tab, bd=2, relief="groove")
        self.frame.pack(side= tk.TOP)

        self.n_columns = 5
        self.columns = [tk.Frame(self.frame) for i in range(self.n_columns)]
        for i in range(self.n_columns):
            self.columns[i].pack(side= tk.LEFT, padx= 10)

        #round_n frame
        self.round_n_frame= tk.Frame(self.columns[0])
        self.round_n_frame.pack()

        self.round_n_label= tk.Label(self.round_n_frame, text= self.round+1, padx= 0, font=(None, 15))
        self.round_n_label.grid(row=0, column= 0)

        #elections frame
        self.elections_frame= tk.Frame(self.columns[1])
        self.elections_frame.pack()

        self.pres= ttk.Combobox(self.elections_frame, values= chairs, width= 5)
        self.chanc= ttk.Combobox(self.elections_frame, values= chairs, width= 5)
        self.pres.grid(row= 0, column=0)
        self.chanc.grid(row= 1, column=0)
        # CreateToolTip(self.pres, "President")
        # CreateToolTip(self.chanc, "Chancellor")

        self.pres.current(pres)

        #deck frame
        self.deck_frame= tk.Frame(self.columns[2])
        self.deck_frame.pack()

        self.red= tk.IntVar()
        self.blu= tk.IntVar()

        self.red.set(red)
        self.blu.set(blu)

        self.blu_entry = tk.Entry(self.deck_frame, width = 5, textvariable= self.blu, bg= 'LightBlue1')
        self.red_entry = tk.Entry(self.deck_frame, width = 5, textvariable= self.red, bg='Pink')
        self.blu_entry.grid(row=0, column=1)
        self.red_entry.grid(row=1, column=1)

        self.blu_down= tk.Button(self.deck_frame, text="-",
                                 command= lambda: [self.blu.set(self.blu.get()-1), self.updatepercent()], width= 1)
        self.blu_up= tk.Button(self.deck_frame, text="+",
                               command= lambda: [self.blu.set(self.blu.get()+1), self.updatepercent()], width= 1)
        self.blu_down.grid(row=0, column=0)
        self.blu_up.grid(row=0, column= 2)

        self.red_down= tk.Button(self.deck_frame, text="-",
                                 command= lambda: [self.red.set(self.red.get()-1), self.updatepercent()], width= 1)
        self.red_up= tk.Button(self.deck_frame, text="+",
                               command= lambda: [self.red.set(self.red.get()+1), self.updatepercent()], width= 1)
        self.red_down.grid(row=1, column=0)
        self.red_up.grid(row=1, column=2)

        self.red_entry.bind('<FocusOut>', lambda _: self.updatepercent())
        self.blu_entry.bind('<FocusOut>', lambda _: self.updatepercent())
        self.red_entry.bind('<Return>', lambda _: self.updatepercent())
        self.blu_entry.bind('<Return>', lambda _: self.updatepercent())

        #votes frame
        self.vote_frame= tk.Frame(self.columns[3])
        self.vote_frame.pack(side= tk.TOP)

        self.votes= [tk.IntVar() for i in range(int(n_players.combobox.get()))]
        self.votes_check = [tk.Checkbutton(self.vote_frame, variable= self.votes[i])
                            for i in range(int(n_players.combobox.get()))]

        for i in range(int(n_players.combobox.get())):
            self.votes_check[i].pack(side= tk.LEFT)
            self.votes[i].set(0)
            CreateToolTip(self.votes_check[i], chairs[i])

        #play frame
        self.play_frame= tk.Frame(self.columns[3])
        self.play_frame.pack(side= tk.BOTTOM)

        self.play = tk.IntVar()
        self.play.set(-1)

        self.play_list= ['R', 'B', 'Pass']
        self.play_colors= ['Pink', 'LightBlue1', 'White']

        self.play_buttons = [tk.Radiobutton(self.play_frame, text=self.play_list[i], bg=self.play_colors[i],
                                            width=5, variable=self.play, value=i, indicatoron=0, selectcolor= self.play_colors[i],
                                            command= lambda: self.playbuttonpressed())
                             for i in range(len(self.play_list))]

        for i in range(len(self.play_buttons)):
            self.play_buttons[i].pack(side= tk.LEFT)


        #pres_claim frame
        self.pres_claim_frame= tk.Frame(self.columns[4])
        self.pres_claim_frame.pack(side= tk.TOP)

        self.pres_claim = tk.IntVar()
        self.pres_claim.set(-1)

        self.value_pres_claim = [['RRR', 'Pink'],
                                 ['RRB', 'Lavender Blush'],
                                 ['RBB', 'Alice Blue'],
                                 ['BBB', 'LightBlue1']]

        self.pres_radios = [tk.Radiobutton(self.pres_claim_frame, text="(%)", bg=self.value_pres_claim[i][1], width=5,
                                           variable=self.pres_claim, value=i, indicatoron=0, selectcolor= self.value_pres_claim[i][1],
                                           command=lambda: electionradioclicked(self.round,
                                                                                self.blu.get(),
                                                                                self.red.get(),
                                                                                self.pres_claim.get()))
                            for i in range(len(self.value_pres_claim))]
        for i in range(len(self.value_pres_claim)):
            self.pres_radios[i].pack(side= tk.LEFT)
            CreateToolTip(self.pres_radios[i], self.value_pres_claim[i][0])

        #chanc_claim frame
        self.chanc_claim_frame= tk.Frame(self.columns[4])
        self.chanc_claim_frame.pack(side= tk.BOTTOM)

        self.value_chanc_claim = [['RR', 'pink'],
                                  ['RB', 'snow'],
                                  ['BB', 'LightBlue1']]

        self.chanc_claim = tk.IntVar()
        self.chanc_claim.set(-1)

        self.chanc_radios = [tk.Radiobutton(self.chanc_claim_frame, text="(%)", bg=self.value_chanc_claim[i][1], width=5,
                                            variable=self.chanc_claim, value=i, indicatoron=0, selectcolor= self.value_chanc_claim[i][1])
                             for i in range(len(self.value_chanc_claim))]
        for i in range(len(self.value_chanc_claim)):
            self.chanc_radios[i].pack(side= tk.LEFT)
            CreateToolTip(self.chanc_radios[i], self.value_chanc_claim[i][0])

    def updatepercent(self):
        self.percents = [1, 1, 1, 1]
        for j in range(4):
            self.total = self.blu.get() + self.red.get()
            if (3-j) > self.red.get() or j > self.blu.get():
                self.percents[j] = 0
            else:
                for k in range(3 - j):
                    self.percents[j] *= (self.red.get() - k) / self.total
                    self.total -= 1
                for k in range(j):
                    self.percents[j] *= (self.blu.get() - k) / self.total
                    self.total -= 1
                if 0<j<3:
                    self.percents[j] *= 3
            self.percents[j] *= 100
            self.pres_radios[j].config(text=('{p:=.1f}%').format(p= self.percents[j]))

    def playbuttonpressed(self):
        self.frame.config(bg= self.play_colors[int(self.play.get())])
        for i in self.columns:
            i.config(bg= self.play_colors[int(self.play.get())])
        self.round_n_label.config(bg= self.play_colors[int(self.play.get())])
        for i in self.votes_check:
            i.config(bg= self.play_colors[int(self.play.get())])

        if self.play.get() == 2: # if 'pass' -> desactivate claims
            self.pres_claim.set(-1)
            self.chanc_claim.set(-1)
            for i in self.pres_radios:
                i.config(state= 'disabled')
            for i in self.chanc_radios:
                i.config(state='disabled')
            self.updatepercent()
        else:
            for i in self.pres_radios:
                i.config(state= 'normal')
            for i in self.chanc_radios:
                i.config(state='normal')

        if actual_round > self.round:
            for i in self.play_buttons:
                i.config(state='disabled')


class PlayersCell:
    def __init__(self, i, j):
        self.row= i + 1
        self.column= j + 1
        self.value= 1

        self.print = tk.StringVar()

        self.cell= tk.Label(players_table_frame, textvariable=self.print, width=3)
        self.cell.grid(row= self.row, column= self.column)

        self.style()

        self.cell.bind("<Enter>", lambda _: [players_table_headers[0][self.column-1].config(bg= self.bg, fg= self.fg),
                                             players_table_headers[1][self.row-1].config(bg= self.bg, fg=self.fg),
                                             self.cell.config(relief="groove")])
        self.cell.bind("<Leave>", lambda _: [players_table_headers[0][self.column-1].config(bg= 'SystemButtonFace', fg='Black'),
                                             players_table_headers[1][self.row-1].config(bg= 'SystemButtonFace', fg='Black'),
                                             self.cell.config(relief="flat")])

        self.display()

    def style(self):
        self.bg= rgb((int(255*(1-self.value)), int(255-(128*self.value)), int(255*(1-self.value))))
        if self.value < 0.5:
            self.fg= 'black'
        else:
            self.fg= 'white'
        self.cell.config(bg= self.bg, fg= self.fg)
        self.print.set("{:0.2f}".format(self.value).lstrip('0'))

    def display(self):
        if self.row > self.column:
            if players_checks_display[0].get() == 1:
                self.cell.grid()
            else:
                self.cell.grid_remove()
        elif self.row == self.column:
            if players_checks_display[1].get() == 1:
                self.cell.grid()
            else:
                self.cell.grid_remove()
        else:
            if players_checks_display[2].get() == 1:
                self.cell.grid()
            else:
                self.cell.grid_remove()

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text= text

    def ShowToolTip(self):
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 7
        y = y + cy + self.widget.winfo_rooty() - 14
        self.frame= tk.Toplevel(self.widget)
        self.frame.wm_overrideredirect(1)
        self.frame.wm_geometry('+{}+{}'.format(x,y))
        self.label = tk.Label(self.frame, text=self.text, justify=tk.LEFT, background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                              font=("tahoma", "8", "normal"))
        self.label.pack(ipadx=1)

    def HideToolTip(self,):
        self.frame.destroy()

########################################
########################################


def tipbox(widget, text):
    pass

#Start Functions
def NPlayersChanged(n):
    player_position.combobox.config(values= [i + 1 for i in range(n)])
    if int(player_position.combobox.get()) > int(n_players.combobox.get()):
        player_position.label.config(bg= 'red')
    else:
        player_position.label.config(bg='SystemButtonFace')

def PlayerRoleChanged():
    pass

def UpdateChairs(n_players):
    global chairs
    for i in range(n_players):
        if i+1 == int(player_position.combobox.get()):
            chairs.append('{} (You)'.format(i+1))
        else:
            chairs.append(i+1)

def initialconditions(n_players):
    global actual_round
    global chairs
    global votes_weight
    global votes_pvp
    global similarity
    actual_round = 0  # integer
    chairs = []  # 1-D array
    votes_weight = np.array([])  # 1-D array
    votes_pvp = [[[] for j in range(i, n_players)] for i in range(1, n_players)]  # 3-D array
    similarity = []  # 2-D array


def newgame(n_players):
    global actual_round
    global rounds
    global votes_pvp
    initialconditions(n_players)
    UpdateChairs(n_players)
    for i in rounds:
        i.frame.destroy()
    rounds.clear()
    rounds= [ElectionRound(0, int(n_red.combobox.get()), int(n_blu.combobox.get()), 0)]
    elections_label[3].config(padx=(14 * n_players) - 14)
    rounds[actual_round].updatepercent()
    players_table_frame.destroy()
    players_checks_frame.destroy()
    rounds[actual_round].chanc.focus_set()
    drawplayerstable(n_players)


#Election functions
def electionradioclicked(round, blu, red, claim):
    global actual_round
    if round < actual_round:
        rounds[round+1].red.set(red - 3 + claim)
        rounds[round+1].blu.set(blu - claim)
        rounds[round+1].updatepercent(int(n_players.combobox.get()))


def electionentrychange(i):
    rounds[i].updatepercent(int(n_players.combobox.get()))


def nextelections(n_players):
    global actual_round
    global rounds
    global election_button_frame
    global election_button
    if rounds[actual_round].pres_claim.get() < 0:
        rounds.append(ElectionRound(actual_round + 1,
                                    rounds[actual_round].red.get(),
                                    rounds[actual_round].blu.get(),
                                    (rounds[actual_round].pres.current() + 1) % n_players))
    else:
        rounds.append(ElectionRound(actual_round + 1,
                                    rounds[actual_round].red.get() - 3 + rounds[actual_round].pres_claim.get(),
                                    rounds[actual_round].blu.get() - rounds[actual_round].pres_claim.get(),
                                    (rounds[actual_round].pres.current() + 1) % n_players))
    for i in rounds[actual_round].votes_check:
        i.config(state= 'disabled')
    if rounds[actual_round].play.get() >= 0:
        for i in rounds[actual_round].play_buttons:
            i.config(state= 'disabled')
    calcvotespvp()
    actual_round += 1
    rounds[actual_round].updatepercent()
    rounds[actual_round].chanc.focus_set()




# Players functions
def drawplayerstable(n_players):
    global players_table_frame
    global players_table_headers
    global players_table_cells

    players_table_frame = tk.Frame(players_tab, bd=2, relief="groove")
    players_table_frame.pack(side=tk.TOP)

    players_corner = tk.Label(players_table_frame, text='', width=3, bd=2, relief="groove")
    players_table_headers = [[tk.Label(players_table_frame, text=j + 1, width=3, bd=2, relief="groove") for j in range(n_players)] for i in range(2)]
    players_corner.grid(row=0, column=0)
    for i in range(len(players_table_headers[0])):
        players_table_headers[0][i].grid(row=0, column=i + 1)
        players_table_headers[1][i].grid(row=i + 1, column=0)
    players_table_cells = [[PlayersCell(i, j) for j in range(n_players)] for i in range(n_players)]
    drawplayerschecks(n_players)


def drawplayerschecks(n_players):
    global players_checks_frame
    global players_checks
    global players_checks_display
    players_checks_frame = tk.Frame(players_tab)
    players_checks_frame.pack(side=tk.TOP)
    players_checks_list = [['Bottom triangle', players_checks_display[0]],
                           ['Diagonal', players_checks_display[1]],
                           ['Top triangle', players_checks_display[2]]]
    players_checks = [tk.Checkbutton(players_checks_frame, text=i[0], variable= i[1], command= lambda: playerscheckdisplay()) for i in players_checks_list]
    for i in players_checks:
        i.pack(side=tk.LEFT)
    players_checks_frame.focus()


def playerscheckdisplay():
    global players_table_cells
    for i in players_table_cells:
        for j in i:
            j.display()


def rgb(rgb):
    return "#%02x%02x%02x" % rgb


def calcvotespvp():
    global votes_weight
    global votes_pvp
    global rounds
    global actual_round
    global players_table_cells

    n_ja = sum([i.get() for i in rounds[actual_round].votes])
    votes_weight = np.append(votes_weight, int(sc.binom(int(n_players.combobox.get()), n_ja)))

    n_ballots = len(rounds[actual_round].votes)
    for i in range(n_ballots):
        for j in range(i+1, n_ballots):
            if int(rounds[actual_round].votes[i].get()) == int(rounds[actual_round].votes[j].get()):
                votes_pvp[i][j-i-1].append(1)
            else:
                votes_pvp[i][j-i-1].append(0)

            players_table_cells[i][j].value = (votes_weight @ votes_pvp[i][j-i-1]) / sum(votes_weight)
            players_table_cells[i][j].style()
            players_table_cells[j][i].value = players_table_cells[i][j].value
            players_table_cells[j][i].style()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget, text)
    def hover(event):
        toolTip.ShowToolTip()
    def leave(event):
        toolTip.HideToolTip()
    widget.bind('<Enter>', hover)
    widget.bind('<Leave>', leave)

###############################################
###############################################

root = tk.Tk()
root.title('Secret Hitler Wizard')
root.resizable(False, False)
dark_bg = 'gray7'

#Creating tabs
master_tab = ttk.Notebook(root)

start_tab = ttk.Frame(master_tab)
elections_tab = ttk.Frame(master_tab)
players_tab = ttk.Frame(master_tab)

master_tab.add(start_tab, text="Start")
master_tab.add(elections_tab, text="Elections")
master_tab.add(players_tab, text="Players")
master_tab.pack()

#Start tab content
n_players_list = [5, 6, 7, 8, 9, 10]
n_fasc_list = [1, 2, 3]
hitler_zone_list = ["after {} R cards".format(i+1) for i in range(5)]
player_position_list = [i+1 for i in range(7)]
player_role_list = ["Liberal", "Fascist", "Hitler"]
n_blu_list = [5, 6, 7, 8]
n_red_list = [i+10 for i in range(10)]

start_frame= tk.Frame(start_tab)
start_frame.pack()

start_combobox_frame = tk.Frame(start_frame, pady= 5)
start_combobox_frame.pack()

start_columns = [tk.Frame(start_combobox_frame, bd=2, relief="groove") for i in range(3)]
for i in start_columns:
    i.pack(side=tk.LEFT, fill='both', anchor='n')

n_players = StartCombobox("Number of players:", n_players_list, 0, 5, 2)
# n_fasc = StartCombobox("Number of fasc (w/o Hitler):", n_fasc_list, 0, 5, 1)
player_position = StartCombobox("My position:", player_position_list, 1, 5, 0)
# player_role = StartCombobox("My role:", player_role_list, 1, 10, 0)
# hitler_position = StartCombobox("Hitler position:", player_position_list, 1, 5, 1)
# fasc_pos = StartCombobox("Others Fasc Pos:", player_position_list, 1, 5, 1)
n_red = StartCombobox("Number of R cards:", n_red_list, 2, 5, 1, bg='pink')
n_blu = StartCombobox("Number of B cards:", n_blu_list, 2, 5, 1, bg='LightBlue1')
# hitler_zone = StartCombobox("Hitler zone starts:", hitler_zone_list, 2, 15, 2)

n_players.combobox.bind('<<ComboboxSelected>>', lambda _: NPlayersChanged(int(n_players.combobox.get())))
player_position.combobox.bind('<<ComboboxSelected>>', lambda _: player_position.label.config(bg='SystemButtonFace'))

start_button_frame = tk.Frame(start_frame)
start_button_frame.pack()
start_button = tk.Button(start_button_frame, text="New Game", padx= 10, pady=10, command= lambda: newgame(int(n_players.combobox.get())))
start_button.pack()

#Election tab content
## Elections Title
elections_title_frame= tk.Frame(elections_tab)
elections_title_frame.pack(side= tk.TOP)

elections_labels_list= [['R.', 15],
                        ['Pres./Chanc.', 0],
                        ['Deck', 25],
                        ['Elections', 84],
                        ['Claims', 80]] # Text and padx
elections_label = [tk.Label(elections_title_frame, text=i[0], padx=i[1]) for i in elections_labels_list]
for i in range(len(elections_label)):
    elections_label[i].pack(side= tk.LEFT)

## Elections Main
rounds =[]

## Election Button
election_button_frame = tk.Frame(elections_tab)
election_button_frame.pack(side= tk.BOTTOM, fill=tk.X, expand=1, anchor='s')

election_button = tk.Button(election_button_frame, text="Next Turn", command= lambda: nextelections(int(n_players.combobox.get())))
election_button.pack(fill=tk.X, expand=1)

#Players tab content
players_title= tk.Label(players_tab, text= "Affinity Coefficient")
players_title.pack(side=tk.TOP)


players_table_frame = tk.Frame(players_tab)
players_checks_frame = tk.Frame(players_tab)

players_checks_display_init = [0, 1, 1]
players_checks_display = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
for i in range(3):
    players_checks_display[i].set(players_checks_display_init[i])

newgame(int(n_players.combobox.get()))


root.mainloop()
