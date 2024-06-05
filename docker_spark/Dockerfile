FROM apache/spark

USER 0 

RUN pip install numpy
COPY ./dataset/data.csv  /tmp
USER spark
