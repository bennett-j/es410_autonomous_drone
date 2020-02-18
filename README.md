# es410_autonomous_drone
Warwick Engineering ES410 Group Project - Group 13

Repository to contain all of the code across 3 devices:

Raspberry Pi
- main.py
- landing_vision.py
- ground_communication.py
- flight_controller.py
- micro_controller.py
- data_logger.py
    
Arduino
- main.ino
    
Ground Control Station
- base_station.py

# User Guide

## Drone
_mostly written for the benefit of whoever writes the GCS code (aka: me)_

#### State: Initialisation
Drone tries to establish connections to other parts of the system. A variety of messages sent. If successful, final message reported is `Initialisation successful.`. If initialisation fails, failure reported then the python program exits. Decided not to reboot else might get stuck in an endless cycle where we can't do anything with the pi.

#### State: Idle
On entry: `Drone is idle. Waiting for command.`
| Command | Description | Expected response |
|---------|-------------|-------------------|
|`shutdown`| shutdown (power off) drone | `Drone is shutting down.` |
|`reboot`| reboot drone | `Drone is rebooting.`
|`mission`† | enter mission mode |

† After mission command, mission details must be received within 5 seconds. Details should be sent as a json with the following keys.
| Key | Data type | Comments |
|---------|-------------|-------------------|
| title | string | used for log title |
|  |  |  |
|  |  |  |

Once the drone receives the mission, it processes it, saving and distributing the necessary parameters. Upon completion, `Mission processing finished.` is returned.

#### State: Wait for battery load
Battery must be connected in 20 seconds. When a voltage is present, drone reports `Battery connected.`. GCS must confirm battery has been secured in a further 20 s with command `battery secured`. Drone reports `Battery loaded.`

#### State: Wait for parcel load
Parcel must be loaded within 30 seconds.

#### State: Check drone is armable
Currently just gets this from pixhawk, unsure if further checks should be done
| Result | Return | 
|---------|-------------|
|Checks Passed| `Drone ready to arm.` |
|Checks Failed| `Arming check failed.` |

#### State: Waiting for HWSS
Switch must be pressed within 30 s
| Description | Message sent | 
|---------|-------------|
| On state entry | `Waiting for hardware safety switch to be pressed.`|
| When switch pressed | `Switch pressed.`|
| Timeout | `Switch press timed out.`|

Between states (after switch is pressed) a pause of 5 seconds happens to prevent immediate arming of the drone.

#### State: Waiting for flight authorisation
Authorisation must be received within 30 s
| Description | Message sent | 
|---------|-------------|
| On state entry | `Waiting for authorisation to fly.`|
| Authorisation message received | `Authorisation received.`|
| Timeout | `Authorisation window timed out.`|

#### State: Release parcel
On entry: `Releasing parcel.`

On completion: `Parcel released.`

## Ground Control Station
_Using the Ground Control Station (GCS) is a trivial task on the whole because the program prompts the user for particular responses. Where commands must be entered, these are the same as required to send to the drone (detailed in 'Drone' section of the user guide). A few notes are contained below for the developer and which explain certain behaviour of the program._

#### Drone timeouts
The software currently doesn't handle drone timeout messages. The message will be printed to the command line but the program is then stuck in an infinite loop. This is undesirable behaviour which should be rectified.
