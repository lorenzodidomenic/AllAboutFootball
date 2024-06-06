FROM apache/spark:3.4.2

USER 0 

RUN pip install numpy
COPY ./dataset/data.csv  /tmp
USER spark
