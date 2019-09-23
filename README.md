# ELASTICSEARCH MANAGEMENT SYSTEM

## How to use

Usage: main.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  delete  Remove index
  fix     Fix index allocation to the current data nodes.
  incr    Increase replic numbers
  info    Show shard locations, allocation and base settings
  move    Move index to the specific tag
  reset   Remove all allocation settings
  wait    Wait index movement to the new location.

You can create some bash script:
```
$ cat /usr/local/bin/elastic-manage 
#!/bin/sh

cd /opt/elastic-manage
python3 main.py "$@"
```

## Example

`elastic-manage move --index some_index_name --tag-value monolith` - move index to tag: monolith

`elastic-manage incr --index some_index_name` - add one replica to index


## Changelog
*0.3.9*
  - decrease the number of replics

*0.3.8*
  - fixed bug when index in 'unassigned' state

*0.3.7*
  - list -- list only indices on selected data node
  - shards-per-node -- set total shards per node 
  - move-index-from-node -- drain index from selected data node
  - drain-node -- move all indices from selected data node to other

*0.3.6*
  - list -- print indices with shard allocations
  - move cluster settings into $HOME/.config/elastic-manage/settings.json 

*0.3.5*
  - translate

*0.3.4*
  - delete index

*0.1.0*
  - Initial release
