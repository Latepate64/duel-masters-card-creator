offsets = ( 
  123,
  116,
  106,
  101,98,95,92,89,86,83,80,77,74,71,68,
  66,64,62,60,58,56,54,52,50,48,
  47,46,45,44,43,42,41,40,39,38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,
  15,15,14,14,13,13,12,12,11,11,10,10,9,9,8,8,7,7,6,6,5,5,
  4,4,4,
  3,3,3,3,3,3,
  2,2,2,2,2,2,
  1,1,1,1,1,1,1
)

from PIL import Image
import argparse
import os

image_width = 323

def save_image(im_path, cropped, destination):
  """Saves an image to a png-file."""
  save_path = "{0}/{1}".format(destination, im_path)[:-3]
  save_path += 'png' 
  cropped.save(save_path)

def crop_images_for_creatures(source, destination):
  """Crops images for creatures."""
  left = 56
  upper = 80
  h = 272
  for im_path in os.listdir(source):
    cropped = Image.open(''.join([source, im_path])).crop((left, upper, image_width + left, upper + h))
    save_image(im_path, cropped, destination)

def crop_images_for_spells(source, destination):
  """Crops images for spells."""
  for im_path in os.listdir(source):
    cropped = crop_image_for_spell('/'.join([source, im_path]))
    save_image(im_path, cropped, destination)

def crop_image_for_spell(image):
  """Crops an image for a spell."""
  left = 38
  upper = 79
  h = 270
  im = Image.open(image).crop((left, upper, image_width + left, upper + h)).convert("RGBA")
  y_pos = 0
  for offset in offsets:
    x_index = 0
    while x_index < offset:
      paint_pixel_transparent(im, x_index, y_pos)
      x_index += 1
    y_pos += 1
  return im

def crop_images_for_cross_gears(source, destination):
  """Crops images for cross gears."""
  for im_path in os.listdir(source):
    cropped = crop_image_for_cross_gear(''.join([source, im_path]))
    save_image(im_path, cropped, destination)

def crop_image_for_cross_gear(image):
  """Crops an image for a cross gear."""
  im = Image.open(image)
  left = 10
  upper = 79
  h = 270
  y_mid = upper+h/2
  width = 55
  im = im.crop((left, upper, image_width + left, upper + h)).convert("RGBA")
  for i in range(width):
    column_pixels_to_remove = y_mid-i
    for j in range(column_pixels_to_remove):
      skip = j + h/2 - column_pixels_to_remove
      paint_pixel_transparent(im, left+i, skip)
      paint_pixel_transparent(im, left+i, skip)
  return im

def paint_transparent_pixels(offset_count, current_offset, sub, im, y_pos):
  """Paints transparent pixels."""
  offset_count_index = 0
  while offset_count_index < offset_count:
    current_offset, offset_count_index, y_pos = paint_transparent_pixels_helper(current_offset, sub, offset_count_index, im, y_pos)
  sub -= 1
  return current_offset, sub, y_pos

def paint_transparent_pixels_helper(current_offset, sub, offset_count_index, im, y_pos):
  current_offset -= sub
  x_index = 0
  while x_index < current_offset:
    paint_pixel_transparent(im, x_index, y_pos)
    x_index += 1
  y_pos += 1
  offset_count_index += 1
  return current_offset, offset_count_index, y_pos

def paint_pixel_transparent(im, x_index, y_pos):
  """Paints a transparent pixel."""
  pixdata = im.load()
  pixdata[x_index, y_pos] = (255, 255, 255, 0)
  pixdata[image_width - x_index - 1, y_pos] = (255, 255, 255, 0)

def main():
  parser = argparse.ArgumentParser(description='Crop artwork from cards.')
  parser.add_argument('source', metavar='source', help='path containing images to be cropped')
  parser.add_argument('destination', metavar='destination', help='destination path for the cropped images (must exist before cropping)')
  parser.add_argument('card_type', metavar='card_type', help='type of the cards (Creature, Spell or Cross Gear)')
  args = parser.parse_args()
  print(args.card_type)
  print(args.card_type == 'Spell')
  if args.card_type == 'Creature':
    crop_images_for_creatures(args.source, args.destination)
  elif args.card_type == 'Spell':
    crop_images_for_spells(args.source, args.destination)
  elif args.card_type == 'Cross Gear':
    crop_images_for_cross_gears(args.source, args.destination)
  else:
    raise Exception('Unknown card type.')

if __name__ == "__main__":
  main()