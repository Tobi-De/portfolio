import os

import click


def run_commands(command, app, env_dict):
    for env_name, env_value in env_dict.items():
        os.system(command.format(app_name=app, env_name=env_name, env_value=env_value))


def read_env_file(env):
    f = env.readlines()
    return {line.strip().split("=")[0]: line.strip().split("=")[1] for line in f}


@click.command()
@click.option(
    "--app",
    default="",
    help="The name of your app, this is neccessary "
    "when your are using the dokku cli directly instead of the dokku-toolbet wrapper",
)
@click.argument(
    "env", type=click.File("r"),
)
def set_dokku_app_envs(env, app):
    """Simple program that set environment variables for a project deploy with dokku
    on a vps, taking the env file path as argument.
    """

    command = (
        "dokku config:set {app} {env_name}={env_value}"
        if app
        else "dt config:set {env_name}={env_value}"
    )

    env_dict = read_env_file(env=env)

    if not env_dict:
        return

    run_commands(command, app, env_dict)

    # set random secret key and admin url, comment if not needed
    extra = {
        "DJANGO_SECRET_KEY": "$(openssl rand -base64 64 | tr -dc 'A-HJ-NP-Za-km-z2-9')",
        "DJANGO_ADMIN_URL": "$(openssl rand -base64 4096 | tr -dc 'A-HJ-NP-Za-km-z2-9' | head -c 32)/",
        "PYTHONHASHSEED": "random",
    }

    run_commands(command=command, app=app, env_dict=extra)


if __name__ == "__main__":
    set_dokku_app_envs()
