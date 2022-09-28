###$ Launch postgres server via docker-compose
> $ cd /docker/
> $ docker-compose up -d  
>  goto http://localhost:5050/login to access pgadmin ui  

### Connecting pgadmin to postgres
> $docker network ls  //find the bridge between postgres 
> 6845bc55d171   postgres_default   bridge    local  
> $ docker network inspect postgres_default  
> //grab this GATEWAY Address for using to connecting pgadmin to postgresql db container
> password of db is root for testing, verify the GATEWAY if unable to connect.
> ### Find postgres container id &/or name 
> [@localhost postgres]$ docker ps      
> ` |26a6e42130f2 |  postgres  | "docker-entrypoint.s…"  | 18 seconds ago  | Up 16 seconds  | 0.0.0.0:5432->5432/tcp, :::5432->5432/tcp  | postgres_postgres_1 `
> ###$ access container shell
>       [@localhost apiary]$ docker exec -it postgres_postgres_1 bash
> ### Create user and database
> #### User Creation:
>       root@7ef8dbd0f8d3:/# su - postgres
>       postgres@7ef8dbd0f8d3:~$ createuser -P -s -e myuser
> #### Database creation:
>       postgres@7ef8dbd0f8d3:~$ createdb -O myuser testdb
> ### using psql log into testdb with myuser
>       root@26a6e42130f2:/# psql -d testdb -U myuser
> ##### Verify tables were created
>       testdb=# \dt

REQUIREMENTS:
python3
psycopg2
jq
docker

ERROR RESOLUTION:
https://stackoverflow.com/questions/12911717/error-command-gcc-failed-with-exit-status-when-installing-psycopg2
if docker wont spin up postgresql check if docker_postgres is running and stop it

## TODO:
   ### docker-compose app service needs volumes
   ### remove hardcoded ID in tests/test_companies.py in func test_get_companies_by_id()
   ### write dispensary tests
   ### test dispensary put, need columns unqness change
   ### swagger post json example:     "json_doc": "{'name':'hthrthrth', 'age':30, \"car\":null}"
   ### need to replace double quotes with singles and than post dutchie product json to db
   ### Unable to post a new dispensary if another dispensary uses any equal column values, ie: dis1 and dis2 cannot both have the same flower_url == "string"
   ### blob_publisher.py works with fastapi, however it uses its own config.

## Migrations
  ### alembic downgrade base
  ### alembic upgrade head