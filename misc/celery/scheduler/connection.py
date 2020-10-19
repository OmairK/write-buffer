import logging

import psycopg2
from redis import Redis
from redis.exceptions import ConnectionError


class BaseConnection:
    """
    Base connection class for databases
    """

    def __init__(
        self, host, port, client=None, password=None, database=None, user=None
    ):
        self.host = host
        self.port = port
        self.client = client
        self.password = password
        self.database = database
        self.user = user

    def sanity_check(self, client):
        """
        Runs a sanity check on the connection
        """
        pass

    def client_initialisation(self):
        """
        Sets up the connection via the given host, port
        """
        pass

    def arguments_to_db_kwargs(self):
        """
        Converts the class arguments
        """
        _fixed_kwargs = {"host": self.host, "port": self.port}

        if self.password is not None:
            _fixed_kwargs["password"] = self.password

        if self.database and self.user:
            _fixed_kwargs["database"] = self.database
            _fixed_kwargs["user"] = self.user

        self.fixed_kwargs = _fixed_kwargs


class RedisConn(BaseConnection):
    def sanity_check(self, client):
        try:
            client.ping()
        except ConnectionError as err:
            logging.critical(
                f"Redis Connection refused on host:'{self.host}' port:'{self.port}'"
            )
            raise err

    def client_initialisation(self):
        self.arguments_to_db_kwargs()
        _r = Redis(**self.fixed_kwargs)
        self.sanity_check(_r)
        self.client = _r


class PostgresqlConn(BaseConnection):
    def sanity_check(self, client):
        # TODO: Better implementation for pinging the postgresql server
        try:
            client = client.cursor()
            client.execute(
                "select relname from pg_class where relkind='r' and relname !~ '^(pg_|sql_)';"
            )
            client.fetchall()
        except Exception as err:
            logging.critical(
                f"Postgres connection refused on host:'{self.host}' port:'{self.port}'"
            )
            raise err

    def client_initialisation(self):
        self.arguments_to_db_kwargs()
        _p = psycopg2.connect(**self.fixed_kwargs)
        self.sanity_check(_p)
        self.client = _p
