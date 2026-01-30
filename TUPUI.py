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
        self.title('The Universal Pokédex')
        self.geometry('1280x780')
        self.configure(background='#ffffff')

        self.currentUserID = None

        #default theme is dark blue
        self.colours = {'bgcolor': '#7f7f7f', 'fgcolor': '#c1dbf3', 
                           'activecolor': '#595959', 'framecolor': '#404040', 
                           'darkcolor': '#232323', 'rootbg': '#232323'}

        self.themes = {
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

        self.themeVar = tk.StringVar(value='Change Theme')

        self.FONT = 'Pokemon X and Y'

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
        self.styleMainB.configure('main.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 35), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleMainB.map('main.TButton', background=[('active', self.colours['activecolor'])])
        
        self.styleEnterB = ttk.Style()
        self.styleEnterB.theme_use('clam')
        self.styleEnterB.configure('enter.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15), bordercolor=self.colours['bgcolor'])
        self.styleEnterB.map('enter.TButton', background=[('active', self.colours['activecolor'])])

        self.styleSmallB = ttk.Style()
        self.styleSmallB.theme_use('clam')
        self.styleSmallB.configure('small.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleSmallB.map('small.TButton', background=[('active', self.colours['activecolor'])])

        #label styles
        self.styleL = ttk.Style()
        self.styleL.theme_use('clam')
        self.styleL.configure('TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 40), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])

        self.styleProgressL = ttk.Style()
        self.styleProgressL.theme_use('clam')
        self.styleProgressL.configure('progress.TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 10))

        self.styleSmallL = ttk.Style()
        self.styleSmallL.theme_use('clam')
        self.styleSmallL.configure('small.TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 28))

        #entry styles
        self.styleE = ttk.Style()
        self.styleE.theme_use('clam')
        self.styleE.configure('TEntry', fieldbackground=self.colours['bgcolor'], foreground=self.colours['fgcolor'], bordercolor=self.colours['bgcolor'])

        #menubutton styles
        self.styleMB = ttk.Style()
        self.styleMB.theme_use('clam')
        self.styleMB.configure('filter.TMenubutton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15), arrowcolor=self.colours['fgcolor'], bordercolor=self.colours['bgcolor'])
        self.styleMB.map('filter.TMenubutton', background=[('active', self.colours['activecolor'])])

        #type chart images
        self.typeChartImage = ImageTk.PhotoImage(Image.open(os.path.join(self.scriptDir, 'assets', 'chart', 'pokemon-type-chart2.png')))

        #sprite cache to reduce loading times
        self.spriteCache = {}

        self.applyTheme(self.themeVar.get())

        #filter
        self.type1Var = tk.StringVar(value='Any')
        self.type2Var = tk.StringVar(value='Any')
        self.heightClassVar = tk.StringVar(value='Any')
        self.weightClassVar = tk.StringVar(value='Any')
        self.bstRangeVar = tk.StringVar(value='Any')

        #pokedex
        self.dexGenVar = tk.StringVar(value='Any')

        #team rater
        self.teamGenVar = tk.StringVar(value='Any')
        self.teamGameVar = tk.StringVar(value='Select Game')

        #games
        self.gamesByGen = {
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

        self.teamSlots = [None]*6

        #pokeAPI game version names
        self.gameVersions = {
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

    #loads a sprite from self.spriteCache
    def loadCachedSprite(self, spriteURL, size=(192, 192)):
        if not spriteURL:
            return None
        
        cacheKey = (spriteURL, size)
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
        self.sideMenuFrame.rowconfigure(2, weight=1)

        self.buttonMenuChart = ttk.Button(self.sideMenuFrame, text='Type Chart', image=self.buttonMenuChartIcon, compound=tk.TOP, command=self.showTypeChartScreen, style='main.TButton')
        self.buttonMenuChart.grid(column=0, row=0, sticky=tk.NSEW, padx=15, pady=15)

        self.themeMenu = ttk.OptionMenu(self.sideMenuFrame, self.themeVar, self.themeVar.get(), *self.themes.keys(), command=lambda choice: self.applyTheme(choice), style='filter.TMenubutton')
        self.themeMenu.grid(column=0, row=1, sticky=tk.NSEW, padx=15, pady=15)

        self.buttonExit = ttk.Button(self.sideMenuFrame, text='Exit Program', image=self.buttonMenuExitIcon, compound=tk.LEFT, command=self.destroy, style='main.TButton')
        self.buttonExit.grid(row=2, column=0, sticky=tk.NSEW, padx=15, pady=15)

        #packing side menu frame
        self.sideMenuFrame.grid(column=1, row=1, sticky=tk.NSEW, padx=15, pady=15)

    #make menu grid
    def makeMenuGrid(self):
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=12)
        self.columnconfigure(0, weight=10)
        self.columnconfigure(1, weight=5)

        self.titleOptions = {'column': 0, 'row': 0, 'columnspan': 2, 'padx': 15, 'pady': 15, 'sticky': tk.EW}
        self.titleLabel = ttk.Label(self, text='The Universal Pokédex', anchor = 'center', style='TLabel')
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
        self.dexSelectFrameOuter = ttk.Frame(self.mainFrame, padding=15, style='TFrame')
        self.dexSelectFrameOuter.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW, padx=15)

        for column in range(4):
            self.dexSelectFrameOuter.columnconfigure(column, weight=1)

        title = ttk.Label(self.dexSelectFrameOuter, text='Select Pokédex Generation', anchor='center', style='small.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.EW, pady=(0, 15))

        self.dexGenMenu = ttk.Menubutton(self.dexSelectFrameOuter, text='Generation', style='filter.TMenubutton')
        self.dexGenMenu.grid(row=1, column=1, columnspan=2, sticky=tk.EW)

        genOptions = [('Any', 'Any')] + [(f'Gen {i}', str(i)) for i in range(1, 10)]
        self.makeFilterMenu(self.dexGenMenu, genOptions, self.dexGenVar)

        self.dexContinueButton = ttk.Button(self.dexSelectFrameOuter, text='Continue', style='enter.TButton', command=self.onDexGenContinue)
        self.dexContinueButton.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=(15, 0))

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
        self.searchEntry = ttk.Entry(self.mainFrame, font = ('Trebuchet MS', 20))
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

    #making frame for encyclopedia
    def encyclopediaFrame(self):
        self.makeDetailsFrame(headerText='Select Entry', framePady=(0, 15), gridRow=0, rowSpan=4)
        self.makeTitle("Encyclopedia")

        #search entry
        self.encycSearchEntry = ttk.Entry(self.mainFrame, font=(self.FONT, 20))
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

        self.makeFilterMenu(self.encycItemMenu, itemOptions, self.encycItemTypeVar, self.refreshEncyclopediaResults)

        #generation menu
        self.encycGenMenu = ttk.Menubutton(self.encycFiltersFrame, text='Gen', style='filter.TMenubutton')
        self.encycGenMenu.grid(row=0, column=1, sticky=tk.EW, padx=(0, 8))
        
        genOptions = [('Any', 'Any')] + [(f'Gen {i}', str(i)) for i in range(1, 10)]

        self.makeFilterMenu(self.encycGenMenu, genOptions, self.encycGenVar, self.refreshEncyclopediaResults)

        #type menu
        self.encycTypeMenu = ttk.Menubutton(self.encycFiltersFrame, text='Type', style='filter.TMenubutton')
        self.encycTypeMenu.grid(row=0, column=2, sticky=tk.EW, padx=(0, 8))

        typeOptions = [('Any', 'Any'), ('Normal', 'Normal'), ('Fire', 'Fire'), ('Water', 'Water'),
                       ('Grass', 'Grass'), ('Electric', 'Electric'), ('Ice', 'Ice'), ('Fighting', 'Fighting'),
                       ('Poison', 'Poison'), ('Ground', 'Ground'), ('Flying', 'Flying'), ('Psychic', 'Psychic'),
                       ('Bug', 'Bug'), ('Rock', 'Rock'), ('Ghost', 'Ghost'), ('Dragon', 'Dragon'),
                       ('Dark', 'Dark'), ('Steel', 'Steel'), ('Fairy', 'Fairy')]
        
        self.makeFilterMenu(self.encycTypeMenu, typeOptions, self.encycTypeVar, self.refreshEncyclopediaResults)

        #scrollable results
        self.encycResultsOuterFrame, self.encycResultsCanvas, self.encycResultsInnerFrame = self.makeScrollableFrame(self.mainFrame)
        self.encycResultsOuterFrame.grid(row=2, column=2, rowspan=2, columnspan=2, sticky=tk.NSEW, padx=15, pady=15)

        self.refreshEncyclopediaResults()
        
    #making screen for Type Chart section
    def typeChartScreen(self):
        self.secondaryScreen()

        for row in range(4):
            self.mainFrame.rowconfigure(row, weight=1, minsize=0)
        for column in range(4):
            self.mainFrame.columnconfigure(column, weight=1)

        for i in range(2, 5):
            self.rowconfigure(i, weight=0)

        #changing title
        self.makeTitle('Type Chart')

        #create side frame buttons
        self.buildSideNav('typechart')

        #type chart image
        self.chartLabel = ttk.Label(self.mainFrame, image=self.typeChartImage, anchor='center')
        self.chartLabel.grid(column=0, row=0, columnspan=4, rowspan=4, padx=15, pady=15, sticky=tk.NSEW)

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

    #making screen for Pokédex
    def pokedexScreen(self):
        self.secondaryScreen()

        #change title
        self.makeTitle('Pokédex')
        
        #create side frame buttons
        self.buildSideNav('pokedex')

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
        self.buildSideNav('encyclopedia')

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
        self.buildSideNav('teamrater')

        #return to main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        #select frame
        self.teamSelectFrame = ttk.Frame(self.mainFrame, padding=15, style='TFrame')
        self.teamSelectFrame.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW, padx=15)

        for column in range(4):
            self.teamSelectFrame.columnconfigure(column, weight=1)

        title = ttk.Label(self.teamSelectFrame, text='Select Game', anchor='center', style='small.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.EW, pady=(0, 15))

        #gen dropdown
        self.teamGenMenu = ttk.Menubutton(self.teamSelectFrame, text='Generation', style='filter.TMenubutton')
        self.teamGenMenu.grid(row=1, column=1, sticky=tk.EW, padx=(0, 8))

        genOptions = [('Any', 'Any')] + [(f'Gen {i}', str(i)) for i in range(1, 10)]
        self.makeFilterMenu(self.teamGenMenu, genOptions, self.teamGenVar, refreshCommand=self.refreshTeamGameMenu)

        #game dropdown
        self.teamGameMenu = ttk.Menubutton(self.teamSelectFrame, text='Game', style='filter.TMenubutton')
        self.teamGameMenu.grid(row=1, column=2, sticky=tk.EW, padx=(8, 0))

        #continue button
        self.teamContinueButton = ttk.Button(self.teamSelectFrame, text='Continue', style='enter.TButton', command=self.onTeamGameContinue)
        self.teamContinueButton.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=(15, 0))

        self.refreshTeamGameMenu()

    #making frame for scrollable canvas
    def makeScrollableFrame(self, parent):
        #frame for canvas and scrollbar
        scrollOuterFrame = ttk.Frame(parent)

        scrollOuterFrame.rowconfigure(0, weight=1)
        scrollOuterFrame.columnconfigure(0, weight=1)

        #canvas
        resultCanvas = tk.Canvas(scrollOuterFrame, highlightthickness=0, bg=self.colours['bgcolor'])
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
        for widget in self.sideFrame.winfo_children():
            widget.destroy()
        
        #main menu button
        self.menuButton = ttk.Button(self.sideFrame, text='Main Menu', image=self.buttonSideHouseIcon, compound=tk.LEFT, command=self.showMainMenu, style='main.TButton')
        self.menuButton.grid(column=0, row=0, padx=15, pady=15, sticky=tk.NSEW)

        buttonNav = [ #key, label, imageAttr, command
            ('pokedex', 'Pokédex', self.buttonSideBallIcon, self.showPokedexScreen),
            ('encyclopedia', 'Encyclopedia', self.buttonSideBookIcon, self.showEncyclopediaScreen),
            ('teamrater', 'Team Rater', self.buttonSideArrowIcon, self.showTeamraterScreen),
            ('typechart', 'Type Chart', self.buttonSideChartIcon, self.showTypeChartScreen)
        ]

        row = 1
        for key, label, icon, cmd in buttonNav:
            if key == currentScreen:
                continue
            
            #side button
            button = ttk.Button(self.sideFrame, text=label, image=icon, compound=tk.TOP, command=cmd, style='main.TButton')
            button.grid(row=row, sticky=tk.NSEW, padx=10, pady=10)

            #store references for updating icons
            if key == 'pokedex':
                self.buttonDex = button
            if key == 'encyclopedia':
                self.buttonEncyc = button
            if key == 'teamrater':
                self.buttonTeam = button
            if key == 'typechart':
                self.buttonSideChart = button

            row += 1
        

    #populates grid with Pokémon that match the search/filter criteria  
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

        for column in range(self.columns):
            self.resultsInnerFrame.columnconfigure(column, weight=1, uniform='resultsCols')

        #for each Pokémon that matches criteria
        for index, (dexMonID, monName, spriteURL) in enumerate(rows):
            self.cardRow = index//self.columns
            self.cardColumn = index%self.columns

            #card frame
            self.card = ttk.Frame(self.resultsInnerFrame, padding=8, style='TFrame')
            self.card.grid(row=self.cardRow, column=self.cardColumn, sticky=tk.NSEW, padx=self.cardPadX, pady=self.cardPadY)

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
                dexNum = TUPitems.getDexNumFromURL(spriteURL)
                if dexNum is not None:
                    spriteURL = TUPitems.spriteURLFromDexNum(dexNum, self.genNum)
                #runs _loadSpriteToLabel in background
                threading.Thread(target=self.loadSpriteToLabel, args=(spriteURL, spriteLabel, dexMonID), daemon=True).start()

    #populates grid with results that match the criteria  
    def populateEncyclopediaGrid(self, rows):
        if not hasattr(self, 'encycResultsInnerFrame'):
            return

        for widget in self.encycResultsInnerFrame.winfo_children():
            widget.destroy()

        self.encycSpriteRefs = {}

        #grid settings
        self.columns = 3
        self.cardPadX = 10
        self.cardPadY = 10

        for column in range(self.columns):
            self.encycResultsInnerFrame.columnconfigure(column, weight=1, uniform='encycCols')

        itemType = self.encycItemTypeVar.get()

        #for each Pokémon that matches criteria
        for index, (itemKey, displayName, spriteURL) in enumerate(rows):
            self.cardRow = index//self.columns
            self.cardColumn = index%self.columns

            #card frame
            self.card = ttk.Frame(self.encycResultsInnerFrame, padding=8, style='TFrame')
            self.card.grid(row=self.cardRow, column=self.cardColumn, sticky=tk.NSEW, padx=self.cardPadX, pady=self.cardPadY)

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
        if not hasattr(self, 'resultsInnerFrame') or not self.resultsInnerFrame.winfo_exists():
            return
        if not hasattr(self, 'searchEntry') or not self.searchEntry.winfo_exists():
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
            self.setText('detailsInfoText', '')
            self.hideDetailsSprite()

            if hasattr(self, "deleteButton"):
                self.deleteButton.state(["disabled"])

    #refreshes displayed results when user changes criteria
    def refreshEncyclopediaResults(self):
        if not hasattr(self, 'encycResultsInnerFrame') or not self.encycResultsInnerFrame.winfo_exists():
            return
        if not hasattr(self, 'encycSearchEntry') or not self.encycSearchEntry.winfo_exists():
            return
        
        #types do not apply to abilities
        if self.encycItemTypeVar.get() == 'Ability' and self.encycTypeVar.get() != 'Any':
            self.encycTypeVar.set('Any')

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

        else:
            self.selectedEncycKey = None
            self.detailsNameLabel.configure(text='No results')
            self.setText('detailsInfoText', 'No results match your search.')
            self.hideDetailsSprite()
    
    #loads specified Pokémon sprite to label
    def loadSpriteToLabel(self, spriteURL, label, monID):
        try:
            response = requests.get(spriteURL, timeout=5)
            response.raise_for_status()

            image = Image.open(BytesIO(response.content))
            image = image.resize((96, 96), Image.NEAREST)
            tkImage = ImageTk.PhotoImage(image)

            def apply():
                label.configure(image=tkImage)
                if hasattr(self, 'resultSpriteRefs'):
                    self.resultSpriteRefs[monID] = tkImage
                if hasattr(self, 'encycSpriteRefs'):
                    self.encycSpriteRefs[monID] = tkImage
            
            self.after(0, apply)
        except:
            pass

    #shows details of a specific Pokémon in the database
    def showMonDetails(self, dexMonID):
        mon = TUPdatabase.returnDexMonForUser(self.currentUserID, dexMonID)
        
        if not mon:
            self.detailsNameLabel.configure(text='No details for this Pokémon')
            self.setText('detailsInfoText', 'No details for this Pokémon')
            self.hideDetailsSprite()
            return

        #update labels
        self.detailsNameLabel.configure(text=mon["MonName"].title())

        #stats, base or custom
        statsLine = f"HP {mon['UHP']} / Atk {mon['UAtk']} / Def {mon['UDef']} / SpA {mon['USpA']} / SpD {mon['USpD']} / Spe {mon['USpe']}"
        bst = sum(int(mon[i]) for i in ["UHP", "UAtk", "UDef", "USpA", "USpD", "USpe"] if mon.get(i) is not None)
                  
        typeLine = self.formatAPIText(mon["Type1"])
        if mon["Type2"]:
            typeLine += " / " + self.formatAPIText(mon["Type2"])

        if mon.get("PreEvo"):
            preEvo = self.formatAPIText(mon["PreEvo"])
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
                    f'Species: {self.formatAPIText(mon.get("Species"))}\n'
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
        dexNum = mon.get('DexNum')
        spriteURL = TUPitems.spriteURLFromDexNum(dexNum, self.genNum)
        sprite = self.loadCachedSprite(spriteURL, size=(256, 256))
        self.showDetailsSprite(sprite)

    #shows details of selected item
    def showEncyclopediaDetails(self, itemKey):
        sprite = None
        itemType = self.encycItemTypeVar.get()
        chosenGen = self.encycGenVar.get()
        if chosenGen != 'Any':
            chosenGenNum = int(chosenGen)
        else:
            chosenGenNum = 9

        self.hideDetailsSprite()

        try:
            if itemType == 'Pokémon':
                monObj = TUPitems.Mon('mon', int(itemKey), chosenGenNum)

                #update sprite
                spriteURL = TUPitems.spriteURLFromDexNum(monObj.getDexNum(), chosenGenNum)
                sprite = self.loadCachedSprite(monObj.getSpriteURL(), size=(256, 256))

                #update labels
                self.detailsNameLabel.configure(text=monObj.getItemName().title())

                #stats, base or custom
                statsLine = f"HP {monObj.getHP()} / Atk {monObj.getAtk()} / Def {monObj.getDef()} / SpA {monObj.getSpA()} / SpD {monObj.getSpD()} / Spe {monObj.getSpe()}"
                bst = monObj.getBST()
                        
                typeLine = self.formatAPIText(monObj.getType1())
                type2 = monObj.getType2()
                if type2 not in (-1, None, '', 'none'):
                    typeLine += " / " + self.formatAPIText(type2)

                if monObj.getPreEvo():
                    preEvo = self.formatAPIText(monObj.getPreEvo())
                else:
                    preEvo = "None"

                evoBlock = self.formatEvo(monObj.getEvoList())
                eggGroupsBlock = self.formatPipeBlock("Egg Groups", monObj.getEggGroups())
                locationsBlock = self.formatPipeBlock("Locations", monObj.getLocations(), maxItems=10)

                movesRaw = monObj.getMoves() or ""
                movesBlock = self.formatPipeBlock("Moves", movesRaw)

                abilitiesRaw = monObj.getAbilities() or ''
                abilitiesBlock = self.formatPipeBlock('Abilities', abilitiesRaw, maxItems=6)

                flavorText = (monObj.getFlavorText() or "").strip()

                infoText = (f'National Dex Number: {monObj.getDexNum()}\n'
                            f'Species: {self.formatAPIText(monObj.getSpecies())}\n'
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

                infoText = (f"Flavor Text: {abilObj.getFlavorText() or 'None'}\n")
            
            self.setText('detailsInfoText', infoText)
            self.showDetailsSprite(sprite)
        
        except:
            self.detailsNameLabel.configure(text='Error')
            self.setText('detailsInfoText', 'Could not load details from PokéAPI.')
            self.hideDetailsSprite()

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
        items = [self.formatAPIText(name) for name in self.splitPipeList(text)]

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
                return f"Evolution: {self.formatAPIText(evoText)}"
            
        #shows even if not list after parsing
        if not isinstance(evoObj, list) or len(evoObj) == 0:
            return f"Evolution: None"
        
        if isinstance(evoObj[0], list):
            baseList = evoObj[0]
        else:
            baseList = [evoObj[0]]

        output = "Evolution: \n" 
        output += " → ".join(self.formatAPIText(name) for name in baseList)
        
        #adds branches
        if len(evoObj) > 1:
            output += "\nBranches: \n"
            for branch in evoObj[1:]:
                if isinstance(branch, list) and branch:
                    output += " " + " → ".join(self.formatAPIText(name) for name in branch) + "\n"
        
        return output.strip() 

    #when a Pokémon is selected
    def onSelectMon(self, dexMonID):
        self.selectedDexMonID = dexMonID

        if hasattr(self, "deleteButton"):
            self.deleteButton.state(["!disabled"])

        self.showMonDetails(dexMonID)

    def onSelectEncyclopediaItem(self, itemID):
        self.selectedEncycKey = itemID
        self.showEncyclopediaDetails(itemID)

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
        self.detailsFrame = ttk.Frame(self.mainFrame, padding=(20, 20), style='TFrame')
        #self.detailsFrame.grid_propagate(False)
        self.detailsFrame.grid(row=gridRow, column=0, columnspan=2, rowspan=rowSpan, sticky=tk.NSEW, padx=(15, 10), pady=framePady)

        self.detailsFrame.rowconfigure(0, weight=0) #name
        self.detailsFrame.rowconfigure(1, weight=0) #sprite
        self.detailsFrame.rowconfigure(2, weight=1) #info
        self.detailsFrame.rowconfigure(3, weight=0)
        self.detailsFrame.columnconfigure(0, weight=1)

        #name label
        self.detailsNameLabel = ttk.Label(self.detailsFrame, text=headerText, anchor='center', style='small.TLabel')
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

        self.detailsInfoText = tk.Text(self.detailsInfoOuterFrame, wrap='word', yscrollcommand=self.detailsInfoScrollbar.set, bg=self.colours['bgcolor'], fg=self.colours['fgcolor'], font=(self.FONT, 12), relief='flat', highlightthickness=0, padx=8, pady=8)
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
        
        #when user presses add button
        def onAdd():
            userIn = self.dexNumEntry.get()
            monKey = self.normaliseMonInput(userIn)

            if not monKey:
                showinfo("Error", "Please enter a Dex number or Pokédex name.")
                return

            #Pokémon object
            try:
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

    #updates available games to select from after user chooses gen 
    def refreshTeamGameMenu(self):
        chosenGen = self.teamGenVar.get()
        menu = tk.Menu(self.teamGameMenu, tearoff=0)

        if chosenGen == 'Any':
            self.teamGameVar.set('Select Game')
            menu.add_command(label='Select a generation first', command=lambda: None)
        else:
            games = self.gamesByGen.get(chosenGen, [])
            if not games:
                self.teamGameVar.set('Select Game')
                menu.add_command(label='No games available', command=lambda: None)
            else:
                #default to first game if current not in list
                current = self.teamGameVar.get()
                if current not in games:
                    self.teamGameVar.set(games[0])

                for game in games:
                    menu.add_radiobutton(label=game, value=game, variable=self.teamGameVar)
        
        self.teamGameMenu['menu'] = menu

    #when user clicks continue button in team rater
    def onTeamGameContinue(self):
        gen = self.teamGenVar.get()
        game = self.teamGameVar.get()

        if gen == 'Any':
            showinfo('Team Rater', 'Please select a generation.')
            return
        
        if not game or game == 'Select Game':
            showinfo('Team Rater', 'Please select a game.')
            return

        self.selectedTeamGen = int(gen)
        self.selectedTeamGame = game
        self.showTeamInput()

    #when user clicks continue button in pokedex
    def onDexGenContinue(self):
        gen = self.dexGenVar.get()

        if gen == 'Any':
            showinfo('Pokédex', 'Please select a generation.')
            return
        
        if hasattr(self, 'dexSelectFrameOuter') and self.dexSelectFrameOuter.winfo_exists():
            self.dexSelectFrameOuter.destroy()

        self.pokemonFrame(gen)

    #make filter criteria
    def makePokedexCriteria(self):
        name = ''

        try:
            if hasattr(self, 'searchEntry') and self.searchEntry.winfo_exists():
                name = self.searchEntry.get().strip()
        except tk.TclError:
            return {'name': None, 'type1': None, 'type2': None, 'heightMin': None, 'heightMax': None, 'weightMin': None, 'weightMax': None, 'bstMin': None, 'bstMax': None}
        
        
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
    
    #shows team select screen
    def showTeamInput(self):
        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        self.makeTitle(f'Team Rater - Gen {self.selectedTeamGen} ({self.selectedTeamGame})')
    
        #details frame
        self.makeDetailsFrame(headerText='Select a Team Slot', framePady=(0, 15), gridRow=1, rowSpan=3)

        #entry button
        self.teamSearchEntry = ttk.Entry(self.mainFrame, font=(self.FONT, 20))
        self.teamSearchEntry.grid(row=0, column=2, sticky=tk.EW, pady=(15, 10), padx=(0 ,10))
        self.teamSearchEntry.bind('<Return>', lambda e: self.onAddTeamMon())

        #add button
        self.teamAddButton = ttk.Button(self.mainFrame, text='Add to Team', style='enter.TButton', command=self.onAddTeamMon)
        self.teamAddButton.grid(row=0, column=3, sticky=tk.EW, pady=(15, 10), padx=(0, 0))

        #team slots frame
        self.teamSlotsFrame = ttk.Frame(self.mainFrame, padding=10, style='TFrame')
        self.teamSlotsFrame.grid(row=1, column=2, columnspan=2, rowspan=3, sticky=tk.NSEW, pady=(0, 15), padx=15)

        for column in range(2):
            self.teamSlotsFrame.columnconfigure(column, weight=1, uniform='teamSlots', minsize=190)
        for row in range(3):
            self.teamSlotsFrame.rowconfigure(row, weight=1, uniform='teamSlotsRows', minsize=170)

        self.showTeamSlots()

        #continue button
        self.teamContinueButton = ttk.Button(self.mainFrame, text='Analyse Team', style='enter.TButton', command=self.onTeamAnalyse)
        self.teamContinueButton.grid(row=0, column=0, sticky=tk.EW, pady=(15, 10), padx=(0, 10))

        #recommend button
        self.teamRecommendButton = ttk.Button(self.mainFrame, text='Recommend', style='enter.TButton', command=self.onTeamRecommend)
        self.teamRecommendButton.grid(row=0, column=1, sticky=tk.EW, pady=(15, 10), padx=(10, 10))

    #shows 6 slots in team
    def showTeamSlots(self):
        for widget in self.teamSlotsFrame.winfo_children():
            widget.destroy()

        self.teamSpriteRefs = {}

        for i in range(6):
            r = i//2
            c= i%2

            card = ttk.Frame(self.teamSlotsFrame, padding=10, style='TFrame')
            card.grid(row=r, column=c, sticky=tk.NSEW, padx=10, pady=10)
            card.columnconfigure(0, weight=1)

            slotData = self.teamSlots[i]

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
            removeButton = ttk.Button(card, text='Remove', style='small.TButton', command=lambda j=i: self.removeTeamSlot(j))
            removeButton.grid(row=2, column=0, sticky=tk.EW, pady=(4, 0))

            if not slotData:
                spriteLabel.configure(image='', text='')
                removeButton.state(['disabled'])
            else:
                sprite = self.loadCachedSprite(slotData['spriteURL'], size=(96, 96))
                if sprite:
                    spriteLabel.configure(image=sprite)
                    self.teamSpriteRefs[i] = sprite
                removeButton.state(['!disabled'])
            
            def onClick(event, j=i):
                self.onSelectTeamSlot(j)

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
            if self.teamSlots[i] is None:
                return i
        
        return None
    
    #validates whether pokemon exists in the chosen game
    def monExistsInGame(self, monKey):
        try:
            teamMon = TUPitems.Mon('mon', monKey, self.selectedTeamGen)
            monFromGen = int(teamMon.getItemFromGen())
            return monFromGen <= int(self.selectedTeamGen)
            
        except:
            return False
    
    #when the user clicks add button
    def onAddTeamMon(self):
        userIn = self.teamSearchEntry.get()
        monKey = self.normaliseMonInput(userIn)

        if monKey is None:
            showinfo('Team Rater', 'Enter a Pokémon name or Dex number.')   
            return
        
        slotIndex = self.findNextEmptySlot()
        if slotIndex is None:
            showinfo('Team Rater', 'Your team already has 6 Pokémon. Please remove one first.')
            return
        
        if not self.monExistsInGame(monKey):
            showinfo('Team Rater', f"That Pokémon isn't valid for {self.selectedTeamGame}.")
            return
        
        try:
            monObj = TUPitems.Mon('mon', monKey, self.selectedTeamGen)
        
        except:
            showinfo('Team Rater', 'Could not load that Pokémon from the API.')
            return
    
        dexNum = int(monObj.getDexNum())
        name = self.formatAPIText(monObj.getItemName())
        spriteURL = monObj.getSpriteURL()

        self.teamSlots[slotIndex] = {'dexNum': dexNum, 'name': name, 'type1': monObj.getType1(), 'type2': monObj.getType2(), 
                                     'bst': monObj.getBST(), 'spriteURL': spriteURL, 'moves': [None, None, None, None]}

        self.teamSearchEntry.delete(0, 'end')
        self.showTeamSlots()
        self.onSelectTeamSlot(slotIndex)

    #removes a pokemon from the team
    def removeTeamSlot(self, i):
        self.teamSlots[i] = None
        self.showTeamSlots()
        self.detailsNameLabel.configure(text='Select a Team Slot')
        self.detailsInfoText.config(state='normal')
        self.detailsInfoText.delete('1.0', 'end')
        self.detailsInfoText.configure(state='disabled')
        self.detailsSpriteLabel.grid_remove()
        self.detailsSpriteRef = None

    #when the user clicks a team slot
    def onSelectTeamSlot(self, i):
        slotData = self.teamSlots[i]
        if not slotData:
            self.detailsNameLabel.configure(text=f'Slot {i+1} (Empty)')
            self.detailsInfoText.configure(state='normal')
            self.detailsInfoText.delete('1.0', 'end')
            self.detailsInfoText.insert('1.0', 'Add a Pokémon to this slot.')
            self.detailsInfoText.configure(state='disabled')
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None
            return
        
        if 'moves' not in slotData:
            slotData['moves'] = [None, None, None, None]

        #clears previous move UI
        if hasattr(self, 'teamMovesFrame') and self.teamMovesFrame.winfo_exists():
            self.teamMovesFrame.destroy()

        self.teamMovesFrame = ttk.Frame(self.detailsFrame, style='TFrame')
        self.teamMovesFrame.grid(row=3, column=0, sticky=tk.EW, pady=(10, 0))

        for column in range(4):
            self.teamMovesFrame.columnconfigure(column, weight=1)

        try:
            validMoves = self.getValidMoves(slotData['dexNum'], self.selectedTeamGen)
        except:
            validMoves = []

        moveOptions = ['None'] + [self.formatAPIText(move) for move in validMoves]

        while len(slotData['moves']) < 4:
            slotData['moves'].append(None)

        self.teamMoveVars = []
        for moveIndex in range(4):
            currentMove = slotData['moves'][moveIndex]
            if not currentMove:
                current = 'None'
            else:
                current = self.formatAPIText(currentMove)

            moveVar = tk.StringVar(value=current)
            self.teamMoveVars.append(moveVar)

            self.moveMenubutton = ttk.Menubutton(self.teamMovesFrame, text=f'Move {moveIndex+1}', style='filter.TMenubutton')
            self.moveMenubutton.grid(row=0, column=moveIndex, sticky=tk.EW, padx=4)

            self.moveMenu = tk.Menu(self.moveMenubutton, tearoff=0)

            varList = self.teamMoveVars

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
                self.moveMenu.add_command(label=option, command=moveCommand(moveIndex, option))

            self.moveMenubutton['menu'] = self.moveMenu
            self.moveMenubutton.configure(textvariable=moveVar)
        
        self.detailsNameLabel.configure(text=slotData['name'])

        typeLine = self.formatAPIText(slotData['type1'])
        if slotData['type2'] not in (-1, None, '', 'none'):
            typeLine += ' / ' + self.formatAPIText(slotData['type2'])

        infoText = (
            f"Dex Number: {slotData['dexNum']}\n"
            f"Type: {typeLine}\n"
            f"BST: {slotData['bst']}\n"
            f"Game: {self.selectedTeamGame}\n"
            f"Generation: {self.selectedTeamGen}\n"
        )

        self.detailsInfoText.configure(state='normal')
        self.detailsInfoText.delete('1.0', 'end')
        self.detailsInfoText.insert('1.0', infoText)
        self.detailsInfoText.configure(state='disabled')

        sprite = self.loadCachedSprite(slotData['spriteURL'], size=(256, 256))

        if sprite:
            self.detailsSpriteLabel.grid()
            self.detailsSpriteLabel.configure(image=sprite)
            self.detailsSpriteRef = sprite
        else:
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None
    
    #gets type of move from cache to reduce number of times fetching from pokeAPI
    def getMoveTypeCached(self, moveName):
        if not moveName:
            return None
        
        moveKey = str(moveName).strip().lower().replace(' ', '-')

        if not hasattr(self, 'moveTypeCache'):
            self.moveTypeCache = {}

        if moveKey in self.moveTypeCache:
            return self.moveTypeCache[moveKey]
        
        try:
            moveObj = pb.move(moveKey)
            moveType = getattr(getattr(moveObj, 'type', None), 'name', None)
            self.moveTypeCache[moveKey] = moveType
            return moveType
        
        except:
            self.moveTypeCache[moveKey] = None
            return None

    #when user clicks analyse button
    def onTeamAnalyse(self):
        overall = TUPteamrater.analyseTeam(teamSlots=self.teamSlots, moveTypeLookup=self.getMoveTypeCached)
        gameKey = self.getTrainerGameKey()
        trainers = TUPteamrater.getTrainerReport(teamSlots=self.teamSlots, gameKey=gameKey, moveTypeLookup=self.getMoveTypeCached)
        report = overall + '\n\n' + trainers

        self.detailsNameLabel.configure(text='Team Analysis')
        self.detailsInfoText.configure(state='normal')
        self.detailsInfoText.delete('1.0', 'end')
        self.detailsInfoText.insert('1.0', report)
        self.detailsInfoText.configure(state='disabled')
        self.detailsSpriteLabel.grid_remove()
        self.detailsSpriteRef = None

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

        return GAMEKEYMAP.get(self.selectedTeamGame, self.gameVersions.get(self.selectedTeamGame, [None])[0])
    
    #when user clicks recommend button
    def onTeamRecommend(self):
        teamSlots = self.teamSlots
        chosenGen = self.selectedTeamGen
        recommended = TUPteamrater.getRecommendedMons(teamSlots=teamSlots, chosenGen=chosenGen, moveTypeLookup=self.getMoveTypeCached)

        lines = []
        lines.append('RECOMMENDATIONS:\n')

        if not recommended:
            lines.append('No recommendations available. Add Pokémon first, or your team already has good coverage.')
        else:
            for r in recommended:
                type1 = self.formatAPIText(r.get('type1'))
                type2 = self.formatAPIText(r.get('type2'))
                if type2:
                    typeLine = f'{type1} / {type2}'
                else:
                    typeLine = f'{type1}'
    
                lines.append(f"- {r['name']} ({typeLine})")
                lines.append(f"   - BST: {r['bst']}")
                lines.append(f"   - {r['reason']}")

            self.detailsNameLabel.configure(text='Team Recommendations')
            self.detailsInfoText.config(state='normal')
            self.detailsInfoText.delete('1.0', 'end')
            self.detailsInfoText.insert('1.0', '\n'.join(lines))
            self.detailsInfoText.configure(state='disabled')
            self.detailsSpriteLabel.configure(image='')
            self.detailsSpriteLabel.grid_remove()
            self.detailsSpriteRef = None
    
    #gets version groups in chosen gen
    def getAllowedVersionGroups(self, genNum):
        if not hasattr(self, 'allowedVersionGroupsCache'):
            self.allowedVersionGroupsCache = {}
        
        if genNum in self.allowedVersionGroupsCache:
            return self.allowedVersionGroupsCache[genNum]
        
        gen = pb.generation(genNum)
        groups = set(versionGroup.name for versionGroup in gen.version_groups)

        self.allowedVersionGroupsCache[genNum] = groups
        
        return groups
    
    #gets moves that Pokémon can learn
    def getValidMoves(self, monKey, genNum):
        cacheKey = (str(monKey), int(genNum))
        if not hasattr(self, 'validMovesCache'):
            self.validMovesCache = {}

        if cacheKey in self.validMovesCache:
            return self.validMovesCache[cacheKey]
        
        allowedGroups = self.getAllowedVersionGroups(genNum)

        mon = pb.pokemon(monKey)
        valid = set()

        for m in mon.moves:
            moveName = m.move.name
            for i in m.version_group_details:
                if i.version_group.name in allowedGroups:
                    valid.add(moveName)
                    break

        validList = sorted(valid)
        self.validMovesCache[cacheKey] = validList

        return validList
        
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

    #applies chosen colour theme
    def applyTheme(self, themeName):
        theme = self.themes.get(themeName, self.themes['Dark Blue'])

        iconSetKey = self.getIconSet(themeName)
        self.loadIcons(iconSetKey)

        self.colours.update({
            'bgcolor': theme['bgcolor'], 'fgcolor': theme['fgcolor'],
            'activecolor': theme['activecolor'], 'framecolor': theme['framecolor'],
            'darkcolor': theme['darkcolor']
        })

        #window background
        self.configure(background=theme.get('rootbg', self.colours['darkcolor']))

        #update styles
        self.styleF.configure('TFrame', background=self.colours['framecolor'])
        self.styleMainB.configure('main.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 35), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleMainB.map('main.TButton', background=[('active', self.colours['activecolor'])])
        self.styleEnterB.configure('enter.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15), bordercolor=self.colours['bgcolor'])
        self.styleEnterB.map('enter.TButton', background=[('active', self.colours['activecolor'])])
        self.styleSmallB.configure('small.TButton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleSmallB.map('small.TButton', background=[('active', self.colours['activecolor'])])
        self.styleL.configure('TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 40), bordercolor=self.colours['bgcolor'], darkcolor=self.colours['darkcolor'])
        self.styleProgressL.configure('progress.TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 10))
        self.styleSmallL.configure('small.TLabel', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 28))
        self.styleE.configure('TEntry', fieldbackground=self.colours['bgcolor'], foreground=self.colours['fgcolor'], bordercolor=self.colours['bgcolor'])
        self.styleMB.configure('filter.TMenubutton', background=self.colours['bgcolor'], foreground=self.colours['fgcolor'], font=(self.FONT, 15), arrowcolor=self.colours['fgcolor'], bordercolor=self.colours['bgcolor'])
        self.styleMB.map('filter.TMenubutton', background=[('active', self.colours['activecolor'])])

        self.configWidget('detailsInfoText', bg=self.colours['bgcolor'], fg=self.colours['fgcolor'])

        self.configWidget('buttonBall', image=self.buttonMenuBallIcon)
        self.configWidget('buttonBook', image=self.buttonMenuBookIcon)
        self.configWidget('buttonArrow', image=self.buttonMenuArrowIcon)
        self.configWidget('buttonExit', image=self.buttonMenuExitIcon)
        self.configWidget('buttonMenuChart', image=self.buttonMenuChartIcon)

        self.configWidget('buttonDex', image=self.buttonSideBallIcon)
        self.configWidget('buttonEncyc', image=self.buttonSideBookIcon)
        self.configWidget('buttonTeam', image=self.buttonSideArrowIcon)
        self.configWidget('buttonSideChart', image=self.buttonSideChartIcon)
        self.configWidget('menuButton', image=self.buttonSideHouseIcon)
    
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
        iconDir = os.path.join(self.scriptDir, 'assets', 'icons')

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

        self.buttonMenuBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuBall'])))
        self.buttonMenuBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuBook'])))
        self.buttonMenuArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuArrow'])))
        self.buttonMenuExitIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuExit'])))
        self.buttonMenuChartIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['menuChart'])))

        self.buttonSideBallIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideBall'])))
        self.buttonSideBookIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideBook'])))
        self.buttonSideArrowIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideArrow'])))
        self.buttonSideHouseIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideHouse'])))
        self.buttonSideChartIcon = ImageTk.PhotoImage(Image.open(os.path.join(iconDir, chosen['sideChart'])))

    #configures a widgets stored on self.attrName
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

    #replace text in text widget stored on self.attrName
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
        if hasattr(self, 'detailsSpriteLabel') and self.detailsSpriteLabel.winfo_exists():
            self.detailsSpriteLabel.configure(image='')
            self.detailsSpriteLabel.grid_remove()

        self.detailsSpriteRef = None

    #show sprite in details section
    def showDetailsSprite(self, sprite):
        if not sprite:
            self.hideDetailsSprite()
            return
        
        try:
            if hasattr(self, 'detailsSpriteLabel') and self.detailsSpriteLabel.winfo_exists():
                self.detailsSpriteLabel.grid()
                self.detailsSpriteLabel.configure(image=sprite)
                self.detailsSpriteRef = sprite
        except tk.TclError:
            self.detailsSpriteRef = None

    #clears window
    def clearWindow(self):
        for widget in self.winfo_children():
            widget.destroy()

    #shows main menu
    def showMainMenu(self):
        self.clearWindow()
        self.makeMenuGrid()
        self.makeButtonFrame()
        self.makeSideMenuFrame(self)

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

