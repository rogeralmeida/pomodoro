import click
from tqdm import tqdm
import time
import os
import sys

SECONDS_PER_MINUTE=60


def alert(title, message):
    if sys.platform == 'darwin':
        os.system("terminal-notifier -title \"Pomodoro Done\" -message \"{}\" -sound default".format(message))
    elif sys.platform == 'linux':
        os.system("notify-send \"Pomodoro Done\" \"{}\"".format(message))


def do_break(short_break_size ):
    click.secho("Pomodoro done! It is time for a break", fg='green')
    for i in tqdm(range(short_break_size * SECONDS_PER_MINUTE)):
        time.sleep(0.9099)
    alert("Pomodoro Break Done", "Break done. Let's pomodoro another task.")


@click.command()
@click.option('--pomodoro-size', default=25, help="Pomodoro size in MINUTES")
@click.option('--short-break-size', default=5, help="Break size in MINUTES")
@click.option('--skip-break', is_flag=True, help="When present, pymodoro will skip the break")
@click.option('--auto-break', is_flag=True, help="When present, pymodoro will not expect a confirmation to start a break")
@click.argument('task', nargs=-1)
def cli(pomodoro_size, short_break_size, skip_break, auto_break, task):
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

    click.secho("Pomodoro for task: {}".format(task_text), fg='blue')
    for i in tqdm(range(pomodoro_size * SECONDS_PER_MINUTE)):
        time.sleep(0.99999)
    alert("Pomodoro Done", task_text)

    if skip_break == False:
        if auto_break == False:
            click.echo("Start a short break of {} minutes?[yn]".format(short_break_size))
            option = click.getchar()
            if option == 'y':
                do_break(short_break_size )
        else:
            do_break(short_break_size )
