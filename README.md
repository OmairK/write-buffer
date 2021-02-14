### Write Buffer

### Implementation details
This API will be tested at peak times of the day when there are write requests incoming, so the primary objective here was to ease the load  database as the Postgresql server would be the first bottleneck here. For that a redis write-buffer is implemented that will store the validated data into redis, [Redis’s Reliable Queue](https://redis.io/commands/rpoplpush#pattern-reliable-queue) pattern. A celery scheduler will then pop <user_defined_value> of elements from  redis and write it onto the Postgresql database via a bulk insert operation, which will be much faster than a single writes hence reducing the load on the database.


* **Query DSL**

    For implementing a OLAP system I would run a Airflow ETL pipeline from the amazon RDS to Apache Superset which would be then used for the analytics.

* **Ideal system Architecture**

	To avoid vendor lockins and easy migrations I wanted to use in house solutions rather than relying too much on the vendor specific features and systems, hence this architecture could be easily implemented via different cloud vendors.
    ![image info](./misc/arch.png)


### Settings up

* Pre-requisites
	* docker-compose

```
docker-compose build
docker-compose up
```

* Endpoint Open API spec
[Redoc link](https://redocly.github.io/redoc/?url=https://raw.githubusercontent.com/OmairK/locale-task/master/misc/openapi/v1.yaml)

* Benchmarking
After running the docker container a benchmark test can be carried out via

```
cd misc/test-data
python benchmark.py
```
