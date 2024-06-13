**SA&P**

***SA&P*** (SerieA Analysis And Prediction) 
is a project based on the studying of data from the Serie A rankings from 2005 to 2023 in order to analyze the rankings from years ago and to be able to 
predict future standings based on certain club statistics.

You can see more details about the application in [Sa&p doc](https://github.com/lorenzodidomenic/AllAboutFootball/blob/main/docs/Presentation.ipynb)

***What you need if you want to run the app by yourself***

- A Bot Client and a Token to access to the Telegram Bot API 
- Api Token to query the [Api-football source](https://www.api-football.com/)
- Docker Engine
- Download the Kibana Dashboard on [Dashboards](https://github.com/lorenzodidomenic/AllAboutFootball/blob/main/DASHBOARD.ndjson)

*** How do you run the app ***

1) Go into the project folder
2) Change in the **footbAll.yml** file the TOKEN and API env variable with your token 
3) Run the command ****docker compose -f footbAll.yml up***
4) Go to [Kibana Managmnet](http://localhost:5601/app/management/kibana/objects) and import the [Dashboards](https://github.com/lorenzodidomenic/AllAboutFootball/blob/main/DASHBOARD.ndjson) downloaded

Now you can send message to the bot and enjoy yuor prediction 



   
