from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes
import requests;
import time
#queste due sono librerie già inglobate in python
import os;
import json 
import random
from telegram.constants import ParseMode

# mi creo un dizionario di coppie squadre id, perchè la richiesta la posso fare solo con l'id della squadra
teams_dict = { "Inter": 505,
         "Milan": 489,
         "Juventus": 496,
         "Atalanta": 499,
         "Bologna": 500,
         "Roma": 497,
         "Lazio": 487,
         "Fiorentina": 502,
         "Torino": 503,
         "Napoli": 492,
         "Genoa": 495,
         "Monza": 1579,
         "Verona": 504,
         "Lecce": 867,
         "Udinese": 494,
         "Cagliari": 490,
         "Empoli": 511,
         "Frosinone": 512,
         "Sassuolo": 488,
         "Salernitana": 514
  }


async def info_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   message = "Command list: \n \
               - /analyze \n  To analyze and match predict Serie A standings from 2010 to 2023 \n \
               - /analyze \"year\" \n To analyze and match predict Serie A standing of the year \n \
               - /predict \"year\" \"team\" \n To predict position of a Serie A team with random stats \n \
               - /predict \"year\" \"gf\" \"gs\" \"win\" \"draw\" \"lose\" \n To predict position of a Serie A team with some stats "
   await update.message.reply_text(message)


#per analizzare e fare predizioni dal 2011 al 2023
async def total_analyze_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
   global teams_dict

   payload={}
   headers = {
    'x-rapidapi-key': str(os.environ["API-KEY"]),
    'x-rapidapi-host':  'v3.football.api-sports.io'
   }

   message = update.message.text
   words = message.split()
   year = None
   
   if(len(words) == 2):
      year = words[1]
   # if (words[1]!="Bundesliga"):
   #    word = words[1]+" "+words[2] # team = words[3] 
   # else:
    #   word = words[1]
      # team = words[2]

   
   # id_team = teams_dict[team]

   id = 135
   #word = word.strip()
  
   # if(word=="Serie A"):
   #    id=135
   # elif (word=="Ligue 1"):
   #    id=61
   # elif(word=="Premier League"):
   #    id=39
   # elif(word=="Bundesliga"):
   #    id=78
   # elif(word=="La Liga"):
   #    id=140
   # else:
   #    await update.message.reply_text("Input League Error. Insert Serie A ")
   #   return
 
 
    #url = "https://v3.football.api-sports.io/standings?league=135&season=202"

   if(year is None): 
      for i in range(2011,2024):
         if i != 2011:
            time.sleep(5)  #tra una richiesta e l\"altra si ferma 6 secondi
 
         url = str(os.environ["URL"])+"league="+str(id)+"&season="+str(i)
         #+"&team="+str(id_team)
         response = requests.request("GET", url, headers=headers, data=payload)

         json_object = json.loads(response.text)  #questo lo devo inviare a logstash
         r = requests.request("POST",url='http://10.0.100.22:8080',json=json_object)  #indirizzo ip di logstash nella rete dei container

         if i == 2023:
            await update.message.reply_text("Result elaborated. See it on http://localhost:5601")
         else:
            await update.message.reply_text("Elaborating...")
   else:
      url = str(os.environ["URL"])+"league="+str(id)+"&season="+str(year)
      #+"&team="+str(id_team)
      response = requests.request("GET", url, headers=headers, data=payload)

      json_object = json.loads(response.text)  #questo lo devo inviare a logstash
      r = requests.request("POST",url="http://10.0.100.22:8080",json=json_object)  #indirizzo ip di logstash nella rete dei container

   
      await update.message.reply_text("Result elaborated. See it on http://localhost:5601")
   

   message = ""
   url = ""


async def predict_random_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

       #devo creare un json come quello che arriva a kafka e e su quello lavorerà spark 
       #lì mi arriva testo e lo faccio in json con load e lo mando a logstash 
      global teams_dict 

      message = update.message.text     #il messaggio  è predict nomeSquadra anno(\"points\" \"gf\" \"gs\" \"win\" \"draw\" \"lose\")
      words = message.split()
      
      team=year=points=win=lose=draw=gol_for=gol_against =  None
 
      if(len(words)< 3 or (len(words)>3 and len(words)!= 8) or(len(words) > 8)):
         await update.message.reply_text("Error in the parameters. Type /info for help ")
         return
      elif(len(words) == 3):
         team =  words[1]
         year = words[2]

        
         while True:
            win = random.randrange(0,39)  #per essere sicuro che il numero di partite perse, vinte  o pareggiato sia 38
            lose = random.randrange(0,39)
            draw = random.randrange(0,39)
            if (win+lose+draw == 38):
               break
      
         gol_for = random.randrange(10,100)
         gol_against = random.randrange(0,100)
         points = win*3+draw*1

      else:
         team =  words[1]
         year = words[2]
         gol_for = words[3]
         gol_against = words[4]
         win = words[5]
         lose = words[6]
         draw = words[7]
         points = int(win)*3+int(draw)*1
      
       #mi creo quindi una stringa con dati random e lo trasformo in json e glielo mando 
      response = "{    \
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

      json_object = json.loads(response)  #questo lo devo inviare a logstash
      r = requests.request("POST",url="http://10.0.100.22:8080",json=json_object)  #indirizzo ip di logstash nella rete dei container

   
      await update.message.reply_text(" Result elaborated. See it on <a href='https://localhost:5601'> kibana </a> ",parse_mode = ParseMode.HTML)
   




token = os.environ["TOKEN"]    #token api telegram bot
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("analyze",total_analyze_function))
app.add_handler(CommandHandler("info",info_function))
app.add_handler(CommandHandler("predict",predict_random_function))
app.run_polling()

