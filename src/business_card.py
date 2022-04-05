"""Module to create a business card."""

import os
import subprocess
import sys
from typing import Dict, Tuple

from dotenv import load_dotenv
from PIL import Image, ImageFont, ImageDraw
import qrcode

load_dotenv()


def format_params(params: Dict[str, str]) -> Dict[str, str]:
    """Formats and returns the parameters with default values, etc.

    Args:
        params: A dictionary of parameters.
    Returns:
        The formatted parameters.
    """
    data = {
        "first-name": params.get("first-name", ""),
        "last-name": params.get("last-name", ""),
        "description": params.get("description", ""),
        "telephone": params.get("telephone", ""),
        "email": params.get("email", "@"),
        "website": params.get("website", ""),
        "street": params.get("street", ""),
        "city": params.get("city", ""),
        "state": params.get("state", ""),
        "postcode": params.get("postcode", ""),
        "country": params.get("country", ""),
        "format": params.get("format", "png"),
        "theme": params.get("theme", "light"),
        "width": params.get("width", 850),
        "height": params.get("height", 550),
        "font": params.get("font", "ubuntu/Ubuntu-Regular.ttf"),
    }
    data.update(get_colors_for_theme(data))
    data.update(
        {
            "font-size": round(min(data["width"], data["height"]) / 7.9),
        }
    )
    return data


def get_colors_for_theme(params: Dict[str, str]) -> Dict[str, str]:
    """Returns the colors for a given theme.

    Args:
        theme: The theme to return the colours for.
    Returns:
        A dictionary of colours for the given theme.
    """
    theme = params["theme"]
    if theme == "light":
        color = (0, 0, 0)
        color_1 = (0, 0, 0)
        color_2 = (0, 0, 0)
        background_color = (255, 255, 255)
    elif theme == "dark":
        color = (255, 255, 255)
        color_1 = (255, 255, 255)
        color_2 = (255, 255, 255)
        background_color = (0, 0, 0)
    elif theme == "bitcoin":
        color = (255, 255, 255)
        color_1 = (242, 169, 0)
        color_2 = (78, 78, 78)
        background_color = (0, 0, 0)
    data = {
        "color": color,
        "color-1": color_1,
        "color-2": color_2,
        "background-color": background_color,
    }
    return data


def get_v_card(params: Dict[str, str]) -> str:
    """Creates, writes and returns a vCard from the parameters.

    Args:
        params: The parameters for the vCard.
    Returns:
        The vCard as a string.
    """
    v_card = f"""
        BEGIN:VCARD
        N:{params["last-name"]};{params["first-name"]};
        ORG:{params["description"]};
        URL:{params["website"]};
        ADR:{params["street"]};{params["city"]};{params["state"]};{params["postcode"]};{params["country"]};
        TEL:{params["telephone"]}
        EMAIL:{params["email"]}
        END:VCARD
    """
    v_card = v_card.strip().replace(" ", "")
    with open("data/v-card.vcf", "w") as f:
        f.write(v_card)
    return v_card


def v_card_to_qr(v_card: str, params: Dict[str, str]) -> Image:
    """Converts the vCard to a QR code and returns it as an image.

    Args:
        v_card: The vCard to convert.
        params: The parameters of the business card.
    Returns:
        The vCard as a QR code image.
    """
    qr = qrcode.QRCode(version=1)
    qr.add_data(v_card)
    qr.make(fit=True)
    img = qr.make_image(
        back_color=params["background-color"], fill_color=params["color-1"]
    )
    img.save("data/v-card.png")
    return img


def get_blank(params: Dict[str, str]) -> Image:
    """Returns a blank business card to annotate the front and back.

    Args:
        params: The parameters of the business card.
    Returns:
        The blank business card.
    """
    img = Image.new(
        "RGB", (params["width"], params["height"]), params["background-color"]
    )
    f = params["format"]
    img.save(f"data/blank.{f.lower()}", f"{f.upper()}")
    return img


def get_front(params: Dict[str, str]) -> Image:
    """Returns the front side of the business card.

    Args:
        params: The business card parameters.
    Returns:
        The front of the business card.
    """
    email = params["email"]
    user, domain = email.split("@")
    width = params["width"]
    height = params["height"]
    font = params["font"]
    font_size = params["font-size"]
    color = params["color"]
    color_1 = params["color-1"]
    color_2 = params["color-2"]
    f = params["format"]
    img = get_blank(params)
    draw = ImageDraw.Draw(img)
    img_font = ImageFont.truetype(f"font/{font}", font_size)
    text = email
    w, h = draw.textsize(text, font=img_font)
    pos = [(width - w) / 2, (height - h) / 2]
    text = user
    draw.text(pos, text, color_2, font=img_font)
    pos[0] += draw.textsize(text, font=img_font)[0]
    text = f"@"
    draw.text(pos, text, color_1, font=img_font)
    pos[0] += draw.textsize(text, font=img_font)[0]
    text = f"{domain}"
    draw.text(pos, text, color, font=img_font)
    img.save(f"data/front.{f.lower()}", f"{f.upper()}")
    return img


def get_back(img_v_card: Image, params: Dict[str, str]) -> Image:
    """Creates and returns the back of the business card.

    Args:
        img_v_card: An image of the vCard as a QR code.
        params: The configuration parameters.
    Returns:
        The back of the business card.
    """
    width = params["width"]
    height = params["height"]
    f = params["format"]
    scale = 0.75
    img = get_blank(params)
    w, h = img_v_card.size
    size = (w * scale, h * scale)
    img_v_card.thumbnail(size, Image.ANTIALIAS)
    w, h = img_v_card.size
    img.paste(img_v_card, ((width - w) // 2, (height - h) // 2))
    img.save(f"data/back.{f.lower()}", f"{f.upper()}")
    return img


def get_params_from_env_file() -> Dict[str, str]:
    """Gets and returns and parameters from an environmental file.

    Returns:
        The parameters as a dictionary from an environmental file.
    """
    params = {
        "first-name": os.getenv("FIRST_NAME"),
        "last-name": os.getenv("LAST_NAME"),
        "description": os.getenv("DESCRIPTION"),
        "telephone": os.getenv("TELEPHONE"),
        "email": os.getenv("EMAIL"),
        "website": os.getenv("WEBSITE"),
        "street": os.getenv("STREET"),
        "city": os.getenv("CITY"),
        "state": os.getenv("STATE"),
        "postcode": os.getenv("POSTCODE"),
        "country": os.getenv("COUNTRY"),
        "theme": os.getenv("THEME"),
    }
    params = {k: v for k, v in params.items() if v is not None}
    return params


def main():
    params = get_params_from_env_file()
    params = format_params(params)
    get_front(params)
    v_card = get_v_card(params)
    img_v_card = v_card_to_qr(v_card, params)
    get_back(img_v_card, params)
    process = subprocess.Popen(
        ["open", "data/front.png", "data/back.png"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()


if __name__ == "__main__":
    main()
