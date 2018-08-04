# Script to remove EXIF metadata from JPEG images
# And try to optimize size
#
# Deps: pip install Pillow
#

from PIL import Image
from PIL.ExifTags import TAGS
import os, sys, glob

os.chdir("../photos")
files = glob.glob('./**/*.JPG', recursive=True)
for imgfile in files:
    print("Loading {0}".format(imgfile))

    image = Image.open(imgfile)
    
    if image._getexif() is not None:
        for (k,v) in image._getexif().items():
            print("\t{0} = {1}".format(TAGS.get(k), v))
        print("EXIF data will be removed")

    data = list(image.getdata())
    image_stripped = Image.new(image.mode, image.size)
    image_stripped.putdata(data)
    image_stripped.save(imgfile, optimize=True)
    print("Stripped image saved: {0}".format(imgfile))

    width, height = image_stripped.size
    ratio = width/height

    image_stripped_small = image_stripped.resize((512,int(512/ratio)),Image.ANTIALIAS)
    image_stripped_small.save(os.path.splitext(imgfile)[0] + "_TN.JPG",optimize=True)
    print("Thumbnail image saved: {0}".format(os.path.splitext(imgfile)[0] + "_TN.JPG"))
    #else:
    #    print("No EXIF metadata found, skipping")
