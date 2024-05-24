# API для получения Wallet Pass (iPhone)

### Описание
API представляет собой приложение, разработанное на Django+REST Framework. Приложение позволяет пользователям создавать и скачивать json объекты, а также zip файлы, в которых могут храниться pass.json, manifest.json (хранятся SHA1-хеши всех файлов в архиве) и jpg.  
Все данные, которые будут отображены в json, заносятся через админ панель, либо отправкой запросов, например через Postman.  
В дальнейшем пользователь должен получить токены аутентфикации в своем ЛК Apple Developer [https://developer.apple.com](https://developer.apple.com), чтобы в дальнейшем создать .pkpass.

## Требования для пользования приложением

Убедитесь, что Docker и Docker-Compose установлены на вашем ПК.


### 1. Склонируйте репозиторий:

    git clone https://github.com/IgChern/wallet_passes

### 2. Перейдите по пути проекта:

    cd wallet_passes

### 3. Создайте файл .env со своими собственными настройками (либо, вы можете оставить .env пустым):

    POSTGRES_NAME=<your_settings>
    POSTGRES_USER=<your_settings>
    POSTGRES_PASSWORD=<your_settings>
    POSTGRES_HOST=<your_settings>
    POSTGRES_PORT=<your_settings>

### 4. Соберите и запустите Docker контейнер, создайте суперпользователя:

    docker-compose build

    docker-compose up

    docker ps

    docker exec -it <ID_pass_proj-django> python manage.py createsuperuser

### 5. Доступ к интерфейсу проекта:  
1. [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/) - Страница API маршрутов
2. [http://127.0.0.1:8000/api/download/<pass_id>/](http://127.0.0.1:8000/api/download/<pass_id>/) - URL для загрузки файла json, указать <pass_id>
3. [http://127.0.0.1:8000/api/downloadzip/<pass_id>/](http://127.0.0.1:8000/api/downloadzip/<pass_id>/) - URL для загрузки zip архива, указать <pass_id>


### 6. Остановка Docker контейнера:

    docker-compose down
