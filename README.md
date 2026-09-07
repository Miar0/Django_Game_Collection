# Game Collection Tracker

Django-застосунок для ведення власної колекції відеоігор: облік ігрових платформ, статусів проходження, оцінок та особистих відгуків.

## Моделі
- **Platform** — ігрова платформа або сервіс дистрибуції (Steam, Epic Games тощо).
- **Game** — відеогра (зв'язок `ManyToManyField` на модель `Platform`).
- **Review** — картка відгуку та прогресу гри (`ForeignKey` на модель `Game`), що містить оцінку від 1 до 10, випадаючий список статусів (`choices`), текстовий коментар і дату створення (`DateTimeField`).

---

## Prerequisites & Package Manager

This project exclusively uses **uv**, a blazingly fast Python package manager written in Rust. Before starting, check if you have it installed:

```bash
uv --version
```

### Installing uv (If not installed)

If the command above is not recognized, install `uv` using one of the following official methods for your OS:

* **macOS / Linux:**

```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

* **Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm [https://astral.sh/uv/install.ps1](https://astral.sh/uv/install.ps1) | iex"
```

---

## Quick Start

Setting up the project environment takes just a single command.

1. **Install all dependencies and setup environment:**

```bash
uv sync
```

*This command automatically creates an isolated virtual environment (`.venv`) and installs all project dependencies.*

2. **Activate the virtual environment:**

* **Windows (Command Prompt):**

```cmd
.venv\Scripts\activate
```


* **macOS / Linux:**

```bash
source .venv/bin/activate
```

---

## Database Setup & Run

1. **Застосувати міграції:**

```bash
python manage.py migrate
```

2. **Створити суперкористувача для адмінки:**

```bash
python manage.py createsuperuser
```

3. **Запустити локальний сервер:**

```bash
python manage.py runserver
```

Панель керування доступна за адресою: `http://127.0.0.1:8000/admin/`

4. **Запустити демонстраційний скрипт з ORM-запитами:**

```bash
python queries.py
```

---

## Скріншоти адмінки

### Платформи
![Platforms](screenshots/img.png)

### Ігри
![Games](screenshots/img_1.png)

### Відгуки
![Reviews](screenshots/img_2.png)