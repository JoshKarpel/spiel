# Making Slides

## Slide Content Functions

Each slide's content is rendered by calling a "content" function that returns a
[Rich `RenderableType`](https://rich.readthedocs.io/en/stable/console.html#printing).

There are two primary ways to define these content functions.
For unique slides you can use the [`Deck.slide`][spiel.Deck.slide] decorator:

```python
--8<-- "examples/slide_via_decorator.py"
```
![Slide content via decorator](./assets/slide_via_decorator.svg)

You might also find yourself wanting to create a set of slides programmatically
(well, even more programmatically).
You can use the [`Deck.add_slides`][spiel.Deck.add_slides] function to add
[`Slide`s][spiel.Slide] that you've created manually to your deck.

```python
--8<-- "examples/slide_loop.py"
```

![Slide content via loop 1](./assets/slide_loop_1.svg)
![Slide content via loop 2](./assets/slide_loop_2.svg)
![Slide content via loop 3](./assets/slide_loop_3.svg)

This pattern is useful when you have a generic "slide template"
that you want to feed multiple values into without copying a lot of code.
You have the full power of Python to define your slides,
so you can use as much (or as little) abstraction as you want.

!!! tip "Slides are added to the deck in execution order"

    The slide order in the presentation is determined by the order
    that the `Deck.slide` decorator and `Deck.add_slides` functions are used.
    The two methods can be freely mixed;
    just make sure to call them in the order you want the slides to
    be presented in.

## When and how often are slide content functions called?

The slide content function is called for a wide variety of reasons
and it is not generally possible to predict how many times or exactly when
it will be called due a mix of time-interval-based and on-demand needs.

Here are some examples of when the content function will be called:

- When you move to the slide in Slide view.
- Sixty times per second when the slide is active in Slide view (see [Triggers](#triggers) below).
- When you switch to Deck view.
- The active slide's content function will be called if the deck is reloaded.

!!! tip

    Because of how many times they will be called,
    your content functions should be *fast* and *stateless*.

    If your content function needs state,
    it should store and use it via the [Fixtures](#fixtures) discussed below.

## Fixtures

The slide content function can take extra
[keyword arguments](https://docs.python.org/3/glossary.html#term-argument)
that provide additional information for advanced rendering techniques.

To have Spiel pass your content function one of these fixtures,
include a keyword argument with the corresponding fixture name in your content function's signature.

### Triggers

- Keyword: `triggers`
- Type: [`Triggers`][spiel.Triggers]

The `triggers` fixture is useful for making slides whose content depends either on
relative time (e.g., time since the slide started being displayed)
or where the content should change when the user "triggers" it
(similar to how a PowerPoint animation can be configured to run
[`On Click`](https://support.microsoft.com/en-us/office/animate-text-or-objects-305a1c94-83b1-4778-8df5-fcf7a9b7b7c6)).

!!! info "`Trigger.now` resolution"

    Your slide content function will be called every sixtieth of a second,
    so the best time resolution you can get is about 16 milliseconds between
    renders, and therefore between `Trigger.now` values.
