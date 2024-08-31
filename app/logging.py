import logging.config

from config import config

config.LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(filename)s %(funcName)s %(lineno)d %(name)s %(levelname)s %(message)s",
            "json_ensure_ascii": False,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "r_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "filename": config.LOGS_DIR / "app.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MiB
            "backupCount": 10,
            "encoding": "utf8",
        },
    },
    "loggers": {
        "": {
            "handlers": ["console", "r_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


def setup_logging() -> None:
    logging.config.dictConfig(LOGGING)
