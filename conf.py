# -*- coding: utf-8 -*-

# List of topics
# How to use: ANNOUNCE_TOPIC.format(cmd="my_command")
CONNECTION_STATUS_TOPIC = "laumio/{name}/status"
ANNOUNCE_TOPIC = "laumio/status/advertise"
COMMAND_ALL_TOPIC = "laumio/all/{cmd}"
COMMAND_TARGET_TOPIC = "laumio/{name}/{cmd}"
