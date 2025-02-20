"""Data models that represent an Xarm Controller"""

from abc import ABC
from dataclasses import dataclass
from typing import List, Iterable

from .const import GRIPPER_ERROR_CODES

from xarm.wrapper import XArmAPI


def error_handler(model, result):
    if result[0] != 0:
        model.error_code = result[0]

@dataclass
class Gripper:
    error_code: int
    error_msg: str
    position: int
    version: int
    # set_gripper_enable: Callable[..., int]
    # set_gripper_mode: Callable[..., int]
    # set_gripper_position: Callable[..., int]
    # set_gripper_speed: Callable[..., int]

    def __init__(self, xarm_client: XArmAPI):
        self.xarm_client = xarm_client
        self.error_code = 0
        self.error_msg = GRIPPER_ERROR_CODES[self.error_code]
        self.position = 0
        self.version = 0
        # self.set_gripper_enable = xarm.set_gripper_enable
        # self.set_gripper_mode = xarm.set_gripper_mode
        # self.set_gripper_position = xarm.set_gripper_position
        # self.set_gripper_speed = xarm.set_gripper_speed

    def update(self, event):
        old_data = f"{self.__dict__}"

        self.error_code = self.xarm.get_gripper_err_code()
        self.position = self.xarm.get_gripper_position()
        self.version = self.xarm.get_gripper_version()
        self.error_msg = self.interpret_error_code(self.error_code)

        new_data = f"{self.__dict__}"
        return old_data != new_data

    def set_gripper_position(self, position: int):
        self.interpret_error_code(self.xarm_client.set_gripper_mode(0))
        self.interpret_error_code(self.xarm_client.set_gripper_enable(True))
        self.interpret_error_code(self.xarm_client.set_gripper_position(position, wait=True))

    def interpret_error_code(self, error_code):
        if error_code in GRIPPER_ERROR_CODES:
            self.callback({"gripper_err_code": error_code})
            self.error_msg = GRIPPER_ERROR_CODES[error_code]
        self.error_msg = "Unknown error"


@dataclass
class ArmPosition:
    pitch: int
    position: List[int]
    x: int
    y: int
    z: int
    roll: int
    yaw: int

    def __init__(self, xarm_client: XArmAPI):
        self.xarm_client = xarm_client
        self.pitch = 0
        self.position = [0, 0, 0, 0, 0, 0]

    def update(self, event):
        old_data = f"{self.__dict__}"

        self.position = self.xarm_client.position
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]
        self.roll = self.position[3]
        self.pitch = self.position[4]
        self.yaw = self.position[5]

        new_data = f"{self.__dict__}"

        return old_data != new_data


@dataclass
class State:
    collision_sensitivity: int
    connected: int
    error_code: int
    has_error: bool
    has_err_warn: bool
    has_warn: bool
    is_moving: int
    mode: int
    motor_brake_states: list[int]
    motor_enable_states: List[int]
    self_collision_params: Iterable  # :return: params, params[0]: self collision detection or not, params[1]: self collision tool type, params[2]: self collision model params
    servo_codes: list[list[int]]
    state: int
    temperatures: list[int]
    warn_code: int

    def __init__(self, xarm_client: XArmAPI):
        self.xarm_client = xarm_client

    def update(self, event):
        old_data = f"{self.__dict__}"

        self.collision_sensitivity = self.xarm_client.collision_sensitivity or 0
        self.connected = self.xarm_client.connected or False
        self.error_code = self.xarm_client.error_code or 0
        self.has_error = self.xarm_client.has_error or False
        self.has_err_warn = self.xarm_client.has_err_warn or False
        self.has_warn = self.xarm_client.has_warn or False
        # self.is_moving = self.xarm_client.get_is_moving()
        self.mode = self.xarm_client.mode or 0
        # self.motor_brake_states = self.xarm_client.motor_brake_states
        # self.motor_enable_states = self.xarm_client.motor_enable_states
        # self.self_collision_params = self.xarm_client.self_collision_params
        # self.servo_codes = self.xarm_client.servo_codes
        self.state = self.xarm_client.state or 0
        self.warn_code = self.xarm_client.warn_code or 0

        new_data = f"{self.__dict__}"

        return old_data != new_data
    
    def set_collision_sensitivity(self, sensitivity: int):
        if sensitivity < 1 or sensitivity > 5:
            raise ValueError("Collision sensitivity must be between 1 and 5")
        err, _ = self.xarm_client.set_collision_sensitivity(sensitivity)


@dataclass
class Info:
    device_type: int
    serial: int
    version: int
    version_number: tuple[int]

    def __init__(self, xarm_client: XArmAPI):
        self.xarm_client = xarm_client
        self.device_type = 1
        self.serial = 123456789
        self.version = 1
        self.version_number = (1, 0, 0)
        # self.device_type = self.xarm_client.device_type or 1
        # self.serial = self.xarm_client.sn or 123456789
        # self.version = self.xarm_client.version or 1
        # self.version_number = self.xarm_client.version_number or (1, 0, 0)

    def update(self, event):
        old_data = f"{self.__dict__}"

        self.device_type = self.xarm_client.device_type
        self.serial = self.xarm_client.sn
        self.version = self.xarm_client.version
        self.version_number = self.xarm_client.version_number

        new_data = f"{self.__dict__}"

        return old_data != new_data


@dataclass
class XArmData:

    def __init__(self, xarm_client: XArmAPI, callback: callable):
        self.xarm_client = xarm_client
        self.callback = callback
        self.gripper = Gripper(xarm_client)
        self.position = ArmPosition(xarm_client)
        # self.state = State(xarm_client)
        self.info = Info(xarm_client)

    def update(self, data):
        send_event = False
        send_event = send_event | self.gripper.update()
        send_event = send_event | self.position.update()
        send_event = send_event | self.state.update()
        send_event = send_event | self.info.update()


def initialize(client: XArmAPI):
    """callback to re-initialize the xArm"""

    client.motion_enable(True)
    client.clean_error()
    client.set_mode(0)
    client.set_state(0)
    client.set_gripper_mode(0)
    client.set_gripper_enable(True)
    client.clean_gripper_error()
