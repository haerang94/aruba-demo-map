from PIL import Image
base = Image.new("RGBA", (64,64), (0,0,0,0))
base.paste(Image.open("web/assets/icons/sleep.png").resize((32,32)), (0,0))
base.paste(Image.open("web/assets/icons/meal.png").resize((32,32)), (32,0))
base.paste(Image.open("web/assets/icons/toilet.png").resize((32,32)), (0,32))
base.paste(Image.open("web/assets/icons/out.png").resize((32,32)), (32,32))
base.save("web/assets/icons/icons_2x2.png")