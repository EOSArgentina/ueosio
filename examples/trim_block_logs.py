#!/usr/bin/env python3
import os
import shutil
import sys
import loguru
import click
from loguru import logger

from ueosio import DataStream
from ueosio.utils import endian_reverse_u32

def get_head_pos_from_index(root):
    with open('{0}/blocks.index'.format(root), 'rb') as fp:
        fp.seek(-8, 2)
        ds = DataStream()
        ds.stream = fp
        res = ds.unpack_uint64()
        return res

def trim_logs_to_v3(root, chain_id, overwrite):
    with open('{0}/blocks.log'.format(root), 'rb') as fp:
        ds = DataStream()
        ds.stream = fp

        fp.seek(-8, 2)
        pos_end_head = fp.tell()
        pos_start_head = ds.unpack_uint64()
        
        if pos_start_head != get_head_pos_from_index(root):
            logger.error("different head offset")
            return False

        fp.seek(pos_start_head+14)
        block_num = endian_reverse_u32(ds.unpack_uint32())+1

        logger.debug("Generating blocks.log with just one block ({})", block_num)

        with open('{0}/blocks.log.new'.format(root), 'wb') as op:
            ds = DataStream()
            ds.stream = op
            ds.pack_uint32(3) # version
            ds.pack_uint32(block_num) # first block
            ds.pack_chain_id_type(chain_id) # chain id
            ds.pack_uint64(2**64-1) # totem
            fp.seek(pos_start_head)
            op.write(fp.read(pos_end_head - pos_start_head)) # block
            ds.pack_uint64(4+4+32+8)

        with open('{0}/blocks.index.new'.format(root), 'wb') as op:
            ds = DataStream()
            ds.stream = op
            ds.pack_uint64(4+4+32+8)

        if overwrite:
            shutil.move('{0}/blocks.index.new'.format(root), '{0}/blocks.index'.format(root))
            shutil.move('{0}/blocks.log.new'.format(root), '{0}/blocks.log'.format(root))

        logger.info("done")
        return True


@click.command()
@click.argument('root')
@click.argument('chain_id')
@click.option('--overwrite', default=False, help='Overwrite blocks.log/blocks.index files')
def trim(root, chain_id, overwrite):
    trim_logs_to_v3(root, chain_id, overwrite)

if __name__ == '__main__':
    trim()


