import hashlib
import json
import os

from settings import UPLOADED_IMAGES_FILE


class ImageHandler(object):
    def _get_uploaded_images(self):
        try:
            with open(UPLOADED_IMAGES_FILE, "r") as f:
                data = f.read()
                uploaded_images_dict = json.loads(data)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            uploaded_images_dict = {}
        return uploaded_images_dict

    def _add_uploaded_image(self, uploaded_images, md5_sum, uploaded_path):
        uploaded_images[md5_sum] = uploaded_path
        with open(UPLOADED_IMAGES_FILE, "w") as f:
            data = json.dumps(uploaded_images, indent=2, sort_keys=True)
            f.write(data)

    def __init__(self, ghost_client):
        self._ghost_client = ghost_client

    def _get_md5_sum(self, path, block_size=64*128):
        md5 = hashlib.md5()
        with open(path, 'rb') as f:
            while True:
                try:
                    data = f.read(block_size)
                except IOError:
                    return 'IOError while reading {path}'.format(path=path)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()

    def upload_image(self, path):
        uploaded_images = self._get_uploaded_images()
        md5_sum = self._get_md5_sum(path=path)
        filename = os.path.basename(path)
        try:
            uploaded_path = uploaded_images[md5_sum]
            print("Image '{filename}' has already been uploaded to '{uploaded_path}'".format(
                filename=filename, uploaded_path=uploaded_path))
        except KeyError:
            with open(path, 'rb') as image:
                image_data = image.read()
            uploaded_path = self._ghost_client.upload(name=filename,
                                                      data=image_data)
            self._add_uploaded_image(uploaded_images=uploaded_images,
                                     md5_sum=md5_sum,
                                     uploaded_path=uploaded_path)
            print("Uploaded {filename} to {uploaded_path}".format(
                filename=filename, uploaded_path=uploaded_path))
        return uploaded_path
