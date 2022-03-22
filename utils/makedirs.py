import os
import config


def make_dirs() -> None:
    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'cookies'), exist_ok=True)

    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'marks'), exist_ok=True)

    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'discipline_sources'), exist_ok=True)

    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'homeworks'), exist_ok=True)

    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'news'), exist_ok=True)

    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'requests', 'questionnaire'), exist_ok=True)
    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'requests', 'doc'), exist_ok=True)
    os.makedirs(os.path.join(config.BASEDIR, 'users_data', 'tracking_data', 'requests', 'reference'), exist_ok=True)
