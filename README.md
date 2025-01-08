# backup_marzban_db

 Этот скрипт на Python выполняет автоматическое резервное копирование базы данных SQLite для marzban и настраивает `systemd` сервис для его автоматического запуска и перезапуска в случае ошибки.
## Зависимости
pip install schedule,psutil

## Описание
 Скрипт выполняет следующие задачи:
 1. Проверяет, запущен ли уже экземпляр скрипта, чтобы избежать дублирования.
 2. Создает и настраивает сервис для автоматического запуска скрипта.
 3. Выполняет резервное копирование, раз  в сутки,  базы данных SQLite каждый день в 18:00(время можно изменить в коде скрипта).

## Установка
 1.Установите python библиотеки:  
   >pip install psutil  
   >pip install schedule  

 2.Перейдите в папку:  
   >cd /var/lib/marzban
   
 3.Скачайте скрипт:  
   >wget https://raw.githubusercontent.com/Vladimirlashuk/backup_marzban_db/refs/heads/main/backup_marzban.py
   
 4.Запустите скрипт:  
   >python3 backup_marzban.py

## Команды
 >systemctl stop/status/start backup_marzban.service

## Log  
>journalctl -u backup_marzban.service
 

