# maykb G4

This is my fourth custom split keyboard, this time using an ANSI layout.

## Caveats / Known Issues

In its current form, the level shifter for the WS2812b LEDs does NOT work.
With most clones, you can just remove the Mosfet and the two resistors next to it and bridge the microcontroller LED data input directly to the LED data input.
Some LEDs might not properly recognize the 3.3V signal though, so you might see some glitches due to this.

Otherwise, the keyboard works without any issues.
