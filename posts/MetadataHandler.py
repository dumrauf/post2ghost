import copy
import os

from images.utils import is_external_image
from settings import METADATA_FEATURE_IMAGE_KEY


class MetadataHandler(object):
    def _add_to_processed_metadata_if_not_in_metadata(self, key, value):
        if key not in self._metadata:
            self.processed_metadata[key] = value

    def _handle_feature_image(self):
        path = self._metadata[METADATA_FEATURE_IMAGE_KEY]
        if is_external_image(path=path):
            uploaded_path = path
        else:
            absolute_path = os.path.join(self._base_dir, path)
            uploaded_path = self._image_handler.upload_image(
                path=absolute_path)
        self.processed_metadata[METADATA_FEATURE_IMAGE_KEY] = uploaded_path

    def _handle_search_engines(self):
        self._add_to_processed_metadata_if_not_in_metadata(
            key="meta_title", value=self._metadata["title"])
        self._add_to_processed_metadata_if_not_in_metadata(
            key="meta_description", value=self._metadata["custom_excerpt"])

    def _handle_twitter(self):
        self._add_to_processed_metadata_if_not_in_metadata(
            key="twitter_title", value=self._metadata["title"])
        self._add_to_processed_metadata_if_not_in_metadata(
            key="twitter_description", value=self._metadata["custom_excerpt"])
        self._add_to_processed_metadata_if_not_in_metadata(
            key="twitter_image", value=self.processed_metadata[METADATA_FEATURE_IMAGE_KEY])

    def _handle_facebook(self):
        self._add_to_processed_metadata_if_not_in_metadata(
            key="og_title", value=self._metadata["title"])
        self._add_to_processed_metadata_if_not_in_metadata(
            key="og_description", value=self._metadata["custom_excerpt"])
        self._add_to_processed_metadata_if_not_in_metadata(
            key="og_image", value=self.processed_metadata[METADATA_FEATURE_IMAGE_KEY])

    def _handle_tags(self):
        ghost_tags = []
        for tag in self._metadata.get("tags", []):
            ghost_tag = self._tag_handler.get_or_create_tag(tag_name=tag)
            ghost_tags.append(ghost_tag)
        self.processed_metadata["tags"] = ghost_tags

    def __init__(self, metadata, base_dir, image_handler, tag_handler):
        self._metadata = metadata
        self._base_dir = base_dir
        self._image_handler = image_handler
        self._tag_handler = tag_handler
        self.processed_metadata = copy.deepcopy(self._metadata)
        self._handle_tags()
        self._handle_feature_image()
        self._handle_search_engines()
        self._handle_twitter()
        self._handle_facebook()
