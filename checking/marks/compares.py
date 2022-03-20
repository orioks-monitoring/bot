from utils import exeptions


def file_compares(old_file: list, new_file: list) -> list:
    if len(old_file) != len(new_file):
        raise exeptions.FileCompareError

    diffs = []
    for old, new in zip(old_file, new_file):
        if old['subject'] != new['subject']:
            raise exeptions.FileCompareError
        if len(old['tasks']) != len(new['tasks']):
            raise exeptions.FileCompareError
        diffs_one_subject = []
        for old_task, new_task in zip(old['tasks'], new['tasks']):
            if old_task['max_grade'] != new_task['max_grade']:
                raise exeptions.FileCompareError
            if old_task['alias'] != new_task['alias']:
                raise exeptions.FileCompareError

            old_grade = old_task['current_grade']
            new_grade = new_task['current_grade']
            if old_grade != new_grade:
                old_grade = 0 if old_grade == '-' or old_grade == 'н' else old_grade
                new_grade = 0 if new_grade == '-' or new_grade == 'н' else new_grade
                diffs_one_subject.append({
                    'task': new_task['alias'],
                    'ball': {
                        'abs_difference': round(abs(old_grade - new_grade), 2),
                        'is_new_bigger': new_grade - old_grade >= 0,
                        'current_ball': new_grade,
                        'old_ball': old_grade,
                        'max_grade': new_task['max_grade'],
                    }
                })
        if len(diffs_one_subject) != 0:
            diffs.append({
                'subject': new['subject'],
                'tasks': diffs_one_subject,
                'final_grade': {
                    'current_ball': new['ball']['current'],
                    'might_be': new['ball']['might_be'],
                },
            })
    return diffs


def get_msg_from_diff(diffs: list) -> str:
    msg = ""  # TODO: изменить это безобразие на aiogram.utils.markdown
    for diff_subject in diffs:
        tmp_msg = ""
        for diff_task in diff_subject['tasks']:
            tmp_msg += '🟢' if diff_task['ball']['is_new_bigger'] else '🔴'
            tmp_msg += f" {diff_task['task']}: \n"
            tmp_msg += f"{diff_task['ball']['old_ball']} -> {diff_task['ball']['current_ball']} (из {diff_task['ball']['max_grade']})"
            tmp_msg += f" ({'+' if diff_task['ball']['is_new_bigger'] else '-'}{diff_task['ball']['abs_difference']})\n"
        msg += f"{diff_subject['subject']} ({diff_subject['final_grade']['current_ball']} из {diff_subject['final_grade']['might_be']})\n{tmp_msg}\n"
    return msg
