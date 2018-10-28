from PIL import Image, ImageDraw, ImageFont
import numpy as np

flairs = [

    # - General Flairs

    {   # Dark theme
        "top_section": (36, 39, 43),
        "bottom_section": (43, 47, 51)
    },
    {   # Light theme
        "top_section": (234, 234, 234),
        "bottom_section": (249, 249, 249)
    },
    {   # Basic Moderator
        "top_section": (53, 159, 87),
        "bottom_section": (69, 193, 109),
        "text": "Moderator"
    },
    {   # Former Mod
        "top_section": (196, 50, 50),
        "bottom_section": (242, 61, 61),
        "text": "Former Mod"
    },
    {   # AMA HOST
        "top_section": (43, 117, 170),
        "bottom_section": (57, 145, 206),
        "text": "AMA Host"
    },
    
    # - Custom Mods

    {   # Abra
        "top_section": (229, 166, 46),
        "bottom_section": (245, 255, 66),
        "text": "Former Mod" 
    },
    {   # Tech
        "top_section": (204, 231, 56),
        "bottom_section": (245, 255, 66),
        "text": "Moderator" 
    },
    {   # Haruka
        "top_section": (136, 67, 213),
        "bottom_section": (178, 74, 255),
        "text": "Moderator" 
    },
    {   # Samz
        "top_section": (45, 170, 152),
        "bottom_section": (156, 101, 234),
        "top_squares": (57, 206, 184),
        "text": "Moderator" 
    },
    #{   # NGB -- DEPRECATED
    #    "top_section": (255, 126, 26),
    #    "bottom_section": (255, 179, 42),
    #    "shape_border": (0, 215, 255),
    #    "text": "Moderator" 
    #},
    {   # Baru
        "top_section": (211, 79, 21),
        "bottom_section": (255, 113, 30),
        "top_squares": (35, 31, 32),
        "text": "Moderator" 
    },
    {   # DLH
        "top_section": (17, 17, 17),
        "bottom_section": (226, 213, 92),
        "top_squares": (81, 81, 81),
        "text": "Moderator" 
    },
    {   # Mudkip
        "top_section": (255, 126, 26),
        "bottom_section": (255, 179, 42),
        "shape_border": (0, 215, 255),
        "text": "Moderator" 
    },
    {   # TexasAndroid
        "top_section": (0, 0, 0),
        "bottom_section": (255, 255, 255),
        "text": "Moderator" 
    },
    {
        # Mockturne
        "top_section": (203, 57, 44),
        "bottom_section": (218, 93, 82),
        "text": "Moderator"
    },

    {
        # Fable
        "top_section": (49, 123, 222),
        "bottom_section": (122, 172, 57),
        "poke_ball": (89, 163, 255),
        "top_squares": (89, 163, 255),
        "text": "Moderator"
    },

    {
        # SnowPhoenix / UrsineKing
        "top_section": (34, 170, 255),
        "bottom_section": (136, 221, 255),
        "text": "Moderator"
    },

    {
        # AnAbsurdlyAngryGoose
        "top_section": (255, 127, 0),
        "bottom_section": (192, 192, 192),
        "poke_ball": (178, 89, 0),
        "top_squares": (178, 89, 0),
        "text": "Moderator"
    },

    {
        # ShinySigma
        "top_section": (151,77,194),
        "bottom_section": (255,113,117),
        "top_squares": (196,117,255),
        "text": "Moderator"
    },

    {
        # Pikaachew
        "top_section": (34, 170, 255),
        "bottom_section": (136, 221, 255),
        "poke_ball": (255,255,255),
        "top_squares": (255, 255, 255),
        "text": "Moderator"
    },

    {
        # Dom
        "top_section": (237, 32, 42),
        "bottom_section": (92, 96, 102),
        "poke_ball": (72, 76, 82),
        "text": "Moderator"
    },

    {   # andyjekal
        "top_section": (196, 50, 50),
        "bottom_section": (242, 61, 61),
        "text": "Moderator"
    },

    {
        # StormSwampert
        "top_section": (0, 152, 205),
        "bottom_section": (0, 174, 235),
        "poke_ball": (242, 150, 3),
        "top_squares": (242, 150, 3),
        "shape_border": (70, 44, 44),
        "text": "Moderator"
    },

    # - OTHER FLAIRS
    {   # Nintendo
        "top_section": (196, 50, 50),
        "bottom_section": (242, 61, 61),
        "top_squares": (255, 255, 255),
        "text": "Nintendo"
    },
    {   # TPCI
        "top_section": (43, 117, 170),
        "bottom_section": (57, 145, 206),
        "text": "TPCI"
    },
    {   # Game Freak
        "top_section": (229, 166, 46),
        "bottom_section": (245, 255, 66),
        "text": "Game Freak" 
    },

]

ss = Image.new('RGBA', (1120, 144 * len(flairs)))

for index, flair in enumerate(flairs):
    im = Image.open('mask.png').convert('RGBA')

    # generate array of colours
    data = np.array(im)
    r, g, b, alpha = data.T

    # replaces colours in image
    for colour, replacement in [
        [(255, 0, 0), flair["top_section"]],
        [(0, 255, 255), flair["bottom_section"]],
        [(0, 255, 0), flair.get("shape_border", tuple([x-20 if x > 20 else 0 for x in flair["top_section"] ]))],
        [(255, 255, 0), flair.get("poke_ball", flair["bottom_section"])],
        [(0, 0, 255), flair.get("top_squares", flair["bottom_section"])]
    ]:
        to_replace = (r==colour[0]) & (g==colour[1]) & (b==colour[2])
        data[..., :-1][to_replace.T] = replacement

    im = Image.fromarray(data)


    # add text if needed
    if flair.get("text", None):
        cc = ImageFont.truetype('chocolate_cake.ttf', 50)
        draw = ImageDraw.Draw(im)
        w, h = draw.textsize(flair["text"], font=cc)

        draw.text((925 - w, -5), flair["text"], font=cc, fill=flair.get("top_squares", flair["bottom_section"]))

    # paste image in spritesheet
    ss.paste(im, (0, index * 144))

ss.save("flairBG.png")
