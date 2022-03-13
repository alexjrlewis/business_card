"""
"""

import qrcode


def make(
    first_name: str = "",
    last_name: str = "",
    description: str = "",
    telephone: str = "",
    email: str = "",
    website: str = "",
    street: str = "",
    city: str = "",
    state: str = "",
    postcode: str = "",
    country: str = "",
):
    vcard = f"""
        BEGIN:VCARD
        N:{last_name};{first_name};
        ORG:{description};
        URL:{website};
        ADR:{street};{city};{state};{postcode};{country};
        TEL:{telephone}
        EMAIL:{email}
        END:VCARD
    """
    vcard = vcard.strip().replace(" ", "")
    return vcard


def to_qr(vcard: str, filename: str = "data/vcard.png"):
    qr = qrcode.QRCode(version=1)
    qr.add_data(vcard)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")    
    img.save(filename)
    return img


def card(email: str):
    from PIL import Image, ImageFont, ImageDraw 
    import png
    width = 1050
    height = 600
    img = []
    for y in range(height):
        row = ()
        for x in range(width):
            row = row + (255, 255, 255)
        img.append(row)
    with open("data/business-card-blank.png", "wb") as f:
        w = png.Writer(width, height, greyscale=False)
        w.write(f, img)

    img = Image.open("data/business-card-blank.png")
    draw = ImageDraw.Draw(img)
    user, domain = email.split("@")
    text = email
    font = ImageFont.truetype("font/ubuntu/Ubuntu-Regular.ttf", 70)
    w, h = draw.textsize(text, font=font)
    draw.text(((width - w) / 2, (height - h) / 2), text, (0, 0, 0), font=font)
    text = user + " " * len(f"@{domain}")
    draw.text(((width - w) / 2, (height - h) / 2), text, (78, 78, 78), font=font)
    img.save("data/business-card-front.png")


def main():
    first_name = "Alex"
    last_name = "Lewis"
    description = ""
    telephone = ""
    email = "hello@alex-lewis.me"
    website = "alex-lewis.me"
    street = ""
    city = "London"
    state = ""
    postcode = "W4"
    country = "UK"
    vcard = make(
        first_name,
        last_name,
        description,
        telephone,
        email,
        website,
        street,
        city,
        state,
        postcode,
        country,
    )
    img = to_qr(vcard)
    card(email)

if __name__ == "__main__":
    main()
