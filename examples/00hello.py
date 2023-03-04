import skit

# create a 2-card deck
deck = skit.Deck(2)

# set background color for all cards
deck.background('white')

# create a title area and set a unique title for both cards
deck.layout(name='title', rect=skit.Rect(x=0, y=0, width=100, height=16))
deck.texts(['Hello', 'World'], layout='title')

# create a copyright area and set a unique title for both cards
deck.layout(name='copyright', rect=skit.Rect(x=0, y=100, width=100, height=16))
typewriter = skit.load_font('AmericanTypewriter', 12)
deck.text('(C) 2023', layout='copyright', font=typewriter)

# make the first card have an additional graphic
deck.layout(name='art', rect=skit.Rect(x=0, y=20, width=100, height=100))
deck[0].png('graphic.png', layout='art')

# create individual PNGs for cards
deck.render_png('hello_{index}.png')
