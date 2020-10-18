import psycopg2


conn = psycopg2.connect(database="fsc_database", user="postgres",host='127.0.0.1', password="test123",port=5432)
curr = conn.cursor()

def scheduled_writer():
    redis_reader = RedisListToPythonNative("XRider:Booking", deserializer=booking_serializer)
    redis_reader.retrieve()

    instance_list = redis_reader.booking_list
    if len(instance_list) == 0:
        return 0
    
    conn = psycopg2.connect(database="fsc_database", user="postgres",host='127.0.0.1', password="test123",port=5432)
    cur = conn.cursor()
    
    args_bytes = b','.join(cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s)", x) for x in instance_list)
    cur.execute(b"INSERT INTO table VALUES " + args_bytes)
