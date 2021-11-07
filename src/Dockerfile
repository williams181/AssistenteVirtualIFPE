FROM  python:3.7

RUN apt-get update && apt-get install -y default-jre
RUN apt-get install -y build-essential libpoppler-cpp-dev pkg-config
RUN apt-get install -y locales

RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=pt_BR.UTF-8

ENV LANG pt_BR.UTF-8 

# Create a working directory
RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 4000
# CMD python assistenteVirtualIFPEChatBotWebCam.py
CMD /usr/local/bin/gunicorn --bind 0.0.0.0:4000 assistenteVirtualIFPEChatBotWebCam:app
