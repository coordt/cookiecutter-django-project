import os
import random
import shutil
import string

try:
    # Inspired by
    # https://github.com/django/django/blob/master/django/utils/crypto.py
    random = random.SystemRandom()
    using_sysrandom = True
except NotImplementedError:
    using_sysrandom = False

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "

DEBUG_VALUE = "debug"
PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def initialize_git(project_directory):
    """
    Initialize the git repo.

    Args:
        project_directory:
    """
    import subprocess

    print("Initializing git repo...")
    result = subprocess.run(
        ["git", "init"],
        cwd=project_directory,
        encoding="utf8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print("Unable to initialize the git repo.")
        print(result.stdout, result.stderr)

    result = subprocess.run(
        ["git", "add", "."],
        cwd=project_directory,
        encoding="utf8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print("Unable to add all files into the git repo.")
        print(result.stdout, result.stderr)

    result = subprocess.run(
        ["git", "commit", '-m"Initial commit"'],
        cwd=project_directory,
        encoding="utf8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print("Unable to make the initial commit.")
        print(result.stdout, result.stderr)

    result = subprocess.run(
        ["git", "tag", "0.1.0"],
        cwd=project_directory,
        encoding="utf8",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        print("Unable to tag the initial commit.")
        print(result.stdout, result.stderr)


def remove_open_source_files():
    file_names = ["CONTRIBUTORS.txt", "LICENSE"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gplv3_files():
    file_names = ["COPYING"]
    for file_name in file_names:
        os.remove(file_name)


def remove_docker_files():
    shutil.rmtree("compose")

    file_names = ["local.yml", ".dockerignore"]
    for file_name in file_names:
        os.remove(file_name)


def remove_gulp_files():
    file_names = ["gulpfile.js"]
    for file_name in file_names:
        os.remove(file_name)


def remove_packagejson_file():
    file_names = ["package.json"]
    for file_name in file_names:
        os.remove(file_name)


def remove_celery_files():
    file_names = [
        os.path.join("{{ cookiecutter.project_slug }}", "celery_app.py"),
        os.path.join("{{ cookiecutter.project_slug }}", "users", "tasks.py"),
        os.path.join(
            "{{ cookiecutter.project_slug }}", "users", "tests", "test_tasks.py"
        ),
        os.path.join("bin", "start-celery-beat"),
        os.path.join("bin", "start-celery-worker"),
        os.path.join("bin", "start-flower"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_dottravisyml_file():
    os.remove(".travis.yml")


def append_to_project_gitignore(path):
    gitignore_file_path = ".gitignore"
    with open(gitignore_file_path, "a") as gitignore_file:
        gitignore_file.write(path)
        gitignore_file.write(os.linesep)


def generate_random_string(
    length, using_digits=False, using_ascii_letters=False, using_punctuation=False
):
    """
    Example:
        opting out for 50 symbol-long, [a-z][A-Z][0-9] string
        would yield log_2((26+26+50)^50) ~= 334 bit strength.
    """
    if not using_sysrandom:
        return None

    symbols = []
    if using_digits:
        symbols += string.digits
    if using_ascii_letters:
        symbols += string.ascii_letters
    if using_punctuation:
        all_punctuation = set(string.punctuation)
        # These symbols can cause issues in environment variables
        unsuitable = {"'", '"', "\\", "$"}
        suitable = all_punctuation.difference(unsuitable)
        symbols += "".join(suitable)
    return "".join([random.choice(symbols) for _ in range(length)])


def set_flag(file_path, flag, value=None, formatted=None, *args, **kwargs):
    if value is None:
        random_string = generate_random_string(*args, **kwargs)
        if random_string is None:
            print(
                f"We couldn't find a secure pseudo-random number generator on your system. Please, make sure to manually {flag} later."
            )
            random_string = flag
        if formatted is not None:
            random_string = formatted.format(random_string)
        value = random_string

    with open(file_path, "r+") as f:
        file_contents = f.read().replace(flag, value)
        f.seek(0)
        f.write(file_contents)
        f.truncate()

    return value


def set_django_secret_key(file_path):
    return set_flag(
        file_path,
        "!!!SET DJANGO_SECRET_KEY!!!",
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def generate_random_user():
    return generate_random_string(length=10, using_ascii_letters=True)


def generate_postgres_user(debug=False):
    return DEBUG_VALUE if debug else generate_random_user()


def set_postgres_user(file_path, value):
    return set_flag(file_path, "!!!SET POSTGRES_USER!!!", value=value)


def set_postgres_password(file_path, value=None):
    return set_flag(
        file_path,
        "!!!SET POSTGRES_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def set_celery_flower_user(file_path, value):
    return set_flag(file_path, "!!!SET CELERY_FLOWER_USER!!!", value=value)


def set_celery_flower_password(file_path, value=None):
    return set_flag(
        file_path,
        "!!!SET CELERY_FLOWER_PASSWORD!!!",
        value=value,
        length=64,
        using_digits=True,
        using_ascii_letters=True,
    )


def append_to_gitignore_file(s):
    with open(".gitignore", "a") as gitignore_file:
        gitignore_file.write(s)
        gitignore_file.write(os.linesep)


def set_flags_in_envs(postgres_user, celery_flower_user, debug=False):
    production_django_envs_path = os.path.join(".envs", "prod", "django")
    dev_postgres_env_path = os.path.join(".envs", "dev", "postgres")
    pg_pass = set_postgres_password(dev_postgres_env_path)
    set_flag(production_django_envs_path, "!!!SET POSTGRES_PASSWORD!!!", value=pg_pass)
    set_flag("local.yml", "!!!SET POSTGRES_PASSWORD!!!", value=pg_pass)
    set_django_secret_key(production_django_envs_path)
    set_celery_flower_user(production_django_envs_path, value=celery_flower_user)
    set_celery_flower_password(production_django_envs_path)


def set_flags_in_settings_files():
    set_django_secret_key(
        os.path.join("{{ cookiecutter.project_slug }}", "settings", "test.py")
    )


def remove_storage():
    os.remove(os.path.join("{{ cookiecutter.project_slug }}", "storage.py"))


def remove_envs_and_associated_files():
    shutil.rmtree(".envs")
    os.remove(os.path.join("bin", "merge_production_dotenvs_in_dotenv.py"))


def create_dev_settings():
    shutil.copy(
        os.path.join("{{ cookiecutter.project_slug }}", "settings", "dev_template.py"),
        os.path.join("{{ cookiecutter.project_slug }}", "settings", "dev.py"),
    )
    shutil.copy(os.path.join(".envs", "prod", "django"), ".env")
    set_flag(
        ".env",
        "DJANGO_SETTINGS_MODULE=test_project.settings.prod",
        value="DJANGO_SETTINGS_MODULE=test_project.settings",
    )


def main():
    set_flags_in_envs(generate_random_user(), generate_random_user())

    set_flags_in_settings_files()
    create_dev_settings()

    if "{{ cookiecutter.open_source_license }}" == "Not open source":
        remove_open_source_files()
    if "{{ cookiecutter.open_source_license}}" != "GPLv3":
        remove_gplv3_files()

    if "{{ cookiecutter.cloud_provider}}".lower() == "none":
        print(
            WARNING + "You chose not to use a cloud provider, "
            "media files won't be served in production." + TERMINATOR
        )
        remove_storage()
    elif "{{ cookiecutter.cloud_provider}}".lower() == "GCP":
        remove_storage()

    if "{{ cookiecutter.use_celery }}".lower() == "n":
        remove_celery_files()

    if "{{ cookiecutter.use_travisci }}".lower() == "n":
        remove_dottravisyml_file()

    initialize_git(PROJECT_DIRECTORY)

    print(f"{SUCCESS}Project initialized, keep up the good work!{TERMINATOR}")


if __name__ == "__main__":
    main()
