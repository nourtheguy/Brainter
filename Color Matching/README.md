# EMOTE - hack112
![EMOTE](emote.jpg?raw=true "EMOTE")

Emote is a therapeutic drawing tool intended to 
help users express their emotions through art.
Usually, people let their drawings represent their
feelings, but where should they start? 

That's where Emote comes in. The user can simply
enter an emotion and then be given three colors
that correspond with the emotion. With the three
colors, the user can draw freely and express 
themselves on the canvas!

We implemented this project using the python module
BeautifulSoup and pandas to find image urls for a 
given set of emotions. For each url, we used 
ColorThief, a python module, to find the dominant 
color in each given image. This section of the code
resulted in a dictionary of emotions with corresponding
colors.

Our app took that dictionary and created a drawing
app using cmu 112 graphics, that selects three colors
for the input emotion and allows the user to draw on
the canvas, switching between colors and changing the
size of the drawing tool as they like.

Modules used: pandas, requests, bs4, csv, colorthief, io

Languages used: Python

To open, run drawing.py
