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

MENU = " Command list:  \n \
- /analyze \nTo analyze and compare exepected Serie A standings from 2010 to 2023 \n \
- /analyze \"year\" \nTo analyze and compare exepected Serie A standing of the year \n \
- /predict \"team\" \"year\" \n To predict position of a Serie A team with random stats \n \
- /predict \"team\" \"year\" \"win\" \"draw\" \"lose\" \"g_f\" \"g_a\" \n To predict position of a Serie A team with some stats \n \
- /simulate \"year\" To simulate the standing of the year with random stats \n"

ELABORATED = "Result Elaborated. See it on Kibana "

ERROR = "Error in the parameters. Command /info for help"

LOGSTASH_URL = "http://logstash:8080"