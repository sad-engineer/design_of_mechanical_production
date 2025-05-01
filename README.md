# Design of Mechanical Production

Приложение запустится в выбранном режиме (GUI или консольном).

`design_of_mechanical_production` - это пакет Python, содержащий расчет площади цеха.

Проект сделан в начале изучения Python. В связи с этим, предыдущие коммиты не сохранились, а техника языка весьма
примитивна.
Тем не менее проект, даже в таком виде использовался в коммерции (с помощью пакета делал расчеты на фрилансе).

Проект демонстрирует умение применить программирование для извлечения прибыли, автоматизировать рутинные задачи.

## Управление режимом запуска

### Команды для управления режимом запуска

Для управления режимом запуска приложения используйте скрипт `launch_manager.py`:

```bash
# Показать текущие настройки запуска
python -m design_of_mechanical_production.launch_manager show

# Установить режим GUI
python -m design_of_mechanical_production.launch_manager gui

# Установить консольный режим
python -m design_of_mechanical_production.launch_manager console

# Установить светлую тему
python -m design_of_mechanical_production.launch_manager theme light

# Установить темную тему
python -m design_of_mechanical_production.launch_manager theme dark
```

### Запуск приложения

После настройки режима запустите приложение:

```bash
python -m design_of_mechanical_production.main
```

## Настройка параметров расчета

Для настройки параметров расчета используйте:
- `manager.py` - скрипт для управления настройками расчета
- `settings.yaml` - файл с параметрами расчета
