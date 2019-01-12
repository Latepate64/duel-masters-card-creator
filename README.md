# Duel Masters Card Creator

The purpose of this project is to provide a way to create printings for Duel Masters cards programatically. Code used in this project is mostly written in Python, so it must be installed in order to print cards [(Install from here)] (https://www.python.org/downloads/). The project contains two major files: code/crop\_utility.py and code/svg_painter.py.  


## crop_utility.py:

crop_utility.py is used in cropping artwork from cards. Cards must be provided in jpg-format in 400x560 resolution and the cards should be aligned properly in original images.

Pillow library must be installed in order to crop images. In command line, execute command: pip install Pillow

In command line, execute crop\_utility.py as follows: crop_utility.py [source] [destination] [card_type]

- source: Path containing images to be cropped.
- destination: Destination path for the cropped images. The path must exist before executing the command.
- card\_type: Specifies the type of the cards (Creature, Spell or Cross Gear). The type of the cards affects how the images are cropped. Therefore, there should be separate source paths for each card type.

Example command: crop_utility.py path/to/spell/images '../img/artwork/DM-05 Survivors of the Megapocalypse' Spell


## svg_painter.py:

svg\_painter.py is used in creating SVG files for Duel Masters cards. The artworks cropped with crop\_utility.py should be moved into img/artworks/{set\_name} directory so that svg_painter.py is able to locate them. The project comes with some images already cropped.

[Download (or git clone) DuelMastersCards.json -file.] (https://github.com/Latepate64/duel-masters-json)
The json-file holds data for Duel Masters cards and is utilized in printing of the cards. The path of the file must be specified in configuration.xml (see below).

In "code"-folder, execute file svg\_painter.py to print images for cards. This can be done by either double-clicking the file or by executing command *python svg_painter.py* via command line.

File code\configuration.xml can be modified in order to print desired cards. The purposes of the xml elements are as follows:

- json\_path: The location of the json-file for the Duel Masters cards. The path is relative to the location of the svg_painter.py file.
- producer\_text: The text that is printed on the left side of rarity symbol on each card (eg. ©2004 Wizards of the Coast)
- print\_set: Prints all cards from a Duel Masters set
    - set: Duel Masters set to be printed.
    - placeholder\_cards: In most cases, cards from a set will not fill files entirely as each file can hold 9 cards. In a set of 60 cards there would be space for (9*7)-60 = 3 more cards. With placeholder_cards element, you can specify what cards will be printed on those empty slots.
- print_cards: Prints 9 target cards
    - name: Name of the file to be generated
- card: Element that represents a card
    - set: Duel Masters set of the card
    - id: Collector's number of the card
