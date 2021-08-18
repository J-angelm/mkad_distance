# Moscow Automobile Ring Road Distance Calculator
To Calculate the distance from any address to the MKAD, you will need a Yandex API Key (you can get it at https://yandex.ru/dev/maps/geocoder/doc/desc/concepts/about.html for free).

To execute the Flask blueprint:
1. Create a new directory and clone this repo
```
$ mkdir mkad_app
```
```
$ cd mkad_app
```
```
$ git clone https://github.com/J-angelm/mkad_distance
```
2. Build your docker container 
```
$ docker build -t mkad_app:latest .
```
3. Run the container
```
$ docker run -d -p 8000:8000 mkad_app
```
4. Access the website through your IPv4 address
