# **Проект «Продуктовый помощник»**

### **Описание**
Продуктовый помщник это онлайн сервис, с возможностью делиться рецептами с другими пользователями.
Добавлять посты с картинками, подписыватся на других пользователей, а так же добавлять рецепты в избранное.

### **Как запустить проект:**
Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://git@github.com:Kirill-Bovin/foodgram-project-react.git
```
Перейти в репозиторий с проектом:
```
cd foodgram-project-react
```

Cоздать и активировать виртуальное окружение:
```
python -m venv env
```
```
source env/scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Перейти в репозиторий backend:
```
cd backend
```
Выполнить миграции:
```
python manage.py migrate
```
Запустить проект:
```
python manage.py runserver
```
### **Как задеплоить проект:**
Подключитесь к серверу:
```
ssh -i 
```
Скопируйте файлы docker-compose.production.yml в папку foodgram:
```
scp -i path_to_SSH/SSH_name docker-compose.production.yml \
    username@server_ip:/home/username/foodgram-project-react/docker-compose.production.yml 
```
Из папки foodgram запустисте проект
```
sudo docker compose -f docker-compose.production.yml up -d 
```
Запустите миграции:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```
Соберите статику:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --noinput
```
Загрузите ингрдиенты:
```
sudo docker compose exec backend python manage.py load_to_base
```
Данные сайта:
```
Доменное имя: foodgram9669.hopto.org

Супеюзер
Почта: Skrill96@e1.ru
Пароль: Abs12345678
```

### Автор:
Студент Яндекс.практикум: Бовин Кирилл Викторович.