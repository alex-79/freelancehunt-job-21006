* https://freelancehunt.com/job/napisannya-parseriv-na-python-dlya-zboru/21006.html

# Завдання

Написати скрипт, який заходить на головну сторінку сайту. Дивиться та парсить категорії продуктів. Заходить на кожен продукт, зчитує відгуки та зберігає у файл формату JSON. Від кожного відгуку зберегти: текст відгуку, оцінка, автора, дату та іншу наявну інформацію.

На виході файли формату JSON. В одному файлі JSON зберігаються відгуки про один продукт.

Не використовувати регулярні вирази.

# INSTALL

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install lxml
python3 -m pip install bs4
python3 -m pip install requests
```