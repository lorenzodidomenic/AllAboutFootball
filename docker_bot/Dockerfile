FROM python 

#mi serve per poter eseguire il file python direttamente
ENV PATH /usr/src/app/bin:$PATH
WORKDIR  /usr/src/app

#scarico i pacchetti che mi servono in python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt 

#copio i file python
COPY ./bin/* ./
COPY file_manager.sh /
#eseguo file bash che mi lancia il bot
ENTRYPOINT [ "/file_manager.sh" ]