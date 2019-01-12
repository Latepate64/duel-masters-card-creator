# -*- coding: utf-8 -*-

_multiplier = 0.0255

_character_ratios = {
  ".": 10,
  "￭": 18,
  " ": 20, #TODO: may need adjustment
  "(": 12,
  ")": 12,
  ",": 10,
  "'": 10,
  ":": 10,
  "!": 12,
  "?": 22,
  "a": 20,
  "b": 22,
  "c": 20,
  "d": 22,
  "e": 20,
  "f": 12,
  "g": 22,
  "h": 22,
  "i": 10,
  "j": 10,
  "k": 20,
  "l": 10,
  "m": 32,
  "n": 22,
  "o": 22,
  "p": 22,
  "q": 22,
  "r": 14,
  "s": 20,
  "t": 12,
  "u": 22,
  "v": 20,
  "w": 28,
  "x": 20,
  "y": 20,
  "z": 18,
  "ä": 20, #TODO: may need adjustment
  "A": 26,
  "B": 26,
  "C": 26,
  "D": 26,
  "E": 24,
  "F": 22,
  "G": 28,
  "H": 26,
  "I": 10,
  "J": 20,
  "K": 26,
  "L": 22,
  "M": 30,
  "N": 26,
  "O": 28,
  "P": 24,
  "Q": 28,
  "R": 26,
  "S": 24,
  "T": 22,
  "U": 26,
  "V": 24,
  "W": 34,
  "X": 24,
  "Y": 24,
  "Z": 22,
  "0": 20,
  "1": 18,
  "2": 20,
  "3": 20,
  "4": 20,
  "5": 20,
  "6": 20,
  "7": 20,
  "8": 20,
  "9": 20,
  "—": 36,
  "-": 12,
  '"': 17,
  "+": 21,
}

def get_text_height(text, fontsize, bold):
  return get_text_width_and_height(text, fontsize, bold)[1]

def get_text_width_and_height(text, fontsize, bold):
  multiplier = 0.62
  w = multiplier * len(text) * fontsize
  h = fontsize
  return w, h

class CardText:
  def __init__(self, paragraphs):
    self.paragraphs = paragraphs

  def get_row_count(self):
    row_count = 0
    for paragraph in self.paragraphs:
      row_count += len(paragraph.text_rows)
    return row_count

class Paragraph:
  def __init__(self, text_rows):
    self.text_rows = text_rows

class OuterParagraph(Paragraph):
  def __init__(self, text_rows, inner_paragraphs):
    Paragraph.__init__(self, text_rows)
    self.inner_paragraphs = inner_paragraphs

class InnerParagraph(Paragraph):
  def __init__(self, text_rows):
    Paragraph.__init__(self, text_rows)

class TextRow:
  def __init__(self, text_row_components):
    self.text_row_components = text_row_components

  def get_width(self, font_size):
    space_width = _character_ratios[" "] * _multiplier * font_size
    width = 0
    for text_row_component in self.text_row_components:
      if type(text_row_component) is AbilityIcon:
        width += text_row_component.get_width(font_size) + space_width
      elif type(text_row_component) is TextRowSpan:
        width += text_row_component.get_width(font_size) + space_width
    return width - space_width

  def deep_copy(self):
    components = []
    for comp in self.text_row_components:
      components.append(comp.deep_copy())
    return TextRow(components)

class TextRowComponent:
  pass

class AbilityIcon(TextRowComponent):
  def __init__(self, name):
    self.name = name

  def deep_copy(self):
    return AbilityIcon(self.name)

  def get_width(self, font_size):
    return font_size * 1.3

class TextRowSpan(TextRowComponent):
  def __init__(self, words, italic):
    self.words = words
    self.italic = italic

  def deep_copy(self):
    return TextRowSpan(self.words[:], self.italic)

  def get_width(self, font_size, add_space=False):
    text = self.get_text()
    if add_space:
      text += " "
    sum = 0
    for letter in text:
      sum += _character_ratios[letter]
    return _multiplier * sum * font_size

  def get_text(self):
    return " ".join(self.words)