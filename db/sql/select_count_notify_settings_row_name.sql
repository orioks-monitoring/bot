SELECT
       COUNT(*)
FROM user_notify_settings
    INNER JOIN user_status on user_notify_settings.user_telegram_id = user_status.user_telegram_id
WHERE
      user_notify_settings.{row_name} = 1
  AND
      user_status.is_user_orioks_authenticated = 1;