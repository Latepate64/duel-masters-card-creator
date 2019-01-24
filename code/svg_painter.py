# -*- coding: utf-8 -*-
import datetime
import math
import xml.etree.cElementTree as ET
import image_painter
from json_factory import JsonFactory
import text_painter
import text_utility

_card_height = 330
_card_width = _card_height*0.7159
_border_width = _card_height/33
_frame_fill = "fill:black"
_misc_font_size_text = "4.4"
_x_text_ratio = 0.125

_dict_civilization_fill = {
  'Light': 'fill:rgb(253,241,159)',
  'Water': 'fill:rgb(186,218,239)',
  'Darkness': 'fill:rgb(89,84,80)',
  'Fire': 'fill:rgb(239,146,112)',
  'Nature':'fill:rgb(155,175,116)'
}

_dict_civilization_dark_fill = {
  'Light': 'fill:rgb(254,217,100)',
  'Water': 'fill:rgb(130,194,230)',
  'Darkness': 'fill:rgb(98,93,89)',
  'Fire': 'fill:rgb(210,37,31)',
  'Nature':'fill:rgb(42,114,90)'
}

def get_circle_points(r, initial_rad, length_rad):
  """Get points that represent a circle."""
  points = []
  point_amount = 100
  for rad in range(point_amount):
    x_help = initial_rad+rad*length_rad/float(point_amount)
    x = r*math.cos(x_help)
    y = r*math.sin(x_help)
    points.append((x, y))
  return points

def get_spec_h(ratio):
  """Returns height relative to card height."""
  return ratio*_card_height

def get_spec_w(ratio):
  """Returns width relative to card width."""
  return ratio*_card_width

def paint_rect(svg, x, y, width, height, style):
  """Paints a rectangle."""
  return ET.SubElement(svg, "rect", width=str(width), height=str(height), style=style, x=str(x), y=str(y))

def paint_rect_with_opacity(svg, x, y, width, height, style, opacity):
  """Paints a rectangle with certain opacity."""
  element = paint_rect(svg, x, y, width, height, style)
  element.set("opacity", str(opacity)) 

def get_fill_for_civilization(civ):
  """Returns a color fill for a civilization."""
  if civ in _dict_civilization_fill:
    return _dict_civilization_fill[civ]
  else: #multiciv
    return 'fill:rgb(196,157,184)'
    
def get_fill_for_civilization_dark(civ):
  """Returns a dark color fill for a civilization."""
  if civ in _dict_civilization_dark_fill:
    return _dict_civilization_dark_fill[civ]
  else:
    raise InvalidCivilizationException

def paint_card_frame(svg, x, y, civ):
  """Paints a frame and background for a card."""
  if '_' in civ:
    civ = 'multi'
  rect = paint_rect(svg, x, y, _card_width, _card_height, _frame_fill)
  rounded = "7"
  rect.set("rx", rounded)
  rect.set("ry", rounded)
  image_painter.paint_image(svg, x+_border_width, y+_border_width, _card_width-2*_border_width, _card_height - 2*_border_width, 'img/background/{}.jpg'.format(civ))

def paint_card_image(svg, x, y, width, height, card_id, card_set):
  """Paints an artwork to a card."""
  card_set = card_set.lower()
  path = 'img/artwork/{0}/{1}.png'.format(card_set, get_id_number(card_id))
  image_painter.paint_image(svg, str(x), str(y), str(width), str(height), path)

def paint_power(svg, x, y, power, font_size):
  """Paints power with black background and white foreground."""
  text_painter.paint_text(svg, x+1.5, y+0.75, power, "900", str(font_size), "armada, sans-serif")
  text_painter.paint_text(svg, x, y, power, "900", str(font_size), "armada, sans-serif", fill="white")
  
def paint_cost_frame(svg, x, y, width_t, length):
  """Paints a cost frame to a card."""
  points_right = [(length,0),(length,width_t)]
  points_left = []
  for point in reversed(points_right):
    points_left.append((point[1], point[0]))
  points = [(0,0)]
  points.extend(points_right)
  points.append((width_t,width_t))
  points.extend(points_left)
  paint_polygon(svg, get_points_text(x, y, points), _frame_fill)
  origo_x = x
  origo_y = y
  radius = get_spec_h(0.088)
  circle_points = get_circle_points(radius, 2*math.pi, math.pi/2)
  circle_points.append((0, 0))
  paint_polygon(svg, get_points_text(origo_x, origo_y, circle_points), _frame_fill)
  
def paint_cost_frame_multi(svg, x, y, fills): 
  rad_inner = get_spec_h(0.052)
  rad_outer = get_spec_h(0.072)
  rad_dist = math.pi/4
  diameter = get_spec_h(0.012)
  rect_length = diameter * 3.5
  paint_cost_frame_multi_helper1(svg, x, y, fills[0], math.pi/4, rad_inner, rad_outer, rad_dist, diameter, rect_length)
  paint_cost_frame_multi_helper2(svg, x, y, fills[1], 0, rad_inner, rad_outer, rad_dist, diameter, rect_length)

def paint_cost_frame_multi_helper1(svg, x, y, fill, initial_rad, rad_inner, rad_outer, rad_dist, diameter, rect_length):
  lower_outer_points = get_circle_points(rad_outer, initial_rad, rad_dist)
  lower_outer_points.append((0, rad_inner))
  lower_outer_points.extend(list(reversed(get_circle_points(rad_inner, initial_rad, rad_dist))))
  paint_polygon(svg, get_points_text(x, y, lower_outer_points), fill)
  paint_rect(svg, x, y+rad_inner, diameter, rect_length, fill)

def paint_cost_frame_multi_helper2(svg, x, y, fill, initial_rad, rad_inner, rad_outer, rad_dist, diameter, rect_length):
  lower_outer_points = list(reversed(get_circle_points(rad_inner, 0, rad_dist)))
  lower_outer_points.append((rad_outer, 0))
  lower_outer_points.extend(get_circle_points(rad_outer, initial_rad, rad_dist))
  paint_polygon(svg, get_points_text(x, y, lower_outer_points), fill)
  paint_rect(svg, x+rad_inner, y, rect_length, diameter, fill)

def get_fills_for_civs(civs):
  fills = []
  for civ in civs:
    fills.append(get_fill_for_civilization_dark(civ))
  return fills

def get_points_text(x, y, points):
  points_texts = []
  for point in points:
    points_texts.append("{0},{1}".format(x+point[0], y+point[1]))
  return ", ".join(points_texts)

def paint_polygon(svg, points_text, fill):
  return ET.SubElement(svg, "polygon", style=fill, points=points_text)

def paint_circle(svg, cx, cy, r, fill):
  return ET.SubElement(svg, "circle", cx=str(cx), cy=str(cy), r=str(r), style=fill)

def paint_mana_number(svg, cx, cy, civ, text_fill):
  r_inner = get_spec_h(0.039)
  paint_circle(svg, cx, cy, get_spec_h(0.044), "fill:black")
  civs = [civ, civ]
  if '_' in civ:
    civs = civ.split('_')

  paint_polygon(svg, get_points_text(cx, cy, get_circle_points(r_inner, math.pi/3, math.pi)), get_fill_for_civilization_dark(civs[0]))
  paint_polygon(svg, get_points_text(cx, cy,  get_circle_points(r_inner,  math.pi*4/3, math.pi)), get_fill_for_civilization_dark(civs[1]))
  x = cx + get_spec_h(0.019)
  y = cy - get_spec_h(0.023)
  element = ET.SubElement(svg, "text", x=str(x), y=str(y), transform="rotate(180,{0},{1})".format(x, y), style=text_fill)
  element.set("font-size", str(get_spec_h(0.07)))
  element.set("font-weight", "bold")
  element.text = '1'
  #text_painter.set_font_family(element, "perceval, sans-serif")

def paint_illustrator(svg, x, y, illustrator, fill, font_size):
  element = ET.SubElement(svg, "text", x=str(x), y=str(y), style=fill)
  element.set("text-anchor", "end")
  element.set("font-weight", "bold")
  element.set("font-size", str(font_size))
  element.text = "illus. {}".format(illustrator)

def paint_card_type(svg, cx, cy, width, height, card_type, fills, font_size):
  sep = 3
  half_width = width/2
  half_height = height/2
  points_left = [(-half_width,-half_height), (-sep, -half_height), (+sep, +half_height), (-half_width,+half_height)]
  paint_polygon(svg, get_points_text(cx, cy, points_left), fills[0])
  index = len(fills)-1
  points_right = [(-sep, -half_height), (half_width, -half_height), (half_width,half_height), (sep,half_height)]
  paint_polygon(svg, get_points_text(cx, cy, points_right), fills[index])
  text = card_type.upper()
  element = ET.SubElement(svg, "text", x=str(cx), y=str(cy+text_utility.get_text_height(text, font_size, True)*0.5))
  element.set("text-anchor", "middle")
  element.set("font-weight", "bold")
  element.set("font-size", str(font_size))
  text_painter.set_font_family(element, "armada, sans-serif")
  element.text = text

def paint_publisher(svg, x, y, fill, producer_text, font_size):
  element = ET.SubElement(svg, "text", x=str(x), y=str(y), style=fill)
  element.set("font-size", str(font_size))
  element.set("text-anchor", "end")
  element.text = producer_text

def paint_rarity(svg, x, y, r, rarity, fill, background_fill):
  if rarity == "Common":
    paint_rarity_common(svg, x, y, r, fill)
  elif rarity == "Uncommon":
    paint_rarity_uncommon(svg, x, y, r, fill)
  elif rarity == "Rare":
    paint_rarity_rare(svg, x, y, r, fill)
  elif rarity == "Very Rare":
    paint_rarity_very_rare(svg, x, y, r, fill, background_fill)
  elif rarity == "Super Rare":
    paint_rarity_super_rare(svg, x, y, r, fill)

def paint_rarity_common(svg, cx, cy, r, fill):
  paint_circle(svg, cx, cy, r, fill)

def paint_rarity_uncommon(svg, x, y, r, fill):
  points = [(0,r), (r,0), (0,-r), (-r,0)]
  paint_polygon(svg, get_points_text(x, y, points), fill)

def paint_rarity_rare(svg, x, y, r, fill):
  points_right = [(r/3,-r/4), (r,-r/4), (r/3,r/4), (2*r/3,r)]
  points_left = []
  for point in reversed(points_right):
    points_left.append((-1 * point[0], point[1]))
  points = [(0,-r)]
  points.extend(points_right)
  points.append((0, r/2))
  points.extend(points_left)
  paint_polygon(svg, get_points_text(x, y, points), fill)

def paint_rarity_very_rare(svg, x, y, r, fill, background_fill):
  paint_rarity_common(svg, x, y, r, fill)
  paint_rarity_rare(svg, x, y, r, background_fill)

def paint_rarity_super_rare(svg, x, y, r, fill):
  paint_rect(svg, x+r/3, y-r/3, 2*r/3, 2*r/3, fill)
  paint_rect(svg, x-r/3, y-r, 2*r/3, 2*r/3, fill)
  paint_rect(svg, x-r/3, y+r/3, 2*r/3, 2*r/3, fill)
  paint_rect(svg, x-r, y-r/3, 2*r/3, 2*r/3, fill)

def get_offsets(x, card_type):
  x_image = x+get_spec_w(0.1041)
  x_illustrator = x+get_spec_w(0.94)
  x_type_box = x+get_spec_w(0.25)
  x_text_box = x+get_spec_w(0.087)
  x_name = x+get_spec_w(0.575)
  width_type_box = get_spec_h(0.25)
  text_width_max = get_spec_h(0.52)
  if card_type == 'Spell' or card_type == 'Loitsu':
    x_image = x+get_spec_w(0.05)
    x_illustrator = x+get_spec_w(0.908)
    x_type_box = x+get_spec_w(0.212)
    width_type_box = get_spec_w(0.25)
    x_name = x_name = x+get_spec_w(0.5)
    text_width_max = get_spec_h(0.432)
  return x_image, x_illustrator, x_type_box, x_text_box, width_type_box, x_name, text_width_max

def paint_evolution_sign(svg, x, y):
  r = 4
  width = 13
  height = 24
  im_length = 10
  points = [(0,0), (0,height), (width,height-r), (width,r)]
  paint_polygon(svg, get_points_text(x, y, points), _frame_fill)
  image_painter.paint_image(svg, x+(width-im_length)*0.5, y+(height-im_length)*0.5, im_length, im_length, "img/ability/evolution.png")

def get_civs(card):
  """Returns the civilization/s of the card as a list."""
  if 'civilization' in card:
    return [card['civilization']]
  elif 'civilizations' in card:
    return card['civilizations']
  else:
    raise MissingCivilizationException

def get_civilization_text(card):
  """Returns the civilization of the card. If card has multiple civilizations, the civilizations are joined by underscores."""
  if 'civilization' in card:
    return card['civilization']
  elif 'civilizations' in card:
    return '_'.join(card['civilizations'])
  else:
    raise MissingCivilizationException

def get_text_fill(card):
  """Returns a color fill for card text based on the civilization of the card."""
  if 'civilization' in card:
    civ = card['civilization']
    if civ == 'Darkness' or civ == 'Fire' or civ == 'Nature':
      return "fill:white"
    elif civ == 'Light' or civ == 'Water':
      return "fill:black"
    else:
      raise InvalidCivilizationException
  elif 'civilizations' in card:
    return "fill:black"
  else:
    raise MissingCivilizationException

def get_svg_for_card(svg, row, column, card, producer_text):
  """Returns a SVG representation for a card."""
  page_offset = 40
  x = row*_card_width + page_offset
  y = column*_card_height + page_offset
  civ = get_civilization_text(card)
  text_fill = get_text_fill(card)
  paint_card_frame(svg, x, y, civ.lower())
  x_image, x_illustrator, x_type_box, x_text_box, width_type_box, x_name, text_width_max = get_offsets(x, card['type'])
  paint_card_image(svg, x_image, y+get_spec_h(0.133), get_spec_h(0.64), get_spec_h(0.49), card['id'], card['set'])
  text_painter.paint_name(svg, x_name, y+get_spec_h(0.065), card['name'], text_width_max, get_spec_h(0.04))
  race = None
  if 'race' in card:
    race = card['race']
  if 'races' in card:
    race =' / '.join(card['races'])
  if race is not None:
    text_painter.paint_race(svg, x+get_spec_h(0.395), y+get_spec_h(0.122), race, get_spec_h(0.02))
  card_type_height = get_spec_h(0.02)
  paint_card_type(svg, x_type_box, y+get_spec_h(0.66), width_type_box, card_type_height, card['type'], get_fills_for_civs(get_civs(card)), get_spec_h(0.016))
  paint_rect_with_opacity(svg, x_text_box, y+get_spec_h(0.65)+card_type_height+0.25, get_spec_w(0.821), get_spec_h(0.245), "fill:white", 0.8)
  if card['type'] != 'Spell' and card['type'] != 'Loitsu':
    image_painter.paint_civilization_logo(svg, x+get_spec_w(0.505), y+get_spec_h(0.785), civ)
  x_text = x+get_spec_w(_x_text_ratio)
  text_painter.paint_card_text(svg, x_text, y+get_spec_h(0.71), 7.26, card, get_spec_h(0.18))
  if 'power' in card:
    paint_power(svg, x+get_spec_w(0.05), y+get_spec_h(0.966), card['power'], get_spec_h(0.064))
  paint_cost_frame(svg, x+_border_width-1, y+_border_width-1, get_spec_w(0.035), get_spec_w(0.145))
  if 'civilizations' in card:
    paint_cost_frame_multi(svg, x+_border_width, y+_border_width, get_fills_for_civs(card['civilizations']))
  text_painter.paint_cost(svg, x+get_spec_w(0.09), y+get_spec_h(0.085), card['cost'], get_spec_h(0.068))
  paint_illustrator(svg, x_illustrator, y+get_spec_h(0.6425), card['illustrator'], text_fill, get_spec_h(0.02))
  misc_font_size =  get_spec_h(0.0178)
  paint_publisher(svg, x+get_spec_w(0.85), y+get_spec_h(0.96), text_fill, producer_text, misc_font_size)
  paint_id(svg, x+get_spec_w(0.945), y+get_spec_h(0.96), text_fill, card['id'], misc_font_size)
  image_painter.paint_set_logo(svg, x+get_spec_w(0.896), y+get_spec_h(0.915), get_spec_h(0.03), get_spec_h(0.03), card['set'])
  paint_rarity(svg, x+get_spec_w(0.868), y+get_spec_h(0.953), get_spec_h(0.009), card['rarity'], text_fill, get_fill_for_civilization(civ))
  paint_mana_number(svg, x+get_spec_w(0.5), y+get_spec_h(0.942), civ, text_fill)
  if card['type'] == 'Evolution Creature':
    paint_evolution_sign(svg, x+_border_width-1, y+get_spec_h(0.613))
  return svg

def get_svg_element():
  """Returns a SVG for a background for the cards."""
  svg = ET.Element("svg")
  svg.attrib['version'] = '1.1'
  svg.attrib['width'] = "210mm"
  svg.attrib['height'] = "297mm"
  svg.attrib['xmlns'] = 'http://www.w3.org/2000/svg'
  svg.attrib['xmlns:xlink'] = 'http://www.w3.org/1999/xlink'
  return svg

def paint_page_for_nine_cards(output_path, producer_text, cards):
  """Paints a page containing 9 cards."""
  svg = get_svg_element()
  index = 0
  row_count = 3
  column_count = 3
  for column in range(row_count):
    for row in range(column_count):
      get_svg_for_card(svg, row, column, cards[index], producer_text)
      index += 1
  ET.ElementTree(svg).write(output_path + '.svg')

def paint_card(output_path, producer_text, card):
  svg = get_svg_element()
  get_svg_for_card(svg, 0, 0, card, producer_text)
  ET.ElementTree(svg).write(output_path + '.svg')

def get_id_number(text):
  """Returns the collector's number from an id (eg. 4/55 results in 4)."""
  return text.split('/')[0]

def paint_set(cards, producer_text, placeholder_cards, json_factory, initial_output_path):
  """Paints all cards from a set."""
  cards_in_page = 9
  chunks = [cards[x:x+cards_in_page] for x in range(0, len(cards), cards_in_page)]
  for chunk in chunks:
    first = chunk[0]
    last = chunk[-1]
    output_path = '{0}/{1}-{2}'.format(initial_output_path, get_id_number(first['id']), get_id_number(last['id']))
    if len(chunk) < cards_in_page:
      diff = cards_in_page - len(chunk)
      if diff == len(placeholder_cards):
        for card in placeholder_cards:
          chunk.append(json_factory.get_card_with_set_id_combination(card.find('set').text, card.find('id').text))
      else:
        raise ValueError('Expected {0} placeholder cards, got {1}.'.format(diff, len(placeholder_cards))) 
    paint_page_for_nine_cards(output_path, producer_text, chunk)

def paint_id(svg, x, y, fill, card_id, font_size):
  element = ET.SubElement(svg, "text", x=str(x), y=str(y), style=fill)
  element.set("text-anchor", "end")
  element.set("font-size", str(font_size))
  element.text = card_id

def main():
  configuration = ET.parse('configuration.xml').getroot()
  output_path = '..'
  json_factory = JsonFactory(configuration.find('json_path').text)
  producer_text = configuration.find('producer_text').text
  for print_set in configuration.iter('print_set'):
    paint_set(json_factory.get_cards_from_set(print_set.find('set').text), producer_text, print_set.find('placeholder_cards'), json_factory, output_path)
  for print_cards in configuration.iter('print_cards'):
    file_name = '{0}/{1}'.format(output_path, print_cards.find('name').text)
    cards = []
    for card in print_cards.find('cards'):
      cards.append(json_factory.get_card_with_set_id_combination(card.find('set').text, card.find('id').text))
    paint_page_for_nine_cards(file_name, producer_text, cards)
  for print_card in configuration.iter('print_card'):
    file_name = '{0}/{1}'.format(output_path, print_card.find('name').text)
    json_card = print_card.find('card')
    card = json_factory.get_card_with_set_id_combination(json_card.find('set').text, json_card.find('id').text)
    paint_card(file_name, producer_text, card)

if __name__ == "__main__":
  main()

class MissingCivilizationException(Exception):
  pass

class InvalidCivilizationException(Exception):
  pass
