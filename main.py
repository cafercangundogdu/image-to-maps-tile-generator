import shutil
import os
import PIL
from PIL import Image
from pathlib import Path

PIL.Image.MAX_IMAGE_PIXELS = 100000000
images_dir = "images"
maps_path = "maps"
map_images = [Image.open(p) for p in Path(maps_path).rglob('*.jpg')]
tile_size = 256
max_zoom = 6

"""
zoom_0 1    256x256
zoom_1 4    512x512  
zoom_2 16   1024x1024
zoom_3 64   2048x2048
zoom_4 256  4096x4096
zoom_5 1024 8192x8192
"""


def copy_null_image():
    shutil.copy("null.jpg", os.path.join(images_dir, "null.jpg"))


def create_if_not_exits(path):
    if not os.path.exists(path):
        os.makedirs(path)


def truncate_images_dir():
    if os.path.exists(images_dir):
        shutil.rmtree(images_dir)
    os.mkdir(images_dir)


def generate_images(zoom):
    image_count = (2**zoom)
    image_size = tile_size * image_count

    print("image_count:", image_count**2)
    print("image_size:", f'{image_size}x{image_size}')

    generad_image_count = 0
    for i in range(0, len(map_images)):
        image = map_images[i]
        pimage = image.resize((image_size, image_size))

        for x in range(0, image_count):
            for y in range(0, image_count):
                left = x * tile_size
                right = left + tile_size
                top = y * tile_size
                bottom = top + tile_size

                image_directory = os.path.join(images_dir, str(i), str(zoom))
                create_if_not_exits(image_directory)
                cropped = pimage.crop((left, top, right, bottom))
                cropped.save(f'{image_directory}/{x}_{y}.jpg')

                generad_image_count += 1

    return generad_image_count


truncate_images_dir()
copy_null_image()
total_generated_image_count = 0
for z in range(0, max_zoom+1):
    total_generated_image_count += generate_images(z)

print("Total Generated Images: ", total_generated_image_count)