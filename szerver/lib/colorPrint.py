# -*- coding: utf-8 -*-

# Színesen kiírja az állapotnak megfelelő ikont, és utána a szöveget
from time import gmtime, strftime
from colorama import Fore, Style

__log = True

__serverStartTime = strftime("%Y-%m-%d %H:%M:%S ", gmtime())

def getLog():
    return __log

def setLogToFalse():
   __log = False

def writeToLogfile(message):
    with open('log/' + __serverStartTime, 'a', encoding='utf-8') as logf:
        logf.write(message)

def ifLogEnabledThenLog(message):
    if  __log == True:
        writeToLogfile(message) 
    else:
        pass

def time():
    return strftime("[ %Y-%m-%d %H:%M:%S ] ", gmtime())

def errPrint(message):
    print('\n'+ Fore.RED + Style.BRIGHT +
          '[&&&] ' + Style.RESET_ALL + time() + message)

    ifLogEnabledThenLog('\n' + time() + message)

def warnPrint(message):
    print('\n' + Fore.YELLOW + Style.BRIGHT +
          '[*] ' + Style.RESET_ALL + time()+ message)

    ifLogEnabledThenLog('\n' + time() + message)

def okPrint(message):
    print('\n' + Fore.GREEN + Style.BRIGHT +
          '[+] ' + Style.RESET_ALL + time()+ message)

    ifLogEnabledThenLog('\n' + time() + message)

def finePrint(message):
    print('\n' + Fore.BLUE + Style.BRIGHT +
          '[-] ' + Style.RESET_ALL + time()+ message)

    ifLogEnabledThenLog('\n' + time() + message)

def dbPrint(message, newline = True):
    if newline:
        print('\n' + Fore.CYAN + Style.BRIGHT +
                  '[DB] ' + Style.RESET_ALL + time()+ message)
        ifLogEnabledThenLog('\n' + time() + message + '\n')
    else:
        print(Fore.CYAN + Style.BRIGHT +
                '[DB] ' + Style.RESET_ALL + time()+ message)
        ifLogEnabledThenLog(time() + message + '\n')

def startPrint(IpAddress):
    print(Fore.GREEN + Style.BRIGHT +
          '[+] ' + Style.RESET_ALL + time()+ 'Szerver fut: ' + IpAddress)

    ifLogEnabledThenLog(time() + 'Szerver fut: ' + IpAddress)

def startPrintNoIP():
    print(Fore.YELLOW + Style.BRIGHT +
          '[*] ' + Style.RESET_ALL + 'Szerver fut, de nem lehetett IP-címet megállapítani')
    ifLogEnabledThenLog(time() + 'Szerver fut, de nem lehetett IP-címet megállapítani')

def lowPortNumberWarn():
    print(Fore.YELLOW + Style.BRIGHT +
          '[*] ' + Style.RESET_ALL + 'Nem javasolt 1000-nél kisebb portszámot megadni\n')

def gotDataPrint(week, day, subj, mat, pic):
    dayDict = {'0':'Hétfő', '1':'Kedd', '2':'Szerda', '3':'Csütörtök', '4':'Péntek', '5':'Szombat'}
    weekS = '--- Hét: {}'.format(week) 
    try:
        dayS = '--- Nap: {}'.format(dayDict[day]) 
    except KeyError:
        dayS = '--- Nap: {}'.format(day) 
    subjS = '--- Tantárgy: {}'.format(subj) 
    matS = '--- Anyag: {}'.format(mat) 
    picS = '--- Kép: {}'.format(pic) 
    
    print(weekS)
    print(dayS)
    print(subjS)
    print(matS)
    print(picS)

    ifLogEnabledThenLog(weekS + '\n')
    ifLogEnabledThenLog(dayS + '\n')
    ifLogEnabledThenLog(subjS + '\n')
    ifLogEnabledThenLog(matS + '\n')
    ifLogEnabledThenLog(picS + '\n')

# dbIO.py-ban kerül használatra, csak az Id-t írja ki a timestamp-el
def IdPrint(objectId):
    print('--- Id: {}'.format(objectId)) 
    ifLogEnabledThenLog('--- Id: {}'.format(str(objectId) + '\n'))

def notValidPortNumberErr():
    print(Fore.RED + Style.BRIGHT +
          '[&&&] ' + Style.RESET_ALL + 'Portszám csak teljes szám lehet')
