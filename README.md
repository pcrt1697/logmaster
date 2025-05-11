# logmaster

## logmaster-client
Client package for Python applications. Provides an interface to configure logging and produce the related messages.
Such messages are written to MongoDB.

## logmaster-server
Backend application that provides a REST interface to query the log messages. It is a middleware used to query for the logs in MongoDB.
It is also provide endpoints to create applications.

## Local run
```bash
docker-compose -f ./docker/docker-compose.local.yml up --force-recreate -d
```

## TODO
- Add backend container to compose file
- Create a notifier framework
