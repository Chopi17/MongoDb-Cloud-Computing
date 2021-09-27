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
            #print(liste_newliste)
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
    doc = collection.find({'localisation': { "$near": {"$geometry": {"type": "Point" ,"coordinates": [ 50.634512, 3.049339 ]},"$maxDistance": 300,"$minDistance": 0}}})
    print(list(doc))

def UpDelete():
  choice = input("Voulez-vous rafraîchir (U) une station ou la détruire (D)?")
  if (choice== "U"):
        choiceStation= input("Quelle station choisissez-vous?")
        #collection.find{}
  """ collection.update_one(
                { "name": choiceStation},
                { "$set":
                 {
                 "localisation": liste_station[i][1],
                 "State":liste_station[i][2],
                 "Available_bikes":liste_station[i][3],
                 "Available_stands":liste_station[i][4]
                 }
                }
        )   """       
def getInit():
     getRefresh()
def getSearchStation():
    choice = input("Recherche station : ")
    doc = collection.find({"name" : {"$regex": choice}})
    print (list(doc))
    
getInit()
getSearchStation()
getSearch()
"""while True:
    getInit()
    sleep(300)"""
