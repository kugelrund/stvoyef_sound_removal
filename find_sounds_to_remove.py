import argparse
import os
import re


class Task:
    def __init__(self, name, sounds, has_progression_code):
        self.name = name
        self.sounds = sounds
        self.has_progression_code = has_progression_code


class Sound:
    def __init__(self, channel, filename):
        self.channel = channel
        self.filename = filename
    def __repr__(self):
        return "<Sound channel:%s filename:%s>" % (self.channel, self.filename)


def find_sounds(code: str) -> list:
    sound_regexp = 'sound *\( *(\/\*@CHANNELS\*\/)? *([a-zA-Z0-9_]*) *, "(.*)" *\) *;'
    sounds = []
    for (_, channel, filename) in re.findall(sound_regexp, code):
        sounds.append(Sound(channel, filename))
    return sounds


def has_progression_code(code: str) -> bool:
    identifiers = ['use *\(.*\) *;', 'run *\(.*\) *;', 'move *\(.*\) *;',
                   'rotate *\(.*\) *;',
                   'set *\((?!.*SET_OBJECTIVE)(?!.*SET_TACTICAL).*\) *;']
    for identifier in identifiers:
        if re.search(identifier, code):
            return True
    return False


def parse_task(code: str) -> Task:
    assert code.startswith('task')
    index_task_statement_start = code.find('(', 4)
    assert index_task_statement_start != -1
    index_name_start = code.find('"', index_task_statement_start + 1)
    assert index_name_start != -1
    index_name_end = code.find('"', index_name_start + 1)
    assert index_name_end != -1
    index_task_statement_end = code.find(')', index_name_end + 1)
    assert index_task_statement_end != -1

    task_name = code[index_name_start+1:index_name_end]

    index_task_code_start = code.find('{', index_task_statement_start)
    index = index_task_code_start + 1
    assert index != -1
    current_level = 1
    while current_level != 0:
        index_next_level = code.find('{', index)
        index_end_level = code.find('}', index)
        index_nested_task = code.find('task', index)
        index_first = min([i for i in [index_next_level, index_end_level,
                                       index_nested_task] if i != -1])
        if index_first == index_nested_task:
            index = index_nested_task + 4
            print('nested task, TODO')
        elif index_first == index_end_level:
            current_level -= 1
            index = index_end_level + 1
        elif index_first == index_next_level:
            current_level += 1
            index = index_next_level + 1
    index_task_code_end = index

    task_code = code[index_task_code_start:index_task_code_end]
    sounds = find_sounds(task_code)
    task_has_progression_code = has_progression_code(task_code)
    return Task(task_name, sounds, task_has_progression_code)


def are_any_tasks_run_in_code(tasks: list, code: str) -> bool:
    task_wait_regexp = 'wait *\( *"(.*)" *\) *;'  # this covers dowait and wait
    task_do_regexp = 'do *\( *"(.*)" *\) *;'
    run_task_names = (re.findall(task_wait_regexp, code) +
                      re.findall(task_do_regexp, code))
    for task in tasks:
        for run_task_name in run_task_names:
            if task.name == run_task_name:
                return True
    return False


def get_tasks_with_sounds_to_remove(tasks_with_sounds: list,
                                    tasks_with_progression_code: list,
                                    code: str) -> list:
    tasks_with_sounds_to_remove = []
    for task in tasks_with_sounds:
        # will find both dowait (which is more common) and wait (which is also
        # sometimes used)
        this_task_wait_regexp = 'wait *\( *"{}" *\) *;'.format(task.name)
        match_task_wait = re.search(this_task_wait_regexp, code)
        if not match_task_wait:
            # there is no waiting for this sound task so no need to remove it
            continue
        code_after_task_wait = code[match_task_wait.end():]

        if has_progression_code(code_after_task_wait):
            # there is impotant stuff after waiting for this sound task, so need
            # to remove it
            tasks_with_sounds_to_remove.append(task)
            continue

        # final check: after waiting for this sound task, are there other tasks
        # being run that themselves have progression stuff?
        if are_any_tasks_run_in_code(tasks_with_progression_code,
                                     code_after_task_wait):
            tasks_with_sounds_to_remove.append(task)
    return tasks_with_sounds_to_remove


def has_following_script_with_progression_code(filepath: str) -> bool:
    script_names_with_next_script_with_progression = [
        os.path.join('tutorial', 'tutorial_pt4.txt'),
        os.path.join('voy1', 'warning.txt')]
    return any([script_name in filepath for script_name in
                script_names_with_next_script_with_progression])


def find_sounds_to_remove(filepath: str) -> list:
    with open(filepath, 'r') as f:
        code = f.read()

    if has_following_script_with_progression_code(filepath):
        # early exit: if this script is followed directly by a script that is
        # important for progression, we have to remove any sound, because the
        # script execution will wait at the end of the script in any case
        return [sound.filename for sound in find_sounds(code)]

    if not has_progression_code(code):
        # early exit: if there is no code for progression at all in this script,
        # no reason to delete any sound. probably a pure dialog script
        return []

    tasks = []
    index = code.find('task')
    while index != -1:
        tasks.append(parse_task(code[index:]))
        index = code.find('task', index + 1)
    tasks_with_sounds = [t for t in tasks if t.sounds]
    tasks_with_progression_code = [t for t in tasks if t.has_progression_code]

    tasks_with_sounds_to_remove = get_tasks_with_sounds_to_remove(
        tasks_with_sounds, tasks_with_progression_code, code)

    sounds_to_remove = []
    for task in tasks_with_sounds_to_remove:
        for sound in task.sounds:
            sounds_to_remove.append(sound.filename)
    return sounds_to_remove


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('real_scripts', type=str,
                        help="Path to the 'real_scripts' directory of the "
                             "original script files of the game "
                             "Star Trek: Voyager - Elite Force.")
    args = parser.parse_args()

    sounds_to_remove = set()
    for subdir, _, files in os.walk(args.real_scripts):
        for filename in files:
            filepath = os.path.join(subdir, filename)
            sounds_to_remove.update(find_sounds_to_remove(filepath))
    sounds_to_remove = sorted(list(sounds_to_remove))
    print(sounds_to_remove)
    print(len(sounds_to_remove))

    with open('sounds_to_remove.txt', 'w') as f:
        for sound in sounds_to_remove:
            f.writelines("%s\n" % sound)


if __name__ == "__main__":
    main()
