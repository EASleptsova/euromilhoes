import random
import datetime
import mysql.connector
import collections
import sys
'''
Class para gerar chaves
'''
class Chave:
    
    def __init__(self):
        self.numeros=[]
        self.estrelas=[]
        self.getChave()
'''
Função para gerar uma chave
'''
    def getChave(self):
        count=0
        while count<5:            
            exists=False
            #variavel n pode ser de 1 até 50
            n=10
            numero=int(random.random()*n+1)
            for i in self.numeros:
                if numero==i:
                    exists=True
                    break
            if exists == False:        
                self.numeros.append(numero)
                count=count+1                
        count=0
        while count<2:
            exists=False
            #variavel estrs pode ser de 1 até 12
            estrs=4
            numero=int(random.random()*estrs+1)
            for i in self.estrelas:
                if numero==i:
                    exists=True
                    break
            if exists == False:        
                self.estrelas.append(numero)
                count=count+1        
'''
Class para gerar sorteios
'''                    
class Sorteio:
    
    def __init__(self):
        self.chave=Chave()        
        self.data=datetime.datetime.now()
        #get last name from database
        self.getNameOfSorteiro() 
        print("Sorteio "+str(self.nomeSorteio)+" de dia: "+
              self.data.strftime("%Y-%m-%d %H:%M"))       
        print(self.chave.numeros, end=" 5 numeros ")
        print(self.chave.estrelas, end=" 2 estrelas\n\n")
        #save sorteiro in db
        self.insert_sorteiro()
       
    def insert_sorteiro(self):
        db=DBconnection()
        numeros=' '.join(str(b) for b in self.chave.numeros)
        estrelas=' '.join(str(e) for e in self.chave.estrelas)
        chave=numeros+" "+estrelas
        db.mycursor.execute("insert into sorteios (name, data, chave) values ( "+
                            str(self.nomeSorteio)+" , '"+str(self.data)+"' , '" + chave+"')" )
        db.mydb.commit()        
        db.close()
        
    def getNameOfSorteiro(self):
        db=DBconnection()        
        sql = "select name from sorteios order by id desc limit 1"       
        db.mycursor.execute(sql)
        myresult = db.mycursor.fetchall()        
        self.nomeSorteio=1
        #incrementa nome do Sorteio
        for x in myresult:                      
                self.nomeSorteio=x[0]+1                                               
        db.close()        
'''
Class para gerar bilhetes
'''                                   
class Bilhete:    
    def __init__(self):
        #get nome do último sorteiro
        self.getNameOfSorteiro()        
        self.chave=Chave()
        self.insert_bilhete()

    def insert_bilhete(self):
        db=DBconnection()
        numeros=' '.join(str(b) for b in self.chave.numeros)
        estrelas=' '.join(str(e) for e in self.chave.estrelas)
        self.chaveMysql=numeros+" "+estrelas              
        db.mycursor.execute("insert into bilhetes (name, chave) values ( "+str(self.nomeSorteio)+" , '"+self.chaveMysql+"')" )
        db.mydb.commit()        
        db.close()
        
    def getNameOfSorteiro(self):
        db=DBconnection()        
        sql = "select name from sorteios order by id desc limit 1"       
        db.mycursor.execute(sql)
        myresult = db.mycursor.fetchall()
        self.nomeSorteio=1  
        for x in myresult:            
                self.nomeSorteio=x[0]+1                                     
        db.close()
    #get id  do bilhete que ganhou  
    def getid(self):
        db=DBconnection()
        id=0
        sql = "select id from bilhetes where name=" + str(self.nomeSorteio) +
        " and chave='"+ self.chaveMysql+ "'"        
        db.mycursor.execute(sql)
        myresult = db.mycursor.fetchall()
        for x in myresult:
           self.id=x[0]           
        db.close()        
        return self.id
'''
Class para criar e usar database connection
'''        
class DBconnection :
    def __init__(self):
        
        self.mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345678",
        database="euromilhoes"
        )
        self.mycursor = self.mydb.cursor()
        
    def close(self):
        self.mydb.close()

'''
função para mostrar estatisticas dos números
'''
def mostra_estatisticas():

    db=DBconnection()
    sorteios=[]
    #receber todas as chaves dos sorteios
    sql = "select chave from sorteios"       
    db.mycursor.execute(sql)
    myresult = db.mycursor.fetchall()
    for x in myresult:
        sorteio=[int(s) for s in x[0].split(' ')]
        sorteios.append(sorteio)         
    db.close()
    print("\n***Estatistica***\nTotal sorteios " + str(len(sorteios)))

    numeros = []
    estrelas = []
    #parse strings to lists numeros and estrelas
    for s in sorteios:
        numeros.append(s[0:5])
        estrelas.append(s[5:])  
    numSaidas=[]
    #número n pode variar de 1 até 51
    n=11
    for i in range (1,n):
        #count - quantas vezes apareceu um número
        count=0
        for n in numeros:        
            if i in n:
                count+=1
        numSaidas.append(count)
        #calcular percentagem
        percent=count/len(sorteios)*100
        print("Numero " + str(i) + " saiu " + str(count)+
              " vez(es), % saidas " + "%.2f" % percent, end="\n")
    numSaidas=[]
    print()
    # número estrs pode variar de 1 até 13
    estrs=5
    for i in range (1,estrs):
        count=0
        for e in estrelas:        
            if i in e:
                count+=1
        numSaidas.append(count)
        percent=count/len(sorteios)*100
        print("Estrela " + str(i) + " saiu " + str(count)+
              " vez(es), % saidas " + "%.2f" % percent, end="\n")

'''
função para mostrar todos os sorteios
'''        
def listar_sorteios():
    print()
    db=DBconnection()
    sorteios=[]
    sql = "select chave from sorteios"       
    db.mycursor.execute(sql)
    myresult = db.mycursor.fetchall()
    for x in myresult:
        sorteio=[int(s) for s in x[0].split(' ')]
        sorteios.append(sorteio)         
    db.close()
    print("\nTotal sorteios " + str(len(sorteios)))
    numeros = []
    estrelas = []
    #parse strings to lists
    for s in sorteios:
        print("Numeros: " + str(s[0:5]) + " estrelas: "+ str(s[5:]))
        numeros.append(s[0:5])
        estrelas.append(s[5:])

'''
função para jogar(criar os bilhetes e um sorteio novo)
'''         
def gerar_novo_sorteio():
    numBilhetes= input("\nQuantas bilhetes gerar? ")
    try:
        numBilhetes = int(numBilhetes)
    except ValueError:
        print("Número invalido! Tenta outra vez", end="\n")
        return
    bilhetes=[]
    #criar bilhetes  
    for i in range(numBilhetes):
        bilhete=Bilhete()    
        bilhetes.append(bilhete)
           
    s=Sorteio()
    print("Os resultados: " , end="\n")
    #verifica se alguem ganhou
    count=0
    ids=[]
    for b in bilhetes:
        if b.nomeSorteio ==s.nomeSorteio:
            if (collections.Counter(b.chave.numeros) == collections.Counter(s.chave.numeros))\
            and (collections.Counter(b.chave.estrelas) == collections.Counter(s.chave.estrelas)):             
                count+=1
                #get id dos bilhetes            
                ids.append(b.getid())
    if count == 0:
        print("Ninguem ganhou", end="\n")
    else:
        print(f"{count} bilhete(s) ganhou! Id dos bilhetes: ")
        print(ids)
        print("*****************************************")
    return    
    
def mostra_menu():   
    print("\n1. listar todos os sorteios", end=" \n")
    print("2. crirar um sorteio novo e gerar as chaves", end=" \n")
    print("3. mostrar estatisticas dos números", end=" \n")
    print("4. sair do programa", end=" \n")

'''
função para sair do programa
''' 
def sair():
    sys.exit()
    
'''
main program
'''
while True:
    mostra_menu()
    escolha= input("Escreve opção (1-4): ")
    try:
        escolha = int(escolha)
    except ValueError:
        print("Escolha invalida! Tenta outra vez", end="\n")
    if escolha== 1:
        listar_sorteios()
    elif escolha== 2:
        gerar_novo_sorteio()
    elif escolha== 3:
        mostra_estatisticas()
    elif escolha== 4:
        sair()
    else:
        print("Escolha invalida! Tenta outra vez", end="\n")

    
    





   

    

        



   


