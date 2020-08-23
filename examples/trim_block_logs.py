#!/usr/bin/env python3
import os
import shutil
import sys
import loguru
import click
from loguru import logger
from utils import trim_logs_to_v3

@click.command()
@click.argument('root')
@click.argument('chain_id')
@click.option('--overwrite', default=False, help='Overwrite blocks.log/blocks.index files')
def trim(root, chain_id, overwrite):
    if os.path.isfile('{0}/blocks.log'.format(root)):
        trim_logs_to_v3(root, chain_id, overwrite)

if __name__ == '__main__':
    trim()


