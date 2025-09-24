#! /usr/bin/env python3

from logging import getLogger
import os

import click
import uvicorn

_LOG = getLogger(__name__)


@click.command()
@click.option("--debug", is_flag=True, default=False)
@click.option("--props")
def main(debug, props):
    port = int(os.environ.get("PORT0", 8080))
    host = os.environ.get("HOST0", "0.0.0.0")

    if debug:
        worker_count = 1
    elif worker_override := os.environ.get("WORKERS", 1):
        worker_count = int(worker_override)
    else:
        # fast api recommends scaling workers using a container orchestrator if that is
        # what is used for deployment docs:
        # https://fastapi.tiangolo.com/deployment/docker/#replication-number-of-processes # noqa: E501
        # so it may be cleaner to scale instances in marvin rather than increasing
        # the worker count alternatively, if you want to have many workers in a
        # single process then it seems to be recommended to use:
        # worker_count = cpu_cores * 2 + 1
        # we recommend to set up some kind of testing to verify performance for
        # any changes to this value
        worker_count = 1

    _LOG.info(f"starting up with {worker_count} workers")

    from mcpskeleton.daemon.implementation import build_app

    uvicorn.run(
        build_app(),
        host=host,
        port=port,
        workers=worker_count,
        reload=debug,
    )


if __name__ == "__main__":
    main()
