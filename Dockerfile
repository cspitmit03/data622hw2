FROM python:3.5

WORKDIR /usr/src/app/hw2

RUN apt-get update -qq && apt-get upgrade -y && \
   apt-get install -y --no-install-recommends \
       libatlas-base-dev gfortran\
        python-pip
RUN pip install --no-cache-dir pandas && \
    pip install bs4 && \
    pip install numpy && \
    pip install Flask-WTF && \
    pip install matplotlib && \
    pip install requests && \
    pip install pymongo && \
    pip install lxml && \
    pip install kaggle && \
    pip install -U scikit-learn
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 27017
COPY . .
CMD ["kaggle", "competitions", "download", "-c", "titanic"]
CMD ["python", "/usr/src/app/hw2/score_model.py"]
