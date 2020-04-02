# ELASTICSEARCH MANAGEMENT SYSTEM

## How to install

```
git clone git@github.com:scor2k/elastic-manage.git
cd elastic-manage && python3 -m venv env && source env/bin/activate
pip install -r requirements.txt && pip install -e .
```

## How to use


## Example

*move index to specific data-nodes*
```
./run move-index --cluster elk.cian.tech:8080 --index sa_autotests --nodes log-data12.cian.tech --nodes log-data13.cian.tech --nodes log-data14.cian.tech
```



## Changelog
*1.0.0*
  - added new move-index command (see an example above)
  - removed cluster configuration, you need to put cluster address
  - removed move_index_to_tag command
  - removed index_move_from_node command (replaced by move-index)
  - removed drain_node command (becaus this is uncontrollable)

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
