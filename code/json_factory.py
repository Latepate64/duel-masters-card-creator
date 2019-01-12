import json

class JsonFactory:

  def __init__(self, path):
    with open(path) as f:
      self._cards = json.load(f)

  def get_cards_from_set(self, card_set):
    """Returns all cards from a set."""
    cards = []
    for card in self._cards:
      if (card['set'] == card_set):
        cards.append(card)
    return cards

  def get_card_with_set_id_combination(self, card_set, id):
    """Returns a card from a set with an id."""
    for card in self._cards:
      if (card['set'] == card_set and card['id'] == id):
        return card