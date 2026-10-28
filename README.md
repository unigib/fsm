# FSM editor examples — CSS45102

A curated collection of finite-state machine (FSM) examples for the University
of Gibraltar's CSS45102 class. The diagrams were created for use with
[Hneemann Digital](https://github.com/hneemann/Digital), a digital logic design
tool with an FSM editor.

## Examples

| File | Example |
| --- | --- |
| [`push1.fsm`](push1.fsm) | Push-button input and output states |
| [`counter10.fsm`](counter10.fsm) | Enabled, clearable decade counter with an overflow output |
| [`SevenSegCounter.fsm`](SevenSegCounter.fsm) | Enabled, clearable decade counter with seven-segment output values |
| [`rotDecoderMoore.fsm`](rotDecoderMoore.fsm) | Rotary encoder decoder with Moore-style outputs |
| [`rotDecoderMealy.fsm`](rotDecoderMealy.fsm) | Rotary encoder decoder with Mealy-style outputs |
| [`stepperSimple.fsm`](stepperSimple.fsm) | Four-state stepper motor sequence controlled by direction |
| [`stepperHalfStep.fsm`](stepperHalfStep.fsm) | Eight-state half-step motor sequence with direction and control inputs |
| [`trafficLightMoore.fsm`](trafficLightMoore.fsm) | Four-state traffic light sequence |
| [`trafficLightMedwedew.fsm`](trafficLightMedwedew.fsm) | Traffic light sequence represented with output-coded states |
| [`trafficLightBlink.fsm`](trafficLightBlink.fsm) | Traffic light sequence with a blinking/off state |
| [`Elevator5Floor.fsm`](Elevator5Floor.fsm) | Five-floor selector with one active-high button per floor |
| [`Elevator5FloorLatched.fsm`](Elevator5FloorLatched.fsm) | Five-floor elevator with latched requests, travel states and arrival clearing (matches the simulator) |
| [`elevator_simulator.py`](elevator_simulator.py) | Animated Tkinter demo of the five-floor elevator FSM |
| [`push_button_simulator.py`](push_button_simulator.py) | Interactive Tkinter demo of the four-state push-button lamp FSM |

These files are FSM diagrams, not standalone programs. Open a `.fsm` file in
Hneemann Digital to inspect or edit its states, transition conditions, and
outputs. The signal names and conditions are part of each example; refer to
them when adapting a diagram for a class exercise or simulation.

## Elevator demo (students)

Three files show the same five-floor elevator at increasing levels of realism.
Work through them in order.

| Step | File | What it shows |
| --- | --- | --- |
| 1 | `Elevator5Floor.fsm` | Simplest model: one state per floor, jumps straight to the selected floor |
| 2 | `Elevator5FloorLatched.fsm` | Realistic model: remembers several button presses and travels floor by floor |
| 3 | `elevator_simulator.py` | Software version that behaves like step 2, with an animated car |

### Running the animated simulator

Requires Python 3 with Tkinter (included with the standard Windows and macOS
installers). From this folder run:

```
python elevator_simulator.py
```

### Push-button lamp demo

Requires Python 3 with Tkinter. Run from this folder:

```
python push_button_simulator.py
```

Press and hold the on-screen switch (or hold Space), then release it. Each
complete press toggles the lamp. The four state bubbles show whether the
switch is up or down and the lamp output; the highlighted bubble is the
current FSM state. Keep [`logo.png`](logo.png) beside the script for the
University of Gibraltar branding.

1. Click one floor button (B5 is at the top, B1 at the bottom). The car
   travels there and the button switches off on arrival.
2. Click several buttons quickly. They light amber and stay lit until served.
3. Watch the panel: the car serves the **lowest-numbered** pressed floor first,
   and finishes the trip it has already started before changing target.
4. The panel shows the FSM output `F` in one-hot form (one bit set per floor,
   e.g. floor 3 is `00100`).

### Step 1: `Elevator5Floor.fsm`

- States: Floor 1 to Floor 5. Inputs: buttons `B1`–`B5` (active high).
- Output `F` is one-hot: Floor 1 = `00001` ... Floor 5 = `10000`.
- If several buttons are pressed, the lowest-numbered wins. No buttons means
  stay on the current floor.
- No travel time, doors or memory of presses: the state changes directly.

### Step 2: `Elevator5FloorLatched.fsm`

An FSM cannot remember an arbitrary set of pending buttons without a huge
number of states, so this model keeps that memory outside the FSM in five
request latches `R1`–`R5`. Each latch is set by its button and cleared by the
FSM's `CLR` output.

- States (25): `Idle n` = stopped at floor n; `p to t` = car at floor p,
  travelling to committed target t, one floor per clock.
- Inputs: `R1`–`R5`.
- Outputs: `F` (one-hot current floor), `M` (1 while moving), `CLR` (one-hot;
  active in `Idle n`, clears latch `Rn`).
- At idle, the lowest-numbered requested floor other than the current one is
  served next. With no requests, it stays put.
- Example: start at floor 1 with `R2`, `R4`, `R5` set. The car goes
  `1 to 2`, `Idle 2` (clears `R2`), `2 to 4`, `3 to 4`, `Idle 4`, `4 to 5`,
  `Idle 5`.

### Suggested exercises

1. In the simulator, press B5 then B2 while the car is moving up from floor 1.
   Predict the visiting order, then check it.
2. In step 2, trace the state sequence for `R3` and `R1` pressed while idle
   at floor 5.
3. Which signals are Moore outputs here (depend only on state)? Why is `CLR`
   needed?
4. Change the priority rule (for example, nearest floor first) by editing the
   transition conditions at an `Idle` state.
5. Compare one-hot (5 bits) with binary (3 bits) encoding of `F`. What are the
   trade-offs?

Note: the `.fsm` diagrams were generated programmatically. If the layout looks
untidy in Hneemann Digital, drag states and transition labels to rearrange them;
this does not change behaviour.

## About this collection

This repository curates example diagrams for educational use; it does not
include the Hneemann Digital application. See the [Digital project](https://github.com/hneemann/Digital)
for the editor and its documentation. The `.fsm` files are provided here as
class materials, separate from the editor project.
