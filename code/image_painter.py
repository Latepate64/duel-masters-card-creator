import xml.etree.cElementTree as ET

def paint_image(svg, x, y, width, height, path):
  element = ET.SubElement(svg, "image", width=str(width), height=str(height), x=str(x), y=str(y))
  element.set("xlink:href", path)

def paint_civilization_logo(svg, x_center, y_center, civ):
  im_path = "../img/civilization_logo/{0}.png".format(civ.lower())
  im_path = im_path[3:]
  width = 112
  height = 70
  element = ET.SubElement(svg, "image", width=str(width), height=str(height), x=str(x_center-width/2), y=str(y_center-height/2), opacity="0.3")
  element.set("xlink:href", im_path)

def paint_set_logo(svg, x, y, width, height, set_name):
  element = ET.SubElement(svg, "image", width=str(width), height=str(height), x=str(x), y=str(y))
  path = "img/set/{}.png".format(set_name)
  element.set("xlink:href", path)