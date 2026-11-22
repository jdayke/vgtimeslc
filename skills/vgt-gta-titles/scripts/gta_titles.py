"""Render a transparent GTA-style hook or outro. Requires Pillow, NumPy, FFmpeg."""
import argparse
import math
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONTS = Path("J:/Claude/VGTimes and LibertyCity/Tools/fonts")
FPS = 60
# Center, local canvas height, vertical offset, line widths, heights, centers.
LAYOUTS = {
    "date": (370, 600, 175, (630, 510, 610, 620), (61, 85, 146, 61), (104, 203, 341, 491)),
    "details": (540, 760, 400, (920, 875, 912, 910), (69, 85, 111, 69), (155, 258, 402, 563)),
}


def lettering(text, font_path, max_width, height, brush=False):
    font = ImageFont.truetype(str(font_path), 210)
    box = font.getbbox(text)
    mask = Image.new("L", (box[2]-box[0]+8, box[3]-box[1]+8))
    ImageDraw.Draw(mask).text((4-box[0], 4-box[1]), text, fill=255, font=font)
    mask = mask.crop(mask.getbbox())
    ratio = min(height / mask.height, max_width / mask.width)
    mask = mask.resize(tuple(max(1, round(n*ratio)) for n in mask.size), Image.Resampling.LANCZOS)
    return mask.rotate(6, Image.Resampling.BICUBIC, expand=True) if brush else mask


def ink(mask, color):
    layer = Image.new("RGBA", mask.size, color)
    layer.putalpha(mask)
    return layer


def make_line(mask, hero):
    pad = 48
    face = Image.new("L", (mask.width+2*pad, mask.height+2*pad))
    face.paste(mask, (pad, pad))
    if not hero:
        shadow = Image.new("L", face.size)
        shadow.paste(mask, (pad+3, pad+8))
        layer = ink(shadow.filter(ImageFilter.GaussianBlur(8)), (30, 12, 22))
        layer.alpha_composite(ink(face, "white"))
        return layer, None
    rim = face.filter(ImageFilter.MaxFilter(5))
    layer = ink(rim.filter(ImageFilter.GaussianBlur(16)), (250, 42, 163))
    depth = ink(rim, (54, 6, 78))
    for offset in range(13, 0, -1):
        layer.alpha_composite(depth, (offset, offset))
    layer.alpha_composite(ink(rim, "white"))
    y,x = np.indices((face.height,face.width), dtype=np.float32)
    t = .67*(y-pad)/mask.height + .33*(x-pad)/mask.width
    rgb = np.stack([np.interp(t,[0,.48,1],values) for values in
                    [(242,249,145),(61,141,59),(139,57,163)]], axis=-1)
    fill = Image.fromarray(rgb.astype(np.uint8))
    fill.putalpha(face)
    layer.alpha_composite(fill)
    return layer, (x+.32*y, np.asarray(face))


def ease(x):
    return min(1,max(0,x))


def render(args):
    cx,h,top,widths,heights,centers = LAYOUTS[args.layout]
    lines = []
    for i, phrase in enumerate(args.lines):
        font = "Rhythmic_RUS.otf" if i == 1 else "TT Commons Pro Trial Condensed Black.ttf"
        mask = lettering(phrase.strip().upper(), args.fonts/font, widths[i], heights[i], i==1)
        lines.append(make_line(mask, i==2))
    total = round(args.duration * FPS)
    output = args.output.resolve()
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as tmp:
        target = Path(tmp)/"titles.mov"
        cmd = ["ffmpeg","-v","error","-f","rawvideo","-pix_fmt","rgba","-s",f"1080x{h}",
               "-r",str(FPS),"-i","-","-vf",f"pad=1080:1920:0:{top}:color=black@0,format=rgba",
               "-c:v","png","-threads","4",str(target)]
        proc = subprocess.Popen(cmd,stdin=subprocess.PIPE)
        try:
            for frame in range(total):
                phase = frame/total
                canvas = Image.new("RGBA",(1080,h))
                for i,(layer,shine) in enumerate(lines):
                    step = ease((phase-(0,.065,.14,.25)[i])/.12)
                    opacity = step * ease((.91-phase)/.09)
                    if opacity <= 0:
                        continue
                    current = layer
                    if shine and .40 <= phase <= .70:
                        axis,alpha = shine
                        beam = ((phase-.40)/.30)*(axis.max()+160)-80
                        stripe = np.maximum(0,1-abs(axis-beam)/52)**2
                        current = layer.copy()
                        current.alpha_composite(ink(Image.fromarray((alpha*stripe*.9).astype(np.uint8)), "white"))
                    if i==2 and step<1:
                        zoom = .84 + .16*step + .09*math.sin(math.pi*step)
                        current = current.resize(tuple(round(n*zoom) for n in current.size),Image.Resampling.BICUBIC)
                    if opacity<1:
                        current = current.copy()
                        current.putalpha(current.getchannel("A").point(lambda p: round(p*opacity)))
                    canvas.alpha_composite(current,(round(cx-current.width/2),round(centers[i]-current.height/2+25*(1-step)**2)))
                proc.stdin.write(canvas.tobytes())
            proc.stdin.close()
            if proc.wait():
                raise RuntimeError("FFmpeg render failed")
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
        os.replace(target,output)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lines",nargs=4,metavar="LINE")
    parser.add_argument("--layout",choices=LAYOUTS,default="details")
    parser.add_argument("--duration",type=float,default=1.9)
    parser.add_argument("--fonts",type=Path,default=FONTS)
    parser.add_argument("--output",type=Path,required=True)
    args = parser.parse_args()
    if not math.isfinite(args.duration) or args.duration < .5 or any(not s.strip() for s in args.lines):
        parser.error("Supply four nonempty lines and a duration of at least 0.5 seconds")
    render(args)
