# -*- coding: utf-8 -*-
from json_factory import JsonFactory
import svg_painter
import unittest
import xml.etree.cElementTree as ET

class TestMethods(unittest.TestCase):

  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')

  def test_lower(self):
    self.assertEqual('FOO'.lower(), 'foo')

  def test_get_cards_from_set(self):
    card_set = 'DM-13 Eternal Phoenix'
    cards = self.get_json_factory().get_cards_from_set(card_set)
    self.assertEqual(60, len(cards))

  def test_paint_creature1(self):
    text = u"When you put this creature into the battle zone, return (test) an evolution creature from your graveyard to your hand.\nBlocker (Whenever an opponent's creature attacks, you may tap this creature to stop the attack. Then the 2 creatures battle.)\nShield trigger (When this spell is put into your hand from your shield zone, you may cast it immediately for no cost.)\nSilent skill (At the start of each of your turns, if this creature is tapped, you may keep it tapped and use its $silent_skill ability.)\n$silent_skill Whenever one of your creature attacks this turn, you may draw a card."
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_creature(name="Testi Olento Jolla on Todella Pitkä Nimi", text=text), self.get_producer_test())

  def test_paint_creature2(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_multicolored_creature(["Light", "Water"]), self.get_producer_test())

  def test_paint_creature3(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_multicolored_creature(["Water", "Nature"]), self.get_producer_test())

  def test_paint_card_common(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_creature(rarity="Common"), self.get_producer_test())

  def test_paint_card_uncommon(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_creature(rarity="Uncommon"), self.get_producer_test())

  def test_paint_card_rare(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_creature(rarity="Rare"), self.get_producer_test())
  
  def test_paint_card_very_rare(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_creature(rarity="Very Rare"), self.get_producer_test())

  def test_paint_card_super_rare(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_creature(rarity="Super Rare"), self.get_producer_test())

  def test_paint_spell(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_spell(), self.get_producer_test())

  def test_paint_evolution_creature(self):
    svg_painter.get_svg_for_card(ET.Element("svg"), 0, 0, self.get_evolution_creature(), self.get_producer_test())

  def test_paint_page_for_nine_cards(self):
    svg_painter.paint_page_for_nine_cards("../test_paint_page.svg", self.get_producer_test(), self.get_json_factory().get_cards_from_set("DM-13 Eternal Phoenix")[0:9])

  def test_spell_without_civilization(self):
    self.assertRaises(svg_painter.MissingCivilizationException, svg_painter.get_svg_for_card, ET.Element("svg"), 0, 0, self.get_spell().pop('civilizations'), self.get_producer_test())

  def test_main(self):
    svg_painter.main()

  def test_creature_with_invalid_civilization(self):
    creature = {
      "name": "Name",
      "set": "DM-13 Eternal Phoenix",
      "civilization": "invalidcivilization",
      "id": "23",
      "rarity": "Common",
      "type": "Creature",
      "cost": 4,
      "illustrator": "Nakagawa",
      "race": "Hedrian",
      "power": "3000"
    }
    self.assertRaises(svg_painter.InvalidCivilizationException, svg_painter.get_svg_for_card, ET.Element("svg"), 0, 0, creature, self.get_producer_test())

  def test_paint_all_pages(self):
    json_factory = self.get_json_factory()
    cards = json_factory.get_cards_from_set("DM-13 Eternal Phoenix")
    self.assertRaises(ValueError, svg_painter.paint_set, cards, self.get_producer_test(), [], json_factory, "..")

  def test_get_civs(self):
    self.assertRaises(svg_painter.MissingCivilizationException, svg_painter.get_civs, {})

  def test_get_text_fill(self):
    self.assertRaises(svg_painter.MissingCivilizationException, svg_painter.get_text_fill, {})

  def test_get_fill_for_civilization_dark(self):
    self.assertRaises(svg_painter.InvalidCivilizationException, svg_painter.get_fill_for_civilization_dark, "invalid_civilization")

  def get_producer_test(self):
    return "©2004 Wizards of the Coast"

  def get_json_factory(self):
    return JsonFactory("../../duel-masters-json/DuelMastersCards.json")

  def get_creature(self, name="Testi Olento", civilization="Light", rarity="Common", text=u"Jotain tekstiä."):
    return {
      "name": name,
      "set": "DM-13 Eternal Phoenix",
      "id": "23",
      "civilization": civilization,
      "rarity": rarity,
      "type": "Creature",
      "cost": 4,
      "text": text,
      "flavor": u"\"Nice to meet you! What followed was a forced regimen of obstacle courses, slopstacle courses, egg races, and pizza slams. Whenever they saw us getting used to a routine, they changed it up. Never letting us rest. Never letting us see our loved ones. Children, teachers, even the custodial staff were randomly pulled out in front of the school and slimed for the cameras. When we tried to sleep, a large man dressed like Porkchop from Doug would bark in our faces, or the cast of All That would fire T-shirt cannons at us. It went on for weeks.\" —Drill Mutant",
      "illustrator": "Nakagawa",
      "race": "Hedrian",
      "power": "3000"
    }

  def get_multicolored_creature(self, civilizations):
    return {
      "name": "Name",
      "set": "DM-13 Eternal Phoenix",
      "id": "23",
      "civilizations": civilizations,
      "rarity": "Common",
      "type": "Creature",
      "cost": 4,
      "illustrator": "Nakagawa",
      "race": "Hedrian",
      "power": "3000"
    }
  
  def get_spell(self):
    return {
      "name": "The Grave of Angels and Demons",
      "set": "DM-13 Eternal Phoenix",
      "id": "16",
      "civilizations": [
        "Light",
        "Darkness"
      ],
      "rarity": "Rare",
      "type": "Spell",
      "cost": 4,
      "text": "(This spell is put into your mana zone tapped.)\nShield trigger (When this spell is put into your hand from your shield zone, you may cast it immediately for no cost.)\nIf there are 2 or more creatures that have the same name in the battle zone, destroy all of them. Then look at each player's mana zone. If there are 2 or more cards that have the same name, put all of them into their owner's graveyards.",
      "illustrator": "Masaki Hirooka"
    }

  def get_evolution_creature(self):
    return {
      "name": "Pacific Champion",
      "set": "DM-13 Eternal Phoenix",
      "id": "9",
      "civilization": "Water",
      "rarity": "Rare",
      "type": "Evolution Creature",
      "cost": 2,
      "text": u"Evolution — Put on one of your Merfolk.\nThis creature can't be attacked or blocked by non-evolution creatures.",
      "illustrator": "Syuichi Obata",
      "race": "Merfolk",
      "power": "5000"
    }

if __name__ == '__main__':
  unittest.main()