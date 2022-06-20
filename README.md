# Яндекс.Практикум

## Проект YaMDb

### Авторы - студенты факультета Python-разработки плюс, Когорта №10+
Иван

Павел Маковкин

Анастасия Домнина

***


## Оглавление

0. [Задача](#Задача)
1. [Разворачивание проекта](#Разворачивание-проекта)
2. [Основные команды для работы с ветками](#Основные-команды-для-работы-с-ветками)
3. [Пользовательские роли](#Пользовательские-роли)
4. [Ресурсы API YaMDb](#Ресурсы-API-YaMDb)
***


## Задача

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.

Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число; из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

***


## Разворачивание проекта

Клонировать репозиторий и перейти в его папку в командной строке:

```
git clone https://github.com/foxygen-d/api_yamdb.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```
Активировать виртуальное окружение:
```
source env/bin/activatepython3 -m venv env
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
***


## Основные команды для работы с ветками
`git branch <название_ветки>` — создать новую ветку

`git checkout <название_ветки>` — переключиться в ветку

`git checkout -b <название_ветки>` — создать ветку и сразу переключиться в неё

`git branch -d <название_ветки>` — удалить ветку (чтобы всё прошло хорошо, нужно переключиться из удаляемой ветки)

`git merge <название_ветки>` — скопировать все изменения из ветки в ветку (чтобы перенести изменения из ветки `develop` в ветку `master`, нужно находиться в ветке `master` и выполнить команду `git merge develop`)
***


## Пользовательские роли

- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **Администратор (admin)** — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.
***


## Ресурсы API YaMDb
- Ресурс **auth**: аутентификация.
- Ресурс **users**: пользователи.
- Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
- Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.
***

[:arrow_up:Оглавление](#Оглавление)
