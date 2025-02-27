"""Data models that represent an Xarm Controller"""

# import functools
from typing import overload
from dataclasses import dataclass
from typing import List, Iterable, Optional

from .const import API_ERRORS, GRIPPER_ERROR_CODES, LOGGER, LOGGERFORHA

from xarm.wrapper import XArmAPI


# TODO: Add error handling for certain methods
# def handle_error_codes(func):
#     @functools.wraps(func)
#     def wrapper(self, *args, **kwargs):
#         result = func(self, *args, **kwargs)
#         return result
#     return wrapper


def interpret_error_code(model: dataclass) -> None:
    """Interpret the error code from the Xarm Controller."""
    if model.error_code in model.error_map:
        if model.__class__ == "Gripper" and getattr(model, "callback"):
            model.callback({"gripper_err_code": model.error_code})
        model.error_msg = model.error_map[model.error_code]
    return "Unknown error"


# TODO: add AttrReader to all attributes in other classes
@dataclass
class AttrReader:
    """Class to read attributes from the Xarm Controller."""

    curr_value: any
    read: callable
    # def __init__(self, value: any, reader: callable) -> None:
    #     self.curr_value = value
    #     self.read = reader


@dataclass
class Gripper:
    """Data model for the Xarm Controller gripper."""

    error_code: int
    error_msg: str
    error_map: dict[int, str]
    speed: int
    position: int
    version: int
    # set_gripper_enable: Callable[..., int]
    # set_gripper_mode: Callable[..., int]
    # set_position: Callable[..., int]
    # set_speed: Callable[..., int]
    # close_lite6_gripper: Callable[..., int]
    # open_lite6_gripper: Callable[..., int]
    # stop_lite6_gripper: Callable[..., int]

    def __init__(self, xarm_client: XArmAPI, callback: callable):
        self.xarm_client = xarm_client
        self.callback = callback

        self.error_code = 0
        self.error_map = GRIPPER_ERROR_CODES
        self.error_msg = interpret_error_code(self)
        self.speed = 0
        self.position = 0
        self.version = 0
        # self._read_version = self.xarm_client.get_gripper_version()
        # self.set_gripper_enable = xarm.set_gripper_enable
        # self.set_gripper_mode = xarm.set_gripper_mode
        # self.set_position = xarm.set_position
        # self.set_speed = xarm.set_speed
        # self.close_lite6_gripper = xarm.close_lite6_gripper
        # self.open_lite6_gripper = xarm.open_lite6_gripper
        # self.stop_lite6_gripper = xarm.stop_lite6_gripper

    def update(self) -> None:
        """Update the gripper data."""

        self.error_code = self.xarm_client.get_gripper_err_code()
        self.error_msg = interpret_error_code(self)
        self.speed = self.xarm_client.get_speed()
        self.position = self.xarm_client.get_position()
        self.version = self.xarm_client.get_gripper_version()

    # def set_position(self, position: int):
    #     self.interpret_error_code(self.xarm_client.set_gripper_mode(0))
    #     self.interpret_error_code(self.xarm_client.set_gripper_enable(True))
    #     self.interpret_error_code(
    #         self.xarm_client.set_position(position, wait=True)
    #     )

    def open(self, is_lite6: bool):
        # TODO: find out open position for non lite6 gripper
        if is_lite6:
            self.xarm_client.open_lite6_gripper()
        else:
            self.xarm_client.set_position(1000, wait=True)

    def close(self, is_lite6: bool):
        # TODO: find out close position for non lite6 gripper
        if is_lite6:
            self.xarm_client.close_lite6_gripper()
        else:
            self.xarm_client.set_position(0, wait=True)

    def set_position(self, position: int):
        self.xarm_client.set_position(position, wait=True)

    def initialize(self):
        self.xarm_client.set_gripper_mode(0)
        self.xarm_client.set_gripper_enable(True)
        self.xarm_client.set_speed(5000)  # TODO: Determine good gripper speed
        self.xarm_client.clean_gripper_error()


@dataclass
class ArmPosition:
    """Data model for the Xarm Controller arm position."""

    pitch: int
    position: List[int]
    x: int
    y: int
    z: int
    target_x: int
    target_y: int
    target_z: int
    roll: int
    yaw: int

    def __init__(self, xarm_client: XArmAPI):
        self.xarm_client = xarm_client
        self.position = [0, 0, 0, 0, 0, 0]
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]
        self.target_x = 0
        self.target_y = 0
        self.target_z = 0
        self.roll = self.position[3]
        self.pitch = self.position[4]
        self.yaw = self.position[5]

    def update(self):
        """Update the arm position data."""

        self.position = self.xarm_client.position
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]
        self.roll = self.position[3]
        self.pitch = self.position[4]
        self.yaw = self.position[5]

    def set_target_position(
        self, target_x: int = None, target_y: int = None, target_z: int = None
    ):
        if target_x is not None:
            self.target_x = target_x
        if target_y is not None:
            self.target_y = target_y
        if target_z is not None:
            self.target_z = target_z

    def set_position_to_targets(self):
        self.xarm_client.set_position(x=self.target_x, y=self.target_y, z=self.target_z)


@dataclass
class State:
    """Data model for the Xarm Controller state."""

    collision_sensitivity: int
    connected: bool
    counter: int
    error_code: int
    error_msg: str
    error_map: dict[int, str]
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
        self.collision_sensitivity = 0
        self.connected = True
        self.counter = 0
        self.error_code = 0
        self.error_msg = ""
        self.error_map = API_ERRORS
        self.has_error = False
        self.has_err_warn = False
        self.has_warn = False
        self.is_moving = False
        self.mode = 0
        self.motor_brake_states = [1, 1, 1, 1, 1, 1]
        self.motor_enable_states = [1, 1, 1, 1, 1, 1]
        self.self_collision_params = [1, 1, 0]
        self.servo_codes = [[1, 0], [1, 0], [1, 0], [1, 0], [1, 0], [1, 0]]
        self.state = 1
        self.warn_code = 0
        self.warn_msg = "warn"

    def update(self):
        """Update the state data."""

        self.collision_sensitivity = self.xarm_client.collision_sensitivity
        self.connected = self.xarm_client.connected
        self.error_code = self.xarm_client.error_code
        self.error_msg = interpret_error_code(self)
        self.has_error = self.xarm_client.has_error
        self.has_err_warn = self.xarm_client.has_err_warn
        self.has_warn = self.xarm_client.has_warn
        self.is_moving = self.xarm_client.get_is_moving()
        self.mode = self.xarm_client.mode
        self.motor_brake_states = self.xarm_client.motor_brake_states
        self.motor_enable_states = self.xarm_client.motor_enable_states
        self.self_collision_params = self.xarm_client.self_collision_params
        self.servo_codes = self.xarm_client.servo_codes
        self.state = self.xarm_client.state
        self.warn_code = self.xarm_client.warn_code
        # self.warn_msg = self.xarm_client.warn_msg

    def set_collision_sensitivity(self, sensitivity: int):
        if sensitivity < 1 or sensitivity > 5:
            raise ValueError("Collision sensitivity must be between 1 and 5")
        err, _ = self.xarm_client.set_collision_sensitivity(sensitivity)


@dataclass
class Info:
    """Data model for the Xarm Controller info."""

    axis: int
    device_type: int
    is_lite6: bool
    serial: int
    version: int
    version_number: tuple[int]

    def __init__(self, xarm_client: XArmAPI):
        self.xarm_client = xarm_client
        self.axis = 0
        self.device_type = 1
        self.is_lite6 = True
        self.serial = xarm_client.sn
        self.version = 1
        self.version_number = (1, 0, 0)
        # self.device_type = self.xarm_client.device_type or 1
        # self.serial = self.xarm_client.sn or 123456789
        # self.version = self.xarm_client.version or 1
        # self.version_number = self.xarm_client.version_number or (1, 0, 0)

    def update(self):
        old_data = f"{self.__dict__}"

        self.axis = self.xarm_client.axis
        self.device_type = self.xarm_client.device_type
        self.is_lite6 = self.xarm_client.is_lite6
        self.serial = self.xarm_client.sn
        self.version = self.xarm_client.version
        self.version_number = self.xarm_client.version_number

        new_data = f"{self.__dict__}"

        return old_data != new_data


@dataclass
class XArmData:
    """Data model for the Xarm Controller."""

    def __init__(self, xarm_client: XArmAPI, callback: callable):
        self.xarm_client = xarm_client
        self.callback = callback
        self.gripper = Gripper(xarm_client, callback)
        self.position = ArmPosition(xarm_client)
        self.state = State(xarm_client)
        self.info = Info(xarm_client)

    def update(self, data):
        send_event = False
        send_event = send_event | self.gripper.update()
        send_event = send_event | self.position.update()
        send_event = send_event | self.state.update()
        send_event = send_event | self.info.update()

    def _interpret_error_code(self, error_code):
        pass

    def clear_errors(self):
        self.xarm_client.clear_errors()

    def emergency_stop(self):
        self.xarm_client.emergency_stop()
        LOGGER.debug("Emergency stop called")

    def go_home(self):
        self.xarm_client.move_gohome()

    def move(self, _x: int, _y: int, _z: int):
        pass

    def open_gripper(self):
        self.gripper.open(self.info.is_lite6)

    def close_gripper(self, position: Optional[int] = None):
        self.gripper.close(position if position is not None else 0, self.info.is_lite6)

    def initialize(self):
        """callback to re-initialize the xArm"""
        self.xarm_client.motion_enable(True)
        self.xarm_client.clean_error()
        self.xarm_client.set_mode(0)
        self.xarm_client.set_state(0)
        self.xarm_client.sleep(1)
