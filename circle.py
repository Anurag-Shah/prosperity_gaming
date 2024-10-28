import json
from PIL import Image, ImageDraw, ImageFont
import random

f = open('config.json')
_config = json.load(f)

_dlist = _config['disasters']
_blacklist = _config['blacklist']

images = [Image.new('RGBA', (7998, 2000)), Image.new('RGBA', (7998, 2000))]
draws = [ImageDraw.Draw(images[0]), ImageDraw.Draw(images[1])]

font = ImageFont.truetype('arial.ttf', 20)

outs = []

for i in range(2):
    image = images[i]
    draw = draws[i]
    col = ([(255, 0, 0, 120), (0, 255, 0, 120)])[i]
    for key in _config['circles']:
        diff = list(set(_dlist).difference(set(_blacklist[key])))
        item = _config['circles'][key]
        if item['opt'] == True:
            if bool(random.getrandbits(1)):
                item = item['opt_1']
            else:
                item = item['opt_2']
            c = 1
        else:
            c = random.randint(int(item['cmin']), int(item['cmax']))
        
        for q in range(c):
            x = random.randint(int(item['xmin']), int(item['xmax']))
            y = random.randint(int(item['ymin']), int(item['ymax']))
            r = random.randint(int(item['rmin']), int(item['rmax'])) // 2

            dis = random.choice(diff).replace(" ", "\n")

            draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=col)
            if i == 0: outs.append(((x-(r*0.66),y-(r*0.66)), dis))
            draw.ellipse([(x-r+3999, y-r), (x+r+3999, y+r)], fill=col)
            if i == 0: outs.append(((x+3999-(r*0.66),y-(r*0.66)), dis))
            draw.ellipse([(x-r-3999, y-r), (x+r-3999, y+r)], fill=col)
            if i == 0: outs.append(((x-3999-(r*0.66),y-(r*0.66)), dis))

for i in outs:
    draws[0].text(i[0], i[1], fill='white', font=font)

out_img = Image.alpha_composite(images[0], images[1])
out_img.save('circles.png')