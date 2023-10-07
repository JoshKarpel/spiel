# Slide Transitions

!!! warning "Under construction!"

    Transitions are a new and experiment feature in Spiel
    and the interface might change dramatically from version to version.
    If you plan on using transitions, we recommend pinning the
    exact version of Spiel your presentation was developed in to ensure stability.

## Setting Transitions

To set the default transition for the entire deck,
which will be used if a slide does not override it,
set [`Deck.default_transition`][spiel.Deck.default_transition] to
a **type** that implements the [`Transition`][spiel.Transition]
protocol.

For example, the default transition is [`Swipe`][spiel.Swipe],
so not passing `default_transition` at all is equivalent to

```python
from spiel import Deck, Swipe

deck = Deck(name=f"Spiel Demo Deck", default_transition=Swipe)
```

To override the deck-wide default for an individual slide,
specify the transition type in the [`@slide`][spiel.Deck.slide] decorator:

```python
from spiel import Deck, Swipe

deck = Deck(name=f"Spiel Demo Deck")

@deck.slide(title="My Title", transition=Swipe)
def slide():
    ...
```

Or, in the arguments to [`Slide`][spiel.Slide]:

```python
from spiel import Slide, Swipe

slide = Slide(title="My Title", transition=Swipe)
```

In either case, the specified transition will be used when
transitioning **to** that slide.
It does not matter whether the slide is the "next" or "previous"
slide: the slide being moved to determines which transition
effect will be used.

## Disabling Transitions

In any of the above examples, you can also set `default_transition`/`transition` to `None`.
In that case, there will be no transition effect when moving to the slide;
it will just be displayed on the next render, already in-place.

## Writing Custom Transitions

To implement your own custom transition, you must write a class which implements
the [`Transition`][spiel.Transition] [protocol](https://docs.python.org/3/library/typing.html#typing.Protocol).

The protocol is:

```python title="Transition Protocol"
--8<-- "spiel/transitions/protocol.py"
```

As an example, consider the [`Swipe`][spiel.Swipe] transition included in Spiel:

```python title="Swipe Transition"
--8<-- "spiel/transitions/swipe.py"
```

The transition effect is implemented using
[Textual CSS styles](https://textual.textualize.io/styles/)
on the [widgets](https://textual.textualize.io/guide/widgets/)
that represent the "from" and "to" widgets.

Because the slide widgets are on [different layers](https://textual.textualize.io/styles/layers/),
they would normally both try to render in the "upper left corner" of the screen,
and since the `from` slide is on the upper layer, it would be the one that actually gets rendered.

In `Swipe.initialize`, the `to` widget is moved to either the left or the right
(depending on the transition direction) by `100%`, i.e., it's own width.
This puts the slides side-by-side, with the `to` slide fully off-screen.

As the transition progresses, the horizontal offsets of the two widgets are adjusted in lockstep
so that they appear to move across the screen.
Again, the direction of offset adjustment depends on the transition direction.
The absolute value of the horizontal offsets always sums to `100%`, which keeps the slides glued together
as they move across the screen.

When `progress=100` in the final state, the `to` widget will be at zero horizontal offset,
and the `from` widget will be at plus or minus `100%`, fully moved off-screen.

!!! tip "Contribute your transitions!"

    If you have developed a cool transition, consider [contributing it to Spiel](./contributing.md)!
