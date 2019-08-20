# -*- coding: UTF-8 -*-
import json
import os
import click

from __init__   import __version__
from __init__   import __application__


from sa_tools import saElastic
from sa_tools import saConfig

config = saConfig()
config.load()
cfg = config.config

elastic = saElastic()

if 'clusters' in cfg :
  # settings has cluster secton
  if 'default' in cfg['clusters'] :
    # default cluster is set
    elastic._change_cluster(host = cfg['clusters']['default']['host'], domain=cfg['clusters']['default']['domain'])

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
def move_index_to_tag(index, tag_value, tag_name, wait, force):
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

@click.command()
@click.option('--index', type=str, required=True, help='Index name')
@click.option('--number', type=str, required=False, help='Shards number or empty for None')
def set_shards_per_node(index,number='None'):
  """
    set total_shards_per_node
  """
  elastic.set_number_shards_per_node( index = index, number = number )

@click.command()
@click.option('--node', type=str, required=False, help='List only indices from data node')
def list(node):
  """
    show index list
  """
  elastic.list_indices(only_this_node=node)

@click.command()
@click.option('--node', type=str, required=True, help='Data node name')
@click.option('--reset', default=False, is_flag=True, help='Reset shards per node settings.')
@click.option('--wait', type=int, default=10, help='Timeout before start moving the shard, sec.')
@click.option('--test', default=False, is_flag=True, help='Just test without action [default]')
def drain_node(node, reset, wait, test):
  """
    drain all indices from data node
  """
  elastic.drain_node(node = node, reset_shards_per_node=reset, wait_after_move=wait, test = test )

@click.command()
@click.option('--index', type=str, required=True, help='Index name')
@click.option('--node', type=str, required=True, help='Data node name')
@click.option('--force', default=False, is_flag=True, help='Without confirmation.')
@click.option('--reset', default=False, is_flag=True, help='Reset shards per node settings.')
def move_index_from_node(index, node, force, reset):
  """
    move selected index from data node
  """
  elastic.index_move_from_node(index = index, node = node, without_confirmation=force, reset_shards_per_node=reset)





cli.add_command(info)
cli.add_command(reset)
cli.add_command(fix)
cli.add_command(wait)
cli.add_command(move_index_to_tag)
cli.add_command(move_index_from_node)
cli.add_command(incr)
cli.add_command(delete)
cli.add_command(list)
cli.add_command(set_shards_per_node)
cli.add_command(drain_node)

if __name__ == '__main__':
  cli()
