# -*- coding: UTF-8 -*-
import json
import sys
import os
import click

from __init__   import __version__
from __init__   import __application__


from sa_tools import saElastic

elastic = saElastic(host = "http://localhost:9200") #  ES5

@click.group()
def cli():
    pass

@click.command()
@click.option('--index', type=str, required=True)
def info(index):
  """
    Show shard locations, allocation and base settings
  """
  tmp = {}
  tmp['location'] = elastic.get_index_location(index) 
  tmp['routing']  = elastic.get_index_routing(index)
  print (tmp)

@click.command()
@click.option('--index', type=str, required=True)
def reset(index):
  """
    Remove all allocation settings
  """
  elastic.index_reset(index)


@click.command()
@click.option('--index', type=str, required=True) 
def fix(index):
  """
    Fix index allocation to the current data nodes.
    Each data node will add to include allocation settings.
  """
  elastic.index_fix(index = index)

@click.command()
@click.option('--index', type=str, required=True) 
def wait(index):
  """
    Wait index movement to the new location.
  """
  elastic.wait_index_relocation(index = index)


@click.command()
@click.option('--index', type=str, required=True, help='Index name')
@click.option('--tag-value', type=str, required=True, help='Tag value')
@click.option('--tag-name', type=str, default='tag', help='Tag name. It can be: tag (default), group, rack_id.')
@click.option('--wait', type=int, default=10, help='Timeout before start moving the shard, sec.')
@click.option('--force', default=False, is_flag=True, help='Without confirmation.')
def move(index, tag_value, tag_name, wait, force):
  """
    Move index to the specific tag
  """
  elastic.index_move( index = index, tag_name = tag_name, tag_value = tag_value, wait_after_move=wait, without_confirmation = force )

@click.command()
@click.option('--index', type=str, required=True, help='Index name')
@click.option('--force', default=False, is_flag=True, help='Without confirmation.')
def incr(index, force):
  """
    Increase replic numbers
  """
  elastic.incr_replica_amount( index = index, without_confirmation = force)

@click.command()
@click.option('--index', type=str, required=True, help='Index name')
def delete(index):
  """
    Remove index
  """
  elastic.delete_index( index = index )

cli.add_command(info)
cli.add_command(reset)
cli.add_command(fix)
cli.add_command(wait)
cli.add_command(move)
cli.add_command(incr)
cli.add_command(delete)

if __name__ == '__main__':
  cli()
