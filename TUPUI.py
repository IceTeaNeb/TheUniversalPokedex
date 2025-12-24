#The Universal Pokédex - User Interface

#-------------------imports--------------------#
import tkinter as tk
import os
from tkinter import PhotoImage, ttk
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk
from ctypes import windll


#------------------------------------------Tkinter-------------------------------------------#
class mainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.FONT = 'Trebuchet MS'
        self.widgetOptions = {'background':'#c1dbf3', 'foreground': 'white', 'font': (self.FONT, 40, 'bold')}

        self.title('The Universal Pokédex')
        self.geometry('1280x780')
        self.configure(background='white')

        #fullscreen
        self.attributes('-fullscreen', True) #window becomes fullscreen automatically
        self.bind('<Escape>', lambda event: self.destroy())  #exits fullscreen if presses escape

        #change icon
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.iconPath = os.path.join(self.scriptDir, 'assets', 'pokeball-icon.ico')
        if os.path.exists(self.iconPath):    
            self.iconbitmap(self.iconPath)
        
        #widget colours
        self.bgColour = '#c1dbf3'
        self.fgColour = '#ffffff'

        #frame styles
        self.styleF = ttk.Style()
        self.styleF.theme_use('clam')
        self.styleF.configure('TFrame', background='#deebf7')

        #button styles
        self.styleMainB = ttk.Style()
        self.styleMainB.theme_use('clam')
        self.styleMainB.configure('main.TButton', background=self.bgColour, foreground=self.fgColour, font=(self.FONT, 35, 'bold'), bordercolor='#c1dbf3', darkcolor='#d9d9d9')
        self.styleMainB.map('main.TButton', background=[('active', '#97c7f3')])

        self.styleEnterB = ttk.Style()
        self.styleEnterB.theme_use('clam')
        self.styleEnterB.configure('enter.TButton', background=self.bgColour, foreground=self.fgColour, font=(self.FONT, 15, 'bold'), bordercolor='#c1dbf3')
        self.styleEnterB.map('enter.TButton', background=[('active', '#97c7f3')])

        #progressbar styles
        self.stylePb = ttk.Style()
        self.stylePb.theme_use('clam')
        self.stylePb.configure('TProgressbar', background='#97c7f3', troughcolor='#c1dbf3', bordercolor='#c1dbf3')

        #label styles
        self.styleL = ttk.Style()
        self.styleL.theme_use('clam')
        self.styleL.configure('TLabel', **self.widgetOptions)

        #entry styles
        self.styleE = ttk.Style()
        self.styleE.theme_use('clam')
        self.styleE.configure('TEntry', fieldbackground='#c1dbf3', foreground='#ffffff', bordercolor='#c1dbf3')

        #menubutton styles
        self.styleMB = ttk.Style()
        self.styleMB.theme_use('clam')
        self.styleMB.configure('filter.TMenubutton', background=self.bgColour, foreground=self.fgColour, font=(self.FONT, 15, 'bold'), arrowcolor='#ffffff', bordercolor='#c1dbf3')
        self.styleMB.map('filter.TMenubutton', background=[('active', '#97c7f3')])

    def sideIconPath(self):
        self.imageBallPath = os.path.join(self.scriptDir, 'assets\icons', 'pokeballIconLightSmall.png')
        self.buttonBallIcon = ImageTk.PhotoImage(Image.open(self.imageBallPath))

        self.imageBookPath = os.path.join(self.scriptDir, 'assets\icons', 'encyclopediaIconLightSmall.png')
        self.buttonBookIcon = ImageTk.PhotoImage(Image.open(self.imageBookPath))

        self.imageArrowPath = os.path.join(self.scriptDir, 'assets\icons', 'teamraterIconLightSmall.png')
        self.buttonArrowIcon = ImageTk.PhotoImage(Image.open(self.imageArrowPath))

        self.imageChartPath = os.path.join(self.scriptDir, 'assets\icons', 'typechartIconLight.png')
        self.buttonChartIcon = ImageTk.PhotoImage(Image.open(self.imageChartPath))

        self.imageHousePath = os.path.join(self.scriptDir, 'assets\icons', 'menuIconLight.png')
        self.buttonHouseIcon = ImageTk.PhotoImage(Image.open(self.imageHousePath))

        self.imageExitPath = os.path.join(self.scriptDir, 'assets\icons', 'exitIconLight.png')
        self.buttonExitIcon = ImageTk.PhotoImage(Image.open(self.imageExitPath))

    def makeButtonFrame(self):
        #button icons
        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.image1Path = os.path.join(self.scriptDir, 'assets\icons', 'pokeballIconLight.png')
        self.button1Icon = ImageTk.PhotoImage(Image.open(self.image1Path))

        self.image2Path = os.path.join(self.scriptDir, 'assets\icons', 'encyclopediaIconLight.png')
        self.button2Icon = ImageTk.PhotoImage(Image.open(self.image2Path))

        self.image3Path = os.path.join(self.scriptDir, 'assets\icons', 'teamraterIconLight.png')
        self.button3Icon = ImageTk.PhotoImage(Image.open(self.image3Path))

        self.frame = ttk.Frame(self)

        #frame grid
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

        #buttons
        self.button1 = ttk.Button(self.frame, text='Pokédex', image=self.button1Icon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.button1.grid(row=0, sticky=tk.NSEW)

        self.button2 = ttk.Button(self.frame, text='Encyclopedia', image=self.button2Icon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.button2.grid(row=1, sticky=tk.NSEW)

        self.button3 = ttk.Button(self.frame, text='Team Rater', image=self.button3Icon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.button3.grid(row=2, sticky=tk.NSEW)

        for widget in self.frame.winfo_children():
            widget.grid(padx=15, pady=15)
        
        #packing button frame
        self.frame.grid(column=0, row=1, sticky=tk.NSEW, padx=15, pady=15)

    def makeSideMenuFrame(self, container):
        self.frame = ttk.Frame(container)

        self.scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.typeChartIconPath = os.path.join(self.scriptDir, 'assets\icons', 'typechartIconLight_resized - Copy.png')
        self.typeChartIconImage = ImageTk.PhotoImage(Image.open(self.typeChartIconPath))

        #frame grid
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=10)
        self.frame.rowconfigure(1, weight=1)

        self.ButtonChart = ttk.Button(self.frame, text='Type Chart', image=self.typeChartIconImage, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.ButtonChart.grid(column=0, row=0, sticky=tk.NSEW, padx=15, pady=15)

        self.ButtonExit = ttk.Button(self.frame, text='Exit Program', image=self.buttonExitIcon, compound=tk.LEFT, command=self.destroy, style='main.TButton')
        self.ButtonExit.grid(row=1, column=0, sticky=tk.NSEW, padx=15, pady=15)

        #packing side menu frame
        self.frame.grid(column=1, row=1, sticky=tk.NSEW, padx=15, pady=15)

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
        self.columnconfigure(1, weight=30)

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
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda: [self.dexFrame.destroy(), self.pokemonFrame(num)])
            self.genButton.grid(row=i, column=0, padx=15, pady=15, sticky=tk.NSEW)

        for i in range(1, 5):
            num=str(i+5)
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda: [self.dexFrame.destroy(), self.pokemonFrame(num)])
            self.genButton.grid(row=i, column=1, padx=15, pady=15, sticky=tk.NSEW)

        self.dexFrame.grid(row=0, column=0, rowspan=4, columnspan=5, padx=15, pady=15, sticky=tk.NSEW)
    
    def filterFrame(self):
        self.filterFrame = ttk.Frame(self.mainFrame)

    def pokemonFrame(self, gen):
        self.genNum = gen
        #test label
        self.testLabel = ttk.Label(self.mainFrame)
        self.testLabel.grid(row=0, column=0, sticky=tk.NSEW, rowspan=4, padx=15, pady=15)
        
        #progress bar test buttons
        startButton = ttk.Button(self.mainFrame, text='start', command=self.showProgressBar)
        startButton.grid(row=3, column=1)
        stopButton = ttk.Button(self.mainFrame, text='stop', command=self.hideProgressBar)
        stopButton.grid(row=3, column=2)


        #enter button
        self.enterButton = ttk.Button(self.mainFrame, text='Enter', style='enter.TButton')
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
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.NSEW}

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
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #type chart image
        self.chartLabel = ttk.Label(self.mainFrame, image=self.typeChartImage, anchor='center')
        self.chartLabel.grid(column=0, row=2, padx=15, pady=15, sticky=tk.NSEW)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def pokedexScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.NSEW}

        self.secondaryScreen()

        #title label
        self.titleLabel = ttk.Label(self, text='Pokédex', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonChartIcon, compound=tk.LEFT, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        self.dexSelectFrame()
        #self.pokemonFrame()
        

    def encyclopediaScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.NSEW}

        self.secondaryScreen()

        #title label
        self.titleLabel = ttk.Label(self, text='Encyclopedia', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonArrowIcon, compound=tk.LEFT, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonChartIcon, compound=tk.LEFT, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def teamraterScreen(self):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.NSEW}

        self.secondaryScreen()

        #title label
        self.titleLabel = ttk.Label(self, text='Team Rater', anchor='center')
        self.titleLabel.grid(**titleOptions)

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonBallIcon, compound=tk.LEFT, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonBookIcon, compound=tk.LEFT, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonChartIcon, compound=tk.LEFT, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)


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
        self.progressBar = ttk.Progressbar(self.mainFrame, mode='indeterminate')
        self.progressBar.grid(row=2, column=1, sticky=tk.NSEW, padx=15, pady=15, columnspan=2)
        self.progressBar.start()

    def hideProgressBar(self):
        self.progressBar.stop()
        self.progressBar.destroy()

    def showMainMenu(self):
        self.clearWindow()
        self.sideIconPath()
        self.makeMenuGrid()
        self.makeButtonFrame()
        self.makeSideMenuFrame(self)