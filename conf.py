# -*- coding: utf-8 -*-
"""Helper to map precisely where are each laumio

Spatial organization:

    (0)  (1)
            (2)
    (3)  (4)
      (5)   (6)
         (7)
     (8)
           (9)            (10)

    And the one in the HAUM room: (11)


"""

# List of topics
# How to use: ANNOUNCE_TOPIC.format(cmd="my_command")
CONNECTION_STATUS_TOPIC = "laumio/{name}/status"
ANNOUNCE_TOPIC = "laumio/status/advertise"
COMMAND_ALL_TOPIC = "laumio/all/{cmd}"
COMMAND_TARGET_TOPIC = "laumio/{name}/{cmd}"
CONNECTION_STATUS_SENSORS = "{sensors}/status"
REMOTE_CMD_TOPIC = "remote/{cmd}/state"
COMMAND_MUSIC = "music/control/{cmd}"
SENSORS_BP_LED = "capteur_bp/switch/led{num}/state"
SENSORS_BP_BUTTON = "capteur_bp/binary_sensor/bp{}/state"
SENSORS_BP_CMD_LED = "capteur_bp/switch/led{}/command"

# Rings def
RINGS = {
    'BOTTOM': 0,
    'MIDDLE': 1,
    'TOP': 2,
}


# List of SENSORS
SENSORS_LIST = ('capteur_bp','presence','distance','atmosphere')

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

SPATIAL_POSITION = {
    'Laumio_1D9486': 0,
    'Laumio_104A13': 1,
    'Laumio_0FBFBF': 2,
    'Laumio_104F03': 3,
    'Laumio_10508F': 4,
    'Laumio_10805F': 5,
    'Laumio_CD0522': 6
    'Laumio_0FC168': 7,
    'Laumio_D454DB': 8,
    'Laumio_107DA8': 9,
    'Laumio_88813D': 10,
    # 'Laumio_439BA9': 11,  # the one that the HAUM use to debug
}
