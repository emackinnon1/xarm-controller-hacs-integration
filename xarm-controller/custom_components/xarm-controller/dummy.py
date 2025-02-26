class XArmDummyAPI:
    """Dummy class to simulate xArm API."""

    def __init__(self, coordinator) -> None:
        """Initialize the dummy xArm API."""
        self.coordinator = coordinator

    @property
    def connected(self) -> None:
        return True

    @property
    def disconnect(self) -> None:
        return True

    @property
    def device_type(self) -> str:
        return 9

    @property
    def sn(self) -> int:
        return 123456789

    @property
    def state(self) -> int:
        return self.coordinator.get_xarm_model().state.state
    
    def connect(self, port: str) -> None:
        return True

    def clear_errors(self):
        self.coordinator.get_xarm_model().state.error_code = 0
        self.coordinator.get_xarm_model().state.has_error = False

    def emergency_stop(self):
        if self.coordinator.get_xarm_model().state.state == 4:
            self.coordinator.get_xarm_model().state.state = 2
        else:
            self.coordinator.get_xarm_model().state.state = 4

    def move_gohome(self):
        self.coordinator.get_xarm_model().position.x = 1
        self.coordinator.get_xarm_model().position.y = 1
        self.coordinator.get_xarm_model().position.z = 1

    def set_position(self, x: int = None, y: int = None, z: int = None):
        # k, v = kwargs
        # self.coordinator.get_xarm_model().position[k] = v
        if x is not None:
            self.coordinator.get_xarm_model().position.x = x
        if y is not None:
            self.coordinator.get_xarm_model().position.y = y
        if z is not None:
            self.coordinator.get_xarm_model().position.z = z

    def open_lite6_gripper(self):
        self.coordinator.get_xarm_model().gripper.position = 1000

    def close_lite6_gripper(self):
        self.coordinator.get_xarm_model().gripper.position = 0

    def open_gripper(self):
        self.coordinator.get_xarm_model().gripper.position = 1000

    def close_gripper(self):
        self.coordinator.get_xarm_model().gripper.position = 0

