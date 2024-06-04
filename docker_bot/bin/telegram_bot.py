from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes
import requests;
import time
#queste due sono librerie già inglobate in python
import os;
import json 

#o punteggio dell'anno successivo o correlazione lineare tra gol fatti e posizione(vedo se c'è correlazione e posso predire punteggio in base ai gol fatti)

#il bot ad una richiesta dell'utente fa richiesta all'api e li manda a logstash 
async def fixtures_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    payload={}
    headers = {
    'x-rapidapi-key': str(os.environ["API-KEY"]),
    'x-rapidapi-host': 'v3.football.api-sports.io'
    }

    message = update.message.text

    words = message.split()

    if (words[1]!="Bundesliga"):
       word = words[1]+" "+words[2]
    else:
       word = words[1]

    id = 0
    word = word.strip()
  
    if(word=="Serie A"):
       id=135
    elif (word=="Ligue 1"):
       id=61
    elif(word=="Premier League"):
       id=39
    elif(word=="Bundesliga"):
       id=78
    elif(word=="La Liga"):
       id=140
    else:
       await update.message.reply_text(word)
       return
 
 
    #url = "https://v3.football.api-sports.io/standings?league=135&season=202"
    for i in range(2011,2024):
      if i != 2011:
         time.sleep(5)  #tra una richiesta e l'altra si ferma 6 secondi

      url = str(os.environ["URL"])+"league="+str(id)+"&season="+str(i)
      response = requests.request("GET", url, headers=headers, data=payload)

      json_object = json.loads(response.text)  #questo lo devo inviare a logstash
      r = requests.request("POST",url='http://10.0.100.22:8080',json=json_object)  #indirizzo ip di logstash nella rete dei container

      if i == 2023:
         await update.message.reply_text('Ok')
      else:
         await update.message.reply_text('Elaborating...')
   
    
    message = ""
    url = ""


    
token = os.environ["TOKEN"]    #token api telegram bot
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("results",fixtures_function))

app.run_polling()

