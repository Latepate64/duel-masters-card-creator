# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import text_utility
from text_utility import CardText, InnerParagraph, OuterParagraph, TextRow, TextRowComponent, TextRowSpan, AbilityIcon
import image_painter

_text_width_diff = 16
_text_width_max = 182
_text_width_inner_max = _text_width_max - _text_width_diff
_y_paragraph_offset = 1
_quote_dash = u'—'
_skip_icon_words = ['Blocker', 'Shield trigger']

def set_font_family(element, font_family):
  element.set("font-family", font_family)

def paint_name(svg, x, y, text, text_width_max, font_size):
  element = ET.SubElement(svg, "text", x=str(x))
  element.set("text-anchor", "middle")
  element.set("font-weight", "bold")
  font_size = get_font_size_for_name(text, font_size, text_width_max)
  element.set("font-size", str(font_size))
  set_font_family(element, "perceval, sans-serif")
  height = text_utility.get_text_height(text, font_size, True)
  element.set("y", str(y+height*0.5))
  element.text = text

def get_font_size_for_name(text, font_size, text_width_max):
  if TextRowSpan(text.split(" "), False).get_width(font_size) > text_width_max:
    return get_font_size_for_name(text, 0.99*font_size, text_width_max)
  else:
    return font_size

def manage_text_rows(font_size, text_row, text_width_max):
  rows = []
  current_row = TextRow([])
  for text_row_component in text_row.text_row_components:
    if type(text_row_component) is AbilityIcon:
      test_row = current_row
      test_row.text_row_components.append(text_row_component)
      if test_row.get_width(font_size) < text_width_max:
        current_row = test_row
      else:
        rows.append(current_row.deep_copy())
        current_row.text_row_components = [text_row_component]

    elif type(text_row_component) is TextRowSpan:
      current_text_row_span = TextRowSpan([], text_row_component.italic)
      test_row = current_row
      test_row.text_row_components.append(current_text_row_span)

      for word in text_row_component.words:
        test_text_row_span = current_text_row_span.deep_copy()
        test_text_row_span.words.append(word)
        test_row = current_row.deep_copy()
        test_row.text_row_components[-1] = test_text_row_span
        if test_row.get_width(font_size) < text_width_max:
          current_row = test_row.deep_copy()
          current_text_row_span = test_text_row_span.deep_copy()
        else:
          rows.append(current_row)
          current_row = TextRow([])
          current_text_row_span = TextRowSpan([word], text_row_component.italic)
          current_row.text_row_components.append(current_text_row_span)
    else:
      raise "Unknown TextRowComponent."
  rows.append(current_row)

  return rows

def modify_card_text_rows(font_size, original_card_text):
  paragraphs = []
  for outer_paragraph in original_card_text.paragraphs:
    latest_outer_paragraph = OuterParagraph([],[])
    original_outer_text_row =  outer_paragraph.text_rows[0]
    latest_outer_paragraph.text_rows.extend(manage_text_rows(font_size, original_outer_text_row, _text_width_max))

    for inner_paragraph in outer_paragraph.inner_paragraphs:
      original_inner_text_row =  inner_paragraph.text_rows[0]
      new_inner_paragraph = InnerParagraph([])
      new_inner_paragraph.text_rows.extend(manage_text_rows(font_size, original_inner_text_row, 0.9 * _text_width_inner_max))
      latest_outer_paragraph.inner_paragraphs.append(new_inner_paragraph)

    paragraphs.append(latest_outer_paragraph)

  return CardText(paragraphs)

def paint_card_text(svg, x, y, font_size, card, y_flavor):
  """Paints text to a card."""
  y_org = y
  font_size_flavor = 0.85*font_size
  text_height = 0
  card_text = CardText([])
  if 'text' in card:
    card_text_org = CardText(get_paragraphs_with_black_squares(manage_special_characters(card['text'])))
    card_text = modify_card_text_rows(font_size, card_text_org)
  flavor_text_row_spans = []
  if 'flavor' in card:
    flavor_text_row_spans = get_text_row_spans_for_flavor(manage_special_characters(card['flavor']), font_size_flavor)
  text_height = (len(card_text.paragraphs)-1) * _y_paragraph_offset + card_text.get_row_count() * font_size + len(flavor_text_row_spans) * font_size_flavor
  height_threshold = 60
  if text_height > height_threshold:
    scale = 0.99
    paint_card_text(svg, x, y, scale*font_size, card, y_flavor)
  else:
    paint_card_text_helper(svg, x, y, font_size, card_text)
    paint_flavor(svg, x, y_org+y_flavor, flavor_text_row_spans, font_size_flavor)

def paint_card_text_helper(svg, x, y, font_size, card_text):
  y_index = 0
  for outer_paragraph in card_text.paragraphs:
    y_index = paint_text_rows(svg, x, y, font_size, outer_paragraph.text_rows, y_index)
    for inner_paragraph in outer_paragraph.inner_paragraphs:
      y_index = paint_text_rows(svg, x + _text_width_diff, y, font_size, inner_paragraph.text_rows, y_index)
  
def paint_text_rows(svg, x, y, font_size, rows, y_index):
  for row in rows:
    paint_text_row(svg, x, y + y_index * (_y_paragraph_offset + font_size), font_size, row)
    y_index += 1
  return y_index + 0.2 # 0.1

def paint_text_row(svg, x, y, font_size, row):
  x_add = 0
  for text_row_component in row.text_row_components:
    if type(text_row_component) is AbilityIcon:
      image_painter.paint_image(svg, x+x_add, y-font_size, font_size, font_size, "img/ability/{}.png".format(text_row_component.name))
      x_add += text_row_component.get_width(font_size)
      pass
    elif type(text_row_component) is TextRowSpan:
      font_style = "normal"
      if text_row_component.italic:
        font_style = "italic"
      paint_text(svg, str(x+x_add), str(y), text_row_component.get_text(), "bold", str(font_size), "itc-officina-sans-pro, sans-serif", font_style=font_style)
      x_add += text_row_component.get_width(font_size, True)
    else:
      raise "Unknown TextRowComponent."

def manage_special_characters(text):
  return text.replace('â€”', u'—')

def get_text_row_spans_for_flavor(flavor, font_size):
  text_row_spans = []
  for line in get_flavor_parts(flavor):
    get_text_row_spans_for_flavor_helper(line, font_size, text_row_spans)
  return text_row_spans

def get_text_row_spans_for_flavor_helper(flavor, font_size, text_row_spans):
  text_row_span_buffer = TextRowSpan([], True)
  for word in flavor.split():
    text_row_span_test = text_row_span_buffer.deep_copy()
    text_row_span_test.words.append(word)
    if text_row_span_test.get_width(font_size) > _text_width_max:
      text_row_spans.append(text_row_span_buffer)
      text_row_span_buffer = TextRowSpan([word], True)
    else:
      text_row_span_buffer = text_row_span_test.deep_copy()
  text_row_spans.append(text_row_span_buffer)

def paint_flavor(svg, x, y, text_row_spans, font_size):
  for i in range(len(text_row_spans)):
    if text_row_spans[i].words[0].startswith(u'—'):
      element = ET.SubElement(svg, "text", x=str(x+178), y=str(y+(i+1-len(text_row_spans))*font_size))
      element.set("font-size", str(font_size))
      element.set("font-style", "italic")
      set_font_family(element, "itc-officina-sans-pro, sans-serif")
      element.set("text-anchor", "end")
      element.text = text_row_spans[i].get_text()
    else:
      element = ET.SubElement(svg, "text", x=str(x), y=str(y+(i+1-len(text_row_spans))*font_size))
      element.set("font-size", str(font_size))
      element.set("font-style", "italic")
      set_font_family(element, "itc-officina-sans-pro, sans-serif")
      element.text = text_row_spans[i].get_text()

def get_paragraphs_with_black_squares(text):
  """Returns paragraphs with black squares added."""
  final_paragraphs = []
  paragraphs = text.split('\n')
  latest_outer_paragraph = None
  for paragraph in paragraphs:
    if paragraph.startswith('$'):
      inner_paragraph = InnerParagraph([get_text_row(paragraph)])
      latest_outer_paragraph.inner_paragraphs.append(inner_paragraph)
    else:
      print_icon = False
      for icon_word in _skip_icon_words:
        if paragraph.startswith(icon_word):
          print_icon = True
          break
      if not print_icon:
        paragraph = u'￭ {}'.format(paragraph)
      text_rows = [get_text_row(paragraph)]
      latest_outer_paragraph = OuterParagraph(text_rows, [])
      final_paragraphs.append(latest_outer_paragraph)
  return final_paragraphs

def get_text_row(paragraph):
  """Returns a text row."""
  return TextRow(get_text_row_components(paragraph))

def get_text_row_components(paragraph):
  """Return components for text rows."""
  text_row_components = []
  text = paragraph

  for icon_word in _skip_icon_words:
    if paragraph.startswith(icon_word):
      text_row_components.append(AbilityIcon(get_text_for_ability(icon_word)))

  current_italic = False
  while len(text) > 0:
    dollar_sign = text.find('$')
    left_bracket = text.find('(')
    right_bracket = text.find(')')

    if dollar_sign == 0:
      splits = text.split(' ', 1)
      text_row_components.append(AbilityIcon(splits[0][1:]))
      text = splits[1]

    elif current_italic == False:
      minimum = -1
      if left_bracket == -1 and dollar_sign == -1:
        text_row_components.append(TextRowSpan(text.split(), False))
        break
      elif dollar_sign == -1: #Left bracket found
        minimum = left_bracket
      elif left_bracket == -1: #Dollar sign found
        minimum = dollar_sign
      if minimum == -1:
        minimum = min([left_bracket, dollar_sign])
      current_italic = (minimum == left_bracket)
      text_row_components.append(TextRowSpan(text[:minimum].split(), False))
      text = text[minimum:]

    else:
      minimum = -1
      if right_bracket == -1 and dollar_sign == -1:
        raise "Expected right bracket."
      elif dollar_sign == -1: #Right bracket found
        minimum = right_bracket
      elif right_bracket == -1: #Dollar sign found
        minimum = dollar_sign
      if minimum == -1:
        minimum = min([right_bracket, dollar_sign])
      current_italic = (minimum != right_bracket)
      if minimum == right_bracket:
        minimum += 2
      text_row_components.append(TextRowSpan(text[:minimum].split(), True))
      text = text[minimum:]
  return text_row_components

def get_text_for_ability(text):
  return text.replace(' ', '_').lower()

def get_flavor_parts(flavor):
  index = flavor.find(_quote_dash)
  parts = [flavor]
  if index > -1:
    parts = [flavor[:index], flavor[index:]]
  return parts

def paint_text(svg, x, y, text, font_weight, font_size, font_family, font_style="normal", fill="black"):
  element = ET.SubElement(svg, "text", x=str(x), y=str(y), fill=fill)
  element.set("font-weight", font_weight)
  element.set("font-size", font_size)
  element.set("font-style", font_style)
  set_font_family(element, font_family)
  element.text = text

def paint_race(svg, x, y, race, font_size):
  """Paints race."""
  element = ET.SubElement(svg, "text", x=str(x), y=str(y))
  element.set("text-anchor", "middle")
  element.set("font-weight", "bold")
  element.set("font-size", str(font_size))
  set_font_family(element, "armada, sans-serif")
  element.text = race.upper()

def paint_cost(svg, x, y, cost, font_size):
  element = ET.SubElement(svg, "text", x=str(x), y=str(y), style="fill:white")
  element.set("font-size", str(font_size))
  element.set("font-weight", "bold")
  element.set("text-anchor", "middle")
  set_font_family(element, "armada, sans-serif")
  element.text = str(cost)