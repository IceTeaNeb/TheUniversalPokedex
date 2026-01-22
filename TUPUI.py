#The Universal Pokédex - User Interface

#-------------------imports--------------------#
import TUPitems
import TUPdatabase
import tkinter as tk
import os
import requests
import threading
import ast
import sqlite3
from tkinter import PhotoImage, ttk
from tkinter.messagebox import showinfo, askyesno
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

        #sprite cache to reduce loading times
        self.spriteCache = {}

        #filter
        self.type1Var = tk.StringVar(value='Any')
        self.type2Var = tk.StringVar(value='Any')
        self.heightClassVar = tk.StringVar(value='Any')
        self.weightClassVar = tk.StringVar(value='Any')
        self.bstRangeVar = tk.StringVar(value='Any')

    #retrieves sprite using given URL
    def getSprite(self, URL, label):
        response = requests.get(URL)
        monImage = Image.open(BytesIO(response.content))
        self.monSprite = ImageTk.PhotoImage(monImage)
        self.after(0, label.configure(image=self.monSprite))

    #loads a sprite from self.spriteCache
    def loadCachedSprite(self, spriteURL, size=(192, 192)):

        #if no sprite URL return None
        if not spriteURL:
            return None
        
        cacheKey = (spriteURL, size)
        #if sprite URL in cache, return URL
        if cacheKey in self.spriteCache:
            return self.spriteCache[cacheKey]
        
        try:
            response = requests.get(spriteURL, timeout=5)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image = image.resize(size, Image.NEAREST)
            sprite = ImageTk.PhotoImage(image)
            self.spriteCache[cacheKey] = sprite
            return sprite
        except:
            return None

    #make frame for main buttons in menu
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

    #make right frame in menu
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

    #make menu grid
    def makeMenuGrid(self):
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=12)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=5)

        self.titleOptions = {'column': 0, 'row': 0, 'columnspan': 2, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self.titleLabel = ttk.Label(self, text='The Universal Pokédex', anchor = 'center')
        self.titleLabel.grid(**self.titleOptions)

    #make secondary screen for Pokédex, Encyclopedia, Team Rater, Type Chart
    def secondaryScreen(self):
        #make window grid
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=20)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=20)

        #create frames
        self.mainFrame = ttk.Frame(self)
        self.mainFrame.grid(row=1, column=1, sticky=tk.NSEW, padx=15, pady=15)
        self.mainFrame.rowconfigure(0, weight=0, minsize=80)
        self.mainFrame.rowconfigure(1, weight=0, minsize=60)
        self.mainFrame.rowconfigure(2, weight=1)
        self.mainFrame.rowconfigure(3, weight=1)

        self.mainFrame.columnconfigure(0, weight=1, uniform='main')
        self.mainFrame.columnconfigure(1, weight=2, uniform='main')
        self.mainFrame.columnconfigure(2, weight=3, uniform='main')
        self.mainFrame.columnconfigure(3, weight=2, uniform='main')


        self.sideFrame = ttk.Frame(self)
        self.sideFrame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW, padx=15, pady=15)
        self.sideFrame.rowconfigure(0, weight=2)
        for i in range(1, 4):
            self.sideFrame.rowconfigure(i, weight=20)
        self.sideFrame.columnconfigure(0, weight=1)

    #make frame for choosing generation number of dex
    def dexSelectFrame(self):
        #frame
        self.dexFrame = ttk.Frame(self.mainFrame)
        for i in range(1, 6):
            self.dexFrame.rowconfigure(i, weight=1)
        self.dexFrame.columnconfigure(0, weight=1)
        self.dexFrame.columnconfigure(1, weight=1)

        #gridding the different buttons for each gen
        for i in range(1, 6):
            num=str(i)
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda n=num: [self.dexFrame.destroy(), self.pokemonFrame(n)])
            self.genButton.grid(row=i, column=0, padx=15, pady=15, sticky=tk.NSEW)

        for i in range(1, 5):
            num=str(i+5)
            self.genButton = ttk.Button(self.dexFrame, text=f'Gen {num}', style='enter.TButton', command=lambda n=num: [self.dexFrame.destroy(), self.pokemonFrame(n)])
            self.genButton.grid(row=i, column=1, padx=15, pady=15, sticky=tk.NSEW)

        self.dexFrame.grid(row=0, column=0, rowspan=4, columnspan=4, padx=15, pady=15, sticky=tk.NSEW)

    #making frame for Pokédex, where Pokémon can be searched, filtered, selected, displayed, added and deleted
    def pokemonFrame(self, gen):
        self.genNum = int(gen)
        self.currentDexID = self.genNum

        self.makeDetailsFrame()

        #change title to match generation chosen
        self.makeTitle(f'Pokédex - Gen {self.genNum}')

        #checks that the desired dex exists first
        TUPdatabase.ensureDexExists(self.currentDexID, self.genNum, "Default")

        #add mon button
        self.addButton = ttk.Button(self.mainFrame, text='Add', style='enter.TButton', command=self.openAddMonPopup)
        self.addButton.grid(row=0, column=0, sticky=tk.EW, pady=(15, 10), padx=(0, 10))

        #delete button
        self.deleteButton = ttk.Button(self.mainFrame, text='Delete', style='enter.TButton', command=self.onDeleteSelectedMon)
        self.deleteButton.grid(row=0, column=1, sticky=tk.EW, pady=(15, 10), padx=(10, 10))
        self.deleteButton.state(["disabled"])

        #search entry
        self.searchEntry = ttk.Entry(self.mainFrame, font = ('Trebuchet MS', 20, 'bold'))
        self.searchEntry.grid(row=0, column=2, sticky=tk.EW, pady=(15, 10), padx=(0, 10))
        self.searchEntry.bind('<Return>', lambda e: self.refreshPokedexResults())

        #search button
        self.searchButton = ttk.Button(self.mainFrame, text='Enter', style='enter.TButton', command=self.refreshPokedexResults)
        self.searchButton.grid(row=0, column=3, sticky=tk.EW, pady=(15, 10), padx=(0, 0))

        #filter
        self.filtersFrame = ttk.Frame(self.mainFrame)
        self.filtersFrame.grid(row=1, column=2, columnspan=2, sticky=tk.EW, pady=(0, 10), padx=(0, 10))
        for column in range(5):
            self.filtersFrame.columnconfigure(column, weight=1)

        #possible type options for filtering
        typeOptions = [('Any', 'Any'), ('Normal', 'Normal'), ('Fire', 'Fire'), ('Water', 'Water'),
                       ('Grass', 'Grass'), ('Electric', 'Electric'), ('Ice', 'Ice'), ('Fighting', 'Fighting'),
                       ('Poison', 'Poison'), ('Ground', 'Ground'), ('Flying', 'Flying'), ('Psychic', 'Psychic'),
                       ('Bug', 'Bug'), ('Rock', 'Rock'), ('Ghost', 'Ghost'), ('Dragon', 'Dragon'),
                       ('Dark', 'Dark'), ('Steel', 'Steel'), ('Fairy', 'Fairy')]
        
        #possible height, weight and bst options for filtering
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
        self.resultsOuterFrame.grid(row=2, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW, padx=15, pady=15)

        #refreshes shown Pokémon
        self.refreshPokedexResults()

    def encyclopediaFrame(self):
        self.makeDetailsFrame()
        self.makeTitle("Encyclopedia")

        #search entry
        self.encycSearchEntry = ttk.Entry(self.mainFrame, font=(self.FONT, 20, 'bold'))
        self.encycSearchEntry.grid(row=0, column=2, sticky=tk.EW, pady=(15, 10), padx=(0, 10))
        self.encycSearchEntry.bind('<Return>', lambda e: self.refreshEncyclopediaResults())

        #search button
        self.encycSearchButton = ttk.Button(self.mainFrame, text='Enter', style='enter.TButton', command=self.refreshEncyclopediaResults)
        self.encycSearchButton.grid(row=0, column=3, sticky=tk.EW, pady=(15, 10), padx=(0, 0))

        #filters frame
        self.encycFiltersFrame = ttk.Frame(self.mainFrame)
        self.encycFiltersFrame.grid(row=1, column=2, columnspan=2, sticky=tk.EW, pady=(0, 10), padx=(0, 10))

        for column in range(3):
            self.encycFiltersFrame.columnconfigure(column, weight=1)

        #string vars
        self.encycGenVar = tk.StringVar(value='Any')
        self.encycTypeVar = tk.StringVar(value='Any')
        self.encycItemTypeVar = tk.StringVar(value='Pokémon')

        #item type menu
        self.encycItemMenu = ttk.Menubutton(self.encycFiltersFrame, text='Item', style='filter.TMenubutton')
        self.encycItemMenu.grid(row=0, column=0, sticky=tk.EW, padx=(0, 8))
        
        itemOptions = [('Pokémon', 'Pokémon'), ('Move', 'Move'), ('Ability', 'Ability')]

        self.makeFilterMenu(self.encycItemMenu, itemOptions, self.encycItemTypeVar)

        #generation menu
        self.encycGenMenu = ttk.Menubutton(self.encycFiltersFrame, text='Gen', style='filter.TMenubutton')
        self.encycGenMenu.grid(row=0, column=1, sticky=tk.EW, padx=(0, 8))
        
        genOptions = [('Any', 'Any')] + [((f'Gen {i}', str(i)) for i in range(1, 10))]

        self.makeFilterMenu(self.encycGenMenu, genOptions, self.encycGenVar)

        #type menu
        self.encycTypeMenu = ttk.MenuButton(self.encycFiltersFrame, text='Type', style='filter.TMenubutton')
        self.encycTypeMenu.grid(row=0, column=2, sticky=tk.EW, padx=(0, 8))

        typeOptions = [('Any', 'Any'), ('Normal', 'Normal'), ('Fire', 'Fire'), ('Water', 'Water'),
                       ('Grass', 'Grass'), ('Electric', 'Electric'), ('Ice', 'Ice'), ('Fighting', 'Fighting'),
                       ('Poison', 'Poison'), ('Ground', 'Ground'), ('Flying', 'Flying'), ('Psychic', 'Psychic'),
                       ('Bug', 'Bug'), ('Rock', 'Rock'), ('Ghost', 'Ghost'), ('Dragon', 'Dragon'),
                       ('Dark', 'Dark'), ('Steel', 'Steel'), ('Fairy', 'Fairy')]
        
        self.makeFilterMenu(self.encycTypeMenu, typeOptions, self.encycTypeVar)

        #scrollable results
        self.encycResultsOuter, self.encycResultsCanvas, self.encycResultsInner, self.makeScrollableFrame(self.mainFrame)
        self.encycResultsOuter.grid(row=2, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW, padx=15, pady=15)

        self.refreshEncyclopediaResults()
        
    #making screen for Type Chart section
    def typeChartScreen(self):
        self.secondaryScreen()
        for i in range(2, 5):
            self.rowconfigure(i, weight=0)

        #changing title
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

    #making screen for Pokédex
    def pokedexScreen(self):
        self.secondaryScreen()

        #change title
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

    #making screen for Encyclopedia
    def encyclopediaScreen(self):
        self.secondaryScreen()

        #change title
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

        #encyclopedia frame
        self.encyclopediaFrame()



    #making screen for Team Rater
    def teamraterScreen(self):
        self.secondaryScreen()

        #change title
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

    #making frame for scrollable canvas
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

        #defines the entire area of the canvas to be scrollable
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

    #populates grid with Pokémon that match the search/filter criteria  
    def populateResultsGrid(self, rows):
        if not hasattr(self, 'resultsInnerFrame'):
            return
        
        for widget in self.resultsInnerFrame.winfo_children():
            widget.destroy()

        self.resultSpriteRefs = {}

        #grid settings
        self.columns = 4
        self.cardPadX = 10
        self.cardPadY = 10

        #for each Pokémon that matches criteria
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
            nameLabel = ttk.Label(self.card, text=monName.title(), anchor='center', style='progress.TLabel', wraplength=160)
            nameLabel.grid(row=1, column=0, sticky=tk.EW)

            #clickable card
            def onClick(event, dID=dexMonID):
                self.onSelectMon(dID)

            self.card.bind("<Button-1>", onClick)
            spriteLabel.bind("<Button-1>", onClick)
            nameLabel.bind("<Button-1>", onClick)

            #if url exists, load sprite async
            if spriteURL:
                threading.Thread(target=self.loadSpriteToLabel, args=(spriteURL, spriteLabel, dexMonID), daemon=True).start()

    #populates grid with results that match the criteria  
    def populateResultsGrid(self, rows):
        for widget in self.encycInnerFrame.winfo_children():
            widget.destroy()

        self.encycSpriteRefs = {}

        #grid settings
        self.columns = 4
        self.cardPadX = 10
        self.cardPadY = 10

        itemType = self.encycItemTypeVar.get()

        #for each Pokémon that matches criteria
        for index, (itemKey, displayName, spriteURL) in enumerate(rows):
            self.cardRow = index//self.columns
            self.cardColumn = index%self.columns

            #card frame
            self.card = ttk.Frame(self.encycInnerFrame, padding=8, style='TFrame')
            self.card.grid(row=self.cardRow, column=self.cardColumn, sticky=tk.NSEW, padx=self.cardPadX, pady=self.cardPadY)

            self.encycResultsInner.columnconfigure(self.cardColumn, weight=1)

            #sprite label
            spriteLabel = ttk.Label(self.card, text='')
            spriteLabel.grid(row=0, column=0, sticky=tk.N, pady=(0, 6))

            #name label
            nameLabel = ttk.Label(self.card, text=displayName, anchor='center', style='progress.TLabel', wraplength=160)
            nameLabel.grid(row=1, column=0, sticky=tk.EW)

            #clickable card
            def onClick(event, k=itemKey):
                self.onSelectEncyclopediaItem(k)

            self.card.bind("<Button-1>", onClick)
            spriteLabel.bind("<Button-1>", onClick)
            nameLabel.bind("<Button-1>", onClick)

            #load sprites for pokemon only
            if itemType =='Pokémon' and spriteURL:
            #if url exists, load sprite async
                if spriteURL:
                    threading.Thread(target=self.loadSpriteToLabel, args=(spriteURL, spriteLabel, itemKey), daemon=True).start()

    #refreshes displayed Pokémon when user changes criteria
    def refreshPokedexResults(self):
        if not hasattr(self, 'resultsInnerFrame'):
            return

        #form criteria dictionary from inputs
        criteria = self.makePokedexCriteria()

        #for building buttons/cards
        rows = TUPdatabase.searchDexMonsForButtons(self.currentUserID, self.currentDexID, criteria)

        #update scrollable grid
        self.populateResultsGrid(rows)

        if rows:
            rowIDs = [row[0] for row in rows]
            current = getattr(self, 'selectedDexMonID', None)

            if current in rowIDs:
                self.showMonDetails(current)
            else:
                self.selectedDexMonID = rows[0][0]
                self.showMonDetails(self.selectedDexMonID)
        
        else:
            self.selectedDexMonID = None
            self.detailsNameLabel.configure(text='No results')
            self.detailsInfoText.config(state='normal')
            self.detailsInfoText.delete('1.0', 'end')
            self.detailsInfoText.configure(state='disabled')
            self.detailsSpriteLabel.configure(image='')
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None

            if hasattr(self, "deleteButton"):
                self.deleteButton.state(["disabled"])

    #refreshes displayed results when user changes criteria
    def refreshEncyclopediaResults(self):
        if not hasattr(self, 'encycInnerFrame'):
            return

        criteria = {'itemType': self.encycItemTypeVar.get(),
                    'gen': self.encycGenVar.get(),
                    'type': self.encycTypeVar.get(),
                    'query': self.encycSearchEntry.get()}

        #for building buttons/cards
        rows = TUPitems.searchEncyclopedia(criteria, limit=200)

        #update scrollable grid
        self.populateEncyclopediaGrid(rows)

        if rows:
            firstKey = rows[0][0]
            self.onSelectEncyclopediaItem(firstKey)
    
    #loads specified Pokémon sprite to label
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

    #shows details of a specific Pokémon in the database
    def showMonDetails(self, dexMonID):
        mon = TUPdatabase.returnDexMonForUser(self.currentUserID, dexMonID)
        
        if not mon:
            self.detailsNameLabel.configure(text='No details for this Pokémon')
            self.detailsInfoText.config(state='normal')
            self.detailsInfoText.delete('1.0', 'end')
            self.detailsInfoText.insert('1.0', 'No details for this Pokémon')
            self.detailsInfoText.configure(state='disabled')
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None
            return

        #update labels
        self.detailsNameLabel.configure(text=mon["MonName"].title())

        #stats, base or custom
        statsLine = f"HP {mon['UHP']} / Atk {mon['UAtk']} / Def {mon['UDef']} / SpA {mon['USpA']} / SpD {mon['USpD']} / Spe {mon['USpe']}"
        bst = sum(int(mon[i]) for i in ["UHP", "UAtk", "UDef", "USpA", "USpD", "USpe"] if mon.get(i) is not None)
                  
        typeLine = self.titleName(mon["Type1"])
        if mon["Type2"]:
            typeLine += " / " + self.titleName(mon["Type2"])

        if mon.get("PreEvo"):
            preEvo = self.titleName(mon["PreEvo"])
        else:
            preEvo = "None"

        evoBlock = self.formatEvo(mon.get("Evo"))
        eggGroupsBlock = self.formatPipeBlock("Egg Groups", mon.get("EggGroups"))
        locationsBlock = self.formatPipeBlock("Locations", mon.get("Location"), maxItems=10)

        movesRaw = mon.get("Moves") or ""
        movesBlock = self.formatPipeBlock("Moves", movesRaw)

        abilitiesRaw = mon.get('Ability') or ''
        abilitiesBlock = self.formatPipeBlock('Abilities', abilitiesRaw, maxItems=6)

        flavorText = (mon.get("FlavorText") or "").strip()

        infoText = (f'National Dex Number: {mon.get("DexNum")}\n'
                    f'Species: {self.titleName(mon.get("Species"))}\n'
                    f'Type: {typeLine}\n'
                    f'Height: {mon.get("Height")} m\n'
                    f'Weight: {mon.get("Weight")} kg\n'
                    f'Egg Cycle: {mon.get("EggCycle")}\n'
                    f'{eggGroupsBlock}\n'
                    f'Pre-Evolution: {preEvo}\n\n'
                    f'{evoBlock}\n\n'
                    f'Stats: {statsLine}\n'
                    f'{abilitiesBlock}\n\n'
                    f'{movesBlock}\n\n'
                    f'BST (from shown stats): {bst}\n\n'
                    f'{("Flavor Text: " + flavorText) if flavorText else "Flavor Text: None"}\n\n'
                    f'{locationsBlock}\n\n'
                    )
        
        self.detailsInfoText.configure(state='normal')
        self.detailsInfoText.delete('1.0', 'end')
        self.detailsInfoText.insert('1.0', infoText)
        self.detailsInfoText.configure(state='disabled')

        #update sprite
        sprite = self.loadCachedSprite(mon.get('SpriteURL'), size=(256, 256))
        if sprite:
            self.detailsSpriteLabel.grid()
            self.detailsSpriteLabel.configure(image=sprite)
            self.detailsSpriteRef = sprite
        else:
            self.detailsSpriteLabel.configure(image='')
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None

    def showEncyclopediaDetails(self, itemKey):
        itemType = self.encycItemTypeVar.get()
        chosenGen = self.encycGenVar.get()
        if chosenGen != 'Any':
            chosenGenNum = int(chosenGen)
        else:
            chosenGenNum = 9

        self.detailsSpriteLabel.grid_remove()
        self.detailsSpriteRef = None

        try:
            if itemType == 'Pokémon':
                monObj = TUPitems.Mon('mon', int(itemKey), chosenGenNum)

                #update sprite
                sprite = self.loadCachedSprite(monObj.getSpriteURL, size=(256, 256))
                if sprite:
                    self.detailsSpriteLabel.grid()
                    self.detailsSpriteLabel.configure(image=sprite)
                    self.detailsSpriteRef = sprite
                else:
                    self.detailsSpriteLabel.configure(image='')
                    self.detailsSpriteLabel.grid_remove()
                    self.detailsSpriteRef = None

                #update labels
                self.detailsNameLabel.configure(text=monObj.getItemName.title())

                #stats, base or custom
                statsLine = f"HP {monObj.getHP()} / Atk {monObj.getAtk()} / Def {monObj.getDef()} / SpA {monObj.getSpA()} / SpD {monObj.getSpD()} / Spe {monObj.getSpe()}"
                bst = monObj.getBST()
                        
                typeLine = {self.titleName(monObj.getType1())}
                if monObj.getType2() != -1:
                    typeLine += " / " + self.titleName(monObj.getType2())

                if monObj.getPreEvo():
                    preEvo = self.titleName(monObj.getPreEvo())
                else:
                    preEvo = "None"

                evoBlock = self.formatEvo(monObj.getEvoList())
                eggGroupsBlock = self.formatPipeBlock("Egg Groups", monObj.getEggGroups)
                locationsBlock = self.formatPipeBlock("Locations", monObj.getLocations(), maxItems=10)

                movesRaw = monObj.getMoves or ""
                movesBlock = self.formatPipeBlock("Moves", movesRaw)

                abilitiesRaw = monObj.getAbilities() or ''
                abilitiesBlock = self.formatPipeBlock('Abilities', abilitiesRaw, maxItems=6)

                flavorText = (monObj.getFlavorText or "").strip()

                infoText = (f'National Dex Number: {monObj.getDexNum}\n'
                            f'Species: {self.titleName(monObj.getSpecies)}\n'
                            f'Type: {typeLine}\n'
                            f'Height: {monObj.getHeight()} m\n'
                            f'Weight: {monObj.getWeight()} kg\n'
                            f'Egg Cycle: {monObj.getEggCycle}\n'
                            f'{eggGroupsBlock}\n'
                            f'Pre-Evolution: {preEvo}\n\n'
                            f'{evoBlock}\n\n'
                            f'Stats: {statsLine}\n'
                            f'{abilitiesBlock}\n\n'
                            f'{movesBlock}\n\n'
                            f'BST: {bst}\n\n'
                            f'{("Flavor Text: " + flavorText) if flavorText else "Flavor Text: None"}\n\n'
                            f'{locationsBlock}\n\n'
                            )
            
            elif itemType == 'Move':
                moveObj = TUPitems.Move('move', int(itemKey), chosenGenNum)
                self.detailsNameLabel.configure(text=moveObj.getItemName().replace('-', ' ').title())

                infoText = (f'Type: {moveObj.getType().name.title()}\n'
                            f'Damage Class: {moveObj.getDmgClass().name.title()}\n'
                            f'Power: {moveObj.getPower()}\n'
                            f'Accuracy: {moveObj.getAccuracy()}\n'
                            f'PP: {moveObj.getPP()}\n'
                            f'Priority: {moveObj.getPriority()}\n'
                            f"Flavor Text: {moveObj.getFlavorText() or 'None'}\n"
                            )
            
            else:   #ability
                abilObj = TUPitems.Ability('ability', int(itemKey), chosenGenNum)
                self.detailsNameLabel.configure(text=abilObj.getItemName().replace('-', ' ').title())

                infoText = (f"Flavor Text: {moveObj.getFlavorText() or 'None'}\n")
            
            self.detailsInfoText.configure(state='normal')
            self.detailsInfoText.delete('1.0', 'end')
            self.detailsInfoText.insert('1.0', infoText)
            self.detailsInfoText.configure(state='disabled')
        
        except:
            self.detailsInfoText.configure(text='No results')
            self.detailsInfoText.configure(state='normal')
            self.detailsInfoText.delete('1.0', 'end')
            self.detailsInfoText.insert('1.0', 'Could not load details from PokéAPI.')
            self.detailsInfoText.configure(state='disabled')        
                

    def titleName(self, text):
        if not text:
            return ""
        return str(text).replace("-", " ").title()

    #splits text into a list
    def splitPipeList(self, text):
        if not text:
            return []
        parts = [part.strip() for part in str(text).split("|") if part.strip()]
        return parts
    
    #formats text to be displayed
    def formatPipeBlock(self, label, text, maxItems=12):
        items = [self.titleName(name) for name in self.splitPipeList(text)]

        if not items:
            return f"{label}: None"
        
        if len(items) > maxItems:
            shown = items[:maxItems]
            return f"{label}: " + ", ".join(shown) + f" (+{len(items)-maxItems} more)"

        return f"{label}: " + ", ".join(items)
    
    #formats evolution
    def formatEvo(self, evoText):
        if not evoText:
            return "Evolution: None"
        
        try:
            evoObj = ast.literal_eval(evoText)
        except:
            return f"Evolution: {evoText}"
        
        base = " → ".join(self.titleName(name) for name in (evoObj[0] if isinstance(evoObj[0], list) else evoObj))
        branches = []
        for branch in evoObj[1:]:
            if isinstance(branch, list) and branch:
                branches.append(" → ".join(self.titleName(name) for name in branch))

        if branches:
            return "Evolution:\n " + base + "\n " + "\n ".join(branches)
        return "Evolution:\n " + base

    #when a Pokémon is selected
    def onSelectMon(self, dexMonID):
        self.selectedDexMonID = dexMonID

        if hasattr(self, "deleteButton"):
            self.deleteButton.state(["!disabled"])

        self.showMonDetails(dexMonID)

    def onSelectEncyclopediaItem(self, itemKey):
        self.selectedEncycKey = itemKey
        self.showEncyclopediaDetails(itemKey)

    #make menu for filtering
    def makeFilterMenu(self, menuButton, options, variable):
        menu = tk.Menu(menuButton, tearoff=False)
        menuButton['menu'] = menu

        for label, value in options:
            menu.add_radiobutton(label=label, value=value, variable=variable, command=self.refreshPokedexResults)
        
        return menu
    
    #make frame for showing selected Pokémon information
    def makeDetailsFrame(self):
        self.detailsFrame = ttk.Frame(self.mainFrame, padding=(20, 20), style='TFrame')
        #self.detailsFrame.grid_propagate(False)
        self.detailsFrame.grid(row=1, column=0, columnspan=2, rowspan=3, sticky=tk.NSEW, padx=(15, 10), pady=15)

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

        #scrollable info label
        self.detailsInfoOuterFrame = ttk.Frame(self.detailsFrame, style='TFrame')
        self.detailsInfoOuterFrame.grid(row=2, column=0, sticky=tk.NSEW)

        self.detailsInfoOuterFrame.rowconfigure(0, weight=1)
        self.detailsInfoOuterFrame.columnconfigure(0, weight=1)

        self.detailsInfoScrollbar = ttk.Scrollbar(self.detailsInfoOuterFrame, orient='vertical')
        self.detailsInfoScrollbar.grid(row=0, column=1, sticky=tk.NS)

        self.detailsInfoText = tk.Text(self.detailsInfoOuterFrame, wrap='word', yscrollcommand=self.detailsInfoScrollbar.set, bg=self.colours['framecolor'], fg=self.colours['fgcolor'], font=(self.FONT, 10, 'bold'), relief='flat', highlightthickness=0, padx=8, pady=8)
        self.detailsInfoText.grid(row=0, column=0, sticky=tk.NSEW)

        self.detailsInfoScrollbar.configure(command=self.detailsInfoText.yview)

        self.detailsInfoText.configure(state='disabled')

        def scrollWheel(event):
            self.detailsInfoText.yview_scroll(int(-1*(event.delta/120)), 'units')

        self.detailsInfoText.bind('<Enter>', lambda e: self.detailsInfoText.bind_all('<MouseWheel>', scrollWheel))
        self.detailsInfoText.bind('<Leave>', lambda e: self.detailsInfoText.unbind_all('<MouseWheel>'))

        #sprite reference
        self.detailsSpriteRef = None
        
    #create popup window when user wants to add a Pokémon to the database
    def openAddMonPopup(self):
        statNames = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
        statVars = {}

        #popup window
        popup = tk.Toplevel(self)
        popup.title('Add Pokémon')
        popup.transient(self)
        popup.resizable(False, False)
        popup.grab_set() 
        popup.iconbitmap(self.iconPath)

        #add Pokémon frame
        self.addMonFrame = ttk.Frame(popup, padding=15)
        self.addMonFrame.grid(row=0, column=0, sticky=tk.NSEW)

        #dex number label
        self.dexNumLabel = ttk.Label(self.addMonFrame, text='Dex # or Name:', style='progress.TLabel')
        self.dexNumLabel.grid(row=0, column=0, sticky=tk.W)

        #dex number entry
        self.dexNumEntry = ttk.Entry(self.addMonFrame, width=12)
        self.dexNumEntry.grid(row=0, column=1, padx=(10, 0), sticky=tk.EW)
        self.dexNumEntry.focus_set()

        #custom stats label
        self.customStatsLabel = ttk.Label(self.addMonFrame, text='Custom Stats (Optional):', style='progress.TLabel')
        self.customStatsLabel.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(12, 6))

        for i, stat in enumerate(statNames):
            ttk.Label(self.addMonFrame, text=f"{stat}", style='progress.TLabel').grid(row=2+i, column=0, sticky=tk.W)
            var = tk.StringVar(value="")
            statVars[stat] = var
            ttk.Entry(self.addMonFrame, textvariable=var, width=12).grid(row=2+i, column=1, padx=(10, 0), sticky=tk.W)

        #parses integer
        def parseInt(text):
            text=text.strip()
            if text == '':
                return None
            else:
                return int(text)
        
        #normalises input
        def normaliseMonInput(text):
            text = text.strip()
            if text == '':
                return None
            return text.lower().replace(" ", "-")

        #when user presses add button
        def onAdd():
            userIn = self.dexNumEntry.get()
            monKey = normaliseMonInput(userIn)

            if not monKey:
                showinfo("Error", "Please enter a Dex number or Pokédex name.")
                return

            #Pokémon object
            try:
                if monKey.isdigit():
                    monObj = TUPitems.Mon('mon', int(monKey), self.genNum)
                else:
                    monObj = TUPitems.Mon('mon', monKey, self.genNum)
            except:
                showinfo("Error", "Could not load that Pokémon from the API.")
                return
            
            try:
                monFromGen = int(monObj.getItemFromGen())
            except:
                monFromGen = None

            if monFromGen is not None and monFromGen > self.genNum:
                showinfo("Wrong Generation", f"{monObj.getItemName().title()} is from Gen {monFromGen}, so it can't be added to a Gen {self.genNum} Dex.")
                return

            try:
                #gets details of Pokémon
                monData = {"dexNum": monObj.getDexNum(), "monName": monObj.getItemName(), "species": str(monObj.getSpecies()),
                        "type1": monObj.getType1().title(), "type2": None if monObj.getType2()==-1 else monObj.getType2().title(),
                        "height": float(monObj.getHeight()), "weight": float(monObj.getWeight()), "bst": int(monObj.getBST()),
                        "catchRate": int(monObj.getCatchRate()), "eggGroups": monObj.getEggGroups(), "gender": float(monObj.getGender()),
                        "eggCycle": int(monObj.getEggCycle()), "evo": str(monObj.getEvoList()), "preEvo": None if monObj.getPreEvo()==-1 else monObj.getPreEvo(),
                        "flavorText": monObj.getFlavorText(), "location": monObj.getLocations(), "spriteURL": monObj.getSpriteURL(), "moves": monObj.getMoves(),
                        "ability": ""
                        }
                
                #default is base stats
                baseStats = {"HP": int(monObj.getHP()), "Atk": int(monObj.getAtk()), "Def": int(monObj.getDef()),
                        "SpA": int(monObj.getSpA()), "SpD": int(monObj.getSpD()), "Spe": int(monObj.getSpe()),
                        }
                
                #override base stats with custom stats
                try:
                    stats = {}
                    for stat in statNames:
                        userValue = parseInt(statVars[stat].get())
                        if userValue is None:
                            stats[stat] = baseStats[stat]
                        else:
                            stats[stat] = userValue
                except ValueError:
                    showinfo("Invalid stats", "Stats must be integers or left blank.")
                    return
                
                #add Pokémon to database
                TUPdatabase.addMonFull(self.currentUserID, self.currentDexID, self.genNum, monData, moves=monObj.getMoves(), ability=monObj.getAbilities(), stats=stats)

            except:
                #error message
                showinfo("Error", "Could not add Pokémon.")
                return
            
            popup.destroy()
            self.refreshPokedexResults()
        
        #on add button
        self.onAddButton = ttk.Button(popup, text='Add', style='small.TButton', command=onAdd)
        self.onAddButton.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky=tk.EW)

    #when user clicks delete button while Pokémon is selected
    def onDeleteSelectedMon(self):
        dexMonID = getattr(self, "selectedDexMonID", None)

        #if no Pokémon is selected
        if dexMonID is None:
            showinfo("Delete Pokémon", "No Pokémon selected.")
            return
        
        mon = TUPdatabase.returnDexMon(dexMonID)
        if mon:
            monName = mon["MonName"]
        else:
            monName = 'this Pokémon'

        #popup asks user if they would like to delete the selected Pokémon
        if not askyesno("Delete Pokémon", f"Delete {monName} from the Dex?"):
            return
        
        #deletes Pokémon
        TUPdatabase.deleteMon(dexMonID)

        #clear selection
        self.selectedDexMonID = None
        self.refreshPokedexResults()

    #show login screen
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

    #attempts to log into account
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

    #attempts to register account
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

    #make filter criteria
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

        type1 = self.type1Var.get().strip()
        type2 = self.type2Var.get().strip()

        if type1 in ("", "Any"):
            type1 = None
        if type2 in ("", "Any"):
            type2 = None

        criteria = {'name': name if name else None, 'type1': type1, 'type2': type2, 'heightMin': heightMin, 'heightMax': heightMax, 'weightMin': weightMin, 'weightMax': weightMax, 'bstMin': bstMin, 'bstMax': bstMax,}

        return criteria

    #clears window
    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()

    #shows Type Chart screen
    def showTypeChartScreen(self):
        self.clearWindow()
        self.typeChartScreen()

    #shows Pokédex screen
    def showPokedexScreen(self):
        self.clearWindow()
        self.pokedexScreen()

    #shows Encyclopedia screen
    def showEncyclopediaScreen(self):
        self.clearWindow()
        self.encyclopediaScreen()

    #shows Team Rater Screen
    def showTeamraterScreen(self):
        self.clearWindow()
        self.teamraterScreen()

    #makes title
    def makeTitle(self, text):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self.titleLabel = ttk.Label(self, text=text, anchor = 'center')
        self.titleLabel.grid(**titleOptions)

    # def showProgressBar(self):
    #     #progress bar
    #     self.progressBarFrame = ttk.Frame(self.mainFrame)
    #     self.progressBarFrame.columnconfigure(0, weight=5)
    #     self.progressBarFrame.columnconfigure(1, weight=1)

    #     self.progressBar = ttk.Progressbar(self.progressBarFrame, mode='indeterminate')
    #     self.progressBar.grid(row=0, column=0, sticky=tk.NSEW, pady=15)

    #     self.progressBarText = ttk.Label(self.progressBarFrame, text='Loading...', style='progress.TLabel', anchor='center')
    #     self.progressBarText.grid(row=0, column=1, sticky=tk.NSEW, pady=15)

    #     self.progressBarFrame.grid(column=1, row=2, columnspan=2, sticky=tk.NSEW)
    #     self.progressBar.start()

    # def hideProgressBar(self):
    #     self.progressBar.stop()
    #     self.progressBarFrame.destroy()

    #shows main menu
    def showMainMenu(self):
        self.clearWindow()
        self.makeMenuGrid()
        self.makeButtonFrame()
        self.makeSideMenuFrame(self)