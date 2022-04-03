# face-analysis
flask crud with mysql and deepface as backend

## Getting started

For standalone web service:

```shell
pip install -r requirements.txt
python app.py
```

Visit [http://localhost:5000](http://localhost:5000)

## Docker Container
CREATE TABLE `users` (
      `id` int NOT NULL AUTO_INCREMENT,
      `name` varchar(250) NOT NULL,
      `email` varchar(250) NOT NULL,
      `photo` varchar(250) NOT NULL,
      `time` varchar(255) NOT NULL,
      `age` int NOT NULL,
      `gender` varchar(250) NOT NULL,
      PRIMARY KEY (`id`) );

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

## Database Schema 

```shell 
Create 
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

```shell
docker logs webappfaceanalysis
```


