import json
import requests
import numpy as np
import ssl
import pymongo
from pymongo import MongoClient
import webbrowser
from time import sleep
from geopy.geocoders import Nominatim
from urllib.request import urlopen
import json
import math


con = pymongo.MongoClient("mongodb+srv://Maxence:Maxence@cluster0.srkjc.mongodb.net/cluster0?retryWrites=true&w=majority",ssl=True,ssl_cert_reqs=ssl.CERT_NONE)
db = con.test
database=con['stations']
collection = database['vélo']
verif=True
def getRefresh():
    liste_station= []
    urlL= "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion&rows=1000"
    responseL = requests.request("GET",urlL)
    response_jsonL= json.loads(responseL.text.encode('utf8'))
    
    
    for K in response_jsonL['records']:
        for l in range(np.size(K['fields'])) :
            liste_newliste=[]
            liste_newliste.append(K['fields']['nom'])
            liste_newliste.append({"type": "Point", "coordinates":K['fields']['localisation']})
            if K['fields']['etat'] == 'EN SERVICE':
                liste_newliste.append(True)
            else :
                liste_newliste.append(False)
            liste_newliste.append(K['fields']['nbvelosdispo'])
            liste_newliste.append(K['fields']['nbplacesdispo'])
        
            
            #print(liste_newliste)

            liste_station.append(liste_newliste)
    urlS= "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json"
    responseS = requests.request("GET",urlS)
    response_jsonS= json.loads(responseS.text.encode('utf8'))
    
    for i in response_jsonS['values']:
        for j in range (np.size(i)):
            liste_newliste= []
            liste_newliste.append(i['name'])
            loc_liste=[]
            loc_liste.append(i['lat'])
            loc_liste.append(i['lon'])
            liste_newliste.append({"type": "Point", "coordinates":loc_liste})
            if i['etat'] == '':
                liste_newliste.append(True)
            else :
                liste_newliste.append(False)            
            liste_newliste.append(i['available_bikes'])
            liste_newliste.append(i['available_bike_stands'])
            liste_station.append(liste_newliste)
    #remplissage de la bdd
    """for m in range (len(liste_station)):    
       collection.insert_one({"name": liste_station[m][0],"localisation":liste_station[m][1],"State":liste_station[m][2],"Available_bikes":liste_station[m][3],"Available_stands":liste_station[m][4]})           
    #update de la bdd    """
    for i in range (len(liste_station)):
        collection.update_one(
                { "name": liste_station[i][0]},
                { "$set":
                 {
                 "localisation": liste_station[i][1],
                 "State":liste_station[i][2],
                 "Available_bikes":liste_station[i][3],
                 "Available_stands":liste_station[i][4]
                 }
                } 
                
            )
    return response_jsonS.get("records",[])

def getSearch():
    lat = input("donner la lattitude : ")
    long = input("donner la longitude : ")
    try :
        lat= float(lat)
        long= float(long)
        doc = collection.find({'localisation': { "$near": {"$geometry": {"type": "Point" ,"coordinates": [ lat, long ]},"$maxDistance": 300,"$minDistance": 0}}})
        print(list(doc))
    except:
        error = input("Erreur value, Rentrez Oui pour rééssayer")
        if (error=="Oui"):
            getSearch()
        else:
            getInit()

def UpDelete():
  choice = input("Voulez-vous rafraîchir (U) une station ou la détruire (D) ? (Quitter = Q)")
  if (choice=="D"):
      choiceStation= input("Quelle station choisissez-vous?")
      getUpDelete(False, choiceStation)
  elif (choice== "U"):
        choiceStation= input("Quelle station choisissez-vous?")
        getUpDelete(True, choiceStation)
  elif (choice== "Q"):
        getInit()     
  else:
      print("Mauvaise réponse réésayer")
      UpDelete()
        

def getUpDelete(boolean, name):
    liste_station= []
    const= 0
    urlL= "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion&rows=1000"
    responseL = requests.request("GET",urlL)
    response_jsonL= json.loads(responseL.text.encode('utf8'))
    
    
    for K in response_jsonL['records']:
        for l in range(np.size(K['fields'])) :
            liste_newliste=[]
            liste_newliste.append(K['fields']['nom'])
            liste_newliste.append({"type": "Point", "coordinates":K['fields']['localisation']})
            if K['fields']['etat'] == 'EN SERVICE':
                liste_newliste.append(True)
            else :
                liste_newliste.append(False)
            liste_newliste.append(K['fields']['nbvelosdispo'])
            liste_newliste.append(K['fields']['nbplacesdispo'])
        
            
            #print(liste_newliste)

            liste_station.append(liste_newliste)
    urlS= "https://download.data.grandlyon.com/ws/rdata/jcd_jcdecaux.jcdvelov/all.json"
    responseS = requests.request("GET",urlS)
    response_jsonS= json.loads(responseS.text.encode('utf8'))
    
    for i in response_jsonS['values']:
        for j in range (np.size(i)):
            liste_newliste= []
            liste_newliste.append(i['name'])
            loc_liste=[]
            loc_liste.append(i['lat'])
            loc_liste.append(i['lon'])
            liste_newliste.append({"type": "Point", "coordinates":loc_liste})
            if i['etat'] == '':
                liste_newliste.append(True)
            else :
                liste_newliste.append(False)            
            liste_newliste.append(i['available_bikes'])
            liste_newliste.append(i['available_bike_stands'])
            liste_station.append(liste_newliste)
    if(boolean==True):
        for i in range (len(liste_station)):
            if (liste_station[i][1]== name):
                const=i
                i=len(liste_station)
        doc = collection.find_one_and_update(
            {"name" : name},
            { '$set':{
                "localisation": liste_station[i][1],
                 "State":liste_station[i][2],
                 "Available_bikes":liste_station[i][3],
                 "Available_stands":liste_station[i][4]
                }})
        print("Station update")
    else:
         for i in range (len(liste_station)):
            if (liste_station[i][1]== name):
                const=i
                i=len(liste_station)
         doc = collection.find_one_and_delete(
            {"name" : name})
         print("Station détruite. (Attention celle ci sera rajouter à chaque refresh)")
def getInit():
    
     dispach= input("Que voulez vous faire : Refresh la BDD (R), Update ou Delete une station (UD), Trouver une station proche (T) : ")
     if(dispach=="R"):
         getRefresh()
     elif(dispach=="UD"):
         UpDelete()
     elif(dispach=="T"):
         getSearch()
     else:
         print("mauvaise commande")
        
def getSearchStation():
    choice = input("Recherche station : ")
    doc = collection.find({"name" : {"$regex": choice}})
    print (list(doc))
    

while (verif):
    i=30
    getRefresh()
    getInit()
    quit = input("Tapez Oui pour quitter! : ")
    if (quit=="Oui"):
        i=3
        verif=False
    sleep(i)
