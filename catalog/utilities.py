from PIL import Image, ExifTags

def rotate_image(filepath):

    dev_test = "On"

    if dev_test == "Off":
        try:
            image = Image.open(filepath)
            for orientation in ExifTags.TAGS.keys():
              if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
            image.save(filepath)
            image.close()
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass
    else:
        try:
            image = Image.open(filepath)
            image = image.rotate(180, expand=True)
            image.save(filepath)
            image.close()
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass
