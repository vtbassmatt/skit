"""
A trading-card game using TOML for layout and data.
"""
import os.path
import tomllib
import skit


BASE_DIR = os.path.dirname(__file__)

# load the layout
with open(BASE_DIR + '/assets/02data.toml', 'rb') as toml_in:
    data_in = tomllib.load(toml_in)

layouts = { k: skit.as_layoutdef(v) for k, v in data_in['layout'].items()}
width, height = data_in['design']['width'], data_in['design']['height']
cards = data_in['cards']

# load some fonts
small_text = skit.load_font('Helvetica', 10*3)
large_text = skit.load_font('Helvetica', 16*3)

# create the deck and a background
deck = skit.Deck(len(cards), width, height)
deck.background('#eeeeee')
deck.layouts_map(layouts)

# draw a border
deck.rectangle('border', 'black', 10)
deck.rectangle('border', 'white', 8)
deck.rectangle('border', 'black', 6)

# fill in the data
deck.texts([c['name'] for c in cards], layouts='name', colors=[skit.Color(c['color']) for c in cards], fonts=large_text)
deck.rectangle('art', 'gray')
deck.images([BASE_DIR + '/assets/' + c['image'] for c in cards], layouts='art')
deck.texts([c['typeline'] for c in cards], layouts='typeline', fonts=small_text)
deck.filled_rectangle('textbox', '#dddddd')
deck.texts([c['text'] for c in cards], layouts='text', fonts=small_text)

# if there's a 'stats' key in the data, draw the stats box
def draw_statsbox(card, data):
    card.filled_rectangle('stats', '#cccccc')
    card.text(data['stats'], layout='stats', font=small_text)

deck.for_each_if(
    cards,
    lambda c: 'stats' in c,
    draw_statsbox,
)

# the above code is equivalent to:
#   for index, c in enumerate(cards):
#       if 'stats' in c:
#           deck[index].filled_rectangle('stats', '#cccccc')
#           deck[index].text(c['stats'], layout='stats', font=small_text)


# create individual PNGs for cards
deck.render_png('tcg_{index}.png')
# also create a PDF
deck.render_pdf('tcg.pdf', resolution=300)
