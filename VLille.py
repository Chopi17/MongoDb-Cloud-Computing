import json
import requests

def getVlille():
    url= "https://opendata.lillemetropole.fr/api/records/1.0/search/?dataset=vlille-realtime&q=&facet=libelle&facet=nom&facet=commune&facet=etat&facet=type&facet=etatconnexion"
    response = requests.request("GET",url)
    response_json= json.loads(response.test.encode('utf8'))
    return response_json.get("records",[])
