import os.path
import skit

BASE_DIR = os.path.dirname(__file__)

# load some fonts
typewriter10 = skit.load_font('AmericanTypewriter', 10*3)
typewriter16 = skit.load_font('AmericanTypewriter', 16*3)

# create a 2-card deck
deck = skit.Deck(2)

# set background color for all cards
deck.background('white')

# create a title area and set a unique title for both cards
deck.layout(name='title', layoutdef=skit.LayoutDef(x=10, y=0, width=730, height=50))
deck.texts(['Hello', 'World'], layouts='title', colors=skit.Color('red'), fonts=typewriter16)

# create a copyright area and set a unique title for both cards
deck.layout(name='copyright', layoutdef=skit.LayoutDef(x=10, y=1000, width=730, height=50))
deck.text('(C) 2023', layout='copyright', font=typewriter10)

# draw an art box
deck.layout(name='art', layoutdef=skit.LayoutDef(x=30, y=90, width=690, height=500, h_align=skit.Alignment.MIDDLE, v_align=skit.Alignment.MIDDLE))
deck.rectangle(layout='art')

# make the first card have an additional graphic
deck[0].image(BASE_DIR + '/assets/apple.png', layout='art')

# create individual PNGs for cards
deck.render_png('hello_{index}.png')
