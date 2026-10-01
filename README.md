# Life Quests — переизобретение

Превращаем личные цели в RPG: мейн-квесты, сайд-квесты, боссы, опыт, уровни и характеристики.  
Клиент на Flutter (Windows / macOS / Linux / Android), бэкенд на FastAPI, база на PostgreSQL, всё в Docker.

---

## Стек

| Слой | Технология | Зачем |
|------|-----------|-------|
| **Клиент** | Flutter (Dart) | Один код на все платформы |
| **Бэкенд** | Python 3.12 + FastAPI | Простота, автодокументация, асинхронность |
| **ORM** | SQLAlchemy 2.0 (async) + Alembic | Работа с БД и миграции |
| **База** | PostgreSQL 16 | Надёжность, JSONB, полнотекстовый поиск |
| **Аутентификация** | JWT (python-jose) | Просто и работает на всех клиентах |
| **Развёртывание** | Docker + Docker Compose | Одна команда для запуска |
| **Хостинг** | VPS (Timeweb / Aeza / Hetzner) | ~300–500 ₽/мес |

---

## Архитектура

```

┌─────────────────────────────────────────────┐
│         Flutter App (один код)              │
│   Windows / macOS / Linux / Android         │
└──────────────────┬──────────────────────────┘
│ HTTP / JSON
▼
┌─────────────────────────────────────────────┐
│         FastAPI Backend (Python)            │
│    REST API + бизнес-логика + JWT           │
└──────────────────┬──────────────────────────┘
│
▼
┌─────────────────────────────────────────────┐
│         PostgreSQL Database                 │
│         (на сервере, Docker)                │
└─────────────────────────────────────────────┘

```

**Принцип:** клиент отправляет намерение («отметить главу»), сервер считает всё сам и возвращает новое состояние целиком. Клиент ничего не досчитывает.

---

## Структура репозитория

```

life-quests/
├── backend/
│   ├── app/
│   │   ├── main.py              # точка входа FastAPI
│   │   ├── config.py            # настройки из окружения
│   │   ├── db.py                # подключение к PostgreSQL
│   │   ├── models/              # SQLAlchemy модели
│   │   ├── schemas/             # Pydantic схемы
│   │   ├── api/                 # роутеры
│   │   │   ├── auth.py
│   │   │   ├── quests.py
│   │   │   ├── chapters.py
│   │   │   ├── profile.py
│   │   │   └── archive.py
│   │   ├── services/            # бизнес-логика
│   │   │   ├── xp.py
│   │   │   └── periods.py       # повторяющиеся квесты
│   │   └── core/
│   │       ├── security.py      # JWT
│   │       └── deps.py          # зависимости
│   ├── alembic/                 # миграции
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── client/                      # Flutter
│   ├── lib/
│   │   ├── main.dart
│   │   ├── app.dart
│   │   ├── core/
│   │   │   ├── api_client.dart  # HTTP + JWT
│   │   │   └── storage.dart     # secure storage
│   │   ├── models/              # Dart-модели
│   │   ├── providers/           # Riverpod
│   │   ├── screens/
│   │   │   ├── hero_screen.dart
│   │   │   ├── mains_screen.dart
│   │   │   ├── bosses_screen.dart
│   │   │   ├── sides_screen.dart
│   │   │   ├── archive_screen.dart
│   │   │   └── settings_screen.dart
│   │   └── widgets/             # переиспользуемые виджеты
│   ├── pubspec.yaml
│   └── analysis_options.yaml
│
├── .env.example
├── .gitignore
└── README.md

```

---

## Этапы разработки

### Этап 1. Бэкенд: база и модели

**Цель:** развернуть PostgreSQL, описать схему, поднять FastAPI.

- [ ] **Docker Compose:** PostgreSQL + pgAdmin (для удобства)
- [ ] **Схема БД:** `profile`, `quests`, `chapters`, `events`, `archive`
- [ ] **SQLAlchemy модели:** отношения, каскады, индексы
- [ ] **Alembic:** первая миграция
- [ ] **FastAPI:** запуск, health-check, Swagger

**Доки:**
- [FastAPI — Getting Started](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 — Async ORM](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic — Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [PostgreSQL 16 — Documentation](https://www.postgresql.org/docs/16/)

---

### Этап 2. Бэкенд: игровая логика

**Цель:** перенести правила из оригинального проекта — опыт, уровни, закрытие квестов, повторения.

- [ ] **XP:** пороги уровней, очки характеристик, прогресс
- [ ] **Мейн-квесты:** главы, подшаги, закрытие родителя, бонус
- [ ] **Сайд-квесты:** галочка, серия, повторения (день/неделя/месяц)
- [ ] **Боссы:** удары, здоровье, победа
- [ ] **Архив:** закрытые и удалённые, восстановление, снятие бонуса
- [ ] **Журнал событий:** коды и параметры (без готовых фраз)
- [ ] **Валидация:** лимиты полей, проверка типов

**Доки:**
- [FastAPI — Request Body](https://fastapi.tiangolo.com/tutorial/body/)
- [Pydantic — Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [SQLAlchemy — Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)

---

### Этап 3. Бэкенд: API и аутентификация

**Цель:** REST-эндпоинты с JWT, готовые для Flutter.

- [ ] **Регистрация/логин:** email + пароль, bcrypt, JWT
- [ ] **Middleware:** проверка токена на защищённых роутах
- [ ] **Эндпоинты:**
  - `GET /api/state` — всё состояние
  - `POST /api/quests` — создать
  - `POST /api/quests/{id}/chapters` — добавить главу
  - `POST /api/quests/{id}/toggle` — сайд
  - `POST /api/quests/{id}/hit` — удар по боссу
  - `POST /api/chapters/{id}/toggle` — глава
  - `POST /api/archive/{id}/restore` — вернуть
  - `POST /api/profile` — настройки
- [ ] **Тесты:** pytest + httpx, живой сервер на свободном порту

**Доки:**
- [FastAPI — Security](https://fastapi.tiangolo.com/tutorial/security/)
- [python-jose — JWT](https://python-jose.readthedocs.io/)
- [passlib — bcrypt](https://passlib.readthedocs.io/)
- [FastAPI — Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest — Documentation](https://docs.pytest.org/)

---

### Этап 4. Flutter: основы и первый экран

**Цель:** запустить Flutter на десктопе и Android, сделать экран героя.

- [ ] **Установка Flutter SDK** (Windows / macOS / Linux)
- [ ] **Настройка VS Code** + Dart/Flutter extensions
- [ ] **Dart crash course:** переменные, функции, классы, async/await, Future
- [ ] **Flutter basics:** виджеты, StatelessWidget vs StatefulWidget, Row/Column, ListView
- [ ] **Первый экран:** лист героя (имя, уровень, XP-бар, характеристики)
- [ ] **API-клиент:** HTTP-запросы, JSON-парсинг, JWT-токен

**Доки:**
- [Flutter — Getting Started](https://docs.flutter.dev/get-started/install)
- [Dart — Language Tour](https://dart.dev/language)
- [Flutter — Widget Catalog](https://docs.flutter.dev/ui/widgets)
- [Dart — Async/Await](https://dart.dev/codelabs/async-await)

---

### Этап 5. Flutter: все экраны

**Цель:** мейн-квесты, сайд-квесты, боссы, архив, журнал.

- [ ] **Мейн-квесты:** список, главы, подшаги, чекбоксы
- [ ] **Сайд-квесты:** список, галочка, серия, повторения
- [ ] **Боссы:** полоса здоровья, кнопка удара, фазы
- [ ] **Архив:** список, восстановление, удаление
- [ ] **Журнал:** список событий с иконками/кодами
- [ ] **Настройки:** имя, язык, тема

**Доки:**
- [Flutter — Navigation](https://docs.flutter.dev/ui/navigation)
- [Flutter — Forms](https://docs.flutter.dev/cookbook/forms)
- [Riverpod — Documentation](https://riverpod.dev/)
- [dio — HTTP client](https://pub.dev/packages/dio)

---

### Этап 6. Синхронизация и офлайн

**Цель:** приложение работает без сети, синхронизируется при подключении.

- [ ] **Локальное хранилище:** SQLite (sqflite / drift) или Hive
- [ ] **Стратегия:** last-write-wins для простоты
- [ ] **Очередь изменений:** отложенные запросы при офлайне
- [ ] **Индикатор статуса:** online / offline / syncing

**Доки:**
- [drift — SQLite для Dart](https://drift.simonbinder.eu/)
- [Hive — Key-value storage](https://docs.hivedb.dev/)
- [connectivity_plus — проверка сети](https://pub.dev/packages/connectivity_plus)

---

### Этап 7. Docker и деплой

**Цель:** всё работает на VPS, доступно отовсюду.

- [ ] **Dockerfile для FastAPI:** multi-stage build
- [ ] **Docker Compose:** api + db + nginx (опционально)
- [ ] **VPS:** SSH, firewall, домен (опционально)
- [ ] **Автодеплой:** GitHub Actions → сборка образа → push → pull на VPS
- [ ] **Бэкапы:** pg_dump по расписанию

**Доки:**
- [Docker — Get Started](https://docs.docker.com/get-started/)
- [Docker Compose — Reference](https://docs.docker.com/compose/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)
- [GitHub Actions — Documentation](https://docs.github.com/en/actions)

---

### Этап 8. Полировка

**Цель:** приятно пользоваться, не стыдно показать.

- [ ] **Тема:** тёмная / светлая, 90-е (как в оригинале) опционально
- [ ] **Иконки и анимации:** мелочи, которые радуют
- [ ] **Уведомления:** напоминания о сроках, днях повторений
- [ ] **Виджеты Android:** быстрая отметка сайд-квеста
- [ ] **Сборка релизов:** APK для Android, exe/msi/dmg для десктопа

---

## Ссылки на всё

### Dart

| Ресурс | Ссылка |
|--------|--------|
| Официальный сайт | https://dart.dev/ |
| Language Tour | https://dart.dev/language |
| API Docs | https://api.dart.dev/ |
| DartPad (песочница) | https://dartpad.dev/ |
| METANIT (рус.) | https://metanit.com/dart/tutorial/ |
| GitHub-конспект (рус.) | https://github.com/mkos11/dart-course |
| Книга «Основы Dart» | ISBN 978-5-4461-4168-5 |

### Flutter

| Ресурс | Ссылка |
|--------|--------|
| Официальная документация | https://docs.flutter.dev/ |
| Widget Catalog | https://docs.flutter.dev/ui/widgets |
| Cookbook (рецепты) | https://docs.flutter.dev/cookbook |
| Хендбук Яндекса (рус.) | https://education.yandex.ru/handbook/flutter |
| Roadmap (рус.) | https://github.com/p0dyakov/flutter_roadmap |
| Pub.dev (пакеты) | https://pub.dev/ |

### Бэкенд

| Ресурс | Ссылка |
|--------|--------|
| FastAPI | https://fastapi.tiangolo.com/ |
| SQLAlchemy 2.0 | https://docs.sqlalchemy.org/en/20/ |
| Alembic | https://alembic.sqlalchemy.org/ |
| PostgreSQL 16 | https://www.postgresql.org/docs/16/ |
| Pydantic | https://docs.pydantic.dev/ |

### Инфраструктура

| Ресурс | Ссылка |
|--------|--------|
| Docker | https://docs.docker.com/ |
| Docker Compose | https://docs.docker.com/compose/ |
| GitHub Actions | https://docs.github.com/en/actions |
| Riverpod (state) | https://riverpod.dev/ |
| dio (HTTP) | https://pub.dev/packages/dio |
| drift (SQLite) | https://drift.simonbinder.eu/ |

---

## Правила игры (из оригинала)

- **Туман.** Мейн-квест без шагов не даёт опыта и рисуется пунктиром.
- **Шаги вкладываются на один уровень.** Шаг с подшагами закрывается сам, когда все подшаги отмечены.
- **Босс — это серия ударов.** Один удар = одно реальное действие. Галочкой не закрыть.
- **Привал.** Пропустил неделю — серия замерзает, ничего не сгорает.
- **Повторение — это ритм.** Сайд-квест возвращается каждый N дней/недель/месяцев. Серия держится, пока закрываешь вовремя.
- **Опыт вычисляется, а не хранится.** Снял галочку — вернулось ровно то состояние, что было.
- **Ничего сделанного не теряется.** Закрытые и удалённые квесты оседают в архиве, откуда их можно вернуть.

---

## Лицензия

MIT
