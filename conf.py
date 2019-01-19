# -*- coding: utf-8 -*-

# List of topics
# How to use: ANNOUNCE_TOPIC.format(cmd="my_command")
CONNECTION_STATUS_TOPIC = "laumio/{name}/status"
ANNOUNCE_TOPIC = "laumio/status/advertise"
COMMAND_ALL_TOPIC = "laumio/all/{cmd}"
COMMAND_TARGET_TOPIC = "laumio/{name}/{cmd}"


# List of commands
# => mapping for commands that differ from their function's name.
COMMANDS = {
    "send_JSON": "json",
}

def get_command(command):
    """Get the API string of the given command.

    .. warning:: Please use it !

    .. note:: How to use it: get_command("my_command")

    """
    return COMMANDS.get(command, command)
