# Репозиторий микросервиса для хранения и обновления информации о собаках для ветклиники

Сервис предоставляет API для хранения и обновления информации о собаках.
Реализуются такие функции, как:
- создание информации о собаке
- получение информации о собаке
- обновление информации о собаке
- получение списка собак

В качестве хранилища используется реляционная СУБД PostgreSQL (версия 14).
Для деплоя приложения используется Docker.


## Авторы
[Елена Шек](https://github.com/alexxten)

## Запуск проекта

Чтобы стартовать этот проект следуйте инструкции ниже:

1. Клонируйте репозиторий с source-кодом и перейдите в него
```
https://github.com/alexxten/vet-clinic-dogs-service.git
```
или gitlab
```
https://gitlab.com/mlds13/vet-clinic-dogs-service.git
```
далее перейдите в директорию с кодом
```
cd vet-clinic-dogs-service
```
2. Заполните файл с переменными окружения variables.env, необходимыми для сервиса

3. Стартуйте приложение средствами Docker
```
docker-compose up
```
или для старта в detached-режиме
```
docker-compose up -d
```
4. После этого сервис стартует на порту 8000. Его сваггер доступен по эндпоинту `/docs`
