import base64
from pathlib import Path

import cv2
import numpy as np
from colorthief import ColorThief
from PIL import Image, ImageDraw


def crop_img_to_round(img):
    img = img.resize((150, 150))
    h, w = img.size
    # creating luminous image
    lum_img = Image.new('L', [h, w], 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0, 0), (h, w)], 0, 360, fill=255)
    img_arr = np.array(img)
    lum_img_arr = np.array(lum_img)
    final_img_arr = np.dstack((img_arr, lum_img_arr))
    return final_img_arr


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


def create_color_image(img_path: str, img_output: str):
    if img_path is None:
        img_path = "img/user.png"
        img = Image.open(img_path)
        img = img.resize((150, 150))
        img.save(img_output)
        color_thief = ColorThief(img_path)
        dominant_color = color_thief.get_color(quality=1)
        return dominant_color
    color_thief = ColorThief(img_path)
    dominant_color = color_thief.get_color(quality=1)
    img = Image.open(img_path)
    img = crop_img_to_round(img)
    cv2.imwrite(img_output, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return dominant_color
