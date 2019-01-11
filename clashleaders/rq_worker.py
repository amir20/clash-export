import logging
import sys

from rq import Connection, Worker

from clashleaders import redis_connection


def main():
    logger = logging.getLogger('rq.worker')
    logger.setLevel('WARN')
    with Connection(connection=redis_connection):
        qs = sys.argv[1:] or ['default']
        w = Worker(qs)
        w.work(logging_level='WARN')


if __name__ == "__main__":
    main()
