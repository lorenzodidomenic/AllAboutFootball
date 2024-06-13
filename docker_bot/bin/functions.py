import requests;
import time

import os;

import json;
from var import LOGSTASH_URL
#funzione che prende da Footbal-api e manda a logstash
def requests_function(url):

   payload={}
   headers = {
    'x-rapidapi-key': str(os.environ["API-KEY"]),
    'x-rapidapi-host':  'v3.football.api-sports.io'
   }

   response = requests.request("GET", url, headers=headers, data=payload)
   json_object = json.loads(response.text)  #questo lo devo inviare a logstash
   r = requests.request("POST",url=LOGSTASH_URL,json=json_object)  

#funzione che mi genera un json da certi parametri
def generate_json(year,team,points,win,draw,lose,gol_for,gol_against):
   response =  "{    \
                \"parameters\": { \
                     \"season\": \" " + year +" \" \
                  }, \
                 \"response\": [ \
                 {    \
               \"league\": {  \
                \"standings\": [  \
                    [    \
                        {     \
                            \"rank\": "+str(0)+",  \
                            \"team\": {     \
                                \"name\": \"" + team + "\" \
                            }, \
                            \"points\": " + str(points) + ", \
                            \"all\": { \
                                \"played\": 38,\
                                \"win\":" + str(win)+",  \
                                \"draw\":"+ str(draw)+",   \
                                \"lose\":"+ str(lose)+",    \
                                \"goals\": {    \
                                    \"for\": " + str(gol_for) +",   \
                                    \"against\":" + str(gol_against)+"  \
                                }  \
                            }   \
                           } ]]\
                           } \
                           } ] \
                        }"
   return response
         

