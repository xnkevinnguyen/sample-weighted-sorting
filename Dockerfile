FROM python:3.6

# USER app
ENV PYTHONUNBUFFERED 1
# RUN mkdir /db
#RUN chown app:app -R /db

RUN mkdir /config
ADD config/app /config/

RUN pip install -r /config/requirements.txt

# Open port 8000 to outside world
EXPOSE 8000

# When container starts, this script will be executed.
# Note that it is NOT executed during building
CMD ["sh", "/config/on-container-start.sh"]

# Creating and putting application inside container
# and setting it to working directory (meaning it is going to be default)
RUN mkdir /app
WORKDIR /app
ADD shopping /app/