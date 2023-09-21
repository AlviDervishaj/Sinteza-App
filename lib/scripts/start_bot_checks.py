import os
import sys
import json
import collections
import ruamel.yaml
from time import sleep
from ruamel.yaml.comments import CommentedSeq

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True


LIST_OF_FILES = [
    "blacklist.txt",
    "config.yml",
    "comments_list.txt",
    "filters.yml",
    "pm_list.txt",
    "telegram.yml",
    "whitelist.txt",
    "config1.yml",
]

AVAILABLE_FILES = []

command = (
    "copy"
    if sys.platform.startswith("win32") or sys.platform.startswith("cygwin")
    else "cp"
)


def compare(x, y) -> bool:
    return collections.Counter(x) == collections.Counter(y)


def _print(value: str):
    print(value, flush=True)


botConfig = sys.argv[1]
customConfig = json.loads(botConfig)
if not customConfig["username"]:
    _print("Please enter a valid instagram username")
    exit()
if not customConfig["device"]:
    _print("Please enter a valid device.")
    exit()


def create_default_configs(username) -> None:
    additional_configs = ["config1.yml"]
    # copy files from config examples folder.

    for config_name in additional_configs:
        default_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "Bot",
            "config-examples",
            config_name,
        )
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "accounts",
            username,
            config_name,
        )
        if config_name not in AVAILABLE_FILES:
            _print(f"[INFO] Copying file from  : {default_path} to {config_path}")
            # copy config files to that dir
            os.popen(f"{command} {default_path} {config_path}")
        else:
            _print(f"[INFO] File {config_name} already exists.")


def change_keys_in_config(username, config) -> None:
    """
    Change config file based on username
    """

    create_default_configs(username)
    sleep(1)
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "accounts", username, config
    )
    try:
        with open(config_path) as fp:
            data = yaml.load(fp)
    except Exception as e:
        _print(f"[ERROR] {e}")
        exit()

    for config in customConfig:
        if config in data:
            if data[config] == customConfig[config]:
                _print(f"[INFO] {config.capitalize()} : DEFAULT")
                continue
            if type(customConfig[config]) == list:
                if len(customConfig[config]) > 1 and customConfig[config][0] != "":
                    _print(
                        f"[INFO] Changing {config} from {data[config]} to {customConfig[config]}"
                    )
                    customConfig[config] = CommentedSeq(customConfig[config])
                    customConfig[config].fa.set_flow_style()
                    data[config] = customConfig[config]
                    continue
                else:
                    data[config] = data[config]
                    continue
            elif type(customConfig[config]) == str and str(customConfig[config]) != "":
                _print(
                    f"[INFO] Changing {config} from {data[config]} to {customConfig[config]}"
                )
                data[config] = customConfig[config]
                continue
            else:
                _print(f"[INFO] Skipping `{config}`")
                continue
        else:
            _print(f"[INFO] Skipping `{config}`")

    with open(config_path, "w") as fp:
        _print(f"[INFO] Writing to {config_path}")
        yaml.default_flow_style = True
        yaml.width = float("inf")
        yaml.dump(data, fp)


# Make the default config files and folders for a user


def make_config(_instagram_username) -> str:
    """
    Make the default config files and folders for a user
    """
    if _instagram_username.strip() == "":
        return "[ERROR] Invalid username."

    for file in LIST_OF_FILES:
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "accounts",
            _instagram_username,
            file,
        )
        default_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "Bot", "config-examples", file
        )
        if file not in AVAILABLE_FILES:
            _print(f"[INFO] Copying file from  : {default_path} to {config_path}")
            # copy config files to that dir
            os.popen(f"{command} {default_path} {config_path}")
        else:
            _print(f"[INFO] File {file} already exists.")
    return "[INFO] Success"


# check base accounts folder
if os.path.exists(os.path.join(os.path.dirname(os.path.dirname(__file__)), "accounts")):
    _print("[INFO] Accounts folder located.")
else:
    _print("[INFO] Creating accounts folder.")
    os.mkdir(os.path.join(os.path.dirname(os.path.dirname(__file__)), "accounts"))
    _print("[INFO] Folder created.")

# check accounts/username folder.
user_dir = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "accounts", customConfig["username"]
)
if os.path.exists(user_dir):
    _print("[INFO] Folder located.")
    _instagram_client_config_files = os.listdir(user_dir)
    AVAILABLE_FILES = _instagram_client_config_files
    # check files
    if compare(_instagram_client_config_files, LIST_OF_FILES):
        _print("[INFO] Config is correct. ")
        # try to change configs to the ones provided
        change_keys_in_config(customConfig["username"], "config.yml")
        change_keys_in_config(customConfig["username"], "config1.yml")
    else:
        _print("[INFO] Config is not correct. ")
        _print("[INFO] Replacing files...")
        make_config(customConfig["username"])
        sleep(0.4)
        change_keys_in_config(customConfig["username"], "config.yml")
        change_keys_in_config(customConfig["username"], "config1.yml")
    _print("[INFO] End")
else:
    os.mkdir(user_dir)
    _print(f"[INFO] accounts/{customConfig['username']} folder created.")
    _print("[INFO] Creating config files...")
    make_config(customConfig["username"])
    sleep(0.8)
    change_keys_in_config(customConfig["username"], "config.yml")
    change_keys_in_config(customConfig["username"], "config1.yml")
    _print("[INFO] End")
