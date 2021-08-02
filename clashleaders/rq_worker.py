import logging
import os
import sys

from rq import Connection, SimpleWorker

from clashleaders import redis_connection


def main():
    logger = logging.getLogger("rq.worker")
    logger.setLevel("WARN")
    with Connection(connection=redis_connection):
        qs = sys.argv[1:] or ["default"]
        w = SimpleWorker(qs)
        w.work(logging_level="WARN", with_scheduler=("USE_SCHEDULER" in os.environ))


if __name__ == "__main__":
    main()
