# Backend-Assignment-Youtube API | FamPay

## Problem Statement:

- To make an API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given search query in a paginated response. 
- Server should call the YouTube API continously in background (async) with some interval (say 5 minutes) for fetching the latest videos for a predefined search query and should store the data of videos (specifically these fields - Video title, description, publishing datetime, thumbnails URLs and any other fields you require) in a database with proper indexes. 

## REFERENCE:
- [YouTube data v3 API]
- [Search API reference]
- To fetch the latest videos you need to specify these: type=video, order=date, publishedAfter=<SOME_DATE_TIME> Without publishedAfter, it will give you cached results which will be too old.

## Tech
Frontend:
    1. HTML,CSS,JS
    2. Bootstrap
    3. Jinja Templating Language
Backend:
    1. Flask
    2. SQLAlchemy

Database:
    1.PostgreSQL
    
## Installation

Install the dependencies and start the server.

```sh
git clone 
cd Youtube-Backend/
docker-compose up -d --build
```
To see logs of docker containers you can use:
```sh
docker-compose logs -f '<service name>'
```

This will create the image of our flask-application and pull in the necessary dependencies.

In this , we have map port 8000 of the host to
port 8080 of the Docker:

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## Additional Points
1. Get Videos (GET, POST Request):
    Returns all the videos order by lates published date. When APIKey's Quota is over, it will try using different key stored in the APIKey table. To Add a new APIKey use Add Key API (2nd point) for adding a new Youtube Data API Key in the database.
2. Add API Key (POST Request)
    When we get an error of APIKey's Quota is over, we can add a new APIKey. Using this api, the service will start again because we have a valid API Key in our database, so it will fetch and store videos in the database.



   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
