-- ============================================================
--  Ascend — схема базы данных
--  PostgreSQL 16
-- ============================================================

-- ------------------------------------------------------------
--  users — аккаунты для входа
-- ------------------------------------------------------------
CREATE TABLE users (
  id              BIGSERIAL     PRIMARY KEY,
  login           VARCHAR(50)   NOT NULL UNIQUE,
  password_hash   VARCHAR(255)  NOT NULL,
  status          VARCHAR(20)   NOT NULL DEFAULT 'active',
  role            VARCHAR(20)   NOT NULL DEFAULT 'client',
  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

  CONSTRAINT users_status_check
    CHECK (status IN ('active', 'blocked', 'deleted')),

  CONSTRAINT users_role_check
    CHECK (role IN ('client', 'admin')),

  CONSTRAINT users_login_check
    CHECK (login ~ '^[a-zA-Z0-9_]{3,50}$')
);

CREATE INDEX users_status_idx ON users (status) WHERE status = 'active';


-- ------------------------------------------------------------
--  characters — игровой профиль
--  Один к одному с users
-- ------------------------------------------------------------
CREATE TABLE characters (
  id              BIGSERIAL     PRIMARY KEY,
  user_id         BIGINT        NOT NULL UNIQUE
                                REFERENCES users(id) ON DELETE CASCADE,

  name            VARCHAR(40)   NOT NULL,
  xp_total        INTEGER       NOT NULL DEFAULT 0,

  -- Очки характеристик. Названия живут в i18n, здесь только ключи.
  strength        INTEGER       NOT NULL DEFAULT 0,
  health          INTEGER       NOT NULL DEFAULT 0,
  resolve         INTEGER       NOT NULL DEFAULT 0,
  craft           INTEGER       NOT NULL DEFAULT 0,
  bonds           INTEGER       NOT NULL DEFAULT 0,

  -- Привал замораживает серию, не сбрасывая её
  resting         BOOLEAN       NOT NULL DEFAULT FALSE,
  rest_started_at TIMESTAMPTZ,

  -- UI-настройки
  skin            VARCHAR(20)   NOT NULL DEFAULT 'win98',
  lang            VARCHAR(5)    NOT NULL DEFAULT 'ru',
  intro_seen      BOOLEAN       NOT NULL DEFAULT FALSE,

  -- Произвольные JSON-настройки (раскладка окон, блокнот и т.д.)
  settings        JSONB         NOT NULL DEFAULT '{}'::jsonb,

  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

  CONSTRAINT characters_xp_check
    CHECK (xp_total >= 0),

  CONSTRAINT characters_stats_check
    CHECK (strength >= 0 AND health >= 0 AND resolve >= 0
           AND craft >= 0 AND bonds >= 0),

  CONSTRAINT characters_name_check
    CHECK (length(trim(name)) > 2)
);


-- ------------------------------------------------------------
--  global_quests — большие цели
--  Живут фоном, в «Сегодня» сами не попадают
-- ------------------------------------------------------------
CREATE TABLE global_quests (
  id              BIGSERIAL     PRIMARY KEY,
  character_id    BIGINT        NOT NULL
                                REFERENCES characters(id) ON DELETE CASCADE,

  title           VARCHAR(120)  NOT NULL,
  why             TEXT          NOT NULL DEFAULT '',  -- «зачем» держит дольше награды
  stat            VARCHAR(20)   NOT NULL,

  status          VARCHAR(20)   NOT NULL DEFAULT 'active',
  closed_at       TIMESTAMPTZ,

  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

  CONSTRAINT global_quests_stat_check
    CHECK (stat IN ('strength', 'health', 'resolve', 'craft', 'bonds')),

  CONSTRAINT global_quests_status_check
    CHECK (status IN ('active', 'done', 'archived')),

  CONSTRAINT global_quests_title_check
    CHECK (length(trim(title)) > 0)
);

CREATE INDEX global_quests_character_idx
  ON global_quests (character_id, status, id);


-- ------------------------------------------------------------
--  tasks — всё, что попадает в «Сегодня»
--  Расписание, сайды и под-квесты глобальных квестов
-- ------------------------------------------------------------
CREATE TABLE tasks (
  id              BIGSERIAL     PRIMARY KEY,
  character_id    BIGINT        NOT NULL
                                REFERENCES characters(id) ON DELETE CASCADE,

  title           VARCHAR(120)  NOT NULL,
  stat            VARCHAR(20)   NOT NULL,
  xp              INTEGER       NOT NULL DEFAULT 10,

  -- Режим появления
  schedule_type   VARCHAR(20)   NOT NULL DEFAULT 'once',
  schedule_data   JSONB,

  -- Когда задача должна появиться в следующий раз.
  -- NULL для разовых, которые уже не повторяются.
  next_due        DATE,

  -- Попадает ли задача в day streak
  counts_for_streak BOOLEAN     NOT NULL DEFAULT FALSE,

  -- Состояние
  status          VARCHAR(20)   NOT NULL DEFAULT 'active',
  done_at         TIMESTAMPTZ,

  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

  CONSTRAINT tasks_stat_check
    CHECK (stat IN ('strength', 'health', 'resolve', 'craft', 'bonds')),

  CONSTRAINT tasks_schedule_type_check
    CHECK (schedule_type IN ('once', 'weekly', 'interval', 'daily')),

  CONSTRAINT tasks_status_check
    CHECK (status IN ('active', 'done', 'archived', 'skipped')),

  CONSTRAINT tasks_xp_check
    CHECK (xp >= 0 AND xp <= 500),

  CONSTRAINT tasks_title_check
    CHECK (length(trim(title)) > 0),

  -- Расписание должно быть заполнено для повторяющихся задач
  CONSTRAINT tasks_schedule_check
    CHECK (
      (schedule_type = 'once' AND schedule_data IS NULL) OR
      (schedule_type = 'daily' AND schedule_data IS NULL) OR
      (schedule_type IN ('weekly', 'interval') AND schedule_data IS NOT NULL)
    ),

  -- done_at заполняется тогда и только тогда, когда задача закрыта
  CONSTRAINT tasks_done_at_check
    CHECK (
      (status = 'done' AND done_at IS NOT NULL) OR
      (status <> 'done')
    )
);

-- Быстрый поиск «что сегодня»: активные с next_due <= сегодня
CREATE INDEX tasks_today_idx
  ON tasks (character_id, status, next_due)
  WHERE status = 'active';

-- История закрытий — для вычисления streak
CREATE INDEX tasks_streak_idx
  ON tasks (character_id, done_at)
  WHERE counts_for_streak = TRUE AND done_at IS NOT NULL;


-- ------------------------------------------------------------
--  quest_links — связь задач с глобальными квестами
--  Одна задача может питать несколько квестов
-- ------------------------------------------------------------
CREATE TABLE quest_links (
  id              BIGSERIAL     PRIMARY KEY,
  quest_id        BIGINT        NOT NULL
                                REFERENCES global_quests(id) ON DELETE CASCADE,
  task_id         BIGINT        NOT NULL
                                REFERENCES tasks(id) ON DELETE CASCADE,

  -- Вклад задачи в прогресс квеста. По умолчанию 1.0 — равный вес.
  weight          NUMERIC(4,2)  NOT NULL DEFAULT 1.0,

  created_at      TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

  CONSTRAINT quest_links_unique
    UNIQUE (quest_id, task_id),

  CONSTRAINT quest_links_weight_check
    CHECK (weight > 0 AND weight <= 10)
);

CREATE INDEX quest_links_quest_idx ON quest_links (quest_id);
CREATE INDEX quest_links_task_idx  ON quest_links (task_id);


-- ------------------------------------------------------------
--  archive — снимок ушедших с доски квестов и задач
--  Причина: closed (закрыт) или deleted (удалён)
-- ------------------------------------------------------------
CREATE TABLE archive (
  id              BIGSERIAL     PRIMARY KEY,
  character_id    BIGINT        NOT NULL
                                REFERENCES characters(id) ON DELETE CASCADE,

  entity_type     VARCHAR(20)   NOT NULL,  -- 'task' | 'global_quest'
  entity_id       BIGINT        NOT NULL,  -- ID оригинала на момент архивации

  snapshot        JSONB         NOT NULL,  -- полный снимок сущности
  reason          VARCHAR(20)   NOT NULL,
  archived_at     TIMESTAMPTZ   NOT NULL DEFAULT NOW(),

  CONSTRAINT archive_entity_type_check
    CHECK (entity_type IN ('task', 'global_quest')),

  CONSTRAINT archive_reason_check
    CHECK (reason IN ('closed', 'deleted'))
);

CREATE INDEX archive_recent_idx
  ON archive (character_id, archived_at DESC);
