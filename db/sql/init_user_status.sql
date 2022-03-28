INSERT OR IGNORE INTO user_status
VALUES (:user_telegram_id, :is_user_agreement_accepted, :is_user_orioks_authenticated, :orioks_login_attempts);