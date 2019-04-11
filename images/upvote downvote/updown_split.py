from PIL import Image

img = Image.open('downup.png')

for i, f in enumerate(['up_a', 'up', 'down_a', 'down']):
    y = img.size[0] * i
    c = img.crop((0, y, img.size[0], y+img.size[0]))
    c.save(f'{f}.png')