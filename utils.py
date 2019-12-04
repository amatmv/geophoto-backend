from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif(image):
    if filename.endswith('.jpg'):
        exif = Image.open(image)._getexif()
    else:
        print "asd"
        exif = Image.frombytes('RGBA', (128,128), image_data, 'raw')._getexif()

    if exif is not None:
        for key, value in exif.items():
            name = TAGS.get(key, key)
            exif[name] = exif.pop(key)

        if 'GPSInfo' in exif:
            for key in exif['GPSInfo'].keys():
                name = GPSTAGS.get(key,key)
                exif['GPSInfo'][name] = exif['GPSInfo'].pop(key)

    return exif

def get_coordinates(info):
    for key in ['Latitude', 'Longitude']:
        if 'GPS'+key in info and 'GPS'+key+'Ref' in info:
            e = info['GPS'+key]
            ref = info['GPS'+key+'Ref']
            info[key] = ( str(e[0][0]/e[0][1]) + '°' +
                          str(e[1][0]/e[1][1]) + '′' +
                          str(e[2][0]/e[2][1]) + '″ ' +
                          ref )

    if 'Latitude' in info and 'Longitude' in info:
        return [info['Latitude'], info['Longitude']]

