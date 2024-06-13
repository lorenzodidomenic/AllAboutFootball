from telegram import Update
from telegram.ext import ApplicationBuilder,CommandHandler,ContextTypes
import requests;
import time

import os;
import json 
import random
from telegram.constants import ParseMode

from functions import *
from var import *



#per rispondere con le funzionalità possibili del bot
async def info_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
   global MENU
   await update.message.reply_text(MENU)


#per analizzare e fare predizioni dal 2011 al 2024
async def total_analyze_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
   global teams_dict
   message = update.message.text
   words = message.split()
   year = None
   id = 135    #id della serie A 

   if(len(words) == 2):
      year = words[1]
   
   if(year is None):    #se l'anno non è stato passato faccio analisi dal 2011 al 2023
      for i in range(2011,2024):
         url = str(os.environ["URL"])+"league="+str(id)+"&season="+str(i)   #url = "https://v3.football.api-sports.io/standings?league=135&season2023"
         requests_function(url)
         time.sleep(4)

         if i == 2023:
            await update.message.reply_text(ELABORATED)
         else:
            await update.message.reply_text("Elaborating...")

   elif (int(year) <2011 or int(year)>2023):
      await update.message.reply_text(ERROR)

   else:   #faccio analisi per l'anno prestabilito
      url = str(os.environ["URL"])+"league="+str(id)+"&season="+str(year)
      requests_function(url) 
      time.sleep(4)

      await update.message.reply_text(ELABORATED)
   
   message = ""
   url = ""

         
#funzione che predice una posizione calcolando statistiche random sul club chiesto
async def predict_random_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

      global teams_dict 
      message = update.message.text     #il messaggio  è predict nomeSquadra anno(\"gf\" \"gs\" \"win\" \"draw\" \"lose\")
      words = message.split()
      team=year=points=win=lose=draw=gol_for=gol_against =  None
 
      if(len(words)< 3 or (len(words)>3 and len(words)!= 8) or(len(words) > 8)):
         await update.message.reply_text(ERROR)
         return 
      elif(len(words) == 3):
         team =  words[1]
         year = words[2]

        
         while True:   #per essere sicuro che il numero di partite perse, vinte  o pareggiato sia 38
            win = random.randrange(0,39) 
            lose = random.randrange(0,39)
            draw = random.randrange(0,39)
            if (win+lose+draw == 38):
               break
      
         gol_for = random.randrange(0,100)
         gol_against = random.randrange(0,100)
         points = win*3+draw*1

      else:
         team =  words[1]
         year = words[2]
         gol_for = words[6]
         gol_against = words[7]
         win = words[3]
         draw = words[4]
         lose = words[5]
         points = int(win)*3+int(draw)*1
      
      #mi creo qui una stringa con dati random e lo trasformo in json e glielo mando 
      response = generate_json(year,team,points,win,draw,lose,gol_for,gol_against)
      json_object = json.loads(response)  #questo lo devo inviare a logstash
      r = requests.request("POST",url=LOGSTASH_URL,json=json_object)  #indirizzo ip di logstash nella rete dei container
      
      time.sleep(3)
      await update.message.reply_text(ELABORATED)
   

async def simulate_year_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
      global teams_dict 

      message = update.message.text     #il messaggio  è \simulate year
      words = message.split()
      year = None

      if(len(words) >= 2):
         year = words[1]
      else: 
         year = "2025"

      for key in teams_dict:   #per ogni squadra nel dizionario 
         points=win=lose=draw=gol_for=gol_against =  None
         team = key

         while True:   #per essere sicuro che il numero di partite perse, vinte  o pareggiato sia 38
            win = random.randrange(0,39) 
            lose = random.randrange(0,39)
            draw = random.randrange(0,39)
            if (win+lose+draw == 38):
               break
         gol_for = random.randrange(0,100)
         gol_against = random.randrange(0,100)
         points = win*3+draw*1

         #mi creo qui una stringa con dati random e lo trasformo in json e glielo mando 
         response = generate_json(year,team,points,win,draw,lose,gol_for,gol_against)
         json_object = json.loads(response)  #questo lo devo inviare a logstash
         r = requests.request("POST",url=LOGSTASH_URL,json=json_object)  #indirizzo ip di logstash nella rete dei container

         time.sleep(4)
         await update.message.reply_text("Elaborated Stats for "+key)

      await update.message.reply_text(ELABORATED)


def main():
   token = os.environ["TOKEN"]    #token api telegram bot
   app = ApplicationBuilder().token(token).build()

   app.add_handler(CommandHandler("analyze",total_analyze_function))
   app.add_handler(CommandHandler("info",info_function))
   app.add_handler(CommandHandler("predict",predict_random_function))
   app.add_handler(CommandHandler("simulate",simulate_year_function))

   app.run_polling()

if __name__=="__main__":
      main()

