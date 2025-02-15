import logging

DOMAIN = "xarm-controller"

ATTR_AVAILABILITY_TOPIC = "availability_topic"
ATTR_COMMAND_TOPIC = "command_topic"
ATTR_DEVICE = "device"
ATTR_DEVICE_CLASS = "device_class"
ATTR_ICON = "icon"
ATTR_NAME = "name"
ATTR_STATE_TOPIC = "state_topic"
ATTR_UNIQUE_ID = "unique_id"

POS_X = "position_x"
POS_Y = "position_y"
POS_Z = "position_z"
ROLL = "roll"
PITCH = "pitch"
YAW = "yaw"

LOGGER = logging.getLogger(__package__)
LOGGERFORHA = logging.getLogger(f"{__package__}_HA")
