# -*- coding: utf-8 -*-

# Színesen kiírja az állapotnak megfelelő ikont, és utána a szöveget
from time import gmtime, strftime
from colorama import Fore, Style

class colorPrint:

    __log = True

    __serverStartTime = strftime("%Y-%m-%d %H:%M:%S ", gmtime())
    
    def getLog(self):
        return self.__log

    def setLogToFalse(self):
       self.__log = False

    def writeToLogfile(self, message):
        with open('log/' + self.__serverStartTime, 'a', encoding='utf-8') as logf:
            logf.write(message)

    def ifLogEnabledThenLog(self, message):
        if self. __log == True:
            self.writeToLogfile(message) 
        else:
            pass

    def time(self):
        return strftime("[ %Y-%m-%d %H:%M:%S ] ", gmtime())

    def errPrint(self, message):
        print('\n'+ Fore.RED + Style.BRIGHT +
              '[&&&] ' + Style.RESET_ALL + self.time() + message)

        self.ifLogEnabledThenLog('\n' + self.time() + message)

    def warnPrint(self, message):
        print('\n' + Fore.YELLOW + Style.BRIGHT +
              '[*] ' + Style.RESET_ALL + self.time()+ message)

        self.ifLogEnabledThenLog('\n' + self.time() + message)

    def okPrint(self, message):
        print('\n' + Fore.GREEN + Style.BRIGHT +
              '[+] ' + Style.RESET_ALL + self.time()+ message)

        self.ifLogEnabledThenLog('\n' + self.time() + message)

    def finePrint(self, message):
        print('\n' + Fore.BLUE + Style.BRIGHT +
              '[-] ' + Style.RESET_ALL + self.time()+ message)

        self.ifLogEnabledThenLog('\n' + self.time() + message)

    def dbPrint(self, message, newline = True):
        if newline:
            print('\n' + Fore.CYAN + Style.BRIGHT +
                      '[DB] ' + Style.RESET_ALL + self.time()+ message)
            self.ifLogEnabledThenLog('\n' + self.time() + message + '\n')
        else:
            print(Fore.CYAN + Style.BRIGHT +
                    '[DB] ' + Style.RESET_ALL + self.time()+ message)
            self.ifLogEnabledThenLog(self.time() + message + '\n')

    def startPrint(self, IpAddress):
        print(Fore.GREEN + Style.BRIGHT +
              '[+] ' + Style.RESET_ALL + self.time()+ 'Szerver fut: ' + IpAddress)

        self.ifLogEnabledThenLog(self.time() + 'Szerver fut: ' + IpAddress)

    def startPrintNoIP(self):
        print(Fore.YELLOW + Style.BRIGHT +
              '[*] ' + Style.RESET_ALL + 'Szerver fut, de nem lehetett IP-címet megállapítani')
        self.ifLogEnabledThenLog(self.time() + 'Szerver fut, de nem lehetett IP-címet megállapítani')

    def lowPortNumberWarn(self):
        print(Fore.YELLOW + Style.BRIGHT +
              '[*] ' + Style.RESET_ALL + 'Nem javasolt 1000-nél kisebb portszámot megadni\n')

    def gotDataPrint(self, week, day, subj, mat, pic):
        weekS = '--- Hét: {}'.format(week) 
        dayS = '--- Nap: {}'.format(day) 
        subjS = '--- Tantárgy: {}'.format(subj) 
        matS = '--- Anyag: {}'.format(mat) 
        picS = '--- Kép: {}'.format(pic) 
        
        print(weekS)
        print(dayS)
        print(subjS)
        print(matS)
        print(picS)

        self.ifLogEnabledThenLog(weekS + '\n')
        self.ifLogEnabledThenLog(dayS + '\n')
        self.ifLogEnabledThenLog(subjS + '\n')
        self.ifLogEnabledThenLog(matS + '\n')
        self.ifLogEnabledThenLog(picS + '\n')

    # dbIO.py-ban kerül használatra, csak az Id-t írja ki a timestamp-el
    def IdPrint(self, objectId):
        print('--- Id: {}'.format(objectId)) 
        self.ifLogEnabledThenLog('--- Id: {}'.format(str(objectId) + '\n'))

    def notValidPortNumberErr(self):
        print(Fore.RED + Style.BRIGHT +
              '[&&&] ' + Style.RESET_ALL + 'Portszám csak teljes szám lehet')
