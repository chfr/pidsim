import random

from pidsim import PidSimulator
from utils import fuzz_factor


class NaiveController(PidSimulator):
    MIN_DELTA = 0.075

    def __init__(self):
        super(NaiveController, self).__init__()
        self.temperature = 20
        self.target_temperature = 25
        self.temperature_delta = 0.0

    def _tick(self):
        super(NaiveController, self)._tick()
        self.temperature += self.temperature_delta * fuzz_factor()

    def _read_sensor(self):
        super(NaiveController, self)._read_sensor()

        reading = self.temperature
        self.print("Sensor returns {}".format(round(reading, 1)))

        return reading

    def _act(self, sensor_value):
        super(NaiveController, self)._act(sensor_value)

        diff = self.target_temperature - self.temperature

        if diff < 0:
            self.temperature_delta = -self.MIN_DELTA
        elif diff == 0.0:
            self.temperature_delta = random.random() * 0.2
        else:
            self.temperature_delta = self.MIN_DELTA


if __name__ == "__main__":
    sim = NaiveController()
    sim.run()
