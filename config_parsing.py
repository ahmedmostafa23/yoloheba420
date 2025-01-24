import os
import json
from collections import deque

from dotenv import load_dotenv

load_dotenv()

def load_default_config_file(config_name, dir, type):
    file_path = os.path.join(dir, f"{config_name}_default_config.{type}")
    with open(file_path, "r") as f:
        if type == "json":
            default_config = json.load(f)

        return default_config


def parse_env_vars_to_config_dict(config_name, env_vars):
    # this is going to be the parsed config dict
    actual_config = {}

    for env_var, val in env_vars.items():
        # checks which env vars belong to our app or not by checking the prefix
        if env_var.startswith(config_name.upper() + "_"):
            target_dict = actual_config
            # splits the env var's name to obtain levels of nesting in a dict
            keys = env_var.replace(f"{config_name.upper()}_", "").split("__")
            keys = [key.lower() for key in keys]

            for i, key in enumerate(keys):
                # if it's a single item, there is no nesting. set the key = val dirctly.
                if len(keys) == 1:
                    target_dict[key] = val
                # if it's not a single item, there are levels of nesting
                else:
                    # if it's not the last level of nesting, add the value as an empty dict
                    if i < len(keys) - 1:
                        target_dict[key] = {}
                        target_dict = target_dict[key]
                    # if it's the last level of nesting, set the value directly.
                    else:
                        target_dict[key] = val

    return actual_config


def consolidate_config(default_config, custom_config):
    """
    Iteratively merge custom_config into default_config without modifying default_config.
    """
    consolidated_dict = default_config.copy()
    stack = deque([(consolidated_dict, custom_config)])

    while stack:
        current_default, current_custom = stack.pop()
        for key, value in current_custom.items():
            if (
                isinstance(value, dict)
                and key in current_default
                and isinstance(current_default[key], dict)
            ):
                stack.append((current_default[key], value))
            else:
                current_default[key] = value

    return consolidated_dict


def get_config(
    config_name, env_vars=os.environ,
    config_file_dir=".", config_file_type="json"
):
    default_config = load_default_config_file(
        config_name, config_file_dir, config_file_type
    )
    custom_config = parse_env_vars_to_config_dict(config_name, env_vars)
    consolidated_config = consolidate_config(default_config, custom_config)
    return consolidated_config
