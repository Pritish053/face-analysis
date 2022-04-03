# face-analysis
flask crud with mysql and deepface as backend

## Getting started

For standalone web service:

```shell
pip install -r requirements.txt
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)


## ML Service API Check

To check whether the ML Service api is working or not (in the case of using third party API for inferencing )
Chnage the IP Address of the API and run

```shell
python3 checkMLSERVICE.py  
```

## Database Schema 



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
