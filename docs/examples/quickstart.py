from spiel import Deck, present

deck = Deck(name="Your Deck Name")


@deck.slide(title="Slide 1 Title")
def slide1():
    return """Your content here!"""


if __name__ == "__main__":
    present(__file__)
