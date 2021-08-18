FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential
WORKDIR /mkad_distance
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . /mkad_distance
ENV FLASK_APP=mkad_distance
ENV FLASK_ENV=development
CMD ["gunicorn", "mkad_distance:create_app()", "-b", "0.0.0.0:8000"]
EXPOSE 8000