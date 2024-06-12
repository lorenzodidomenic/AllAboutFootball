from __future__ import print_function

import sys
import numpy

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F

from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.ml import Pipeline
from pyspark.ml.pipeline import PipelineModel
#from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.conf import SparkConf
from pyspark.ml.evaluation import RegressionEvaluator

spark = SparkSession.builder.appName("FootbALL").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")   # To reduce verbose output


#ho file csv con dati classifiche dal 2005 al 2023
#in un campioato vorrei capire la relazione che c'è tra [punti,gf,gs,w,d,l] => rank
#predno quelle come features per la regressione lineare e da esse predico il ranking
#alleno il modello coi dati del file csv
def model_trainer(nome_file):
    training = spark.read.format("csv").options(header='true',inferschema='true',delimiter=",").load(nome_file)
    featureassembler = VectorAssembler(inputCols = ["points","for","against","win","draw","lose"],outputCol = "features") #definisco le colonne che saranno i parametri della predizione
    lr = LinearRegression(featuresCol="features",labelCol="rank",predictionCol="Predicted_rank")
    pipeline = Pipeline(stages=[featureassembler,lr])
    model = pipeline.fit(training)
    return model


#l'ho usato per stamparmi il RMSE (circa 0.007)
training = spark.read.format("csv").options(header='true',inferschema='true',delimiter=",").load("/tmp/data.csv")
model = model_trainer("/tmp/data.csv")
training_predictions = model.transform(training)
evaluator = RegressionEvaluator(labelCol='rank', predictionCol='Predicted_rank', metricName='rmse')
rmse = evaluator.evaluate(training_predictions)
print("Root Mean Squared Error (RMSE) on test data:", rmse/20)

#coefficients = lr_model.coefficients
#intercept = lr_model.intercept
#print("Coefficitents: ",coefficients)
#print("Intercept: {:.3f}".format(intercept))

#mi salvo il modello in un volume condiviso
model.save("/tmp/footbAllVolume/Completemodel")   #PER SALVARE IL MODELLO IN UN VOLUME CHE HO MONTATO