import string,time,pdb,itertools,time
import Tkinter as tk
#import sys #Serve per sys.setrecursionlimit(numero>1000)

#>http://stackoverflow.com/questions/4140437/python-tkinter-interactively-validating-entry-widget-content/4140988#4140988

   
#NB: Le cinque variabili globali(tranne start) sono usate solo nella funzione dictionaryCheck. Devono veramente essere globali?
global dictionary,italianDictionary,validWords,validCoordinates,gameToAnalyze
    
###GIOCO DA ANALIZZARE
gameToAnalyze=[['c','o','c','p'],['i','n','i','a'],['a','e','g','v'],['f','c','s','i']]
#357 parole TOTALI(dizionario Ruzzle) vs 291 parole ruzzleSolver
###FINE GIOCO DA ANALIZZARE

dictionary={}
italianDictionary={}
validWords=[]
validCoordinates=[]
#gameToAnalyze=[['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]


#Funzione che vaglia le possibili caselle vicine e scarta quelle inesistenti,
#ad esempio quelle con x e/o y minori di zero e/o maggiori di 3

def checkCellsWithinBounds(row,col):
    tempCellsWithinBounds=list()
    for x in [-1,0,1]:
        for y in [-1,0,1]:
            tempCellsWithinBounds.append([row+x,col+y])
    tempCellsWithinBounds.remove([row,col]) #Rimuovo la cella con le stesse coordinate della cella iniziale, per non creare loop
    
    #Scarto le celle fuori dai confini della tavola
    correctCellsWithinBounds=list()
    for cell in tempCellsWithinBounds:
        if (0<=cell[0]<=3) and (0<=cell[1]<=3):
            correctCellsWithinBounds.append(cell)
    correctCellsWithinBounds.sort()
    return correctCellsWithinBounds


#Funzione che scarta le celle da cui sono gia' passato
#NB: Possono esserci delle liste vuote alla fine del processo

def checkCellsWithinBoundsFromWhomIDidNotPass(cellsWithinBounds, cellsAlreadyProcessed):
    #cellsAlreadyProcessed.sort() <-PORCO DIO MAI PIU'
    cellsToProcess=list()
    for cell in cellsWithinBounds:
        if not (cell in cellsAlreadyProcessed):
            cellsToProcess.append(cell) #Aggiungo a cellsToProcess le celle da cui non sono passato
    return cellsToProcess


#Funzione che si occupa di effettuare la ricerca nel dizionario delle parole

def dictionaryCheck(cellIAmNowAnalyzing,cellsToFormWord):
#        #Controllo if per evitare che cellIAmNowAnalyzing non sia gia' presente nella lista.
#        #Mi serve solo per debuggare, visto che non si da' il caso in cui si entra nell'else
#        if cellsToFormWord[(len(cellsToFormWord)-1)]!=cellIAmNowAnalyzing:
#            cellsToFormWord.append(cellIAmNowAnalyzing)
#        else:
#            return -1 # -1 corrisponde a cella non valida
    
    #wordToCheck e' una stringa(trasformata da una lista e "mergiata") contenente
    #le lettere del gioco a cui corrispondono le coordinate passate come parametro da cellsToFormWord
    wordToCheck=''.join([gameToAnalyze[x[0]][x[1]] for x in cellsToFormWord])
    
    if wordToCheck in italianDictionary:
        if not (wordToCheck in validWords):
            validWords.append(wordToCheck)
            validCoordinates.append([entryList[couple[0]][couple[1]] for couple in cellsToFormWord])
                        
    if wordToCheck in dictionary:
        return 1
    elif not wordToCheck in dictionary:
        return 0


#Funzione che si occupa della ricorsione, e che e' l'unica ad essere chiamata da main()

def startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord):
    evaluableCells=checkCellsWithinBoundsFromWhomIDidNotPass(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)
    if len(evaluableCells)!=0:
        for cellToProcess in evaluableCells:
            cellsAlreadyProcessedAndToFormWord.append(cellToProcess)
            
            #Questo mi porta a sapere se il mio inizio di parola avra' seguiti oppure dovro' fare backtracking
            dictionaryMatch=dictionaryCheck(cellToProcess,cellsAlreadyProcessedAndToFormWord)
            if dictionaryMatch>0: #uguale a if dictionaryMatch and dictionaryMatch!=-1
                cellsWithinBounds=checkCellsWithinBounds(cellToProcess[0],cellToProcess[1])
                startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)
                
            elif dictionaryMatch==0:
                #Cancello l'ultimo elemento(alias lettera), ovvero quello con cui nessuna parola inizia
                del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]
    else:
        del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]
        return 
    del cellsAlreadyProcessedAndToFormWord[(len(cellsAlreadyProcessedAndToFormWord)-1)]


def main():
    global validCoordinates,validWords #Mannaggia alla madonna non si puo' togliere    
    f=open("ruzzleFinalWordListWithCommas.txt","r")
    for line in f.read().split(','):
        italianDictionary[line]=True
        l=len(line)+1
        for i in range(1,l):
            dictionary[line[:i]]=True #Nel dizionario ci sono le parole più tutti gli inizi di parola, da len=1 a len=len-1
    f.close()

    ###Inizio algoritmo vero e proprio###
    
    start=time.time()
    for mainRow in range(4):
        for mainCol in range(4):
            cellsWithinBounds=checkCellsWithinBounds(mainRow,mainCol)
            cellsAlreadyProcessedAndToFormWord=[[mainRow,mainCol]] #La lista delle celle gia' valutate e formanti la parola deve contenere la cella stessa
            startProcess(cellsWithinBounds,cellsAlreadyProcessedAndToFormWord)

    #Inverto validWords (validCoordinates lo inverto direttamente nel return)
    validWords=sorted(validWords,key=len,reverse=True)

    end=time.time()-start
    return sorted(validCoordinates,key=len,reverse=True)
    #print "In %f secondi, si e' trovato che:\n a)Il gioco ha %d soluzioni, le quali sono(ordinate secondo le piu' lunghe):"%(end,len(validWords))
    #for x in validWords:
        #print x+',',


####################################
############TKINTER#################
####################################


def solveGame():
    for x in range(4):
        for y in range(4):
            #gameToAnalyze[x][y]=(entryList[x][y].get().lower())
            entryList[x][y].insert(0,gameToAnalyze[x][y])
    entriesToColour=main()
        
    allEntries=itertools.chain(entriesToColour)
    divideListToColour(allEntries)
    
def changebg(listOfAllEntries):
    listOfAllEntries = iter(listOfAllEntries) #Permetto di passare una lista come argomento di changebg
    entry = next(listOfAllEntries,None)
    if entry is not None:
        entry['bg']='yellow'
        root.after(100,lambda : changebg(listOfAllEntries))
    else:
        return entry

def divideListToColour(setOfAllEntries):
    listToSplit=next(setOfAllEntries,None)
    if listToSplit is not None:
        print changebg(listToSplit)
    
        #changebg(listToSplit,0,'white')
        
        #root.after(1000,lambda : divideListToColour(setOfAllEntries))
    #FINE TUTTI A CASA
        
def newgame():
    #gameToAnalyze=[['0','0','0','0'],['0','0','0','0'],['0','0','0','0'],['0','0','0','0']]
    for x in range(4):
        for y in range(4):
            entryList[x][y].delete(0)
    ###
    entryList[0][0].focus_set()

def validate(string):
    try:root.focus_get().insert(0,string.upper())
    except: root.focus_get().insert(0,'')
    nextBox()

def nextBox():
    for row in range(4):
        try: #Cerco la tk.Entry in tutte e 4 le righe. Restituisce sempre 3 ValueError, tranne la volta in cui trova la riga giusta
            column=entryList[row].index(root.focus_get())
            entryList[row][column+1].focus_set()
        except ValueError: pass
        except IndexError:
            if row<3:
                #Vado alla riga successiva, nella prima casella(column=0)
                entryList[row+1][0].focus_set()
                return
root = tk.Tk()
root.option_add("*Entry.Font","Arial 32 bold")

emptyLabel=tk.Label()
emptyLabel.grid(row=4)
entryList=[]

vcmd=(root.register(validate),'%S')
for x in range(4):
    entryList.append([])
    for y in range(4):
        entryList[x].append('')
        entryList[x][y]=tk.Entry(root, bg="white",width=2,justify="center",
                                 takefocus=True,insertofftime=True,
                                 validate="key",validatecommand=vcmd)
        entryList[x][y].grid(row=x,column=y)

solvebt=tk.Button(root,text='Risolvi',command=solveGame).grid(row=5,column=2)
newgamebt=tk.Button(root,text='Nuovo',command=newgame).grid(row=5,column=1)

entryList[0][0].focus_set()

root.mainloop()














