
# 🏠 Rental Housing API (Django)

A full-featured backend API for a housing rental platform in Germany, built with Django and DRF.

---

## 📌 Project Goals

- Manage property listings (CRUD) with status control (`active`/`inactive`)  
- Advanced search & filtering by:  
  - Keywords (title/description)  
  - Price range  
  - City (in Germany)  
  - Number of rooms  
  - Housing type (apartment, house, studio, etc.)  
- Sorting by price or date  
- User roles: **Tenant** vs **Landlord**  
- Booking system with confirmation flow  
- Reviews & ratings **only after completed booking**  
- Search history & view history  
- Popular listings based on views  
- RESTful API with JWT authentication  
- OpenAPI (Swagger) documentation  
- MySQL as main database  
- Docker containerization  
- Deployment-ready for AWS EC2  

---

## 🛠️ Technologies Used

- **Backend**: Python 3, Django 5.2, Django REST Framework  
- **Authentication**: JWT (via `djangorestframework-simplejwt`)  
- **Database**: MySQL (production), SQLite (development)  
- **API Docs**: `drf-spectacular` (OpenAPI 3.0 + Swagger UI)  
- **Deployment**: Docker, Docker Compose  
- **Cloud**: AWS EC2 (planned)  
- **Other**: `django-environ` for `.env` management  

---

## 📂 Project Structure

```
ich_django_final_project/
├── apps/
│   ├── users/          # Custom User model, registration
│   ├── listings/       # Property listings, search, filters
│   ├── bookings/       # Booking logic
│   ├── reviews/        # Reviews with validation
│   ├── history/        # Search & view history
│   └── common/         # Shared permissions (IsLandlord, IsOwner)
├── utils/              # Helpers
├── manage.py
├── requirements.txt
├── .env.example
├── .env                # ← not in Git!
├── Dockerfile
├── docker-compose.yml  # ← if implemented
└── ...
```

---

## ⚙️ Setup and Run

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rental-housing-api.git
cd rental-housing-api
```

### 2. Create virtual environment & install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and fill in your secrets:

```ini
# .env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=127.0.0.1,localhost

# MySQL (optional)
MYSQL=False
DB_NAME=rental_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

> 🔒 Never commit `.env` to Git!

### 4. Run migrations & start server

```bash
python manage.py migrate
python manage.py runserver
```

### 5. Explore the API

- **Swagger UI**: http://127.0.0.1:8000/api/docs/  
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

---

## 🔐 Authentication

- Register: `POST /api/v1/users/register/`  
- Login: returns JWT access/refresh tokens  
- Protected endpoints require `Authorization: Bearer <token>`  

---

## 📊 Example Review Validation Logic

A user can leave a review **only if**:
- They are authenticated  
- They have a **completed booking** for that listing  
- The booking’s `end_date` is in the past  

This is enforced in `ReviewSerializer.validate_booking()`.

---

## 🚀 Deployment (Planned)

- ✅ Dockerized app (`Dockerfile` + `docker-compose.yml`)  
- ✅ Runs on AWS EC2 with MySQL RDS  
- ✅ Environment variables managed via `.env` on server  

> ⚠️ Not yet implemented? Add it before final submission!

---

## 🤝 Author: Alexander Pankow

This project was created as the **final assignment** for the **Python Advanced** course at ITCareerHub.de.

---

<br><hr><br>

# 🏠 API для системы аренды жилья (Django)

Полнофункциональный бэкенд для платформы аренды жилья в Германии на Django и DRF.

---

## 📌 Цели проекта

- Управление объявлениями (CRUD) со статусом (`активно`/`неактивно`)  
- Расширенный поиск и фильтрация по:  
  - Ключевым словам (в заголовке/описании)  
  - Диапазону цены  
  - Городу (в Германии)  
  - Количеству комнат  
  - Типу жилья (квартира, дом, студия и т.д.)  
- Сортировка по цене или дате добавления  
- Разделение ролей: **Арендатор** и **Арендодатель**  
- Система бронирования с подтверждением  
- Отзывы и рейтинги **только после завершённого бронирования**  
- История поиска и просмотров  
- Популярные объявления по количеству просмотров  
- REST API с JWT-аутентификацией  
- Документация OpenAPI (Swagger)  
- MySQL как основная БД  
- Контейнеризация через Docker  
- Готовность к развёртыванию на AWS EC2  

---

## 🛠️ Используемые технологии

- **Бэкенд**: Python 3, Django 5.2, Django REST Framework  
- **Аутентификация**: JWT (`djangorestframework-simplejwt`)  
- **База данных**: MySQL (продакшен), SQLite (разработка)  
- **Документация**: `drf-spectacular` (OpenAPI 3.0 + Swagger UI)  
- **Деплой**: Docker, Docker Compose  
- **Облако**: AWS EC2 (в планах)  
- **Прочее**: `django-environ` для управления `.env`  

---

## ⚙️ Установка и запуск

(Аналогично английской версии — все команды идентичны)

> 💡 Все инструкции идентичны — просто переведите при необходимости.

---

## 🤝 Автор: Александр Панков

Проект выполнен как **финальная работа** по курсу **Python Advanced** в ITCareerHub.de.

---

<br><hr><br>

# 🏠 Rental Housing API (Django)

Ein vollständiges Backend-API für eine Wohnungsvermietungsplattform in Deutschland, entwickelt mit Django und DRF.

---

## 📌 Projektziele

- Verwaltung von Wohnungsanzeigen (CRUD) mit Status (`aktiv`/`inaktiv`)  
- Erweiterte Suche & Filterung nach:  
  - Stichworten (Titel/Beschreibung)  
  - Preisspanne  
  - Stadt (in Deutschland)  
  - Anzahl der Zimmer  
  - Wohnungsart (Wohnung, Haus, Studio usw.)  
- Sortierung nach Preis oder Datum  
- Benutzerrollen: **Mieter** vs **Vermieter**  
- Buchungssystem mit Bestätigungsprozess  
- Bewertungen & Sterne **nur nach abgeschlossener Buchung**  
- Suchverlauf & Ansichtsverlauf  
- Beliebte Wohnungen basierend auf Aufrufen  
- RESTful API mit JWT-Authentifizierung  
- OpenAPI-Dokumentation (Swagger)  
- MySQL als Hauptdatenbank  
- Containerisierung mit Docker  
- Bereit für Bereitstellung auf AWS EC2  

---

## 🛠️ Verwendete Technologien

- **Backend**: Python 3, Django 5.2, Django REST Framework  
- **Authentifizierung**: JWT (`djangorestframework-simplejwt`)  
- **Datenbank**: MySQL (Produktion), SQLite (Entwicklung)  
- **API-Dokumentation**: `drf-spectacular` (OpenAPI 3.0 + Swagger UI)  
- **Deployment**: Docker, Docker Compose  
- **Cloud**: AWS EC2 (geplant)  
- **Sonstiges**: `django-environ` für `.env`-Verwaltung  

---

## ⚙️ Einrichtung und Ausführung

(Identisch zur englischen Version)

---

## 🤝 Autor: Alexander Pankow

Dieses Projekt wurde als **Abschlussarbeit** für den **Python Advanced**-Kurs bei ITCareerHub.de erstellt.
