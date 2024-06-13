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
         