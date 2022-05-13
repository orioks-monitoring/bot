UPDATE user_notify_settings
SET
    marks = :marks,
    news = :news,
    discipline_sources = :discipline_sources,
    homeworks = :homeworks,
    requests = :requests
WHERE
      user_telegram_id = :user_telegram_id;