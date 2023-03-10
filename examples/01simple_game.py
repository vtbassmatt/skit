"""
This sample shows off a toy game based on chess. Each piece has
a unique card, and both colors are represented. The cards use a
relatively complex layout, so that's loaded from a JSON file.
And because each card is unique, stats are loaded from a CSV file.
An empty box is drawn where art would go.
"""
import csv
import json
import os.path
import skit

BASE_DIR = os.path.dirname(__file__)

# load some fonts
typewriter10 = skit.load_font('AmericanTypewriter', 10*2)
typewriter16 = skit.load_font('AmericanTypewriter', 16*2)

# load the layout
with open(BASE_DIR + '/assets/01layout.json') as json_in:
    layouts = json.load(json_in, object_hook=skit.as_layoutdef)

# load pieces
pieces = []
with open(BASE_DIR + '/assets/01pieces.csv') as csv_in:
    pieces_csv = csv.DictReader(csv_in, dialect='unix')
    for row in pieces_csv:
        pieces.append(row)

# expand to the full list of pieces
total_pieces = []
for p in pieces:
    for _ in range(int(p['Number'])):
        total_pieces.append((p['Name'], p['Text']))

piece_count = len(total_pieces)

deck_w = skit.Deck(piece_count, 300, 300)
deck_w.background('#cccccc')

deck_w.layouts_map(layouts)
deck_w.texts(['White ' + p[0] for p in total_pieces], 'name', typewriter16)
deck_w.texts([p[1] for p in total_pieces], 'text', typewriter10)
deck_w.rectangle('border', '#444444', 2)
deck_w.rectangle('art', '#888888')

deck_b = skit.Deck(piece_count, 300, 300)
deck_b.background('#444444')

deck_b.layouts_map(layouts)
deck_b.texts(['Black ' + p[0] for p in total_pieces], 'name', typewriter16, 'white')
deck_b.texts([p[1] for p in total_pieces], 'text', typewriter10, 'white')
deck_b.rectangle('border', '#cccccc', 2)
deck_b.rectangle('art', '#888888')

# create individual PNGs for cards
deck = deck_w + deck_b
deck.render_png('simple_{index}.png')
