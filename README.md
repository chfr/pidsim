

## PidSim
Some upcoming hardware projects of mine might require the use of PID control, so I put together a small utility to get familiar with it.

The simulator runs in ticks, and the sensor(s) read on a specific interval to simulate real-world conditions where sensor readings from (for example) a microcontroller may be slow but the real world continues to tick along on the outside.

For example, if we're modeling a control system for a heating element in a room (as `naive.py`, `p_controller.py` and `pi_controller.py` do currently, we can't expect the room's temperature to change instantly as we update the output of the heating element. Therefore, we control the delay between output and the next reading by changing the `TICKS_PER_READING` variable.


### Implementations
Each of these attempts to model a controller for a heating element in a room, where the sensor is a thermometer placed somewhere in the room.
#### NaiveController
A controller that does the equivalent turning the heating element up or down a set amount depending on if the temperature is higher or lower than desired. Very prone to oscillation.

#### PController
Controller that implements **p**roportional control, where the heating element is adjusted based on how far from the target we are. The closer we get to the target temperature, the less "power" we feed to the heating element.

#### PIController
Controller that implements both **p**roptional and **i**ntegral control. Integral control looks at the previous readings and allows us to turn up the "power" even more if we continue to be far off the target.