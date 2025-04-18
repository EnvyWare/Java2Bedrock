from PIL import Image
from font_sprite import sprite
from io import BytesIO
import glob, os, json

lines = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "a", "b", "c", "d", "e", "f"]
try:
    with open("pack/assets/minecraft/font/default.json", "r") as f:
        data = json.load(f)
except Exception as e:
    print("[FONT ERROR]")
    print(e)
symbols = []
paths = []
heights = []
ascents = []
for d in data['providers']:
    try:
        for char in d['chars']:
            symbols.append(char)
            paths.append(d['file'])
            heights.append(d['height'])
            ascents.append(d['ascent'])
    except:
        continue

def createfolder(glyph):
    os.makedirs(f"images/{glyph}", exist_ok = True)
    os.makedirs(f"export/{glyph}", exist_ok = True)
    os.makedirs(f"font/", exist_ok = True)
    
def create_empty(glyph, blankimg):
    for line in lines:
        for linee in lines:
            if linee != lines:
                name = f"{line}{linee}"
                if os.path.isfile(f"images/{glyph}/0x{glyph}{name}.png"):
                    continue
                else:
                    imagesus = Image.open(blankimg)
                    image = imagesus.copy()
                    image.save(f"images/{glyph}/0x{glyph}{name}.png", "PNG")
    for line in lines:
        name = f"{line}{line}"
        if os.path.isfile(f"images/{glyph}/0x{glyph}{name}.png"):
            continue
        else:
            imagesus = Image.open(blankimg)
            image = imagesus.copy()
            image.save(f"images/{glyph}/0x{glyph}{name}.png", "PNG")

def imagetoexport(glyph, blankimg):
    filelist = [file for file in os.listdir(f'images/{glyph}') if file.endswith('.png')]
    for img in filelist:
        image = Image.open(blankimg)
        logo = Image.open(f'images/{glyph}/{img}')
        image_copy = image.copy()
        w, h = image.size
        wl, hl = logo.size
        for height, symboll in zip(heights, symbols):
            symbolbe = ''.join(symboll)
            symbolbehex = (hex(ord(symbolbe)))
            if len(symbolbehex) == 6:
                symbol = symbolbehex[4:]
            elif len(symbolbehex) == 5:
                symbolbehex = symbolbehex[:2] + "0" + symbolbehex[2:]
                symbol = symbolbehex[4:]
            name = f"0x{glyph}{symbol}"
            imgname = f"0x{glyph}{img}"
            if name == imgname:
                if height >= 1 and height < w and height < h:
                    size = (height, height)
                    logo.thumbnail(size,Image.ANTIALIAS)                 
        if wl > (w/2) and hl > (h/2):
            position = (0, 0)
            image_copy.paste(logo, position)
            image_copy.save(f"export/{glyph}/{img}")
        else:
            position = (0, (h//2) - (hl//2))
            image_copy.paste(logo, position)
            image_copy.save(f"export/{glyph}/{img}")

            
glyphs = []
for i in symbols:
    if i not in glyphs:
        try:
            symbolbe = ''.join(i)
            sbh = (hex(ord(symbolbe)))
            a = sbh[2:]
            ab = a[:2]
            glyphs.append(ab.upper())
        except:
            print(f"Symbol Error: {symbolbe}")
            symbols.remove(i)
            continue
glyphs = list(dict.fromkeys(glyphs))
print("[FONT FILE]")
print(glyphs)

listglyphdone = []
def converterpack(glyph):
    createfolder(glyph)
    if len(symbols) == len(paths):
        maxsw, maxsh = 0, 0
        for symboll, path in zip(symbols, paths):
            symbolbe = ''.join(symboll)
            symbolbehex = (hex(ord(symbolbe)))
            if glyph in listglyphdone:
                return False
            if len(symbolbehex) == 6:
                symbol = symbolbehex[4:]
                symbolac = symbolbehex[2:]
                symbolcheck = symbolac[:2]
            elif len(symbolbehex) == 5:
                symbolbehex = symbolbehex[:2] + "0" + symbolbehex[2:]
                symbol = symbolbehex[4:]
                symbolac = symbolbehex[2:]
                symbolcheck = symbolac[:2]
                glyphs.append(symbolcheck.upper())
            if (symbolcheck.upper()) == (glyph.upper()):
                if ":" in path:
                    try:
                        namespace = path.split(":")[0]
                        pathnew = path.split(":")[1]
                        imagefont = Image.open(f"pack/assets/{namespace}/textures/{pathnew}")
                        image = imagefont.copy()
                        image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                    except Exception as e:
                        print(e)
                        continue
                else:
                    try:
                        imagefont = Image.open(f"pack/assets/minecraft/textures/{path}")
                        image = imagefont.copy()
                        image.save(f"images/{glyph}/0x{glyph}{symbol}.png", "PNG")
                    except Exception as e: 
                        print(e)
                        continue
            else:
                continue
        else:                
            files = glob.glob(f"images/{glyph}/*.png")
            for file in files:
                image = Image.open(file)
                sw, sh = image.size
                maxsw, maxsh = (max(maxsw, sw), max(maxsh, sh))
            if maxsw == maxsh:
                size = (int(maxsw + 1), int(maxsw + 1))
            elif maxsw > maxsh:
                size = (int(maxsw + 1), int(maxsw + 1))
            elif maxsh > maxsw:
                size = (int(maxsh + 1), int(maxsh + 1))
            if size == (0, 0):
                pass
            else:
                glyphsize = size * 16
                img = Image.open("blank256.png")
                imgre = img.resize(size)
                imgre.save("blankimg.png")
                blankimg = "blankimg.png"
                create_empty(glyph, blankimg) 
                imagetoexport(glyph, blankimg)
                sprite(glyph, glyphsize, size)
                listglyphdone.append(glyph)
            
for glyph in glyphs:
    converterpack(glyph)
