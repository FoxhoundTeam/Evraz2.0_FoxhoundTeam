# Хакатон Evraz2.0, 17-19 февраля 2023, решение команды Foxhound
# FoxControl

# Инструкция по запуску

Демо решение расположено по адресу [foxhound-team.pro](https://foxhound-team.pro)

Для запуска локально, см. [Развертывание через docker-compose](#развертывание-через-docker-compose)

Документация по API доступна по пути [foxhound-team.pro/docs](https://foxhound-team.pro/docs)

# Развертывание через docker-compose
1. Установить [docker](https://docs.docker.com/engine/install/ubuntu/)
2. В папке compose создать файл .env и [заполнить](#описание-переменных-окружения) его в соответствии с примерами (.env.example)
3. Запустить команду docker compose up -d с правами суперпользователя
```bash
sudo docker compose up -d
```
5. Настроить внешний nginx, который будет пересылать все запросы на порт приложения

# Описание переменных окружения

## HTTP_PORT
Файлы: .env

Тип: целое число

Назначение: порт на котором будет крутиться приложение
## KAFKA_PASSWORD
Файлы: .env

Тип: строка

Назначение: пароль для kafka

# Команды docker-compose 
Все команды необходимо выполнять в папке compose
- Остановить все контейнеры
```bash
sudo docker-compose stop
```
- Перезапустить контейнер
```bash
sudo docker-compose restart {container_name}
```
- Запуск ipython
```bash
sudo docker-compose exec backend ipython
```

