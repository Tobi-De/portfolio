import os
import sys


def set_dokku_app_envs(env_dict, app_name):
    command = "dt config:set {env_name}={env_value}"
    if env_dict:
        for env_name, env_value in env_dict.items():
            os.system(
                command.format(
                 env_name=env_name, env_value=env_value
                )
            )
    # set random secret key and admin url, comment if not needed

    # os.system(
    #     f'dt config:set DJANGO_SECRET_KEY="$(openssl rand -base64 64)"'
    # )
    # os.system(
    #     f'dt config:set DJANGO_ADMIN_URL="$(openssl rand -base64 4096 | tr -dc "A-HJ-NP-Za-km-z2-9" | head -c 32)/"'
    # )


def read_env_file(file_path):
    env_dict = {}
    with open(file_path, "r") as f:
        for line in f:
            env_list = line.strip().split("=")
            env_dict[env_list[0]] = env_list[1]
    return env_dict


if __name__ == "__main__":
    try:
        env_file = sys.argv[2]
    except IndexError:
        env_file = ".env"
    try:
        app_name = sys.argv[1]
    except IndexError:
        print("usage: python dokku_config.py <app_name> <env_file>(optional)")
    else:
        env_dict = read_env_file(env_file)
        set_dokku_app_envs(env_dict, app_name)
