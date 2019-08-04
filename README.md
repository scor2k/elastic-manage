# ELASTICSEARCH MANAGEMENT SYSTEM


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
