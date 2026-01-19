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
            self.colours['fgcolor'] = '#c1dbf3'
            self.colours['activecolor'] = '#595959'
            self.colours['framecolor'] = '#404040'
            self.colours['darkcolor'] = '#232323'
            self.configure(background='#232323')

        #dark red colour
        def darkRedMode():
            self.colours['bgcolor'] = '#7f7f7f'
            self.colours['fgcolor'] = '#ff7171'
            self.colours['activecolor'] = '#595959'
            self.colours['framecolor'] = '#404040'
            self.colours['darkcolor'] = '#232323'
            self.configure(background='#232323')
        
        #lightRedMode()
        darkBlueMode()
        #darkRedMode()

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

        #light main menu large icons
        self.buttonMenuBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'pokeballIconLight.png')))
        self.buttonMenuBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'encyclopediaIconLight.png')))
        self.buttonMenuArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'teamraterIconLight.png')))
        self.buttonMenuExitIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'exitIconLight.png')))

        #light side menu small icons
        self.buttonSideBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'pokeballIconLightSmall.png')))
        self.buttonSideBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'encyclopediaIconLightSmall.png')))
        self.buttonSideArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'teamraterIconLightSmall.png')))
        self.buttonSideHouseIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'menuIconLight.png')))
        self.buttonSideChartIcon = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'icons', 'typechartIconLight.png')))

        #type chart images
        self.typeChartImage = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'chart', 'pokemon-type-chart2.png')))

        #sprites
        self.spriteCache = {}

        #filter
        self.type1Var = tk.StringVar(value='')
        self.type2Var = tk.StringVar(value='')
        self.heightClassVar = tk.StringVar(value='Any')
        self.weightClassVar = tk.StringVar(value='Any')
        self.bstRangeVar = tk.StringVar(value='Any')

    def getSprite(self, URL, label):
        response = requests.get(URL)
        monImage = Image.open(BytesIO(response.content))
        self.monSprite = ImageTk.PhotoImage(monImage)
        self.after(0, label.configure(image=self.monSprite))

    def loadCachedSprite(self, spriteURL):
        if not spriteURL:
            return None
        if spriteURL in self.spriteCache:
            return self.spriteCache[spriteURL]
        
        try:
            response = requests.get(spriteURL, timeout=5)
            image = Image.open(BytesIO(response.content))
            sprite = ImageTk.PhotoImage(image)
            self.spriteCache[spriteURL] = sprite
            return sprite
        except:
            return None

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

        self.buttonChart = ttk.Button(self.sideMenuFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(column=0, row=0, sticky=tk.NSEW, padx=15, pady=15)

        self.buttonExit = ttk.Button(self.sideMenuFrame, text='Exit Program', image=self.buttonMenuExitIcon, compound=tk.LEFT, command=self.destroy, style='main.TButton')
        self.buttonExit.grid(row=1, column=0, sticky=tk.NSEW, padx=15, pady=15)

        #packing side menu frame
        self.sideMenuFrame.grid(column=1, row=1, sticky=tk.NSEW, padx=15, pady=15)

    def makeMenuGrid(self):
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=12)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=5)

        self.titleOptions = {'column': 0, 'row': 0, 'columnspan': 2, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self.titleLabel = ttk.Label(self, text='The Universal Pokédex', anchor = 'center')
        self.titleLabel.grid(**self.titleOptions)

    def secondaryScreen(self):
        #make window grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)

        #create frames
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.grid(row=1, column=1, sticky=tk.NSEW, padx=15, pady=15)
        self.mainFrame.rowconfigure(0, weight=1)
        self.mainFrame.rowconfigure(1, weight=1)
        self.mainFrame.rowconfigure(2, weight=1)
        self.mainFrame.rowconfigure(3, weight=100)

        self.mainFrame.columnconfigure(0, weight=8, minsize=400)
        self.mainFrame.columnconfigure(1, weight=8)
        self.mainFrame.columnconfigure(2, weight=8)
        self.mainFrame.columnconfigure(3, weight=0)


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
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda n=num: [self.dexFrame.destroy(), self.pokemonFrame(n)])
            self.genButton.grid(row=i, column=0, padx=15, pady=15, sticky=tk.NSEW)

        for i in range(1, 5):
            num=str(i+5)
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda n=num: [self.dexFrame.destroy(), self.pokemonFrame(n)])
            self.genButton.grid(row=i, column=1, padx=15, pady=15, sticky=tk.NSEW)

        self.dexFrame.grid(row=0, column=0, rowspan=4, columnspan=5, padx=15, pady=15, sticky=tk.NSEW)

    def pokemonFrame(self, gen):
        self.genNum = int(gen)
        self.currentDexID = self.genNum

        TUPdatabase.ensureDexExists(self.currentDexID, self.genNum, "Default")

        #enter button
        self.searchButton = ttk.Button(self.mainFrame, text='Enter', style='enter.TButton', command=self.refreshPokedexResults)
        self.searchButton.grid(row=0, column=2, sticky=tk.NSEW, pady=15)

        #search entry
        self.searchEntry = ttk.Entry(self.mainFrame, font = ('Trebuchet MS', 20, 'bold'))
        self.searchEntry.grid(row=0, column=1, sticky=tk.NSEW, pady=15)
        self.searchEntry.bind('<Return>', lambda e: self.refreshPokedexResults())

        #filter
        self.filtersFrame = ttk.Frame(self.mainFrame)
        self.filtersFrame.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=(0, 10))
        for column in range(5):
            self.filtersFrame.columnconfigure(column, weight=1)

        typeOptions = [('Any', ''), ('Normal', 'Normal'), ('Fire', 'Fire'), ('Water', 'Water'),
                       ('Grass', 'Grass'), ('Electric', 'Electric'), ('Ice', 'Ice'), ('Fighting', 'Fighting'),
                       ('Poison', 'Poison'), ('Ground', 'Ground'), ('Flying', 'Flying'), ('Psychic', 'Psychic'),
                       ('Bug', 'Bug'), ('Rock', 'Rock'), ('Ghost', 'Ghost'), ('Dragon', 'Dragon'),
                       ('Dark', 'Dark'), ('Steel', 'Steel'), ('Fairy', 'Fairy')]
        
        heightOptions = [('Any', 'Any'), ('Small', 'Small'), ('Medium', 'Medium'), ('Large', 'Large')]
        weightOptions = [('Any', 'Any'), ('Light', 'Light'), ('Medium', 'Medium'), ('Heavy', 'Heavy')]
        bstOptions = [('Any', 'Any'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')]

        #type1 menubutton
        self.type1MenuButton = ttk.Menubutton(self.filtersFrame, text='Type 1', style='filter.TMenubutton')
        self.type1MenuButton.grid(row=0, column=0, sticky=tk.EW, padx=(0, 8))
        self.makeFilterMenu(self.type1MenuButton, typeOptions, self.type1Var)

        #type2 menubutton
        self.type2MenuButton = ttk.Menubutton(self.filtersFrame, text='Type 2', style='filter.TMenubutton')
        self.type2MenuButton.grid(row=0, column=1, sticky=tk.EW, padx=(0, 8))
        self.makeFilterMenu(self.type2MenuButton, typeOptions, self.type2Var)

        #height menubutton
        self.heightMenuButton = ttk.Menubutton(self.filtersFrame, text='Height', style='filter.TMenubutton')
        self.heightMenuButton.grid(row=0, column=2, sticky=tk.EW, padx=(0, 8))
        self.makeFilterMenu(self.heightMenuButton, heightOptions, self.heightClassVar)

        #weight menubutton
        self.weightMenuButton = ttk.Menubutton(self.filtersFrame, text='Weight', style='filter.TMenubutton')
        self.weightMenuButton.grid(row=0, column=3, sticky=tk.EW, padx=(0, 8))
        self.makeFilterMenu(self.weightMenuButton, weightOptions, self.weightClassVar)

        #bst menubutton
        self.bstMenuButton = ttk.Menubutton(self.filtersFrame, text='BST', style='filter.TMenubutton')
        self.bstMenuButton.grid(row=0, column=4, sticky=tk.EW, padx=(0, 8))
        self.makeFilterMenu(self.bstMenuButton, bstOptions, self.bstRangeVar)

        #scrollable area
        self.resultsOuterFrame, self.resultsCanvas, self.resultsInnerFrame = self.makeScrollableFrame(self.mainFrame)
        self.resultsOuterFrame.grid(row=2, column=1, columnspan=2, sticky=tk.NSEW, padx=15, pady=15)

        self.refreshPokedexResults()


    def typeChartScreen(self):
        self.secondaryScreen()
        for i in range(2, 5):
            self.rowconfigure(i, weight=0)

        self.makeTitle('Type Chart')

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonSideBallIcon, compound=tk.TOP, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonSideBookIcon, compound=tk.TOP, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonSideArrowIcon, compound=tk.TOP, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #type chart image
        self.chartLabel = ttk.Label(self.mainFrame, image=self.typeChartImage, anchor='center')
        self.chartLabel.grid(column=0, row=2, padx=15, pady=15, sticky=tk.NSEW)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def pokedexScreen(self):
        self.secondaryScreen()
        self.makeDetailsFrame()

        self.makeTitle('Pokédex')
        
        #create side frame buttons
        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonSideBookIcon, compound=tk.TOP, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonSideArrowIcon, compound=tk.TOP, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        self.dexSelectFrame()

    def encyclopediaScreen(self):
        self.secondaryScreen()

        self.makeTitle('Encyclopedia')

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonSideBallIcon, compound=tk.TOP, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonTeam = ttk.Button(self.sideFrame, text='Team Rater', image=self.buttonSideArrowIcon, compound=tk.TOP, command=self.showTeamraterScreen, style='main.TButton')
        self.buttonTeam.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def teamraterScreen(self):
        self.secondaryScreen()

        self.makeTitle('Team Rater')

        #create side frame buttons
        self.buttonDex = ttk.Button(self.sideFrame, text='Pokédex', image=self.buttonSideBallIcon, compound=tk.TOP, command=self.showPokedexScreen, style='main.TButton')
        self.buttonDex.grid(row=1, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonEncyc = ttk.Button(self.sideFrame, text='Encyclopedia', image=self.buttonSideBookIcon, compound=tk.TOP, command=self.showEncyclopediaScreen, style='main.TButton')
        self.buttonEncyc.grid(row=2, sticky=tk.NSEW, padx=10, pady=10)

        self.buttonChart = ttk.Button(self.sideFrame, text='Type Chart', image=self.buttonSideChartIcon, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonChart.grid(row=3, sticky=tk.NSEW, padx=10, pady=10)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    def makeScrollableFrame(self, parent):
        #frame for canvas and scrollbar
        scrollOuterFrame = ttk.Frame(parent)

        scrollOuterFrame.rowconfigure(0, weight=1)
        scrollOuterFrame.columnconfigure(0, weight=1)

        #canvas
        resultCanvas = tk.Canvas(scrollOuterFrame, highlightthickness=0, bg=self.colours['framecolor'])
        resultCanvas.grid(row=0, column=0, sticky=tk.NSEW)

        #scrollbar
        resultsScrollbar = ttk.Scrollbar(scrollOuterFrame, orient='vertical', command=resultCanvas.yview)
        resultsScrollbar.grid(row=0, column=1, sticky=tk.NS)

        resultCanvas.configure(yscrollcommand=resultsScrollbar.set)

        #frame for buttons
        scrollInnerFrame = ttk.Frame(resultCanvas)
        scrollInnerWindow = resultCanvas.create_window((0, 0), window=scrollInnerFrame, anchor='nw')

        def frameConfigure(event):
            resultCanvas.configure(scrollregion=resultCanvas.bbox('all'))
        
        #makes inner frame match canvas width
        def canvasConfigure(event):
            resultCanvas.itemconfigure(scrollInnerWindow, width=event.width)
        
        scrollInnerFrame.bind('<Configure>', frameConfigure)
        resultCanvas.bind('<Configure>', canvasConfigure)

        #mousewheel scrolling
        def mouseWheel(event):
            resultCanvas.yview_scroll(int(-1*(event.delta/120)), 'units')
        
        #only scrolls when mouse over scrollable area
        resultCanvas.bind('<Enter>', lambda e: resultCanvas.bind_all('<MouseWheel>', mouseWheel))
        resultCanvas.bind('<Leave>', lambda e: resultCanvas.unbind_all('<MouseWheel>'))

        return scrollOuterFrame, resultCanvas, scrollInnerFrame
                            
    def populateResultsGrid(self, rows):
        if not hasattr(self, 'resultsInnerFrame'):
            return
        
        for widget in self.resultsInnerFrame.winfo_children():
            widget.destroy()

        self.resultSpriteRefs = {}

        #grid settings
        self.columns = 3
        self.cardPadX = 10
        self.cardPadY = 10

        for index, (dexMonID, monName, spriteURL) in enumerate(rows):
            self.cardRow = index//self.columns
            self.cardColumn = index%self.columns

            #card frame
            self.card = ttk.Frame(self.resultsInnerFrame, padding=8, style='TFrame')
            self.card.grid(row=self.cardRow, column=self.cardColumn, sticky=tk.NSEW, padx=self.cardPadX, pady=self.cardPadY)

            self.resultsInnerFrame.columnconfigure(self.cardColumn, weight=1)

            #sprite label
            spriteLabel = ttk.Label(self.card, text='')
            spriteLabel.grid(row=0, column=0, sticky=tk.N, pady=(0, 6))

            #name label
            nameLabel = ttk.Label(self.card, text=monName, anchor='center', style='progress.TLabel', wraplength=160)
            nameLabel.grid(row=1, column=0, sticky=tk.EW)

            #clickable card
            selectButton = ttk.Button(self.card, text='', style='small.TButton', command=lambda dID=dexMonID: self.showMonDetails(dID))
            selectButton.place(relx=0, rely=0, relwidth=1, relheight=1)
            selectButton.lift()

            #if url exists, load sprite async
            if spriteURL:
                threading.Thread(target=self.loadSpriteToLabel, args=(spriteURL, spriteLabel, dexMonID), daemon=True).start()

    def refreshPokedexResults(self):
        if not hasattr(self, 'resultsInnerFrame'):
            return

        #form criteria dictionary from inputs
        criteria = self.makePokedexCriteria()

        #for building buttons/cards
        rows = TUPdatabase.searchDexMonsForButtons(self.currentDexID, criteria)

        #update scrollable grid
        self.populateResultsGrid(rows)

        if rows:
            self.showMonDetails(rows[0][0])
    
    def loadSpriteToLabel(self, spriteURL, label, monID):
        try:
            response = requests.get(spriteURL, timeout=5)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            image = image.resize((96, 96))
            tkImage = ImageTk.PhotoImage(image)

            def apply():
                label.configure(image=tkImage)
                self.resultSpriteRefs[monID] = tkImage
            
            self.after(0, apply)
        except:
            pass

    def showMonDetails(self, dexMonID):
        mon = TUPdatabase.returnDexMon(dexMonID)
        
        if not mon:
            return

        #update labels
        self.detailsNameLabel.configure(text=mon["MonName"])

        infoText = (f'Species: {mon["Species"]}\n'
                    f'Type: {mon["Type1"]}' + (f' / {mon["Type2"]}' if mon["Type2"] else '') + '\n'
                    f'Height: {mon["Height"]} m\n'
                    f'Weight: {mon["Weight"]} kg\n'
                    f'BST: {mon["BST"]}\n\n'
                    f"{mon['FlavorText'] or ''}\n\n"
                    f"Location: {mon['Location'] or ''}"
                    )
        self.detailsInfoLabel.configure(text=infoText)

        #update sprite
        sprite = self.loadCachedSprite(mon["SpriteURL"])
        if sprite:
            self.detailsSpriteLabel.grid()
            self.detailsSpriteLabel.configure(image=sprite)
            self.detailsSpriteRef = sprite
        else:
            self.detailsSpriteLabel.configure(image='')
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None

    def makeFilterMenu(self, menuButton, options, variable):
        menu = tk.Menu(menuButton, tearoff=False)
        menuButton['menu'] = menu

        for label, value in options:
            menu.add_radiobutton(label=label, value=value, variable=variable, command=self.refreshPokedexResults)
        
        return menu
    
    def makeDetailsFrame(self):
        self.detailsFrame = ttk.Frame(self.mainFrame, padding=(20, 20), style='TFrame')
        self.detailsFrame.grid(row=0, column=0, rowspan=4, sticky=tk.NSEW, padx=15, pady=15)

        self.detailsFrame.rowconfigure(0, weight=0) #name
        self.detailsFrame.rowconfigure(1, weight=0) #sprite
        self.detailsFrame.rowconfigure(2, weight=1) #info
        self.detailsFrame.rowconfigure(3, weight=0)
        self.detailsFrame.columnconfigure(0, weight=1)

        #name label
        self.detailsNameLabel = ttk.Label(self.detailsFrame, text='Select Pokémon', anchor='center', style='small.TLabel')
        self.detailsNameLabel.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))

        #sprite label
        self.detailsSpriteLabel = ttk.Label(self.detailsFrame, text='', anchor='center')
        self.detailsSpriteLabel.grid(row=1, column=0, pady=(0, 10))
        self.detailsSpriteLabel.grid_remove()

        #info label
        self.detailsInfoLabel = ttk.Label(self.detailsFrame, text='', anchor='nw', justify='left', style='progress.TLabel', wraplength=420)
        self.detailsInfoLabel.grid(row=2, column=0, sticky=tk.NSEW)

        #sprite reference
        self.detailsSpriteRef = None


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
            self.loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
            return
        
        #checks login details are valid
        success, userID = TUPdatabase.checkLogin(username, password)

        if success:
            self.currentUserID = userID
            self.showMainMenu()
        else:
            self.loginErrorLabel.config(text='Invalid username or password')
            self.loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)

    def tryRegister(self):
        #retrieve user input from entry widgets
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        #if no username or password are entered
        if not username or not password:
            self.loginErrorLabel.config(text='Please enter a username and password')
            self.loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
            return
        
        #tries to add details to database
        try:
            TUPdatabase.addUser(username, password)
            self.loginErrorLabel.config(text='Account made - Please login')
            self.loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
        
        #error message if username already exists
        except sqlite3.IntegrityError:
            self.loginErrorLabel.config(text='Username already exists')
            self.loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self.loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)

    def makePokedexCriteria(self):
        if hasattr(self, 'searchEntry'):
            name = self.searchEntry.get().strip()
        else:
            name = ''
        
        #maps to numeric ranges
        heightMap = {'Any': (None, None), 'Small': (0.0, 1.0), 'Medium': (1.0, 2.0), 'Large': (2.0, 100.0),}
        weightMap = {'Any': (None, None), 'Light': (0.0, 25.0), 'Medium': (25.0, 100.0), 'Heavy': (100.0, 10000.0),}
        bstMap = {'Any': (None, None), 'Low': (0, 300), 'Medium': (300, 500), 'High': (500, 9999),}

        heightMin, heightMax = heightMap.get(self.heightClassVar.get(), (None, None))
        weightMin, weightMax = weightMap.get(self.weightClassVar.get(), (None, None))
        bstMin, bstMax = bstMap.get(self.bstRangeVar.get(), (None, None))

        criteria = {'name': name if name else None, 'type1': self.type1Var.get() or None, 'type2': self.type2Var.get() or None, 'heightMin': heightMin, 'heightMax': heightMax, 'weightMin': weightMin, 'weightMax': weightMax, 'bstMin': bstMin, 'bstMax': bstMax,}

        return criteria

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

    def makeTitle(self, text):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self.titleLabel = ttk.Label(self, text=text, anchor = 'center')
        self.titleLabel.grid(**titleOptions)

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