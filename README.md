# EV-BaseGame
Evolutionary algorithms to play basic games

## Experimental Examples

### Survival Rate

![surv](/sample_survival_progress.png)

### Gen 1:

![gen0](/sample_env_gifs/gen_000.gif)

### Gen 10:

![gen9](/sample_env_gifs/gen_009.gif)

### Gen 25:

![gen9](/sample_env_gifs/gen_024.gif)

### Gen 100:

![gen100](/sample_env_gifs/gen_099.gif)

## Experimental Examples 2

### Survival Rate

![surv](/sample2_survival_progress.png)

### Gen 1:

![gen0](/sample2_env_gifs/gen_000.gif)

### Gen 10:

![gen9](/sample2_env_gifs/gen_009.gif)

### Gen 25:

![gen9](/sample2_env_gifs/gen_024.gif)

### Gen 100:

![gen100](/sample2_env_gifs/gen_099.gif)

## Sample Mind-Map:

### Final Generation's Map:

![mind](/sample2_env_mind/gen_099_survived.png)

As we can see that when `y` is large, the agent is at the `bottom` of the map, which makes sense why the `move_north` neuron is activate. On the other hand, when `x` is too large, which means agent is on the `right` hand side, it activates the `move_west` neuron which pushes it towards the `left` side. The `move_west` neuron also gets deactivated with large values of `y` which means it potentially prefers to cover the `y` distance first.

### Interesting Maps:

![mind](/sample2_env_mind/gen_093_survived.png)

Taking a look at this we can see that when a pixel appears directly to the `west(02)` of the agent it reduces it's response-impulse towards `move_west` implying that it offers the agent to move `north`. This builds to the concept that upon blockage the agent has learnt to overcome it.
## Input Representations

```py
{
	"prev_direction" : options ("north", "south", "west", "east") --> default (Any of the four)
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
	"next_move" : options ("rest", "north", "south", "east", "west") # "forward", "left", "right", "backward")
}
```

The output must be a single probability distributions allowing the individual to make the next move. --> SOFTMAX (5 neurons in the output wing)

## Inner Neurons:

```py
// TO BE DEFINED
```

## Understanding the genomics:

Input context - 28 `input_variables` and 5 `output_variables`. Reconstituting the individual inputs to be representable.

`28 input_variables` --> closest 2 power is `32` --> basically `val=(00000)` to restrict space, to the 28 possible inputs, we mod val with 28 (`val%28`). Can extend by 4 new inputs.

`5 output_variables` --> closest 2 power is `8` --> basically `out=(000)` to restrict space, to the 5 possible inputs, we mod val with 5 (`out%5`). Can extend by 3 new outputs.

Now we want float values to represent the passing weights between the inputs/outputs. Lets begin understanding the sensitivity of the softmax function, we can simply extend the sigmoid function's sensitive to approximate softmax, as sigmoid is simply limited softmax.

![sigmoid](/images/sigmoid.png)

Looking at the graph, it should be substantial to consider upto 3 decimal places `._ _ _` at the same time, a bar between `[-4, 4]` should be sufficient. Therefore we need to find a numeric range constituting an integer space ??? `[0, 8000] ~ [0, 8192) = [0, 2^13)`. It will then be normalized as `(value-4096)/1000`.

```
| 0 | 00000 | 000 | 0-000-000-000-000 |
```
basically a total of `(1+5+3+13)=22` stream of binaries.

### Representation:

Although this isn't an essential representations are essential for visualizations. So lets discuss representations, now human DNA is represented by:

```md
1. adenine (A) - 00
2. guanine (G) - 01
3. cytosine (C) - 10
4. thymine (T) - 11
```

Basically it can encode two bins (`00`). So, we can represent our entire stream by a stream of 11 (`A/G/C/T`). Colour representation - pixel colours are an interesting aspect of visulaization so, what we do is represent them by `RGB=[0,256)`, therefore we can extend our stream of `22 bins` by `2 bins`, making it `24 bins`. Divide it into `8-8-8 bins` allowing us to compute RGB values.
