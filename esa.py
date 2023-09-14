class ExamException(Exception):
    pass




class CSVTimeSeriesFile:
    #controllo che il nome del file sia una stringa 
    def __init__(self, name):
        if not isinstance(name,str):
            raise ExamException('la variabile name dell\'oggetto non è una stringa')
        self.name = name

        
    def get_data(self):
        #controllo che non ci siano errori in apertura o lettura del file
        try:
            file = open(self.name,'r')
            file.readline()
        except:
            raise ExamException('c\'è stato un problema in apertura o lettura del file')

        #leggo il file riga per riga
        valori = []
        data_precedente = None
        for i,line in enumerate(file):
            colonne = line.split(',') 
            #se non ho due elementi, passo oltre
            if len(colonne) < 2:
                continue
            #converto i valori in int e mi assicuro che siano positivi
            try:
                value = int(colonne[1].strip())
            except:
                continue
            if value <= 0 :
                continue

            #controllo di star lavorando con una data e separo tra mesi e anni trasformati in int
            data = colonne[0]
            try:
                mese = int(data.split('-')[1])
                anno = int(data.split('-')[0])   
            except:
                continue
            if mese not in range (1,13) :
                    continue    
        
            #controllo che anni e mesi siano ordinati
            if data_precedente is not None :
                if anno - int(data_precedente.split('-')[0]) < 0 :
                    raise ExamException ('non devono esserci anni disordinati')
                if anno - int(data_precedente.split('-')[0]) == 0:
                    if mese - int(data_precedente.split('-')[1]) <= 0 :
                        raise ExamException('non devono esserci mesi uguali o disordinati')
                

            data_precedente = data
            valori.append([data, value])

        file.close()
        return valori


def detect_similar_monthly_variations(time_series, years):
    
    if abs(years[0] - years[1]) != 1 :
        raise ExamException ('gli anni dati in input non sono consecutivi')
        
    #inizializzo gli anni dati in input come 12 None
    anno1 = [None for i in range (12)]
    anno2 = [None for i in range (12)]
   
    #scorro il file e inserisco i valori di ogni mese in anno1 e anno2
    for line in time_series :
        anno = int(line[0].split('-')[0])
        mese = int(line[0].split('-')[1])
        
        if anno == years[0]:
            anno1[mese-1] = line[1]
        if anno == years[1]:
            anno2[mese-1] = line[1]

    #controllo di avere i dati degli anni richiesti
    a1valido = False  
    a2valido = False
    for i in range (12):      
        if anno1[i] is not None :
            a1valido = True
        if anno2[i] is not None :
            a2valido = True

    if a1valido is False or a2valido is False :
        raise ExamException('manca un anno intero')

    #controllo che siano quasi uguali
    lista = []
    for i in range (11):
        try:
            lista.append(abs(abs(anno1[i] - anno1[i+1]) - abs(anno2[i] - anno2[i+1])) <= 2) 
        except:
            lista.append(False)      

    return lista
