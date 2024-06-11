from exif import Image

def jpg_open(jpg):
    if isinstance(jpg, str) and (jpg.lower().endswith(".jpg") or jpg.lower().endswith(".jpeg")):
        with open(jpg, 'rb') as img_file:
            img = Image(img_file)
        return img
    else:
        raise Exception("Invalid path was given, pass a valid path to a JPEG file")

def dms_to_decimal_degrees(latitude_d, latitude_m, latitude_s, longitude_d, longitude_m, longitude_s, lat_ref, long_ref):
    latitude_dd = (latitude_d + latitude_m/60 + latitude_s/3600) * (-1 if lat_ref == 'S' else 1)
    longitude_dd = (longitude_d + longitude_m/60 + longitude_s/3600) * (-1 if long_ref == 'W' else 1)
    return latitude_dd, longitude_dd

def get_jpg_coor(jpg_path):
    img = jpg_open(jpg_path)
    if img.has_exif and img.gps_latitude and img.gps_longitude:
        lat = img.gps_latitude
        lat_ref = img.gps_latitude_ref
        lon = img.gps_longitude
        lon_ref = img.gps_longitude_ref
        return dms_to_decimal_degrees(lat[0], lat[1], lat[2], lon[0], lon[1], lon[2], lat_ref, lon_ref)
    else:
        raise Exception("No GPS data found in image metadata.")
