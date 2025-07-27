## Игра "Змейка"

Игрок управляет змейкой, движущейся по полю, так, чтобы она поедала яблоки. После каждого съеденного яблока змейка увеличивается в длине. Задача игрока - не допустить столкновение змейки со своим телом.

Для запуска игры на компьютере клонируйте репозиторий, разверните и активируйте виртуальное окружение
```
git clone git@github.com:mivasilyev/the_snake.git
cd the_snake
python3.9 -m venv venv
source venv/bin/activate
```
установите зависимости
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
и запустите игру
```
python the_snake.py
```