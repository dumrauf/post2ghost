import json
import os

from tags.TagHandler import TagHandler
from ghost_config.GhostConfigHandler import PostToGhostGhostClient
from images.ImageHandler import ImageHandler


class TagFileHandler(object):
    def _get_tag_data(self):
        with open(self._path, 'r') as f:
            tag_data = json.load(f)
        return tag_data

    def __init__(self):
        self._ghost_client = PostToGhostGhostClient()
        self._image_handler = ImageHandler(ghost_client=self._ghost_client)

    def create_or_update_tag(self, path):
        self._path = path
        self._absolute_filename = os.path.abspath(path)
        self._base_dir = os.path.dirname(self._absolute_filename)

        tag_data = self._get_tag_data()
        self._tag_handler = TagHandler(ghost_client=self._ghost_client)

        self._tag_handler.create_or_update_tag(
            base_dir=self._base_dir, image_handler=self._image_handler, tag_dict=tag_data)
