from exif import Image

p = r"C:\Users\nadav.k\Documents\DS\py_proj_br_ilan\jpgs\20201015_232635.jpg"

def jpg_open(jpg):
    '''
     Opens a JPEG file and returns its EXIF metadata.

    :param jpg_path: path to jpg file
    :return: An Image object containing the EXIF metadata of the JPEG file
    '''
    if type(jpg) == str and (p.lower().endswith(".jpg") or p.lower().endswith(".jpeg")):
        with open(jpg, 'rb') as img_file:
            img = Image(img_file)

        return img
    else:
        raise Exception("Invalid path was given, pass a valid path to a JPEG file")

def dms_to_decimal_degrees(latitude_d, latitude_m, latitude_s, longitude_d, longitude_m, longitude_s, lat_ref, long_ref):
    '''
    converts Deg,min,sec coordinates to decimal degrees.

    :param latitude_d: latitude degrees
    :param latitude_m: latitude minutes
    :param latitude_s: latitude seconds
    :param longitude_d: longitude degrees
    :param longitude_m: longitude minutes
    :param longitude_s: longitude seconds
    :param lat_ref: reference for East or West hemisphere
    :param long_ref: reference for South or North hemisphere
    :return:
    '''

    latitude_dd = (latitude_d + latitude_m/60 + latitude_s/3600) * (-1 if lat_ref == 'S' else 1)
    longitude_dd = (longitude_d + longitude_m/60 + longitude_s/3600) * (-1 if long_ref == 'W' else 1)

    return latitude_dd, longitude_dd



def get_jpg_coor(jpg_path):
    '''
    Executes jpg_open() and dms_to_decimal_degrees() to return latitude and longitude coordinates from JPEG file.

    :param jpg_path: path to jpg file
    :return: latitude and longitude coordinates in decimal degrees
    '''
    img = jpg_open(jpg_path)
    if img.has_exif and img.gps_latitude and img.gps_longitude:
        lat = img.gps_latitude
        lat_ref = img.gps_latitude_ref
        lon = img.gps_longitude
        lon_ref = img.gps_longitude_ref

        lat, long = dms_to_decimal_degrees(lat[0], lat[1], lat[2], lon[0], lon[1], lon[2], lat_ref, lon_ref)
        return lat, long

    else:
        raise Exception("No GPS data found in image metadata.")


