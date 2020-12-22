FROM python:3.7

RUN apt-get update
ADD / /
COPY data/london_postcodes-ons-postcodes-directory-MAY20.csv /data
RUN pip install -r /requirements.txt
#RUN pip freeze > requirements.txt
CMD python faker.py /data/london_postcodes-ons-postcodes-directory-MAY20.csv /data/rides.csv --num_rows=10_000