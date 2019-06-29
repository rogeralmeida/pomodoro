import click
from tqdm import tqdm
import time
import os
import sys

SECONDS_PER_MINUTE=60

def do_break(short_break_size ):
    click.secho("Pomodoro done! It is time for a break", fg='green')
    for i in tqdm(range(short_break_size * SECONDS_PER_MINUTE)):
        time.sleep(0.9099)
    os.system('terminal-notifier -title "Pomodoro Break Done" -message "Break done. Lets pomodoro another task" -sound default')


@click.command()
@click.option('--pomodoro-size', default=25, help="Pomodoro size in MINUTES")
@click.option('--short-break-size', default=5, help="Break size in MINUTES")
@click.option('--skip-break', is_flag=True, help="When present, pymodoro will skip the break")
@click.option('--auto-break', is_flag=True, help="When present, pymodoro will not expect a confirmation to start a break")
@click.option('--task-file', is_flag=True, help="When present, interprets the task argument as a file path")
@click.argument('task', nargs=-1)
def cli(pomodoro_size, short_break_size, skip_break, auto_break, task_file, task):
    """
        pymodoro is a Pomodoro Timer!

        The basic usage is:

            pymodoro <TASK>
            

        Examples:

            Starting a default 25 minutes long pomodoro on task 'write blog post': `pymodoro write blog post`

            Starting a 35 minutes long pomodoro on task 'call mum': `pymodoro --pomodoro-size 35 call mum`

            Starting a default 25 long pomodoro task reading the task title from stdin: `echo "This is a test" | pymodoro -`

            Starting a default 25 minutes long pomodoro that will start a 5 minutes break automatically when the pomodoro finishes: `pymodoro --auto-break some custom task`
            
    """
    task_text = ""
    if len(task) == 1 and  task[0] == '-':
        task_text = sys.stdin.read()
    else:
        task_text = " ".join(task)

    tasks = []
    if task_file:
        f_path = task_text if task_text else sys.stdin.read()
        with open(f_path.strip()) as f:
            tasks = [task.strip() for task in f.readlines()]
    else:
        tasks = [task_text]

    while tasks:
        try:
            task = tasks.pop(0)
            click.secho("Pomodoro for task: {}".format(task), fg='blue')
            for i in tqdm(range(pomodoro_size * SECONDS_PER_MINUTE)):
                time.sleep(0.99999)

            has_terminal_notifier = os.system('which terminal-notifier') == 0
            if has_terminal_notifier:
                os.system('terminal-notifier -title "Pomodoro Done" -message "'+" ".join(task)+'" -sound default')
            else:
                click.secho("Pomodoro Done: " + task, fg='green')

            if skip_break == False:
                if auto_break == False:
                    click.echo("Start a short break of {} minutes?[yn]".format(short_break_size))
                    option = click.getchar()
                    if option == 'y':
                        do_break(short_break_size )
                else:
                    do_break(short_break_size )
        except KeyboardInterrupt:
            click.echo("Quit?[ynA]".format(short_break_size))
            option = click.getchar()

            if option == 'y':
                continue
            elif option == 'n':
                tasks.insert(0, task)
            elif option == 'A':
                break
            else:
                click.echo("Didn't understand choice, continuing")
                tasks.insert(0, task)
