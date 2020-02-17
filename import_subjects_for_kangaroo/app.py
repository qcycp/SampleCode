import base64
import json
import os
import requests
import traceback
from io import BytesIO
from PIL import Image

HOST = "192.168.56.3:8857"
username = "admin"
password = "123456"
import_folder = 'LH'

class Auth(object):
    token = "unknown"

    @classmethod
    def checkAuth(cls):
        code = 200
        res = {}

        if cls.token == "unknown":
            url = "http://" + HOST + "/api/auth/login"
            payload = {
                "username": username,
                "password": password
            }
            res = requests.post(url, data=payload)
            if res.status_code == 200:
                res_json = res.json()
                if res_json['code'] == 0:
                    cls.token = "Bearer " + res_json['data']['token']
                else:
                    cls.token = "unknown"
            else:
                cls.token = "unknown"

def image_to_base64(image_path):
    img = Image.open(image_path)
    output_buffer = BytesIO()
    if img.format == 'PNG':
        img.save(output_buffer, format='PNG')
    else:
        img.save(output_buffer, format='JPEG')
    byte_data = output_buffer.getvalue()
    base64_str = base64.b64encode(byte_data)
    return base64_str

def upload_photo(imgpath):
    Auth.checkAuth()

    url = "http://" + HOST + "/api/subject/photo"
    headers = {'Authorization': Auth.token}
    files = {'photo': open(imgpath, 'rb')}

    try:
        res = requests.post(url, headers=headers, files=files, timeout=5)
        res_json = json.loads(res.text)
        if res_json['code'] == 0:
            photo_id = res_json['data']['id']
            return photo_id
    except:
        print(traceback.format_exc())

    return None

def subject_create(index_json):
    Auth.checkAuth()

    with open(index_json, 'r') as fp:
        subjects = json.load(fp)

    url = "http://" + HOST + "/api/subject"
    headers = {'Authorization': Auth.token}

    for i, subject in enumerate(subjects):
        if subject['avatar']:
            avatar_img = image_to_base64(os.path.join(import_folder, subject['avatar']))
        else:
            avatar_img = ''
        photo_ids = list()
        for photo in subject['photos']:
            photo_ids.append(upload_photo(os.path.join(import_folder, photo)))

        payload = {
            'subject_type': subject['subject_type'],
            'name': subject['name'],
            'job_number': subject['job_number'],
            'avatar': avatar_img.decode('utf-8'),
            'photo_ids': photo_ids
        }

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=2)
            res_json = json.loads(res.text)
            if res_json['code'] == 0:
                job_number = res_json['data']['job_number']
            print("%s: subject %s create done" % (i+1, job_number))
        except:
            print(traceback.format_exc())

if __name__ == '__main__':
    subject_create(os.path.join(import_folder, 'index.json'))
