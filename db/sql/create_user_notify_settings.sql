CREATE TABLE IF NOT EXISTS user_notify_settings (
    user_telegram_id INTEGER unique,
    marks TINYINT,
    news TINYINT,
    discipline_sources TINYINT,
    homeworks TINYINT,
    requests TINYINT
);