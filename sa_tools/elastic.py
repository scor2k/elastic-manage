# -*- coding: UTF-8 -*-

from typing     import Dict, Any, Optional
from requests   import HTTPError
from time       import sleep

from sa_tools import saLogs

import json
import requests

log   = saLogs()

class saElastic:
  def __init__(self, host = 'http://localhost:9200', domain='') :
    self.host = host 
    self.domain = domain

  def __del__(self) :
    pass

  def _change_cluster(self, host, domain=''):
    """
      change elasticsearch cluster
    """
    self.host = host
    self.domain = domain
    log.debug(msg='Set Elasticsearch cluster', host = host, domain = domain)

  def _request(self, url: str, method: str = 'get', params: Optional[Dict[str, Any]] = None ):
    """
      request to elasticsearch (get/post/put/etc...)
    """
    _url = f'{self.host.rstrip("/")}/{url.lstrip("/")}'

    try :
      headers = {'Content-type': 'application/json'}
      response = requests.request( method = method, url = _url, json=params, headers = headers )
      response.raise_for_status()
    except HTTPError as e:
      print (e)
      return [{}]

    if response.text: 
      return response.json()

  def index_swap_one_node(self, index, tag_name, tag_value) :
    """
      Get one node from include._name and move it to exclude._name
      incluge.tag always include tag_value 
    """

    routing = self.get_index_routing(index = index)

    include_name = list()
    exclude_name = list()

    if 'include' in routing:
      include = routing['include']
      if '_name' in include and len(include['_name']) > 0:
        include_name = include['_name'].split(',')

      else :
        log.debug(msg = f'Nothing to do in [{index}]. No one node in include list ')
        return False

    if 'exclude' in routing:
      exclude = routing['exclude']
      if '_name' in exclude :
        exclude_name = exclude['_name'].split(',')

    if len(include_name) > 0 :
      # move 1 item from include -> exclude
      #log.debug(msg = f'Index [{index}] before include: [{include_name}], exclude: [{exclude_name}]')
      exclude_name.append( include_name.pop() )
      log.debug(msg = f'Index [{index}] after this step. include: [{include_name}], exclude: [{exclude_name}]')

      # need to send configuration to elastic
      reset = {
        "index.routing.allocation.include._name" : ",".join(include_name),
        "index.routing.allocation.exclude._name" : ",".join(exclude_name),
        f"index.routing.allocation.include.{tag_name}" : f"{tag_value}"
      }

      #yn = input("Continue?")

      url = f'/{index}/_settings'
      rez = self._request( url = url, method='put', params = reset )
      print (rez)

      return True

    log.debug(msg = f'Nothing to do in [{index}].')
    return False

  def index_move(self, index, tag_value, tag_name, wait_after_move=10, without_confirmation=False) :
    """
      tag_name = 'tag, group, etc...'
      tag_value = 'hot, warm, etc...'

      move index to the specifiend tag value
      algorithm: 
       - fix index to current data nodes
       - step by step move one shard from old data-node to new
       - wait after every step
    """
    print ( f"Index location: {self.get_index_location(index = index)}" )
    print ( f"Index routing: {self.get_index_routing(index = index)}" )

    if without_confirmation :
      log.info(msg = f'Move [{index}] without confirmation!')
    else :
      yn = input(f'Are you sure to move [{index}] into the tag [{tag_name}:{tag_value}]? (y/N) :')
      if yn == 'y' :
        pass
      else :
        log.debug(msg = f'User cancel move index [{index}] to the tag [{tag_name}:{tag_value}]')
        return True

    # fix  index with Force mode (not ask confirmation)
    self.index_fix( index = index, force = True )

    moving = True

    while ( moving ) :
      moving = self.index_swap_one_node( index = index, tag_name = tag_name, tag_value = tag_value )
      self.wait_index_relocation(index = index)

      if moving: 
        log.debug(msg = f'Waiting for [{wait_after_move}] seconds before next iteration')
        sleep( wait_after_move )

  def wait_index_relocation(self, index):
    """
      Wait index movement to the new location.
    """
    status = 'waiting'

    while ( len(status) > 0 ) :
      # reset status
      status = ''
      # get current location
      location = self.get_index_location(index = index)
      # check status
      if location :
        for shard in location:
          if 'state' in shard:
            if shard['state'] != 'started' :
              status += shard['state']
          else :
            log.error(msg = 'Shard has not state field')
            return False

        # check status len 
        if len(status) == 0 :
          log.info(msg = f'Index [{index}] started.')
          pass
        else :
          log.debug(msg = f'Index [{index}] still moving. ')
          sleep(10)
      else :
        log.error(msg = 'Can not get index location')
        return False

  def index_fix(self, index, force = False):
    """
      Fix index allocation to the current data nodes.
    """

    index_shards = self.get_index_location(index = index)

    include_node = set()
    include_name = ""

    if index_shards :
      # collect data nodes 
      for shard in index_shards :
        if 'node' in shard:
          include_node.add( shard['node'] )

      if len(include_node) == 0 :
        # looks like we have a problem
        log.error(msg='Index has not any shard to fix in one place', index = index)
        log.debug(msg='get_index_location', response = index_shards)
        return False

      # generate string with separator
      include_name = ",".join(include_node)



    else :
      return False

    reset = {
      "index.routing.allocation.include._name" : include_name,
      "index.routing.allocation.include.tag" : None,
      "index.routing.allocation.include.box_type" : None,
      "index.routing.allocation.include.group" : None,
      "index.routing.allocation.exclude._name" : None,
      "index.routing.allocation.exclude.tag" : None,
      "index.routing.allocation.exclude.box_type" : None,
      "index.routing.allocation.exclude.group" : None
    }

    if force == False : 
      yn = input(f'Are you sure to fix [{index}] in the [{include_name}]? (y/N) :')
      if yn == 'y' :
        pass
      else :
        log.debug(msg = f'User cancel fix in one place allocation for the index [{index}]')
        return True

    else :
      log.debug(msg=f'Fix index [{index}] with force mode')

    log.info(msg=f'Fix index [{index}] in one place', nodes=include_name)

    url = f'/{index}/_settings'
    rez = self._request( url = url, method='put', params = reset )
    print (rez)

  def index_reset(self, index):
    """
      Remove all allocation settings
    """
    reset = {
      "index.routing.allocation.include._name" : None,
      "index.routing.allocation.include.tag" : None,
      "index.routing.allocation.include.box_type" : None,
      "index.routing.allocation.include.group" : None,
      "index.routing.allocation.exclude._name" : None,
      "index.routing.allocation.exclude.tag" : None,
      "index.routing.allocation.exclude.box_type" : None,
      "index.routing.allocation.exclude.group" : None
    }

    yn = input(f'Are you sure to reset allocation settings for [{index}]? (y/N): ')
    if yn == 'y' :
      pass
    else :
      log.debug(msg = f'User cancel reseting allocation for the index [{index}]')
      return True

    url = f'/{index}/_settings'

    rez = self._request( url = url, method='put', params = reset )
    print (rez)

  def get_index_routing(self, index):
    """
      get include/exclude for tag/host + shards/replics count
    """
    url = f'/{index}/_settings?format=json'
    rez = self._request( url = url )

    idx_allocation = {}

    if index in rez:
      rez = rez[index]

      if 'settings' in rez :
        rez = rez['settings']

        if 'index' in rez :

          rez = rez['index']

          number_of_replicas = -1
          number_of_shards = -1 

          if 'number_of_replicas' in rez :
            number_of_replicas = int(rez['number_of_replicas'])
          
          if 'number_of_shards' in rez :
            number_of_shards = int(rez['number_of_shards'])

          if 'routing' in rez :
            alloc = rez['routing']

            if 'allocation' in alloc :
              alloc = alloc['allocation']

              if 'exclude' in alloc :
                # add all exclude settings
                idx_allocation['exclude'] = alloc['exclude']
              
              if 'include' in alloc :
                # add all include settings
                idx_allocation['include'] = alloc['include']

    # generate response
    idx_allocation['number_of_replicas'] = number_of_replicas
    idx_allocation['number_of_shards'] = number_of_shards
 
    return idx_allocation

  def get_index_location(self, index):
    """
      get shards list where index located
    """
    url = f'/_cat/shards/{index}?format=json'
    rez = self._request( url = url )

    idx_location = list()

    if rez :
      for shard in rez :
        tmp = {}
        if 'state' in shard and not shard['state'] == None :
          tmp['state'] = shard['state'].lower()
          if 'node' in shard:
            tmp['node'] = shard['node']

          # if state 'relocation' try to get destination
          if tmp['state'] == 'relocating' :
            _nodes = tmp['node'].split(' ')
            tmp['old_node'] = _nodes[0]
            tmp['node'] = _nodes[len(_nodes)-1]
          

        # add shard to list 
        idx_location.append (tmp)

    return idx_location

  def incr_replica_amount(self, index, without_confirmation=False) :
    """
      get current replica amount and incr this number 
    """

    routing = self.get_index_routing(index = index)
    amount = int(routing['number_of_replicas'])

    print( f"Index routing: {routing} ")
    print (f"Replica count after increase: {amount+1}.")

    if without_confirmation :
      log.info(msg = f'Move [{index}] without confirmation!')
    else :
      yn = input(f'Are you sure to add one replica to index [{index}] ? (y/N) :')
      if yn == 'y' :
        pass
      else :
        log.debug(msg = f'User cancel incr replica number to index [{index}]')
        return True

    replica = {
      "index.number_of_replicas" : amount+1
    }

    url = f'/{index}/_settings'
    rez = self._request( url = url, method='put', params = replica )

    # change. then wait
    self.wait_index_relocation(index = index)

    print (rez)

  def delete_index(self, index) :
    """
      delete index
    """
    yn = input(f'Are you sure to DELETE index [{index}] ? (y/N) :')
    if yn == 'y' :
      pass
    else :
      log.debug(msg = f'User cancel delete index [{index}]')
      return True

    url = f'/{index}'
    rez = self._request( url = url, method='delete', params = None )

    print (rez)
  
  def _print_indices(self, idx: dict):
    """
      just print idx dictionary from list_indices def
    """
    max_len = 20
    for i in idx.keys() :
      if len(i) > max_len:
        max_len = len(i)

    for index, shard in idx.items():
      spaces = " "*(max_len - len(index) + 1)
      _size = '{:{width}.{prec}f}'.format(shard["size"]/(1024*1024*1024), width=6, prec=2)
      _prim = f'| {" ; ".join(shard["prim_nodes"])}'.replace('STARTED','OK').replace(self.domain, '')
      if len(shard["repl_nodes"]) > 0 :
        _repl = f'| {" ; ".join(shard["repl_nodes"])}'.replace('STARTED','OK').replace(self.domain, '')
      else :
        _repl = f''

      _str = f'{index}{spaces} | {_size} GB {_prim} {_repl} '
      print (_str)
    
    pass

    

  def list_indices(self) :
    """
      get all indices and print it
    """
    url = f'/_cat/shards?format=json&bytes=b'
    rez = self._request( url = url )

    idx = {}
    # idx[index_name] = { size: 1111, prim_nodes: [node1, node2], repl_nodes: [node3, node4] }

    for shard in rez :
      if 'index' in shard :
        index = shard['index']
      else :
        continue

      if index in idx :
        # index already exists in the list
        size = idx[index]['size']
        prim_nodes = idx[index]['prim_nodes']
        repl_nodes = idx[index]['repl_nodes']

        if shard['prirep'] == 'p' :
          # it is primary shard
          size = size + int(shard['store'])
          node = f"{shard['node']} - {shard['state']}"
          prim_nodes.append(node)
          idx[index] = { 'size' : size, 'prim_nodes' : prim_nodes, 'repl_nodes' : repl_nodes }
        elif shard['prirep'] == 'r' :
          node = f"{shard['node']} - {shard['state']}"
          repl_nodes.append(node)
          idx[index] = { 'size' : size, 'prim_nodes' : prim_nodes, 'repl_nodes' : repl_nodes }

      else :
        # just add this shard into indx
        if shard['prirep'] == 'p' :
          # it is primary shard
          size = int(shard['store'])
          node = f"{shard['node']} - {shard['state']}"
          prim_nodes = list()
          prim_nodes.append(node)
          repl_nodes = list()
          idx[index] = { 'size' : size, 'prim_nodes' : prim_nodes, 'repl_nodes' : repl_nodes }
        elif shard['prirep'] == 'r' :
          size = 0
          node = f"{shard['node']} - {shard['state']}"
          prim_nodes = list()
          repl_nodes = list()
          repl_nodes.append(node)
          idx[index] = { 'size' : size, 'prim_nodes' : prim_nodes, 'repl_nodes' : repl_nodes }
    
    self._print_indices(idx)




        
        



