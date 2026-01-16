#The Universal Pokédex - User Interface

#-------------------imports--------------------#
import TUPitems
import TUPdatabase
import tkinter as tk
import os
import requests
import threading
import sqlite3
from tkinter import PhotoImage, ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from ctypes import windll
from io import BytesIO



#------------------------------------------Tkinter-------------------------------------------#
class mainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('The Universal Pokédex')
        self.geometry('1280x780')
        self.configure(background='#ffffff')

        self.currentUserID = None

        #default colour is light blue
        self.colours = {'bgcolor': '#c1dbf3', 'fgcolor': '#ffffff', 'activecolor': '#97c7f3', 'framecolor': '#deebf7', 'darkcolor': '#d9d9d9'}

        #light red colour
        def lightRedMode():
            self.colours['bgcolor'] = '#ff7171'
            self.colours['fgcolor'] = '#ffffff'
            self.colours['activecolor'] = '#ff5252'
            self.colours['framecolor'] = '#ffabab'
            self.colours['darkcolor'] = '#d9d9d9'
            #self.configure(background='#ffc8c8')          

        #dark blue colour
        def darkBlueMode():
            self.colours['bgcolor'] = '#7f7f7f'
            self.colours['fgcolor'] = '#ffffff'
            self.colours['activecolor'] = '#595959'
            self.colours['framecolor'] = '#404040'
            self.colours['darkcolor'] = '#232323'
            self.configure(background='#232323')
        
        #lightRedMode()
        darkBlueMode()

        self.FONT = 'Trebuchet MS'
        self.widgetOptions = {'background': self.colours['bgcolor'], 'foreground': self.colours['fgcolor'], 'font': (self.FONT, 40, 'bold')}

        #fullscreen
        self.attributes('-fullscreen', True) #window becomes fullscreen automatically
        self.bind('<Escape>', lambda event: self.destroy())  #exits fullscreen if presses escape

        #change icon
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.iconPath = os.path.join(self.scriptDir, 'assets', 'pokeball-icon.ico')
        if os.path.exists(self.iconPath):    
            self.iconbitmap(self.iconPath)
        
        #frame styles
        self.styleF = ttk.Style()
        self.styleF.theme_use('clam')
        self.styleF.configure('TFrame', background=self.colours['framecolor'])

        #button styles
        self.styleMainB = ttk.Style()
        self.styleMainB.theme_use('clam')
        self.styleMainB.configure('main.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 35, 'bold'), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleMainB.map('main.TButton', background=[('active', self.colours['activecolor'])])

        self.styleEnterB = ttk.Style()
        self.styleEnterB.theme_use('clam')
        self.styleEnterB.configure('enter.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15, 'bold'), bordercolor=self.colours['bgcolor'])
        self.styleEnterB.map('enter.TButton', background=[('active', self.colours['activecolor'])])

        self.styleSmallB = ttk.Style()
        self.styleSmallB.theme_use('clam')
        self.styleSmallB.configure('small.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15, 'bold'), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleSmallB.map('small.TButton', background=[('active', self.colours['activecolor'])])

        #progressbar styles
        self.stylePb = ttk.Style()
        self.stylePb.theme_use('clam')
        self.stylePb.configure('TProgressbar', background=self.colours['activecolor'], troughcolor=self.colours['bgcolor'], bordercolor=self.colours['bgcolor'])

        #label styles
        self.styleL = ttk.Style()
        self.styleL.theme_use('clam')
        self.styleL.configure('TLabel', **self.widgetOptions)

        self.styleProgressL = ttk.Style()
        self.styleProgressL.theme_use('clam')
        self.styleProgressL.configure('progress.TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 10, 'bold'))

        self.styleSmallL = ttk.Style()
        self.styleSmallL.theme_use('clam')
        self.styleSmallL.configure('small.TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 28, 'bold'))

        #entry styles
        self.styleE = ttk.Style()
        self.styleE.theme_use('clam')
        self.styleE.configure('TEntry', fieldbackground=self.colours['bgcolor'], foreground=self.colours['fgcolor'], bordercolor=self.colours['bgcolor'])

        #menubutton styles
        self.styleMB = ttk.Style()
        self.styleMB.theme_use('clam')
        self.styleMB.configure('filter.TMenubutton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15, 'bold'), arrowcolor=self.colours['fgcolor'], bordercolor=self.colours['bgcolor'])
        self.styleMB.map('filter.TMenubutton', background=[('active', self.colours['activecolor'])])

        #main menu large icons
        self.buttonMenuBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'pokeballIconLight.png')))
        self.buttonMenuBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'encyclopediaIconLight.png')))
        self.buttonMenuArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'teamraterIconLight.png')))
        self.buttonMenuExitIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'exitIconLight.png')))


        #side menu small icons
        self.buttonSideBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'pokeballIconLightSmall.png')))
        self.buttonSideBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'encyclopediaIconLightSmall.png')))
        self.buttonSideArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'teamraterIconLightSmall.png')))
        self.buttonSideHouseIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'menuIconLight.png')))
        self.buttonSideChartIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets/icons', 'typechartIconLight.png')))

    def getSprite(self, URL, label):
        response = requests.get(URL)
        monImage = Image.open(BytesIO(response.content))
        self.monSprite = ImageTk.PhotoImage(monImage)
        self.after(0, label.configure(image=self.monSprite))

    def makeButtonFrame(self):
        self.mainMenuButtonFrame = ttk.Frame(self)

        #frame grid
        self.mainMenuButtonFrame.rowconfigure(0, weight=1)
        self.mainMenuButtonFrame.rowconfigure(1, weight=1)
        self.mainMenuButtonFrame.rowconfigure(2, weight=1)
        self.mainMenuButtonFrame.columnconfigure(0, weight=1)

        #buttons
        self.buttonBall = ttk.Button(self.mainMenuButtonFrame, text='Pokédex', image=self.buttonMenuBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonBall.grid(row=0, sticky=tk.NSEW)

        self.buttonBook = ttk.Button(self.mainMenuButtonFrame, text='Encyclopedia', image=self.buttonMenuBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonBook.grid(row=1, sticky=tk.NSEW)

        self.buttonArrow = ttk.Button(self.mainMenuButtonFrame, text='Team Rater', image=self.buttonMenuArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonArrow.grid(row=2, sticky=tk.NSEW)

        for widget in self.mainMenuButtonFrame.winfo_children():
            widget.grid(padx=15, pady=15)
        
        #packing button frame
        self.mainMenuButtonFrame.grid(column=0, row=1, sticky=tk.NSEW, padx=15, pady=15)

    def makeSideMenuFrame(self, container):
        self.sideMenuFrame = ttk.Frame(container)

        #frame grid
        self.sideMenuFrame.columnconfigure(0, weight=1)
        self.sideMenuFrame.rowconfigure(0, weight=10)
        self.sideMenuFrame.rowconfigure(1, weight=1)

        self.ButtonChart = ttk.Button(self.sideMenuFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.ButtonChart.grid(column=0, row=0, sticky=tk.NSEW, padx=15, pady=15)

        self.ButtonExit = ttk.Button(self.sideMenuFrame, text='Exit Program', image=self.buttonMenuExitIcon, compound=tk.LEFT, command=self.destroy, style='main.TButton')
        self.ButtonExit.grid(row=1, column=0, sticky=tk.NSEW, padx=15, pady=15)

        #packing side menu frame
        self.sideMenuFrame.grid(column=1, row=1, sticky=tk.NSEW, padx=15, pady=15)

    def makeMenuGrid(self):
        titleOptions = {'column': 0, 'row': 0, 'padx': 15, 'pady': 15, 'columnspan': 2, 'sticky': tk.NSEW}

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=12)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=5)

        self.titleLabel = ttk.Label(self, text='The Universal Pokédex', anchor='center')
        self.titleLabel.grid(**titleOptions)

    def secondaryScreen(self):
        #make window grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=6)

        #create frames
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.grid(row=1, column=1, sticky=tk.NSEW, padx=15, pady=15)
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(2, weight=1)
        self.mainFrame.rowconfigure(3, weight=100)
        self.mainFrame.columnconfigure(0, weight=18)
        self.mainFrame.columnconfigure(1, weight=1)
        self.mainFrame.columnconfigure(2, weight=1)
        self.mainFrame.columnconfigure(3, weight=1)

        self.sideFrame = ttk.Frame(self)
        self.sideFrame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW, padx=15, pady=15)
        self.sideFrame.rowconfigure(0, weight=2)
        for i in range(1, 4):
            self.sideFrame.rowconfigure(i, weight=20)
        self.sideFrame.columnconfigure(0, weight=1)

    def dexSelectFrame(self):
        self.dexFrame = ttk.Frame(self.mainFrame)
        for i in range(1, 6):
            self.dexFrame.rowconfigure(i, weight=1)
        self.dexFrame.columnconfigure(0, weight=1)
        self.dexFrame.columnconfigure(1, weight=1)

        for i in range(1, 6):
            num=str(i)
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda n=num: [self.dexFrame.destroy(), self.pokemonFrame(num)])
            self.genButton.grid(row=i, column=0, padx=15, pady=15, sticky=tk.NSEW)

        for i in range(1, 5):
            num=str(i+5)
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda n=num: [self.dexFrame.destroy(), self.pokemonFrame(num)])
            self.genButton.grid(row=i, column=1, padx=15, pady=15, sticky=tk.NSEW)

        self.dexFrame.grid(row=0, column=0, rowspan=4, columnspan=5, padx=15, pady=15, sticky=tk.NSEW)
    
    def filterFrame(self):
        self.filterFrame = ttk.Frame(self.mainFrame)

    def pokemonFrame(self, gen):
        self.genNum = gen

        # #test label
        # self.testLabel = ttk.Label(self.mainFrame)
        # self.testLabel.grid(row=0, column=0, sticky=tk.NSEW, rowspan=4, padx=15, pady=15)
        
        # # threading.Thread(target=self.getSprite, daemon=True).start()
        # # self.spriteURL = TUPitems.getTestSpriteURL()        
        # # self.getSprite(self.spriteURL, self.testLabel)

        # self.spriteURL = TUPitems.getTestSpriteURL()
        # threading.Thread(tar)

        #progress bar test buttons
        stopButton = ttk.Button(self.mainFrame, text='stop', command=self.hideProgressBar)
        stopButton.grid(row=3, column=2)

        #enter button
        self.enterButton = ttk.Button(self.mainFrame, text='Enter', style='enter.TButton', command=self.showProgressBar)
        self.enterButton.grid(row=0, column=2, sticky=tk.NSEW, pady=15)

        #search textbox
        self.searchTextbox = ttk.Entry(self.mainFrame, text='Search...', font = ('Trebuchet MS', 20, 'bold'))
        self.searchTextbox.grid(row=0, column=1, sticky=tk.NSEW, pady=15)

        #filter menu
        self.filterOptions = ('Option 1', 'Option 2', 'Option 3')
        self.selectedFilter = tk.StringVar()

        self.filterMenuButton = ttk.Menubutton(self.mainFrame, text='Filter...', style='filter.TMenubutton')
        self.filterMenu = tk.Menu(self.filterMenuButton, tearoff=False)
        self.filterMenuButton['menu'] = self.filterMenu

        for option in self.filterOptions:
            self.filterMenu.add_radiobutton(label=option, value=option, variable=self.selectedFilter)
        
        self.filterMenuButton.grid(row=1, column=1, sticky=tk.NSEW, columnspan=2)

        


        # #canvas to scroll
        # self.canvas = tk.Canvas(self)
        # self.canvFrame = ttk.Frame(self.canvas)

        # #vertical scrollbar
        # self.scrollbar = ttk.Scrollbar(self.ca, orient=tk.VERTICAL, command=self.canvas.yview)
        # self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # self.scrollbar.grid


    def typeChartScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}

        #image paths
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.typeChartPath = os.path.join(self.scriptDir, 'assets\chart', 'pokemon-type-chart2.png')
        self.typeChartImage = ImageTk.PhotoImage(Image.open(self.typeChartPath))

        self.typeChartKeyPath = os.path.join(self.scriptDir, 'assets\chart', 'pokemon-type-chart-key.png')
        self.typeChartKeyImage = ImageTk.PhotoImage(Image.open(self.typeChartKeyPath))

        self.typeChartLegendPath = os.path.join(self.scriptDir, 'assets\chart', 'pokemon-type-chart-legend.png')
        self.typeChartLegendImage = ImageTk.PhotoImage(Image.open(self.typeChartLegendPath))

        self.secondaryScreen()
        for i in range(2, 5):
            self.rowconfigure(i, weight=0)

        #title label
        self.titleLabel = ttk.Label(self, text='Type Chart', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonSideBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonSideBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonSideArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #type chart image
        self.chartLabel = ttk.Label(self.mainFrame, image=self.typeChartImage, anchor='center')
        self.chartLabel.grid(column=0, row=2, padx=15, pady=15, sticky=tk.NSEW)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def pokedexScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}

        self.secondaryScreen()

        #title label
        self.titleLabel = ttk.Label(self, text='Pokédex', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonSideBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonSideArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.LEFT, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        self.dexSelectFrame()
        #self.pokemonFrame()
        

    def encyclopediaScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}

        self.secondaryScreen()

        #title label
        self.titleLabel = ttk.Label(self, text='Encyclopedia', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonSideBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonSideArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.LEFT, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def teamraterScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}

        self.secondaryScreen()

        #title label
        self.titleLabel = ttk.Label(self, text='Team Rater', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonSideBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonSideBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.LEFT, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def showLogin(self):
        self.clearWindow()

        #window grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=8)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        #main login frame
        self.loginFrame = ttk.Frame(self, padding=20)
        self.loginFrame.grid(row=1, column=0, columnspan=3, padx=30, pady=30, sticky=tk.NSEW)

        #login frame grid
        for i in range(7):
            self.loginFrame.rowconfigure(i, weight=1)
        self.loginFrame.columnconfigure(0, weight=2)
        self.loginFrame.columnconfigure(1, weight=3)
        self.loginFrame.columnconfigure(2, weight=3)
        self.loginFrame.columnconfigure(3, weight=3)
        self.loginFrame.columnconfigure(4, weight=2)

        #login title frame
        self.loginTitleFrame = ttk.Frame(self)
        self.loginTitleFrame.grid(row=0, column=0, columnspan=3, sticky=tk.EW)

        self.loginTitleFrame.columnconfigure(0, weight=1)

        #login title label
        self.loginTitleLabel = ttk.Label(self.loginTitleFrame, text='The Universal Pokédex', anchor='center', style='TLabel')
        self.loginTitleLabel.grid(row=0, column=0, pady=15, sticky=tk.EW)

        #username label
        self.usernameLabel = ttk.Label(self.loginFrame, text='Username', anchor='center', style='small.TLabel')
        self.usernameLabel.grid(row=1, column=2, padx=20, pady=(12, 2), sticky=tk.EW)

        #username entry
        self.usernameEntry = ttk.Entry(self.loginFrame, font=(self.FONT, 18))
        self.usernameEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=(2, 10), sticky=tk.EW)

        #password label
        self.passwordLabel = ttk.Label(self.loginFrame, text='Password', anchor='center', style='small.TLabel')
        self.passwordLabel.grid(row=3, column=2, padx=20, pady=(10, 2), sticky=tk.EW)

        #password entry
        self.passwordEntry = ttk.Entry(self.loginFrame, show='•', font=(self.FONT, 18)) 
        self.passwordEntry.grid(row=4, column=1, columnspan=3, padx=20, pady=(2, 10), sticky=tk.EW)

        #error frame
        self.loginErrorFrame = ttk.Frame(self.loginFrame)

        self.loginErrorFrame.columnconfigure(0, weight=1)

        #error label
        self.loginErrorLabel = ttk.Label(self.loginErrorFrame, text='', anchor='center', style='progress.TLabel', wraplength=600)

        #button frame
        self.buttonFrame = ttk.Frame(self.loginFrame)
        self.buttonFrame.grid(row=6, column=2, padx=5, pady=20, sticky=tk.NSEW)

        self.buttonFrame.columnconfigure(0, weight=1)
        self.buttonFrame.columnconfigure(1, weight=1)

        #login button
        self.loginButton = ttk.Button(self.buttonFrame, text='Login', style='small.TButton', command=self.tryLogin)
        self.loginButton.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)

        #register button
        self.registerButton = ttk.Button(self.buttonFrame, text='Create Account', style='small.TButton', command=self.tryRegister)
        self.registerButton.grid(row=0, column=1, padx=(10, 0), sticky=tk.EW)

    def tryLogin(self):
        #retrieves user input from entry widgets
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        #if no username or password entered
        if not username or not password:
            self.loginErrorLabel.config(text='Please enter a username and password')
            self.loginErrorFrame.grid(row=5, column=0, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
            return
        
        #checks login details are valid
        success, userID = TUPdatabase.checkLogin(username, password)

        if success:
            self.currentUserID = userID
            self.showMainMenu()
        else:
            self.loginErrorLabel.config(text='Invalid username or password')
            self.loginErrorFrame.grid(row=5, column=0, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)

    def tryRegister(self):
        #retrieve user input from entry widgets
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        #if no username or password are entered
        if not username or not password:
            self.loginErrorLabel.config(text='Please enter a username and password')
            self.loginErrorFrame.grid(row=5, column=0, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
            return
        
        #tries to add details to database
        try:
            TUPdatabase.addUser(username, password)
            self.loginErrorLabel.config(text='Account made - Please login')
            self.loginErrorFrame.grid(row=5, column=0, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
        
        #error message if username already exists
        except sqlite3.IntegrityError:
            self.loginErrorLabel.config(text='Username already exists')
            self.loginErrorFrame.grid(row=5, column=0, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)

    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()

    def showTypeChartScreen(self):
        self.clearWindow()
        self.typeChartScreen()

    def showPokedexScreen(self):
        self.clearWindow()
        self.pokedexScreen()

    def showEncyclopediaScreen(self):
        self.clearWindow()
        self.encyclopediaScreen()

    def showTeamraterScreen(self):
        self.clearWindow()
        self.teamraterScreen()

    def showProgressBar(self):
        #progress bar
        self.progressBarFrame = ttk.Frame(self.mainFrame)
        self.progressBarFrame.columnconfigure(0, weight=5)
        self.progressBarFrame.columnconfigure(1, weight=1)

        self.progressBar = ttk.Progressbar(self.progressBarFrame, mode='indeterminate')
        self.progressBar.grid(row=0, column=0, sticky=tk.NSEW, pady=15)

        self.progressBarText = ttk.Label(self.progressBarFrame, text='Loading...', style='progress.TLabel', anchor='center')
        self.progressBarText.grid(row=0, column=1, sticky=tk.NSEW, pady=15)

        self.progressBarFrame.grid(column=1, row=2, columnspan=2, sticky=tk.NSEW)
        self.progressBar.start()

    def hideProgressBar(self):
        self.progressBar.stop()
        self.progressBarFrame.destroy()

    def showMainMenu(self):
        self.clearWindow()
        self.makeMenuGrid()
        self.makeButtonFrame()
        self.makeSideMenuFrame(self)