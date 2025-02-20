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

ERROR_CODE = "error_code"
WARN_CODE = "warn_code"
GRIPPER_ERROR_CODE = "gripper_error_code"
GRIPPER_SPEED = "gripper_speed"
GRIPPER_POSITION = "gripper_position"
COLLISION_SENSITIVITY = "collision_sensitivity"
POS_X = "position_x"
POS_Y = "position_y"
POS_Z = "position_z"
ROLL = "roll"
PITCH = "pitch"
YAW = "yaw"

MOVE_ARM_EVENT = "xarm_move_arm"

LOGGER = logging.getLogger(__package__)
LOGGERFORHA = logging.getLogger(f"{__package__}_HA")

API_ERRORS = {
    -12: "run blockly app exception",
    -11: "convert blockly app to pythen exception",
    -9: "emergency stop",
    -8: "out of range",
    -7: "joint angle limit",
    -6: "cartesian pos limit",
    -5: "revesed, no use",
    -4: "command is not exist",
    -3: "revesed, no use",
    -2: "xArm is not ready, may be the motion is not enable or not set state",
    -1: "xArm is disconnect or not connected",
    0: "success",
    1: "there are errors that have not been cleared",
    2: "there are warnings that have not been cleared",
    3: "get response timeout",
    4: "tcp reply length error",
    5: "tcp reply number error",
    6: "tcp protocol flag error",
    7: "tcp reply command and send command do not match",
    8: "send command error, may be network exception",
    9: "state is not ready to move",
    10: "the result is invalid",
    11: "other error",
    12: "parameter error",
    20: "host id error",
    21: "modbus baudrate not supported",
    22: "modbus baudrate not correct",
    23: "modbus reply length error",
    31: "trajectory read/write failed",
    32: "trajectory read/write timeout",
    33: "playback trajectory timeout",
    34: "playback trajectory failed",
    41: "wait to set suction cup timeout",
    80: "linear track has error",
    81: "linear track sci is low",
    82: "linear track is not initialized",
    100: "wait finish timeout",
    101: "too many consecutive failed tests",
    102: "end effector has error",
    103: "end effector is not enabled",
    129: "(standard modbus tcp)illegal/unsupported function code",
    120: "(standard modbus tcp)illegal target address",
    131: "(standard modbus tcp)exection of requested data",
}

GRIPPER_ERROR_CODES = {
    0: "Gripper No Error",
    9: "Gripper Current Detection Error",
    11: "Gripper Current Overlimit",
    12: "Gripper Speed Overlimit",
    14: "Gripper Position Command Overlimit",
    15: "Gripper EEPROM Read and Write Error",
    20: "Gripper Driver IC Hardware Error",
    21: "Gripper Driver IC Initialization Error",
    23: "Gripper Large Motor Position Deviation",
    25: "Gripper Command Over Software Limit",
    26: "Gripper Feedback Position Software Limit",
    33: "Gripper Drive Overloaded",
    34: "Gripper Motor Overloaded",
    36: "Gripper Driver Type Error",
}

WARN_CODES = {
    11: "uxbux queue is full",
    12: "parameter error",
    13: "the instruction does not exist",
    14: "command has no solution",
    15: "modbus cmd full",
}

MODES = {
    0: "position control mode",
    1: "servo motion mode",
    2: "joint teaching mode",
    3: "cartesian teaching mode (invalid)",
    4: "joint velocity control mode",
    5: "cartesian velocity control mode",
    6: "joint online trajectory planning mode",
    7: "cartesian online trajectory planning mode"
}

STATES = {
    1: "in motion",
    2: "sleeping",
    3: "suspended",
    4: "stopping"
}
