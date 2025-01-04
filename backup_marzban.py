
#developer Lashuk Vladimir
#Version 1.0.0
# Установить библиотеки schedule,psutil
import os
import shutil
from datetime import datetime
import schedule
import time
import getpass
import psutil

# Функция для проверки, запущен ли уже скрипт
def is_already_running():
    script_name = os.path.basename(__file__)
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        if proc.info['name'] == 'python3' and script_name in proc.info['cmdline']:
            if proc.info['pid'] != os.getpid():
                return True
    return False

# Проверка на наличие уже запущенного процесса
if is_already_running():
    print("Script already exists! exit!")
    exit()

# Параметры
username = getpass.getuser()
script_path = os.path.abspath(__file__)
service_name = 'backup_marzban.service'
service_path = f'/etc/systemd/system/{service_name}'

# Проверка на существование файла сервиса
if not os.path.exists(service_path):
    # Содержимое файла сервиса
    service_content = f"""
    [Unit]
    Description=Backup SQLite Database
    After=network.target

    [Service]
    ExecStart=/usr/bin/python3 {script_path}
    Restart=always
    RestartSec=10
    User={username}
    WorkingDirectory={os.path.dirname(script_path)}

    [Install]
    WantedBy=multi-user.target
    """

    # Создание файла сервиса
    with open(service_name, 'w') as service_file:
        service_file.write(service_content)

    # Копирование файла сервиса в /etc/systemd/system/
    os.system(f'sudo mv {service_name} {service_path}')

    # Перезагрузка systemd и включение сервиса
    os.system('sudo systemctl daemon-reload')
    os.system(f'sudo systemctl enable {service_name}')
    os.system(f'sudo systemctl start {service_name}')

    print(f'Service {service_name} create and started.')

else:
    print(f'Service {service_name} already exists.')

# Функция для бэкапа базы данных
def backup_db():
    # Путь к исходной базе данных
    src = '/var/lib/marzban/db.sqlite3'
    # Путь к папке для бэкапов
    dst_folder = '/var/lib/marzban/my_backup'
    # Создание папки для бэкапов, если она не существует
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    # Создание имени файла с текущей датой
    date_str = datetime.now().strftime('%Y-%m-%d')
    dst = os.path.join(dst_folder, f'db_backup_{date_str}.sqlite3')
    
    # Копирование файла
    shutil.copy2(src, dst)
    print(f'Backup created: {dst}')

# Планирование выполнения скрипта каждый день в  18:00, при необходимости  заменить на нужное время
schedule.every().day.at("18:00").do(backup_db)

# Бесконечный цикл для выполнения задач по расписанию
while True:
    schedule.run_pending()
    time.sleep(1)
