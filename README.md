# 📝 Task Manager

Aplikacja webowa do zarządzania zadaniami. Pozwala użytkownikom na tworzenie kont, logowanie się, dodawanie, edytowanie i oznaczanie zadań jako wykonane, edycję profilu oraz usuwanie konta.

---

## 📆 Spis treści

- [📖 Wstęp](#-wstęp)
- [📦 Architektura aplikacji](#-architektura-aplikacji)
- [🚀 Jak uruchomić aplikację lokalnie](#-jak-uruchomić-aplikację-lokalnie)
- [⚙️ Zmienne środowiskowe](#⚙️-zmienne-środowiskowe)
- [📅 Dalsze kroki](#-dalsze-kroki)

---

## 📖 Wstęp

Task Manager to pełnoprawna aplikacja webowa do zarządzania zadaniami. Projekt składa się z:

- **Frontend**: Vite + React + TypeScript
- **Backend**: Flask + SQLAlchemy
- **Baza danych** (obsługuje bazy MySQL i SQLite)

Funkcjonalności:

- Rejestracja i logowanie użytkowników
- Tworzenie, edycja, usuwanie zadań
- Oznaczanie zadań jako wykonane/niewykonane
- Edycja danych profilu
- Zmiana hasła i usuwanie konta

---

## 📦 Architektura aplikacji

### 🔌 Frontend

- Framework: React
- Komunikacja z API: Axios

### 💻 Backend / API

- Framework: Flask
- ORM: SQLAlchemy
- Autoryzacja: JWT + CSRF + Cookies

### 📊 Baza danych

- SQLite (dla developmentu) lub MySQL (zalecane na produkcji)

---

## 🚀 Jak uruchomić aplikację lokalnie

### ✅ Wymagania

- Python 3.10+
- Node.js + npm
- (opcjonalnie) Docker

### 🔧 Backend

Zanim uruchomisz backend, ustaw zmienną do połączenia z bazą danych w następujący sposób:
1) Jeśli zamierzasz wykorzystać MySQL:
- SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://<nazwa_uzytkownika>:<haslo>@<nazwa_hosta_bazy_danych>:<port_bazy_danych>/<nazwa_bazy_danych>
2) Jeśli zamierzasz skorzystać z SQLite:
- SQLALCHEMY_DATABASE_URI=sqlite:///test.db

1. Stwórz i aktywuj wirtualne środowisko:
   ```bash
   cd api
   python -m venv venv
   source venv/bin/activate
   ```
2. Zainstaluj zależności:
   ```bash
   pip install -r requirements.txt
   ```
3. Uruchom serwer:
   ```bash
   python3 app.py
   ```

### 🖥️ Frontend

1. Przejdź do folderu `frontend`:
   ```bash
   cd frontend
   ```
2. Zainstaluj zależności:
   ```bash
   npm install
   ```
3. Uruchom frontend:
   ```bash
   npm run dev
   ```

---

## ⚙️ Zmienne środowiskowe

Poniżej lista zmiennych środowiskowych dla backendu:

| Nazwa                     | Wymagana | Opis                                                                                             |
| ------------------------- | -------- | ------------------------------------------------------------------------------------------------ |
| `SQLALCHEMY_DATABASE_URI` | ✅        | URI do bazy danych SQLite lub MySQL                             |
| `JWT_SECRET_KEY`          | ❌        | Klucz JWT używany do podpisywania tokenów (zalecane)                                             |
| `TODOLIST_PORT`                | ❌        | Port, na którym uruchamia się API (domyślnie 80)                                                                |
| `TODOLIST_ADMIN_USERNAME` | ❌        | Nazwa użytkownika będącego domyślnym administratorem obecnym w bazie po inicjalizacji aplikacji (domyślnie admin). |
| `TODOLIST_ADMIN_EMAIL` | ❌        | Adres email domyślnego administratora aplikacji (domyślnie admin@example.pl). |
| `TODOLIST_ADMIN_PASSWORD` | ❌        | Hasło domyślnego administratora aplikacji (zalecane). |
| `FRONTEND_ORIGIN`         | ✅        | Adres URL frontendu (np. `http://localhost:5173`) do ustawienia CORS/cookies (wymagany do połączenia frontendu z API, jeśli działają one w osobnych domenach, można podać więcej adresów rozdzielając je przecinkiem)                    |

Poniżej lista zmiennych środowiskowych dla frontendu:
| Nazwa                     | Wymagana | Opis                                                                                             |
| ------------------------- | -------- | ------------------------------------------------------------------------------------------------ |
| `VITE_API_URL`            | ✅       | Adres URL backendu, z którym komunikuje się frontend. Ustawiany w pliku `frontend/frontend.dockerfile` przed zbudowaniem kontenera. Domyślnie `/api`, wartość tę zmień tylko, jeśli zamierzasz uruchomić backend nie wykorzystując Dockera lub poza siecią frontendu. |
---

## 📅 Dalsze kroki

- Przygotowanie stylów CSS dla aplikacji

---

Autor: *Marcin Ramotowski*\
Licencja: MIT

---
