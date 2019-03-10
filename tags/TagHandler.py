import copy
import os

from images.utils import is_external_image
from settings import TAG_FEATURE_IMAGE_KEY


class TagHandler(object):
    def __init__(self, ghost_client):
        self._ghost_client = ghost_client

    def _get_tag(self, tag_name):
        tags = self._ghost_client.tags.list(fiels="name", limit="all")
        while tags:
            for tag in tags:
                if tag["name"] == tag_name:
                    return tag
                try:
                    tags = tags.next_page()
                except AttributeError:
                    tags = False
        return None

    def get_or_create_tag(self, tag_name):
        ghost_tag = self._get_tag(tag_name=tag_name)
        if not ghost_tag:
            ghost_tag = self._ghost_client.tags.create(name=tag_name)
        return ghost_tag

    def create_or_update_tag(self, base_dir, image_handler, tag_dict):
        processed_tag_dict = copy.deepcopy(tag_dict)
        tag_name = tag_dict["name"]
        ghost_tag = self.get_or_create_tag(tag_name=tag_name)
        if TAG_FEATURE_IMAGE_KEY in tag_dict:
            path = tag_dict[TAG_FEATURE_IMAGE_KEY]
            if is_external_image(path=path):
                uploaded_path = path
            else:
                absolute_path = os.path.join(base_dir, path)
                uploaded_path = image_handler.upload_image(
                    path=absolute_path)
            processed_tag_dict[TAG_FEATURE_IMAGE_KEY] = uploaded_path
        self._ghost_client.tags.update(ghost_tag.id, **tag_dict)
