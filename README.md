# EV-BaseGame
Evolutionary algorithms to play basic games

## Defining agent inputs:

```py
{
	"prev_direction" : options ("north", "south", "west", "east") --> default ("north")
	"moving" : options (0 - `previously_at_rest`, 1 - `previously_moving`) --> default (0)
	"x" : range (0, WIDTH)
	"y" : range (0, HEIGHT)
	"surround_space_pixel_00" --> options (0 - `empty space`, 1 - `map_border`, 2 - `another_bot`) --> default (0)
	...
	"surround_space_pixel_13" --> options (0 - `empty space`, 1 - `map_border`, 2 - `another_bot`) --> default (0)
	...
	"surround_space_pixel_44" --> options (0 - `empty space`, 1 - `map_border`, 2 - `another_bot`) --> default (0)
}
```

The model basically receives a total of 2 (self-based) + 2 (global) + 24 (surroundings) --> 28 inputs.

## Defining agent outputs:

```py
{
	"next_move" : options ("rest", "forward", "left", "right", "backward")
}
```

The output must be a single probability distributions allowing the individual to make the next move. --> SOFTMAX (5 neurons in the output wing)

## Inner Neurons:

```py
// TO BE DEFINED
```

## Understanding the genomics:

Input context - 