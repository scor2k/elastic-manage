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
*0.3.5*
  - translate

*0.3.4*
  - delete index

*0.3.3*
  - incr добавляем 1 реплику к индексу
  - rename commands (set it shorter)

*0.3.2*
  - fix bug with --force flag 

*0.3.1*
  - index-move --force - для перемещения индекса без подтверждения

*0.3.0*
  - index-move   инициируем переезд индекса в указанный tag 
  - index-wait   ждем переезда индекса
  - урезал вывод логов для большей читаемости

*0.2.0*
  - index-fix    Фиксируем индекс на текущих нодах (где шарды)
  - index-info   показать расположение, привязку и базовые настройки
  - index-reset  удалить все настройки маршрутов (allocation)
  
*0.1.0*
  - Initial release
