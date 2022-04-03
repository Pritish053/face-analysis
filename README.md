# face-analysis
flask crud with mysql and deepface as backend

## Getting started

For standalone web service:

## Installation

Clone this repository 
```shell
git clone https://github.com/Pritish053/face-analysis.git
cd face-analysis/
```

Create a new pip environment
```shell
python3.8 -m venv env_flask

#just to make sure you have updated version of pip
pip install -U pip

pip install -r requirements.txt
```
Run with flask.
```shell
python api.py
```

Visit [http://localhost:5000](http://localhost:5000)

## ML Service API Check

To check whether the ML Service api is working or not (in the case of using third party API for inferencing )
Chnage the IP Address of the API and run

```shell
python3 checkMLSERVICE.py  
```

## Database Schema 

<img src="https://github.com/Pritish053/face-analysis/blob/3d9df4593bd4387595e4f2405e737d079ef3476a/Untitled.png">

### Create users table 
```shell 
CREATE TABLE `users` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(250) NOT NULL,
      `email` varchar(250) NOT NULL,
      `photo` varchar(250) NOT NULL,
      `time` varchar(255) NOT NULL,
      `age` int NOT NULL,
      `gender` varchar(250) NOT NULL,
       PRIMARY KEY (`id`) );
```
### Create table for storing admin credentials
```shell
CREATE TABLE `admin` (
       `id` int NOT NULL AUTO_INCREMENT,
       `username` varchar(50) NOT NULL,
       `password` varchar(255) NOT NULL,
        PRIMARY KEY (`id`));

```

## Docker Container
```shell
docker build -t faceanalysiswebapp .
docker run -d -p 5000:5000 --name webappfaceanalysis faceanalysiswebapp
# docker stop webappfaceanalysis
```

## Logs

Check logs with docker logs:

```shell
docker logs webappfaceanalysis
```
