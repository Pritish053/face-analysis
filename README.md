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
