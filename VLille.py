import json
import requests
import numpy as np

def getVelo():
    urlL= "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion&rows=1000"
    responseL = requests.request("GET",urlL)
    response_jsonL= json.loads(responseL.text.encode('utf8'))
    
    liste_station= []
    for K in response_jsonL['records']:
        for l in range(np.size(K['fields'])) :
            liste_newliste=[]
            liste_newliste.append(K['fields']['nom'])
            liste_newliste.append(K['fields']['localisation'])
            if K['fields']['etat'] == 'EN SERVICE':
                liste_newliste.append(True)
            else :
                liste_newliste.append(False)
            
        
            
            taille = K['fields']['nbvelosdispo'] + K['fields']['nbplacesdispo']
            #if taille ==0:
             #   print(liste_newliste)
            
            liste_newliste.append(taille)
            liste_station.append(liste_newliste)
    print(liste_station)
    urlS= "https://velib-metropole-opendata.smoove.pro/opendata/Velib_Metropole/station_information.json"
    responseS = requests.request("GET",urlS)
    response_jsonS= json.loads(responseS.text.encode('utf8'))
    
    for i in response_jsonS['data']['stations']:
        for j in range (np.size(i)):
            liste_newliste= []
            liste_newliste.append(i['name'])
            loc_liste=[]
            loc_liste.append(i['lat'])
            loc_liste.append(i['lon'])
            liste_newliste.append(loc_liste)
            liste_newliste.append(True)
            liste_newliste.append(i['capacity'])
            liste_station.append(liste_newliste)
            
    print (liste_station)
    
    return response_jsonS.get("records",[])


getVelo()
