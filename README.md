# Lead service

Lead service to create and manage tasks concerned with `leads`


```shell
$ git clone https://github.com/bistegra/lead_service.git
$ cd fwork
```

## Run service in Docker
Build the images and start the containers:
```shell
$ make image
$ make run
```

## Testing

### Run tests
Run built image tests in docker:
```shell
$ make test
```

For manual testing on host without image re-building after edits (with application source code mounted as volume):
```shell
$ make test_local
```

## Run manually
Start Redis and PostgreSQL (create empty database in advance). Set connection parameters:
```shell
$ export POSTGRES_DB='<db_name>' POSTGRES_USER='<db_user>' POSTGRES_PASSWORD='<db_password>'
```

Run database migrations:
```shell
$ cd source/migrations 
$ alembic upgrade head
$ cd ../..
```

Run service:
```shell
$ python -m source.app
```
