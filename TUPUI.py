#The Universal Pokédex - User Interface

#-------------------imports--------------------#
import TUPitems
import TUPdatabase
import TUPteamrater
import tkinter as tk
import os
import requests
import threading
import ast
import sqlite3
import pokebase as pb
from tkinter import PhotoImage, ttk
from tkinter.messagebox import showinfo, askyesno
from PIL import Image, ImageTk
from ctypes import windll
from io import BytesIO

#------------------------------------------Tkinter-------------------------------------------#
class mainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self._title('The Universal Pokédex')
        self._geometry('1280x780')
        self._configure(background='#ffffff')

        self._currentUserID = None

        #default theme is dark blue
        self._colours = {'bgcolor': '#7f7f7f', 'fgcolor': '#c1dbf3', 
                           'activecolor': '#595959', 'framecolor': '#404040', 
                           'darkcolor': '#232323', 'rootbg': '#232323'}

        self._themes = {
            'Light Blue': {'bgcolor': '#c1dbf3', 'fgcolor': '#ffffff', 
                           'activecolor': '#97c7f3', 'framecolor': '#deebf7', 
                           'darkcolor': '#d9d9d9', 'rootbg': '#ffffff'},
            'Light Red': {'bgcolor': '#ff7171', 'fgcolor': '#ffffff', 
                           'activecolor': '#ff4444', 'framecolor': '#d9d9d9', 
                           'darkcolor': '#bfbfbf', 'rootbg': '#ffffff'},
            'Dark Blue': {'bgcolor': '#7f7f7f', 'fgcolor': '#c1dbf3', 
                           'activecolor': '#595959', 'framecolor': '#404040', 
                           'darkcolor': '#232323', 'rootbg': '#232323'},
            'Dark Red': {'bgcolor': '#7f7f7f', 'fgcolor': '#ff7171', 
                           'activecolor': '#595959', 'framecolor': '#404040', 
                           'darkcolor': '#232323', 'rootbg': '#232323'},
        }

        self._themeVar = tk.StringVar(value='Change Theme')

        self._FONT = 'Pokemon X and Y'

        #fullscreen
        self._attributes('-fullscreen', True) #window becomes fullscreen automatically
        self._bind('<Escape>', lambda event: self._destroy())  #exits fullscreen if presses escape

        #change icon
        self._scriptDir = os.path.dirname(os.path.abspath(__file__))
        self._iconPath = os.path.join(self._scriptDir, 'assets', 'pokeball-icon.ico')
        if os.path.exists(self._iconPath):    
            self._iconbitmap(self._iconPath)
        
        #frame styles
        self._styleF = ttk.Style()
        self._styleF.theme_use('clam')
        self._styleF.configure('TFrame', background=self._colours['framecolor'])

        #button styles
        self._styleMainB = ttk.Style()
        self._styleMainB.theme_use('clam')
        self._styleMainB.configure('main.TButton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 35), bordercolor=self._colours['bgcolor'], darkcolor=self._colours['darkcolor'])
        self._styleMainB.map('main.TButton', background=[('active', self._colours['activecolor'])])
        
        self._styleEnterB = ttk.Style()
        self._styleEnterB.theme_use('clam')
        self._styleEnterB.configure('enter.TButton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 15), bordercolor=self._colours['bgcolor'])
        self._styleEnterB.map('enter.TButton', background=[('active', self._colours['activecolor'])])

        self._styleSmallB = ttk.Style()
        self._styleSmallB.theme_use('clam')
        self._styleSmallB.configure('small.TButton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 15), bordercolor=self._colours['bgcolor'], darkcolor=self._colours['darkcolor'])
        self._styleSmallB.map('small.TButton', background=[('active', self._colours['activecolor'])])

        #label styles
        self._styleL = ttk.Style()
        self._styleL.theme_use('clam')
        self._styleL.configure('TLabel', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 40), bordercolor=self._colours['bgcolor'], darkcolor=self._colours['darkcolor'])

        self._styleProgressL = ttk.Style()
        self._styleProgressL.theme_use('clam')
        self._styleProgressL.configure('progress.TLabel', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 10))

        self._styleSmallL = ttk.Style()
        self._styleSmallL.theme_use('clam')
        self._styleSmallL.configure('small.TLabel', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 28))

        #entry styles
        self._styleE = ttk.Style()
        self._styleE.theme_use('clam')
        self._styleE.configure('TEntry', fieldbackground=self._colours['bgcolor'], foreground=self._colours['fgcolor'], bordercolor=self._colours['bgcolor'])

        #menubutton styles
        self._styleMB = ttk.Style()
        self._styleMB.theme_use('clam')
        self._styleMB.configure('filter.TMenubutton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 15), arrowcolor=self._colours['fgcolor'], bordercolor=self._colours['bgcolor'])
        self._styleMB.map('filter.TMenubutton', background=[('active', self._colours['activecolor'])])

        #type chart images
        self._typeChartImage = ImageTk.PhotoImage(Image.open(os.path.join(self._scriptDir, 'assets', 'chart', 'pokemon-type-chart2.png')))

        #sprite cache to reduce loading times
        self._spriteCache = {}

        self._applyTheme(self._themeVar.get())

        #filter
        self._type1Var = tk.StringVar(value='Any')
        self._type2Var = tk.StringVar(value='Any')
        self._heightClassVar = tk.StringVar(value='Any')
        self._weightClassVar = tk.StringVar(value='Any')
        self._bstRangeVar = tk.StringVar(value='Any')

        #pokedex
        self._dexGenVar = tk.StringVar(value='Any')

        #team rater
        self._teamGenVar = tk.StringVar(value='Any')
        self._teamGameVar = tk.StringVar(value='Select Game')

        #games
        self._gamesByGen = {
            '1': ['Red/Blue', 'Yellow'],
            '2': ['Gold/Silver', 'Crystal'],
            '3': ['Ruby/Sapphire', 'Emerald', 'Fire Red/Leaf Green'],
            '4': ['Diamond/Pearl', 'Platinum', 'Heart Gold/Soul Silver'],
            '5': ['Black/White', 'Black 2/White 2'],
            '6': ['X/Y', 'Omega Ruby/Alpha Sapphire'],
            '7': ['Sun/Moon', 'Ultra Sun/Ultra Moon', "Let's Go Pikachu/Eevee"],
            '8': ['Sword/Shield', 'Brilliant Diamond/Shining Pearl', 'Legends: Arceus'],
            '9': ['Scarlet/Violet']
        }

        self._teamSlots = [None]*6

        #pokeAPI game version names
        self._gameVersions = {
            #gen 1
            'Red/Blue': ['red', 'blue'],
            'Yellow': ['yellow'],
            #gen2
            'Gold/Silver': ['gold', 'silver'],
            'Crystal': ['crystal'],
            #gen3
            'Ruby/Sapphire': ['ruby', 'sapphire'],
            'Emerald': ['emerald'],
            'FireRed/LeafGreen': ['firered', 'leafgreen'],
            #gen4
            'Diamond/Pearl': ['diamond', 'pearl'],
            'Platinum': ['platinum'],
            'HeartGold/SoulSilver': ['heartgold', 'soulsilver'],
            #gen5
            'Black/White': ['black', 'white'],
            'Black 2/White 2': ['black-2', 'white-2'],
            #gen6
            'X/Y': ['x', 'y'],
            'Omega Ruby/Alpha Sapphire': ['omega-ruby', 'alpha-sapphire'],
            #gen7
            'Sun/Moon': ['sun', 'moon'],
            'Ultra Sun/Ultra Moon': ['ultra-sun', 'ultra-moon'],
            "Let's Go Pikachu/Eevee": ['lets-go-pikachu', 'lets-go-eevee'],
            #gen8
            'Sword/Shield': ['sword', 'shield'],
            'Brilliant Diamond/Shining Pearl': ['brilliant-diamond', 'shining-pearl'],
            'Legends: Arceus': ['legends-arceus'],
            #gen9
            'Scarlet/Violet': ['scarlet', 'violet']
        }

    #retrieves sprite using given URL
    def getSprite(self, URL, label):
        response = requests.get(URL)
        monImage = Image.open(BytesIO(response.content))
        self._monSprite = ImageTk.PhotoImage(monImage)
        self._after(0, label.configure(image=self._monSprite))

    #loads a sprite from self._spriteCache
    def loadCachedSprite(self, spriteURL, size=(192, 192)):
        if not spriteURL:
            return None
        
        cacheKey = (spriteURL, size)
        if cacheKey in self._spriteCache:
            return self._spriteCache[cacheKey]
        
        try:
            response = requests.get(spriteURL, timeout=5)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image = image.resize(size, Image.NEAREST)
            sprite = ImageTk.PhotoImage(image)
            self._spriteCache[cacheKey] = sprite
            return sprite
        except:
            return None

    #make frame for main buttons in menu
    def makeButtonFrame(self):
        self._mainMenuButtonFrame = ttk.Frame(self)

        #frame grid
        self._mainMenuButtonFrame.rowconfigure(0, weight=1)
        self._mainMenuButtonFrame.rowconfigure(1, weight=1)
        self._mainMenuButtonFrame.rowconfigure(2, weight=1)
        self._mainMenuButtonFrame.columnconfigure(0, weight=1)

        #buttons
        self._buttonBall = ttk.Button(self._mainMenuButtonFrame, text='Pokédex', image=self._buttonMenuBallIcon, compound=tk.LEFT, command=self._showPokedexScreen, style='main.TButton')
        self._buttonBall.grid(row=0, sticky=tk.NSEW)

        self._buttonBook = ttk.Button(self._mainMenuButtonFrame, text='Encyclopedia', image=self._buttonMenuBookIcon, compound=tk.LEFT, command=self._showEncyclopediaScreen, style='main.TButton')
        self._buttonBook.grid(row=1, sticky=tk.NSEW)

        self._buttonArrow = ttk.Button(self._mainMenuButtonFrame, text='Team Rater', image=self._buttonMenuArrowIcon, compound=tk.LEFT, command=self._showTeamraterScreen, style='main.TButton')
        self._buttonArrow.grid(row=2, sticky=tk.NSEW)

        for widget in self._mainMenuButtonFrame.winfo_children():
            widget.grid(padx=15, pady=15)
        
        #packing button frame
        self._mainMenuButtonFrame.grid(column=0, row=1, sticky=tk.NSEW, padx=15, pady=15)

    #make right frame in menu
    def makeSideMenuFrame(self, container):
        self._sideMenuFrame = ttk.Frame(container)

        #frame grid
        self._sideMenuFrame.columnconfigure(0, weight=1)
        self._sideMenuFrame.rowconfigure(0, weight=10)
        self._sideMenuFrame.rowconfigure(1, weight=1)
        self._sideMenuFrame.rowconfigure(2, weight=1)

        self._buttonMenuChart = ttk.Button(self._sideMenuFrame, text='Type Chart', image=self._buttonMenuChartIcon, compound=tk.TOP, command=self._showTypeChartScreen, style='main.TButton')
        self._buttonMenuChart.grid(column=0, row=0, sticky=tk.NSEW, padx=15, pady=15)

        self._themeMenu = ttk.OptionMenu(self._sideMenuFrame, self._themeVar, self._themeVar.get(), *self._themes.keys(), command=lambda choice: self._applyTheme(choice), style='filter.TMenubutton')
        self._themeMenu.grid(column=0, row=1, sticky=tk.NSEW, padx=15, pady=15)

        self._buttonExit = ttk.Button(self._sideMenuFrame, text='Exit Program', image=self._buttonMenuExitIcon, compound=tk.LEFT, command=self._destroy, style='main.TButton')
        self._buttonExit.grid(row=2, column=0, sticky=tk.NSEW, padx=15, pady=15)

        #packing side menu frame
        self._sideMenuFrame.grid(column=1, row=1, sticky=tk.NSEW, padx=15, pady=15)

    #make menu grid
    def makeMenuGrid(self):
        self._rowconfigure(0, weight=2)
        self._rowconfigure(1, weight=12)
        self._columnconfigure(0, weight=10)
        self._columnconfigure(1, weight=5)

        self._titleOptions = {'column': 0, 'row': 0, 'columnspan': 2, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self._titleLabel = ttk.Label(self, text='The Universal Pokédex', anchor = 'center', style='TLabel')
        self._titleLabel.grid(**self._titleOptions)

    #make secondary screen for Pokédex, Encyclopedia, Team Rater, Type Chart
    def secondaryScreen(self):
        #make window grid
        self._rowconfigure(0, weight=1)
        self._rowconfigure(1, weight=20)
        self._columnconfigure(0, weight=1)
        self._columnconfigure(1, weight=20)

        #create frames
        self._mainFrame = ttk.Frame(self)
        self._mainFrame.grid(row=1, column=1, sticky=tk.NSEW, padx=15, pady=15)
        self._mainFrame.rowconfigure(0, weight=0, minsize=80)
        self._mainFrame.rowconfigure(1, weight=0, minsize=60)
        self._mainFrame.rowconfigure(2, weight=1)
        self._mainFrame.rowconfigure(3, weight=1)

        self._mainFrame.columnconfigure(0, weight=1, uniform='main')
        self._mainFrame.columnconfigure(1, weight=2, uniform='main')
        self._mainFrame.columnconfigure(2, weight=3, uniform='main')
        self._mainFrame.columnconfigure(3, weight=2, uniform='main')


        self._sideFrame = ttk.Frame(self)
        self._sideFrame.grid(row=0, column=0, rowspan=2, sticky=tk.NSEW, padx=15, pady=15)
        self._sideFrame.rowconfigure(0, weight=2)
        for i in range(1, 4):
            self._sideFrame.rowconfigure(i, weight=20)
        self._sideFrame.columnconfigure(0, weight=1)

    #make frame for choosing generation number of dex
    def dexSelectFrame(self):
        self._dexSelectFrameOuter = ttk.Frame(self._mainFrame, padding=15, style='TFrame')
        self._dexSelectFrameOuter.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW, padx=15)

        for column in range(4):
            self._dexSelectFrameOuter.columnconfigure(column, weight=1)

        title = ttk.Label(self._dexSelectFrameOuter, text='Select Pokédex Generation', anchor='center', style='small.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.EW, pady=(0, 15))

        self._dexGenMenu = ttk.Menubutton(self._dexSelectFrameOuter, text='Generation', style='filter.TMenubutton')
        self._dexGenMenu.grid(row=1, column=1, columnspan=2, sticky=tk.EW)

        genOptions = [('Any', 'Any')] + [(f'Gen {i}', str(i)) for i in range(1, 10)]
        self._makeFilterMenu(self._dexGenMenu, genOptions, self._dexGenVar)

        self._dexContinueButton = ttk.Button(self._dexSelectFrameOuter, text='Continue', style='enter.TButton', command=self._onDexGenContinue)
        self._dexContinueButton.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=(15, 0))

    #making frame for Pokédex, where Pokémon can be searched, filtered, selected, displayed, added and deleted
    def pokemonFrame(self, gen):
        self._genNum = int(gen)
        self._currentDexID = self._genNum

        self._makeDetailsFrame()

        #change title to match generation chosen
        self._makeTitle(f'Pokédex - Gen {self._genNum}')

        #checks that the desired dex exists first
        TUPdatabase.ensureDexExists(self._currentDexID, self._genNum, "Default")

        #add mon button
        self._addButton = ttk.Button(self._mainFrame, text='Add', style='enter.TButton', command=self._openAddMonPopup)
        self._addButton.grid(row=0, column=0, sticky=tk.EW, pady=(15, 10), padx=(0, 10))

        #delete button
        self._deleteButton = ttk.Button(self._mainFrame, text='Delete', style='enter.TButton', command=self._onDeleteSelectedMon)
        self._deleteButton.grid(row=0, column=1, sticky=tk.EW, pady=(15, 10), padx=(10, 10))
        self._deleteButton.state(["disabled"])

        #search entry
        self._searchEntry = ttk.Entry(self._mainFrame, font = ('Trebuchet MS', 20))
        self._searchEntry.grid(row=0, column=2, sticky=tk.EW, pady=(15, 10), padx=(0, 10))
        self._searchEntry.bind('<Return>', lambda e: self._refreshPokedexResults())

        #search button
        self._searchButton = ttk.Button(self._mainFrame, text='Enter', style='enter.TButton', command=self._refreshPokedexResults)
        self._searchButton.grid(row=0, column=3, sticky=tk.EW, pady=(15, 10), padx=(0, 0))

        #filter
        self._filtersFrame = ttk.Frame(self._mainFrame)
        self._filtersFrame.grid(row=1, column=2, columnspan=2, sticky=tk.EW, pady=(0, 10), padx=(0, 10))
        for column in range(5):
            self._filtersFrame.columnconfigure(column, weight=1)

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
        self._type1MenuButton = ttk.Menubutton(self._filtersFrame, text='Type 1', style='filter.TMenubutton')
        self._type1MenuButton.grid(row=0, column=0, sticky=tk.EW, padx=(0, 8))
        self._makeFilterMenu(self._type1MenuButton, typeOptions, self._type1Var)

        #type2 menubutton
        self._type2MenuButton = ttk.Menubutton(self._filtersFrame, text='Type 2', style='filter.TMenubutton')
        self._type2MenuButton.grid(row=0, column=1, sticky=tk.EW, padx=(0, 8))
        self._makeFilterMenu(self._type2MenuButton, typeOptions, self._type2Var)

        #height menubutton
        self._heightMenuButton = ttk.Menubutton(self._filtersFrame, text='Height', style='filter.TMenubutton')
        self._heightMenuButton.grid(row=0, column=2, sticky=tk.EW, padx=(0, 8))
        self._makeFilterMenu(self._heightMenuButton, heightOptions, self._heightClassVar)

        #weight menubutton
        self._weightMenuButton = ttk.Menubutton(self._filtersFrame, text='Weight', style='filter.TMenubutton')
        self._weightMenuButton.grid(row=0, column=3, sticky=tk.EW, padx=(0, 8))
        self._makeFilterMenu(self._weightMenuButton, weightOptions, self._weightClassVar)

        #bst menubutton
        self._bstMenuButton = ttk.Menubutton(self._filtersFrame, text='BST', style='filter.TMenubutton')
        self._bstMenuButton.grid(row=0, column=4, sticky=tk.EW, padx=(0, 8))
        self._makeFilterMenu(self._bstMenuButton, bstOptions, self._bstRangeVar)

        #scrollable area
        self._resultsOuterFrame, self._resultsCanvas, self._resultsInnerFrame = self._makeScrollableFrame(self._mainFrame)
        self._resultsOuterFrame.grid(row=2, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW, padx=15, pady=15)

        #refreshes shown Pokémon
        self._refreshPokedexResults()

    #making frame for encyclopedia
    def encyclopediaFrame(self):
        self._makeDetailsFrame(headerText='Select Entry', framePady=(0, 15), gridRow=0, rowSpan=4)
        self._makeTitle("Encyclopedia")

        #search entry
        self._encycSearchEntry = ttk.Entry(self._mainFrame, font=(self._FONT, 20))
        self._encycSearchEntry.grid(row=0, column=2, sticky=tk.EW, pady=(15, 10), padx=(0, 10))
        self._encycSearchEntry.bind('<Return>', lambda e: self._refreshEncyclopediaResults())

        #search button
        self._encycSearchButton = ttk.Button(self._mainFrame, text='Enter', style='enter.TButton', command=self._refreshEncyclopediaResults)
        self._encycSearchButton.grid(row=0, column=3, sticky=tk.EW, pady=(15, 10), padx=(0, 0))

        #filters frame
        self._encycFiltersFrame = ttk.Frame(self._mainFrame)
        self._encycFiltersFrame.grid(row=1, column=2, columnspan=2, sticky=tk.EW, pady=(0, 10), padx=(0, 10))

        for column in range(3):
            self._encycFiltersFrame.columnconfigure(column, weight=1)

        #string vars
        self._encycGenVar = tk.StringVar(value='Any')
        self._encycTypeVar = tk.StringVar(value='Any')
        self._encycItemTypeVar = tk.StringVar(value='Pokémon')

        #item type menu
        self._encycItemMenu = ttk.Menubutton(self._encycFiltersFrame, text='Item', style='filter.TMenubutton')
        self._encycItemMenu.grid(row=0, column=0, sticky=tk.EW, padx=(0, 8))
        
        itemOptions = [('Pokémon', 'Pokémon'), ('Move', 'Move'), ('Ability', 'Ability')]

        self._makeFilterMenu(self._encycItemMenu, itemOptions, self._encycItemTypeVar, self._refreshEncyclopediaResults)

        #generation menu
        self._encycGenMenu = ttk.Menubutton(self._encycFiltersFrame, text='Gen', style='filter.TMenubutton')
        self._encycGenMenu.grid(row=0, column=1, sticky=tk.EW, padx=(0, 8))
        
        genOptions = [('Any', 'Any')] + [(f'Gen {i}', str(i)) for i in range(1, 10)]

        self._makeFilterMenu(self._encycGenMenu, genOptions, self._encycGenVar, self._refreshEncyclopediaResults)

        #type menu
        self._encycTypeMenu = ttk.Menubutton(self._encycFiltersFrame, text='Type', style='filter.TMenubutton')
        self._encycTypeMenu.grid(row=0, column=2, sticky=tk.EW, padx=(0, 8))

        typeOptions = [('Any', 'Any'), ('Normal', 'Normal'), ('Fire', 'Fire'), ('Water', 'Water'),
                       ('Grass', 'Grass'), ('Electric', 'Electric'), ('Ice', 'Ice'), ('Fighting', 'Fighting'),
                       ('Poison', 'Poison'), ('Ground', 'Ground'), ('Flying', 'Flying'), ('Psychic', 'Psychic'),
                       ('Bug', 'Bug'), ('Rock', 'Rock'), ('Ghost', 'Ghost'), ('Dragon', 'Dragon'),
                       ('Dark', 'Dark'), ('Steel', 'Steel'), ('Fairy', 'Fairy')]
        
        self._makeFilterMenu(self._encycTypeMenu, typeOptions, self._encycTypeVar, self._refreshEncyclopediaResults)

        #scrollable results
        self._encycResultsOuterFrame, self._encycResultsCanvas, self._encycResultsInnerFrame = self._makeScrollableFrame(self._mainFrame)
        self._encycResultsOuterFrame.grid(row=2, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW, padx=15, pady=15)

        self._refreshEncyclopediaResults()
        
    #making screen for Type Chart section
    def typeChartScreen(self):
        self._secondaryScreen()

        for row in range(4):
            self._mainFrame.rowconfigure(row, weight=1, minsize=0)
        for column in range(4):
            self._mainFrame.columnconfigure(column, weight=1)

        for i in range(2, 5):
            self._rowconfigure(i, weight=0)

        #changing title
        self._makeTitle('Type Chart')

        #create side frame buttons
        self._buildSideNav('typechart')

        #type chart image
        self._chartLabel = ttk.Label(self._mainFrame, image=self._typeChartImage, anchor='center')
        self._chartLabel.grid(column=0, row=0, columnspan=4, rowspan=4, padx=15, pady=15, sticky=tk.NSEW)

        #return to main menu button
        self._menuButton = ttk.Button(self._sideFrame, text='Main Menu', image=self._buttonSideHouseIcon, compound=tk.LEFT, command=self._showMainMenu, style='main.TButton')
        self._menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    #making screen for Pokédex
    def pokedexScreen(self):
        self._secondaryScreen()

        #change title
        self._makeTitle('Pokédex')
        
        #create side frame buttons
        self._buildSideNav('pokedex')

        #return to main menu button
        self._menuButton = ttk.Button(self._sideFrame, text='Main Menu', image=self._buttonSideHouseIcon, compound=tk.LEFT, command=self._showMainMenu, style='main.TButton')
        self._menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        self._dexSelectFrame()

    #making screen for Encyclopedia
    def encyclopediaScreen(self):
        self._secondaryScreen()

        #change title
        self._makeTitle('Encyclopedia')

        #create side frame buttons
        self._buildSideNav('encyclopedia')

        #return to main menu button
        self._menuButton = ttk.Button(self._sideFrame, text='Main Menu', image=self._buttonSideHouseIcon, compound=tk.LEFT, command=self._showMainMenu, style='main.TButton')
        self._menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        #encyclopedia frame
        self._encyclopediaFrame()

    #making screen for Team Rater
    def teamraterScreen(self):
        self._secondaryScreen()

        #change title
        self._makeTitle('Team Rater')

        #create side frame buttons
        self._buildSideNav('teamrater')

        #return to main menu button
        self._menuButton = ttk.Button(self._sideFrame, text='Main Menu', image=self._buttonSideHouseIcon, compound=tk.LEFT, command=self._showMainMenu, style='main.TButton')
        self._menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        #select frame
        self._teamSelectFrame = ttk.Frame(self._mainFrame, padding=15, style='TFrame')
        self._teamSelectFrame.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW, padx=15)

        for column in range(4):
            self._teamSelectFrame.columnconfigure(column, weight=1)

        title = ttk.Label(self._teamSelectFrame, text='Select Game', anchor='center', style='small.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.EW, pady=(0, 15))

        #gen dropdown
        self._teamGenMenu = ttk.Menubutton(self._teamSelectFrame, text='Generation', style='filter.TMenubutton')
        self._teamGenMenu.grid(row=1, column=1, sticky=tk.EW, padx=(0, 8))

        genOptions = [('Any', 'Any')] + [(f'Gen {i}', str(i)) for i in range(1, 10)]
        self._makeFilterMenu(self._teamGenMenu, genOptions, self._teamGenVar, refreshCommand=self._refreshTeamGameMenu)

        #game dropdown
        self._teamGameMenu = ttk.Menubutton(self._teamSelectFrame, text='Game', style='filter.TMenubutton')
        self._teamGameMenu.grid(row=1, column=2, sticky=tk.EW, padx=(8, 0))

        #continue button
        self._teamContinueButton = ttk.Button(self._teamSelectFrame, text='Continue', style='enter.TButton', command=self._onTeamGameContinue)
        self._teamContinueButton.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=(15, 0))

        self._refreshTeamGameMenu()

    #making frame for scrollable canvas
    def makeScrollableFrame(self, parent):
        #frame for canvas and scrollbar
        scrollOuterFrame = ttk.Frame(parent)

        scrollOuterFrame.rowconfigure(0, weight=1)
        scrollOuterFrame.columnconfigure(0, weight=1)

        #canvas
        resultCanvas = tk.Canvas(scrollOuterFrame, highlightthickness=0, bg=self._colours['bgcolor'])
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

    #builds sidebar to navigate through secondary screens
    def buildSideNav(self, currentScreen):
        #clears existing widgets in sideFrame
        for widget in self._sideFrame.winfo_children():
            widget.destroy()
        
        #main menu button
        self._menuButton = ttk.Button(self._sideFrame, text='Main Menu', image=self._buttonSideHouseIcon, compound=tk.LEFT, command=self._showMainMenu, style='main.TButton')
        self._menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        buttonNav = [ #key, label, imageAttr, command
            ('pokedex', 'Pokédex', self._buttonSideBallIcon, self._showPokedexScreen),
            ('encyclopedia', 'Encyclopedia', self._buttonSideBookIcon, self._showEncyclopediaScreen),
            ('teamrater', 'Team Rater', self._buttonSideArrowIcon, self._showTeamraterScreen),
            ('typechart', 'Type Chart', self._buttonSideChartIcon, self._showTypeChartScreen)
        ]

        row = 1
        for key, label, icon, cmd in buttonNav:
            if key == currentScreen:
                continue
            
            #side button
            button = ttk.Button(self._sideFrame, text=label, image=icon, compound=tk.TOP, command=cmd, style='main.TButton')
            button.grid(row=row, sticky=tk.NSEW, padx=10, pady=10)

            #store references for updating icons
            if key == 'pokedex':
                self._buttonDex = button
            if key == 'encyclopedia':
                self._buttonEncyc = button
            if key == 'teamrater':
                self._buttonTeam = button
            if key == 'typechart':
                self._buttonSideChart = button

            row += 1
        

    #populates grid with Pokémon that match the search/filter criteria  
    def populateResultsGrid(self, rows):
        if not hasattr(self, 'resultsInnerFrame'):
            return
        
        for widget in self._resultsInnerFrame.winfo_children():
            widget.destroy()

        self._resultSpriteRefs = {}

        #grid settings
        self._columns = 3
        self._cardPadX = 10
        self._cardPadY = 10

        for column in range(self._columns):
            self._resultsInnerFrame.columnconfigure(column, weight=1, uniform='resultsCols')

        #for each Pokémon that matches criteria
        for index, (dexMonID, monName, spriteURL) in enumerate(rows):
            self._cardRow = index//self._columns
            self._cardColumn = index%self._columns

            #card frame
            self._card = ttk.Frame(self._resultsInnerFrame, padding=8, style='TFrame')
            self._card.grid(row=self._cardRow, column=self._cardColumn, sticky=tk.NSEW, padx=self._cardPadX, pady=self._cardPadY)

            #sprite label
            spriteLabel = ttk.Label(self._card, text='')
            spriteLabel.grid(row=0, column=0, sticky=tk.N, pady=(0, 6))

            #name label
            nameLabel = ttk.Label(self._card, text=monName.title(), anchor='center', style='progress.TLabel', wraplength=160)
            nameLabel.grid(row=1, column=0, sticky=tk.EW)

            #clickable card
            def onClick(event, dID=dexMonID):
                self._onSelectMon(dID)

            self._card.bind("<Button-1>", onClick)
            spriteLabel.bind("<Button-1>", onClick)
            nameLabel.bind("<Button-1>", onClick)

            #if url exists, load sprite async
            if spriteURL:
                threading.Thread(target=self._loadSpriteToLabel, args=(spriteURL, spriteLabel, dexMonID), daemon=True).start()

    #populates grid with results that match the criteria  
    def populateEncyclopediaGrid(self, rows):
        if not hasattr(self, 'encycResultsInnerFrame'):
            return

        for widget in self._encycResultsInnerFrame.winfo_children():
            widget.destroy()

        self._encycSpriteRefs = {}

        #grid settings
        self._columns = 3
        self._cardPadX = 10
        self._cardPadY = 10

        for column in range(self._columns):
            self._encycResultsInnerFrame.columnconfigure(column, weight=1, uniform='encycCols')

        itemType = self._encycItemTypeVar.get()

        #for each Pokémon that matches criteria
        for index, (itemKey, displayName, spriteURL) in enumerate(rows):
            self._cardRow = index//self._columns
            self._cardColumn = index%self._columns

            #card frame
            self._card = ttk.Frame(self._encycResultsInnerFrame, padding=8, style='TFrame')
            self._card.grid(row=self._cardRow, column=self._cardColumn, sticky=tk.NSEW, padx=self._cardPadX, pady=self._cardPadY)

            #sprite label
            spriteLabel = ttk.Label(self._card, text='')
            spriteLabel.grid(row=0, column=0, sticky=tk.N, pady=(0, 6))

            #name label
            nameLabel = ttk.Label(self._card, text=displayName, anchor='center', style='progress.TLabel', wraplength=160)
            nameLabel.grid(row=1, column=0, sticky=tk.EW)

            #clickable card
            def onClick(event, k=itemKey):
                self._onSelectEncyclopediaItem(k)

            self._card.bind("<Button-1>", onClick)
            spriteLabel.bind("<Button-1>", onClick)
            nameLabel.bind("<Button-1>", onClick)

            #load sprites for pokemon only
            if itemType =='Pokémon' and spriteURL:
            #if url exists, load sprite async
                if spriteURL:
                    threading.Thread(target=self._loadSpriteToLabel, args=(spriteURL, spriteLabel, itemKey), daemon=True).start()

    #refreshes displayed Pokémon when user changes criteria
    def refreshPokedexResults(self):
        if not hasattr(self, 'resultsInnerFrame') or not self._resultsInnerFrame.winfo_exists():
            return
        if not hasattr(self, 'searchEntry') or not self._searchEntry.winfo_exists():
            return

        #form criteria dictionary from inputs
        criteria = self._makePokedexCriteria()

        #for building buttons/cards
        rows = TUPdatabase.searchDexMonsForButtons(self._currentUserID, self._currentDexID, criteria)

        #update scrollable grid
        self._populateResultsGrid(rows)

        if rows:
            rowIDs = [row[0] for row in rows]
            current = getattr(self, 'selectedDexMonID', None)

            if current in rowIDs:
                self._showMonDetails(current)
            else:
                self._selectedDexMonID = rows[0][0]
                self._showMonDetails(self._selectedDexMonID)
        
        else:
            self._selectedDexMonID = None
            self._detailsNameLabel.configure(text='No results')
            self._setText('detailsInfoText', '')
            self._hideDetailsSprite()

            if hasattr(self, "deleteButton"):
                self._deleteButton.state(["disabled"])

    #refreshes displayed results when user changes criteria
    def refreshEncyclopediaResults(self):
        if not hasattr(self, 'encycResultsInnerFrame') or not self._encycResultsInnerFrame.winfo_exists():
            return
        if not hasattr(self, 'encycSearchEntry') or not self._encycSearchEntry.winfo_exists():
            return
        
        #types do not apply to abilities
        if self._encycItemTypeVar.get() == 'Ability' and self._encycTypeVar.get() != 'Any':
            self._encycTypeVar.set('Any')

        criteria = {'itemType': self._encycItemTypeVar.get(),
                    'gen': self._encycGenVar.get(),
                    'type': self._encycTypeVar.get(),
                    'query': self._encycSearchEntry.get()}

        #for building buttons/cards
        rows = TUPitems.searchEncyclopedia(criteria, limit=200)

        #update scrollable grid
        self._populateEncyclopediaGrid(rows)

        if rows:
            firstKey = rows[0][0]
            self._onSelectEncyclopediaItem(firstKey)

        else:
            self._selectedEncycKey = None
            self._detailsNameLabel.configure(text='No results')
            self._setText('detailsInfoText', 'No results match your search.')
            self._hideDetailsSprite()
    
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
                if hasattr(self, 'resultSpriteRefs'):
                    self._resultSpriteRefs[monID] = tkImage
                if hasattr(self, 'encycSpriteRefs'):
                    self._encycSpriteRefs[monID] = tkImage
            
            self._after(0, apply)
        except:
            pass

    #shows details of a specific Pokémon in the database
    def showMonDetails(self, dexMonID):
        mon = TUPdatabase.returnDexMonForUser(self._currentUserID, dexMonID)
        
        if not mon:
            self._detailsNameLabel.configure(text='No details for this Pokémon')
            self._setText('detailsInfoText', 'No details for this Pokémon')
            self._hideDetailsSprite()
            return

        #update labels
        self._detailsNameLabel.configure(text=mon["MonName"].title())

        #stats, base or custom
        statsLine = f"HP {mon['UHP']} / Atk {mon['UAtk']} / Def {mon['UDef']} / SpA {mon['USpA']} / SpD {mon['USpD']} / Spe {mon['USpe']}"
        bst = sum(int(mon[i]) for i in ["UHP", "UAtk", "UDef", "USpA", "USpD", "USpe"] if mon.get(i) is not None)
                  
        typeLine = self._formatAPIText(mon["Type1"])
        if mon["Type2"]:
            typeLine += " / " + self._formatAPIText(mon["Type2"])

        if mon.get("PreEvo"):
            preEvo = self._formatAPIText(mon["PreEvo"])
        else:
            preEvo = "None"

        evoBlock = self._formatEvo(mon.get("Evo"))
        eggGroupsBlock = self._formatPipeBlock("Egg Groups", mon.get("EggGroups"))
        locationsBlock = self._formatPipeBlock("Locations", mon.get("Location"), maxItems=10)

        movesRaw = mon.get("Moves") or ""
        movesBlock = self._formatPipeBlock("Moves", movesRaw)

        abilitiesRaw = mon.get('Ability') or ''
        abilitiesBlock = self._formatPipeBlock('Abilities', abilitiesRaw, maxItems=6)

        flavorText = (mon.get("FlavorText") or "").strip()

        infoText = (f'National Dex Number: {mon.get("DexNum")}\n'
                    f'Species: {self._formatAPIText(mon.get("Species"))}\n'
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
        
        self._detailsInfoText.configure(state='normal')
        self._detailsInfoText.delete('1.0', 'end')
        self._detailsInfoText.insert('1.0', infoText)
        self._detailsInfoText.configure(state='disabled')

        #update sprite
        sprite = self._loadCachedSprite(mon.get('SpriteURL'), size=(256, 256))
        self._showDetailsSprite(sprite)

    #shows details of selected item
    def showEncyclopediaDetails(self, itemKey):
        sprite = None
        itemType = self._encycItemTypeVar.get()
        chosenGen = self._encycGenVar.get()
        if chosenGen != 'Any':
            chosenGenNum = int(chosenGen)
        else:
            chosenGenNum = 9

        self._hideDetailsSprite()

        try:
            if itemType == 'Pokémon':
                monObj = TUPitems.Mon('mon', int(itemKey), chosenGenNum)

                #update sprite
                sprite = self._loadCachedSprite(monObj.getSpriteURL(), size=(256, 256))

                #update labels
                self._detailsNameLabel.configure(text=monObj.getItemName().title())

                #stats, base or custom
                statsLine = f"HP {monObj.getHP()} / Atk {monObj.getAtk()} / Def {monObj.getDef()} / SpA {monObj.getSpA()} / SpD {monObj.getSpD()} / Spe {monObj.getSpe()}"
                bst = monObj.getBST()
                        
                typeLine = self._formatAPIText(monObj.getType1())
                type2 = monObj.getType2()
                if type2 not in (-1, None, '', 'none'):
                    typeLine += " / " + self._formatAPIText(type2)

                if monObj.getPreEvo():
                    preEvo = self._formatAPIText(monObj.getPreEvo())
                else:
                    preEvo = "None"

                evoBlock = self._formatEvo(monObj.getEvoList())
                eggGroupsBlock = self._formatPipeBlock("Egg Groups", monObj.getEggGroups())
                locationsBlock = self._formatPipeBlock("Locations", monObj.getLocations(), maxItems=10)

                movesRaw = monObj.getMoves() or ""
                movesBlock = self._formatPipeBlock("Moves", movesRaw)

                abilitiesRaw = monObj.getAbilities() or ''
                abilitiesBlock = self._formatPipeBlock('Abilities', abilitiesRaw, maxItems=6)

                flavorText = (monObj.getFlavorText() or "").strip()

                infoText = (f'National Dex Number: {monObj.getDexNum()}\n'
                            f'Species: {self._formatAPIText(monObj.getSpecies())}\n'
                            f'Type: {typeLine}\n'
                            f'Height: {monObj.getHeight()} m\n'
                            f'Weight: {monObj.getWeight()} kg\n'
                            f'Egg Cycle: {monObj.getEggCycle()}\n'
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
                self._detailsNameLabel.configure(text=moveObj.getItemName().replace('-', ' ').title())

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
                self._detailsNameLabel.configure(text=abilObj.getItemName().replace('-', ' ').title())

                infoText = (f"Flavor Text: {abilObj.getFlavorText() or 'None'}\n")
            
            self._setText('detailsInfoText', infoText)
            self._showDetailsSprite(sprite)
        
        except:
            self._detailsNameLabel.configure(text='Error')
            self._setText('detailsInfoText', 'Could not load details from PokéAPI.')
            self._hideDetailsSprite()

    #formats text from pokeAPI
    def formatAPIText(self, text):
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
        items = [self._formatAPIText(name) for name in self._splitPipeList(text)]

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
        
        evoObj = evoText
        
        #if string, parse into lists
        if isinstance(evoText, str):
            try:
                evoObj = ast.literal_eval(evoText)
            except:
                return f"Evolution: {self._formatAPIText(evoText)}"
            
        #shows even if not list after parsing
        if not isinstance(evoObj, list) or len(evoObj) == 0:
            return f"Evolution: None"
        
        if isinstance(evoObj[0], list):
            baseList = evoObj[0]
        else:
            baseList = [evoObj[0]]

        output = "Evolution: \n" 
        output += " → ".join(self._formatAPIText(name) for name in baseList)
        
        #adds branches
        if len(evoObj) > 1:
            output += "\nBranches: \n"
            for branch in evoObj[1:]:
                if isinstance(branch, list) and branch:
                    output += " " + " → ".join(self._formatAPIText(name) for name in branch) + "\n"
        
        return output.strip() 

    #when a Pokémon is selected
    def onSelectMon(self, dexMonID):
        self._selectedDexMonID = dexMonID

        if hasattr(self, "deleteButton"):
            self._deleteButton.state(["!disabled"])

        self._showMonDetails(dexMonID)

    def onSelectEncyclopediaItem(self, itemID):
        self._selectedEncycKey = itemID
        self._showEncyclopediaDetails(itemID)

    #make menu for filtering
    def makeFilterMenu(self, menuButton, options, variable, refreshCommand=None):
        menu = tk.Menu(menuButton, tearoff=0)

        if refreshCommand is None:
            refreshCommand = lambda: None

        for label, value in options:
            menu.add_radiobutton(label=label, value=value, variable=variable, command=refreshCommand)
        
        menuButton['menu'] = menu
    
    #make frame for showing selected Pokémon information
    def makeDetailsFrame(self, headerText='Select Pokémon', framePady=15, gridRow=1, rowSpan=3):
        self._detailsFrame = ttk.Frame(self._mainFrame, padding=(20, 20), style='TFrame')
        #self._detailsFrame.grid_propagate(False)
        self._detailsFrame.grid(row=gridRow, column=0, columnspan=2, rowspan=rowSpan, sticky=tk.NSEW, padx=(15, 10), pady=framePady)

        self._detailsFrame.rowconfigure(0, weight=0) #name
        self._detailsFrame.rowconfigure(1, weight=0) #sprite
        self._detailsFrame.rowconfigure(2, weight=1) #info
        self._detailsFrame.rowconfigure(3, weight=0)
        self._detailsFrame.columnconfigure(0, weight=1)

        #name label
        self._detailsNameLabel = ttk.Label(self._detailsFrame, text=headerText, anchor='center', style='small.TLabel')
        self._detailsNameLabel.grid(row=0, column=0, sticky=tk.EW, pady=(0, 10))

        #sprite label
        self._detailsSpriteLabel = ttk.Label(self._detailsFrame, text='', anchor='center')
        self._detailsSpriteLabel.grid(row=1, column=0, pady=(0, 10))
        self._detailsSpriteLabel.grid_remove()

        #scrollable info label
        self._detailsInfoOuterFrame = ttk.Frame(self._detailsFrame, style='TFrame')
        self._detailsInfoOuterFrame.grid(row=2, column=0, sticky=tk.NSEW)

        self._detailsInfoOuterFrame.rowconfigure(0, weight=1)
        self._detailsInfoOuterFrame.columnconfigure(0, weight=1)

        self._detailsInfoScrollbar = ttk.Scrollbar(self._detailsInfoOuterFrame, orient='vertical')
        self._detailsInfoScrollbar.grid(row=0, column=1, sticky=tk.NS)

        self._detailsInfoText = tk.Text(self._detailsInfoOuterFrame, wrap='word', yscrollcommand=self._detailsInfoScrollbar.set, bg=self._colours['bgcolor'], fg=self._colours['fgcolor'], font=(self._FONT, 12), relief='flat', highlightthickness=0, padx=8, pady=8)
        self._detailsInfoText.grid(row=0, column=0, sticky=tk.NSEW)

        self._detailsInfoScrollbar.configure(command=self._detailsInfoText.yview)

        self._detailsInfoText.configure(state='disabled')

        def scrollWheel(event):
            self._detailsInfoText.yview_scroll(int(-1*(event.delta/120)), 'units')

        self._detailsInfoText.bind('<Enter>', lambda e: self._detailsInfoText.bind_all('<MouseWheel>', scrollWheel))
        self._detailsInfoText.bind('<Leave>', lambda e: self._detailsInfoText.unbind_all('<MouseWheel>'))

        #sprite reference
        self._detailsSpriteRef = None
        
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
        popup.iconbitmap(self._iconPath)

        #add Pokémon frame
        self._addMonFrame = ttk.Frame(popup, padding=15)
        self._addMonFrame.grid(row=0, column=0, sticky=tk.NSEW)

        #dex number label
        self._dexNumLabel = ttk.Label(self._addMonFrame, text='Dex # or Name:', style='progress.TLabel')
        self._dexNumLabel.grid(row=0, column=0, sticky=tk.W)

        #dex number entry
        self._dexNumEntry = ttk.Entry(self._addMonFrame, width=12)
        self._dexNumEntry.grid(row=0, column=1, padx=(10, 0), sticky=tk.EW)
        self._dexNumEntry.focus_set()

        #custom stats label
        self._customStatsLabel = ttk.Label(self._addMonFrame, text='Custom Stats (Optional):', style='progress.TLabel')
        self._customStatsLabel.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(12, 6))

        for i, stat in enumerate(statNames):
            ttk.Label(self._addMonFrame, text=f"{stat}", style='progress.TLabel').grid(row=2+i, column=0, sticky=tk.W)
            var = tk.StringVar(value="")
            statVars[stat] = var
            ttk.Entry(self._addMonFrame, textvariable=var, width=12).grid(row=2+i, column=1, padx=(10, 0), sticky=tk.W)

        #parses integer
        def parseInt(text):
            text=text.strip()
            if text == '':
                return None
            else:
                return int(text)
        
        #when user presses add button
        def onAdd():
            userIn = self._dexNumEntry.get()
            monKey = self._normaliseMonInput(userIn)

            if not monKey:
                showinfo("Error", "Please enter a Dex number or Pokédex name.")
                return

            #Pokémon object
            try:
                monObj = TUPitems.Mon('mon', monKey, self._genNum)
            except:
                showinfo("Error", "Could not load that Pokémon from the API.")
                return
            
            try:
                monFromGen = int(monObj.getItemFromGen())
            except:
                monFromGen = None

            if monFromGen is not None and monFromGen > self._genNum:
                showinfo("Wrong Generation", f"{monObj.getItemName().title()} is from Gen {monFromGen}, so it can't be added to a Gen {self._genNum} Dex.")
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
                TUPdatabase.addMonFull(self._currentUserID, self._currentDexID, self._genNum, monData, moves=monObj.getMoves(), ability=monObj.getAbilities(), stats=stats)

            except:
                #error message
                showinfo("Error", "Could not add Pokémon.")
                return
            
            popup.destroy()
            self._refreshPokedexResults()
        
        #on add button
        self._onAddButton = ttk.Button(popup, text='Add', style='small.TButton', command=onAdd)
        self._onAddButton.grid(row=1, column=0, columnspan=2, padx=10, pady=15, sticky=tk.EW)

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
        self._selectedDexMonID = None
        self._refreshPokedexResults()

    #updates available games to select from after user chooses gen 
    def refreshTeamGameMenu(self):
        chosenGen = self._teamGenVar.get()
        menu = tk.Menu(self._teamGameMenu, tearoff=0)

        if chosenGen == 'Any':
            self._teamGameVar.set('Select Game')
            menu.add_command(label='Select a generation first', command=lambda: None)
        else:
            games = self._gamesByGen.get(chosenGen, [])
            if not games:
                self._teamGameVar.set('Select Game')
                menu.add_command(label='No games available', command=lambda: None)
            else:
                #default to first game if current not in list
                current = self._teamGameVar.get()
                if current not in games:
                    self._teamGameVar.set(games[0])

                for game in games:
                    menu.add_radiobutton(label=game, value=game, variable=self._teamGameVar)
        
        self._teamGameMenu['menu'] = menu

    #when user clicks continue button in team rater
    def onTeamGameContinue(self):
        gen = self._teamGenVar.get()
        game = self._teamGameVar.get()

        if gen == 'Any':
            showinfo('Team Rater', 'Please select a generation.')
            return
        
        if not game or game == 'Select Game':
            showinfo('Team Rater', 'Please select a game.')
            return

        self._selectedTeamGen = int(gen)
        self._selectedTeamGame = game
        self._showTeamInput()

    #when user clicks continue button in pokedex
    def onDexGenContinue(self):
        gen = self._dexGenVar.get()

        if gen == 'Any':
            showinfo('Pokédex', 'Please select a generation.')
            return
        
        if hasattr(self, 'dexSelectFrameOuter') and self._dexSelectFrameOuter.winfo_exists():
            self._dexSelectFrameOuter.destroy()

        self._pokemonFrame(gen)

    #make filter criteria
    def makePokedexCriteria(self):
        name = ''

        try:
            if hasattr(self, 'searchEntry') and self._searchEntry.winfo_exists():
                name = self._searchEntry.get().strip()
        except tk.TclError:
            return {'name': None, 'type1': None, 'type2': None, 'heightMin': None, 'heightMax': None, 'weightMin': None, 'weightMax': None, 'bstMin': None, 'bstMax': None}
        
        
        #maps to numeric ranges
        heightMap = {'Any': (None, None), 'Small': (0.0, 1.0), 'Medium': (1.0, 2.0), 'Large': (2.0, 100.0),}
        weightMap = {'Any': (None, None), 'Light': (0.0, 25.0), 'Medium': (25.0, 100.0), 'Heavy': (100.0, 10000.0),}
        bstMap = {'Any': (None, None), 'Low': (0, 300), 'Medium': (300, 500), 'High': (500, 9999),}

        heightMin, heightMax = heightMap.get(self._heightClassVar.get(), (None, None))
        weightMin, weightMax = weightMap.get(self._weightClassVar.get(), (None, None))
        bstMin, bstMax = bstMap.get(self._bstRangeVar.get(), (None, None))

        type1 = self._type1Var.get().strip()
        type2 = self._type2Var.get().strip()

        if type1 in ("", "Any"):
            type1 = None
        if type2 in ("", "Any"):
            type2 = None

        criteria = {'name': name if name else None, 'type1': type1, 'type2': type2, 'heightMin': heightMin, 'heightMax': heightMax, 'weightMin': weightMin, 'weightMax': weightMax, 'bstMin': bstMin, 'bstMax': bstMax,}

        return criteria
    
    #shows team select screen
    def showTeamInput(self):
        for widget in self._mainFrame.winfo_children():
            widget.destroy()

        self._makeTitle(f'Team Rater - Gen {self._selectedTeamGen} ({self._selectedTeamGame})')
    
        #details frame
        self._makeDetailsFrame(headerText='Select a Team Slot', framePady=(0, 15), gridRow=1, rowSpan=3)

        #entry button
        self._teamSearchEntry = ttk.Entry(self._mainFrame, font=(self._FONT, 20))
        self._teamSearchEntry.grid(row=0, column=2, sticky=tk.EW, pady=(15, 10), padx=(0 ,10))
        self._teamSearchEntry.bind('<Return>', lambda e: self._onAddTeamMon())

        #add button
        self._teamAddButton = ttk.Button(self._mainFrame, text='Add to Team', style='enter.TButton', command=self._onAddTeamMon)
        self._teamAddButton.grid(row=0, column=3, sticky=tk.EW, pady=(15, 10), padx=(0, 0))

        #team slots frame
        self._teamSlotsFrame = ttk.Frame(self._mainFrame, padding=10, style='TFrame')
        self._teamSlotsFrame.grid(row=1, column=2, columnspan=2, rowspan=3, sticky=tk.NSEW, pady=(0, 15), padx=15)

        for column in range(2):
            self._teamSlotsFrame.columnconfigure(column, weight=1, uniform='teamSlots', minsize=190)
        for row in range(3):
            self._teamSlotsFrame.rowconfigure(row, weight=1, uniform='teamSlotsRows', minsize=170)

        self._showTeamSlots()

        #continue button
        self._teamContinueButton = ttk.Button(self._mainFrame, text='Analyse Team', style='enter.TButton', command=self._onTeamAnalyse)
        self._teamContinueButton.grid(row=0, column=0, sticky=tk.EW, pady=(15, 10), padx=(0, 10))

        #recommend button
        self._teamRecommendButton = ttk.Button(self._mainFrame, text='Recommend', style='enter.TButton', command=self._onTeamRecommend)
        self._teamRecommendButton.grid(row=0, column=1, sticky=tk.EW, pady=(15, 10), padx=(10, 10))

    #shows 6 slots in team
    def showTeamSlots(self):
        for widget in self._teamSlotsFrame.winfo_children():
            widget.destroy()

        self._teamSpriteRefs = {}

        for i in range(6):
            r = i//2
            c= i%2

            card = ttk.Frame(self._teamSlotsFrame, padding=10, style='TFrame')
            card.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
            card.columnconfigure(0, weight=1)

            slotData = self._teamSlots[i]

            #sprite
            spriteLabel = ttk.Label(card, text='', anchor='center', width=12)
            spriteLabel.grid(row=0, column=0, sticky=tk.EW, pady=(0, 6))

            #name
            if slotData:
                nameText = slotData['name']
            else:
                nameText = f'Slot {i+1} (Empty)'

            nameLabel = ttk.Label(card, text=nameText, anchor='center', style='progress.TLabel', wraplength=160)
            nameLabel.grid(row=1, column=0, sticky=tk.EW)

            #remove button
            removeButton = ttk.Button(card, text='Remove', style='small.TButton', command=lambda j=i: self._removeTeamSlot(j))
            removeButton.grid(row=2, column=0, sticky=tk.EW, pady=(4, 0))

            if not slotData:
                spriteLabel.configure(image='', text='')
                removeButton.state(['disabled'])
            else:
                sprite = self._loadCachedSprite(slotData['spriteURL'], size=(96, 96))
                if sprite:
                    spriteLabel.configure(image=sprite)
                    self._teamSpriteRefs[i] = sprite
                removeButton.state(['!disabled'])
            
            def onClick(event, j=i):
                self._onSelectTeamSlot(j)

            card.bind('<Button-1>', onClick)
            spriteLabel.bind('<Button-1>', onClick)
            nameLabel.bind('<Button-1>', onClick)

    #converts user input into a consistent format
    def normaliseMonInput(self, text):
        text = (text or '').strip()

        if not text:
            return None
        if text.isdigit():
            return int(text)
        
        return text.lower().replace(' ', '-')
    
    #picks next slot to add to
    def findNextEmptySlot(self):
        for i in range(6):
            if self._teamSlots[i] is None:
                return i
        
        return None
    
    #validates whether pokemon exists in the chosen game
    def monExistsInGame(self, monKey):
        try:
            teamMon = TUPitems.Mon('mon', monKey, self._selectedTeamGen)
            monFromGen = int(teamMon.getItemFromGen())
            return monFromGen <= int(self._selectedTeamGen)
            
        except:
            return False
    
    #when the user clicks add button
    def onAddTeamMon(self):
        userIn = self._teamSearchEntry.get()
        monKey = self._normaliseMonInput(userIn)

        if monKey is None:
            showinfo('Team Rater', 'Enter a Pokémon name or Dex number.')   
            return
        
        slotIndex = self._findNextEmptySlot()
        if slotIndex is None:
            showinfo('Team Rater', 'Your team already has 6 Pokémon. Please remove one first.')
            return
        
        if not self._monExistsInGame(monKey):
            showinfo('Team Rater', f"That Pokémon isn't valid for {self._selectedTeamGame}.")
            return
        
        try:
            monObj = TUPitems.Mon('mon', monKey, self._selectedTeamGen)
        
        except:
            showinfo('Team Rater', 'Could not load that Pokémon from the API.')
            return
    
        dexNum = int(monObj.getDexNum())
        name = self._formatAPIText(monObj.getItemName())
        spriteURL = monObj.getSpriteURL()

        self._teamSlots[slotIndex] = {'dexNum': dexNum, 'name': name, 'type1': monObj.getType1(), 'type2': monObj.getType2(), 
                                     'bst': monObj.getBST(), 'spriteURL': spriteURL, 'moves': [None, None, None, None]}

        self._teamSearchEntry.delete(0, 'end')
        self._showTeamSlots()
        self._onSelectTeamSlot(slotIndex)

    #removes a pokemon from the team
    def removeTeamSlot(self, i):
        self._teamSlots[i] = None
        self._showTeamSlots()
        self._detailsNameLabel.configure(text='Select a Team Slot')
        self._detailsInfoText.config(state='normal')
        self._detailsInfoText.delete('1.0', 'end')
        self._detailsInfoText.configure(state='disabled')
        self._detailsSpriteLabel.grid_remove()
        self._detailsSpriteRef = None

    #when the user clicks a team slot
    def onSelectTeamSlot(self, i):
        slotData = self._teamSlots[i]
        if not slotData:
            self._detailsNameLabel.configure(text=f'Slot {i+1} (Empty)')
            self._detailsInfoText.configure(state='normal')
            self._detailsInfoText.delete('1.0', 'end')
            self._detailsInfoText.insert('1.0', 'Add a Pokémon to this slot.')
            self._detailsInfoText.configure(state='disabled')
            self._detailsSpriteLabel.grid_remove()
            self._detailsSpriteRef = None
            return
        
        if 'moves' not in slotData:
            slotData['moves'] = [None, None, None, None]

        #clears previous move UI
        if hasattr(self, 'teamMovesFrame') and self._teamMovesFrame.winfo_exists():
            self._teamMovesFrame.destroy()

        self._teamMovesFrame = ttk.Frame(self._detailsFrame, style='TFrame')
        self._teamMovesFrame.grid(row=3, column=0, sticky=tk.EW, pady=(10, 0))

        for column in range(4):
            self._teamMovesFrame.columnconfigure(column, weight=1)

        try:
            validMoves = self._getValidMoves(slotData['dexNum'], self._selectedTeamGen)
        except:
            validMoves = []

        moveOptions = ['None'] + [self._formatAPIText(move) for move in validMoves]

        while len(slotData['moves']) < 4:
            slotData['moves'].append(None)

        self._teamMoveVars = []
        for moveIndex in range(4):
            currentMove = slotData['moves'][moveIndex]
            if not currentMove:
                current = 'None'
            else:
                current = self._formatAPIText(currentMove)

            moveVar = tk.StringVar(value=current)
            self._teamMoveVars.append(moveVar)

            self._moveMenubutton = ttk.Menubutton(self._teamMovesFrame, text=f'Move {moveIndex+1}', style='filter.TMenubutton')
            self._moveMenubutton.grid(row=0, column=moveIndex, sticky=tk.EW, padx=4)

            self._moveMenu = tk.Menu(self._moveMenubutton, tearoff=0)

            varList = self._teamMoveVars

            #creates command for move slot to save selected move into right slot
            def moveCommand(i, valueLabel):
                def command():
                    #saves into slotData as None
                    if valueLabel == 'None':
                        slotData['moves'][i] = None
                        varList[i].set('None')
                    #otherwise saves into slotData in API format
                    else:
                        APIName = valueLabel.lower().replace(' ', '-')
                        slotData['moves'][i] = APIName
                        varList[i].set(valueLabel)
                return command
        
            for option in moveOptions:
                self._moveMenu.add_command(label=option, command=moveCommand(moveIndex, option))

            self._moveMenubutton['menu'] = self._moveMenu
            self._moveMenubutton.configure(textvariable=moveVar)
        
        self._detailsNameLabel.configure(text=slotData['name'])

        typeLine = self._formatAPIText(slotData['type1'])
        if slotData['type2'] not in (-1, None, '', 'none'):
            typeLine += ' / ' + self._formatAPIText(slotData['type2'])

        infoText = (
            f"Dex Number: {slotData['dexNum']}\n"
            f"Type: {typeLine}\n"
            f"BST: {slotData['bst']}\n"
            f"Game: {self._selectedTeamGame}\n"
            f"Generation: {self._selectedTeamGen}\n"
        )

        self._detailsInfoText.configure(state='normal')
        self._detailsInfoText.delete('1.0', 'end')
        self._detailsInfoText.insert('1.0', infoText)
        self._detailsInfoText.configure(state='disabled')

        sprite = self._loadCachedSprite(slotData['spriteURL'], size=(256, 256))

        if sprite:
            self._detailsSpriteLabel.grid()
            self._detailsSpriteLabel.configure(image=sprite)
            self._detailsSpriteRef = sprite
        else:
            self._detailsSpriteLabel.grid_remove()
            self._detailsSpriteRef = None
    
    #gets type of move from cache to reduce number of times fetching from pokeAPI
    def getMoveTypeCached(self, moveName):
        if not moveName:
            return None
        
        moveKey = str(moveName).strip().lower().replace(' ', '-')

        if not hasattr(self, 'moveTypeCache'):
            self._moveTypeCache = {}

        if moveKey in self._moveTypeCache:
            return self._moveTypeCache[moveKey]
        
        try:
            moveObj = pb.move(moveKey)
            moveType = getattr(getattr(moveObj, 'type', None), 'name', None)
            self._moveTypeCache[moveKey] = moveType
            return moveType
        
        except:
            self._moveTypeCache[moveKey] = None
            return None

    #when user clicks analyse button
    def onTeamAnalyse(self):
        overall = TUPteamrater.analyseTeam(teamSlots=self._teamSlots, moveTypeLookup=self._getMoveTypeCached)
        gameKey = self._getTrainerGameKey()
        trainers = TUPteamrater.getTrainerReport(teamSlots=self._teamSlots, gameKey=gameKey, moveTypeLookup=self._getMoveTypeCached)
        report = overall + '\n\n' + trainers

        self._detailsNameLabel.configure(text='Team Analysis')
        self._detailsInfoText.configure(state='normal')
        self._detailsInfoText.delete('1.0', 'end')
        self._detailsInfoText.insert('1.0', report)
        self._detailsInfoText.configure(state='disabled')
        self._detailsSpriteLabel.grid_remove()
        self._detailsSpriteRef = None

    #maps to trainer key, 'Red/Blue' -> 'red-blue'
    def getTrainerGameKey(self):
        GAMEKEYMAP = {
            'Red/Blue': 'red-blue',
            'Gold/Silver': 'gold-silver',
            'Ruby/Sapphire': 'ruby-sapphire',
            'Fire Red/Leaf Green': 'firered-leafgreen',
            'Diamond/Pearl': 'diamond-pearl',
            'Heart Gold/Soul Silver': 'heartgold-soulsilver',
            'Black/White': 'black-white',
            'Black 2/White 2': 'black-2-white-2',
            'X/Y': 'x-y',
            'Omega Ruby/Alpha Sapphire': 'omega-ruby-alpha-sapphire',
            'Sun/Moon': 'sun-moon',
            'Ultra Sun/Ultra Moon': 'ultra-sun-ultra-moon',
            "Let's Go Pikachu/Eevee": 'lets-go-pikachu-lets-go-eevee',
            'Sword/Shield': 'sword-shield',
            'Brilliant Diamond/Shining Pearl': 'brilliant-diamond-shining-pearl',
            'Scarlet/Violet': 'scarlet-violet',
        }

        return GAMEKEYMAP.get(self._selectedTeamGame, self._gameVersions.get(self._selectedTeamGame, [None])[0])
    
    #when user clicks recommend button
    def onTeamRecommend(self):
        teamSlots = self._teamSlots
        chosenGen = self._selectedTeamGen
        recommended = TUPteamrater.getRecommendedMons(teamSlots=teamSlots, chosenGen=chosenGen, moveTypeLookup=self._getMoveTypeCached)

        lines = []
        lines.append('RECOMMENDATIONS:\n')

        if not recommended:
            lines.append('No recommendations available. Add Pokémon first, or your team already has good coverage.')
        else:
            for r in recommended:
                type1 = self._formatAPIText(r.get('type1'))
                type2 = self._formatAPIText(r.get('type2'))
                if type2:
                    typeLine = f'{type1} / {type2}'
                else:
                    typeLine = f'{type1}'
    
                lines.append(f"- {r['name']} ({typeLine})")
                lines.append(f"   - BST: {r['bst']}")
                lines.append(f"   - {r['reason']}")

            self._detailsNameLabel.configure(text='Team Recommendations')
            self._detailsInfoText.config(state='normal')
            self._detailsInfoText.delete('1.0', 'end')
            self._detailsInfoText.insert('1.0', '\n'.join(lines))
            self._detailsInfoText.configure(state='disabled')
            self._detailsSpriteLabel.configure(image='')
            self._detailsSpriteLabel.grid_remove()
            self._detailsSpriteRef = None
    
    #gets version groups in chosen gen
    def getAllowedVersionGroups(self, genNum):
        if not hasattr(self, 'allowedVersionGroupsCache'):
            self._allowedVersionGroupsCache = {}
        
        if genNum in self._allowedVersionGroupsCache:
            return self._allowedVersionGroupsCache[genNum]
        
        gen = pb.generation(genNum)
        groups = set(versionGroup.name for versionGroup in gen.version_groups)

        self._allowedVersionGroupsCache[genNum] = groups
        
        return groups
    
    #gets moves that Pokémon can learn
    def getValidMoves(self, monKey, genNum):
        cacheKey = (str(monKey), int(genNum))
        if not hasattr(self, 'validMovesCache'):
            self._validMovesCache = {}

        if cacheKey in self._validMovesCache:
            return self._validMovesCache[cacheKey]
        
        allowedGroups = self._getAllowedVersionGroups(genNum)

        mon = pb.pokemon(monKey)
        valid = set()

        for m in mon.moves:
            moveName = m.move.name
            for i in m.version_group_details:
                if i.version_group.name in allowedGroups:
                    valid.add(moveName)
                    break

        validList = sorted(valid)
        self._validMovesCache[cacheKey] = validList

        return validList
        
    #show login screen
    def showLogin(self):
        self._clearWindow()

        #window grid
        self._rowconfigure(0, weight=1)
        self._rowconfigure(1, weight=8)
        self._rowconfigure(2, weight=1)
        self._columnconfigure(0, weight=1)
        self._columnconfigure(1, weight=2)
        self._columnconfigure(2, weight=1)

        #main login frame
        self._loginFrame = ttk.Frame(self, padding=20)
        self._loginFrame.grid(row=1, column=0, columnspan=3, padx=30, pady=30, sticky=tk.NSEW)

        #login frame grid
        for i in range(7):
            self._loginFrame.rowconfigure(i, weight=1)
        self._loginFrame.columnconfigure(0, weight=2)
        self._loginFrame.columnconfigure(1, weight=3)
        self._loginFrame.columnconfigure(2, weight=3)
        self._loginFrame.columnconfigure(3, weight=3)
        self._loginFrame.columnconfigure(4, weight=2)

        #login title frame
        self._loginTitleFrame = ttk.Frame(self)
        self._loginTitleFrame.grid(row=0, column=0, columnspan=3, sticky=tk.EW)

        self._loginTitleFrame.columnconfigure(0, weight=1)

        #login title label
        self._loginTitleLabel = ttk.Label(self._loginTitleFrame, text='The Universal Pokédex', anchor='center', style='TLabel')
        self._loginTitleLabel.grid(row=0, column=0, pady=15, sticky=tk.EW)

        #username label
        self._usernameLabel = ttk.Label(self._loginFrame, text='Username', anchor='center', style='small.TLabel')
        self._usernameLabel.grid(row=1, column=2, padx=20, pady=(12, 2), sticky=tk.EW)

        #username entry
        self._usernameEntry = ttk.Entry(self._loginFrame, font=(self._FONT, 18))
        self._usernameEntry.grid(row=2, column=1, columnspan=3, padx=20, pady=(2, 10), sticky=tk.EW)

        #password label
        self._passwordLabel = ttk.Label(self._loginFrame, text='Password', anchor='center', style='small.TLabel')
        self._passwordLabel.grid(row=3, column=2, padx=20, pady=(10, 2), sticky=tk.EW)

        #password entry
        self._passwordEntry = ttk.Entry(self._loginFrame, show='•', font=(self._FONT, 18)) 
        self._passwordEntry.grid(row=4, column=1, columnspan=3, padx=20, pady=(2, 10), sticky=tk.EW)

        #error frame
        self._loginErrorFrame = ttk.Frame(self._loginFrame)

        self._loginErrorFrame.columnconfigure(0, weight=1)

        #error label
        self._loginErrorLabel = ttk.Label(self._loginErrorFrame, text='', anchor='center', style='progress.TLabel', wraplength=600)

        #button frame
        self._buttonFrame = ttk.Frame(self._loginFrame)
        self._buttonFrame.grid(row=6, column=2, padx=5, pady=20, sticky=tk.NSEW)

        self._buttonFrame.columnconfigure(0, weight=1)
        self._buttonFrame.columnconfigure(1, weight=1)

        #login button
        self._loginButton = ttk.Button(self._buttonFrame, text='Login', style='small.TButton', command=self._tryLogin)
        self._loginButton.grid(row=0, column=0, padx=(0, 10), sticky=tk.EW)

        #register button
        self._registerButton = ttk.Button(self._buttonFrame, text='Create Account', style='small.TButton', command=self._tryRegister)
        self._registerButton.grid(row=0, column=1, padx=(10, 0), sticky=tk.EW)

    #attempts to log into account
    def tryLogin(self):
        #retrieves user input from entry widgets
        username = self._usernameEntry.get()
        password = self._passwordEntry.get()

        #if no username or password entered
        if not username or not password:
            self._loginErrorLabel.config(text='Please enter a username and password')
            self._loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self._loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
            return
        
        #checks login details are valid
        success, userID = TUPdatabase.checkLogin(username, password)

        if success:
            self._currentUserID = userID
            self._showMainMenu()
        else:
            self._loginErrorLabel.config(text='Invalid username or password')
            self._loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self._loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)

    #attempts to register account
    def tryRegister(self):
        #retrieve user input from entry widgets
        username = self._usernameEntry.get()
        password = self._passwordEntry.get()

        #if no username or password are entered
        if not username or not password:
            self._loginErrorLabel.config(text='Please enter a username and password')
            self._loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self._loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
            return
        
        #tries to add details to database
        try:
            TUPdatabase.addUser(username, password)
            self._loginErrorLabel.config(text='Account made - Please login')
            self._loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self._loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)
        
        #error message if username already exists
        except sqlite3.IntegrityError:
            self._loginErrorLabel.config(text='Username already exists')
            self._loginErrorFrame.grid(row=5, column=2, padx=20, pady=10, sticky=tk.EW)
            self._loginErrorLabel.grid(row=0, column=0, pady=5, sticky=tk.EW)

    #applies chosen colour theme
    def applyTheme(self, themeName):
        theme = self._themes.get(themeName, self._themes['Dark Blue'])

        iconSetKey = self._getIconSet(themeName)
        self._loadIcons(iconSetKey)

        self._colours.update({
            'bgcolor': theme['bgcolor'], 'fgcolor': theme['fgcolor'],
            'activecolor': theme['activecolor'], 'framecolor': theme['framecolor'],
            'darkcolor': theme['darkcolor']
        })

        #window background
        self._configure(background=theme.get('rootbg', self._colours['darkcolor']))

        #update styles
        self._styleF.configure('TFrame', background=self._colours['framecolor'])
        self._styleMainB.configure('main.TButton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 35), bordercolor=self._colours['bgcolor'], darkcolor=self._colours['darkcolor'])
        self._styleMainB.map('main.TButton', background=[('active', self._colours['activecolor'])])
        self._styleEnterB.configure('enter.TButton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 15), bordercolor=self._colours['bgcolor'])
        self._styleEnterB.map('enter.TButton', background=[('active', self._colours['activecolor'])])
        self._styleSmallB.configure('small.TButton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 15), bordercolor=self._colours['bgcolor'], darkcolor=self._colours['darkcolor'])
        self._styleSmallB.map('small.TButton', background=[('active', self._colours['activecolor'])])
        self._styleL.configure('TLabel', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 40), bordercolor=self._colours['bgcolor'], darkcolor=self._colours['darkcolor'])
        self._styleProgressL.configure('progress.TLabel', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 10))
        self._styleSmallL.configure('small.TLabel', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 28))
        self._styleE.configure('TEntry', fieldbackground=self._colours['bgcolor'], foreground=self._colours['fgcolor'], bordercolor=self._colours['bgcolor'])
        self._styleMB.configure('filter.TMenubutton', background=self._colours['bgcolor'], foreground=self._colours['fgcolor'], font=(self._FONT, 15), arrowcolor=self._colours['fgcolor'], bordercolor=self._colours['bgcolor'])
        self._styleMB.map('filter.TMenubutton', background=[('active', self._colours['activecolor'])])

        self._configWidget('detailsInfoText', bg=self._colours['bgcolor'], fg=self._colours['fgcolor'])

        self._configWidget('buttonBall', image=self._buttonMenuBallIcon)
        self._configWidget('buttonBook', image=self._buttonMenuBookIcon)
        self._configWidget('buttonArrow', image=self._buttonMenuArrowIcon)
        self._configWidget('buttonExit', image=self._buttonMenuExitIcon)
        self._configWidget('buttonMenuChart', image=self._buttonMenuChartIcon)

        self._configWidget('buttonDex', image=self._buttonSideBallIcon)
        self._configWidget('buttonEncyc', image=self._buttonSideBookIcon)
        self._configWidget('buttonTeam', image=self._buttonSideArrowIcon)
        self._configWidget('buttonSideChart', image=self._buttonSideChartIcon)
        self._configWidget('menuButton', image=self._buttonSideHouseIcon)
    
    #gets necessary icons based on chosen theme
    def getIconSet(self, themeName):
        if themeName == 'Dark Red':
            return 'red'
        elif themeName in ('Light Blue', 'Light Red'):
            return 'white'
        else:
            return 'blue'
    
    #loads necessary icons
    def loadIcons(self, iconSetKey):
        iconDir = os.path.join(self._scriptDir, 'assets', 'icons')

        iconFiles = {
            'white': {
                'menuBall': 'pokeballIcon.png',
                'menuBook': 'encyclopediaIcon.png',
                'menuArrow': 'teamraterIcon.png',
                'menuExit': 'exitIcon.png',
                'menuChart': 'typechartIcon.png',
                'sideBall': 'pokeballIconSmall.png',
                'sideBook': 'encyclopediaIconSmall.png',
                'sideArrow': 'teamraterIconSmall.png',
                'sideHouse': 'menuIcon.png',
                'sideChart': 'typechartIconSmall.png',
            },
            'red': {
                'menuBall': 'pokeballIconRed.png',
                'menuBook': 'encyclopediaIconRed.png',
                'menuArrow': 'teamraterIconRed.png',
                'menuExit': 'exitIconRed.png',
                'menuChart': 'typechartIconRed.png',
                'sideBall': 'pokeballIconSmallRed.png',
                'sideBook': 'encyclopediaIconSmallRed.png',
                'sideArrow': 'teamraterIconSmallRed.png',
                'sideHouse': 'menuIconRed.png',
                'sideChart': 'typechartIconSmallRed.png',
            },
            'blue': {
                'menuBall': 'pokeballIconBlue.png',
                'menuBook': 'encyclopediaIconBlue.png',
                'menuArrow': 'teamraterIconBlue.png',
                'menuExit': 'exitIconBlue.png',
                'menuChart': 'typechartIconBlue.png',
                'sideBall': 'pokeballIconSmallBlue.png',
                'sideBook': 'encyclopediaIconSmallBlue.png',
                'sideArrow': 'teamraterIconSmallBlue.png',
                'sideHouse': 'menuIconBlue.png',
                'sideChart': 'typechartIconSmallBlue.png',
            }
        }

        chosen = iconFiles.get(iconSetKey, iconFiles['blue'])

        self._buttonMenuBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuBall'])))
        self._buttonMenuBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuBook'])))
        self._buttonMenuArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuArrow'])))
        self._buttonMenuExitIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuExit'])))
        self._buttonMenuChartIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuChart'])))

        self._buttonSideBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideBall'])))
        self._buttonSideBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideBook'])))
        self._buttonSideArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideArrow'])))
        self._buttonSideHouseIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideHouse'])))
        self._buttonSideChartIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideChart'])))

    #configures a widgets stored on self._attrName
    def configWidget(self, attrName, **kwargs):
        widget = getattr(self, attrName, None)
        if widget is None:
            return False
        
        try:
            if hasattr(widget, 'winfo_exists') and not widget.winfo_exists():
                return False
            widget.configure(**kwargs)
            return True
        except tk.TclError:
            return False

    #replace text in text widget stored on self._attrName
    def setText(self, attrName, text):
        widget = getattr(self, attrName, None)
        if widget is None:
            return False
        
        try:
            if hasattr(widget, 'winfo_exists') and not widget.winfo_exists():
                return False
            widget.configure(state='normal')
            widget.delete('1.0', 'end')
            widget.insert('1.0', text)
            widget.configure(state='disabled')
            return True
        except tk.TclError:
            return False
    
    #hide sprite in details section
    def hideDetailsSprite(self):
        if hasattr(self, 'detailsSpriteLabel') and self._detailsSpriteLabel.winfo_exists():
            self._detailsSpriteLabel.configure(image='')
            self._detailsSpriteLabel.grid_remove()

        self._detailsSpriteRef = None

    #show sprite in details section
    def showDetailsSprite(self, sprite):
        if not sprite:
            self._hideDetailsSprite()
            return
        
        try:
            if hasattr(self, 'detailsSpriteLabel') and self._detailsSpriteLabel.winfo_exists():
                self._detailsSpriteLabel.grid()
                self._detailsSpriteLabel.configure(image=sprite)
                self._detailsSpriteRef = sprite
        except tk.TclError:
            self._detailsSpriteRef = None

    #clears window
    def clearWindow(self):
        for widget in self._winfo_children():
            widget.destroy()

    #shows main menu
    def showMainMenu(self):
        self._clearWindow()
        self._makeMenuGrid()
        self._makeButtonFrame()
        self._makeSideMenuFrame(self)

    #shows Type Chart screen
    def showTypeChartScreen(self):
        self._clearWindow()
        self._typeChartScreen()

    #shows Pokédex screen
    def showPokedexScreen(self):
        self._clearWindow()
        self._pokedexScreen()

    #shows Encyclopedia screen
    def showEncyclopediaScreen(self):
        self._clearWindow()
        self._encyclopediaScreen()

    #shows Team Rater Screen
    def showTeamraterScreen(self):
        self._clearWindow()
        self._teamraterScreen()

    #makes title
    def makeTitle(self, text):
        titleOptions = {'column': 1, 'row': 0, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self._titleLabel = ttk.Label(self, text=text, anchor = 'center')
        self._titleLabel.grid(**titleOptions)

