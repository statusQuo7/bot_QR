import os
import uuid
import qrcode

dirname = os.path.dirname(__file__)
abs_path = os.path.join(dirname, '../qr_images/')

def create_qr(url):
    img = qrcode.make(url)
    name = str(uuid.uuid4())
    path_to_qr = abs_path+name+'.png'
    img.save(path_to_qr)
    return path_to_qr