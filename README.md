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

Input context - 24 `input_variables` and 5 `output_variables`. Reconstituting the individual inputs to be representable.

`24 input_variables` --> closest 2 power is `32` --> basically `val=(00000)` to restrict space, to the 24 possible inputs, we mod val with 24 (`val%24`).

`5 output_variables` --> closest 2 power is `8` --> basically `out=(000)` to restrict space, to the 5 possible inputs, we mod val with 5 (`out%5`).

Now we want float values to represent the passing weights between the inputs/outputs. Lets begin understanding the sensitivity of the softmax function, we can simply extend the sigmoid function's sensitive to approximate softmax, as sigmoid is simply limited softmax.



```
| 0/1 | 00000 | 000 | 
```