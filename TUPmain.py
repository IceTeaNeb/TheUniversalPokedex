#The Universal Pokedex - Main Program

#----------------------imports----------------------#
import TUPUI
import TUPitems
import TUPdatabase

#--------------------------------------------#
if __name__ == '__main__':
    TUPdatabase.createDatabase()
    mainWin = TUPUI.mainWindow()
    mainWin.showLogin()
    mainWin.mainloop()
    