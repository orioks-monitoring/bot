CREATE TABLE IF NOT EXISTS user_status (
    user_telegram_id INTEGER unique,
    is_user_agreement_accepted TINYINT,
    is_user_orioks_authenticated TINYINT,
    orioks_login_attempts TINYINT
);