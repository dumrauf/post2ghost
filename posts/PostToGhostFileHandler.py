import json
import os

from posts.MarkdownHandler import MarkdownHandler
from posts.MetadataHandler import MetadataHandler
from posts.ReceiptFile import Receipt
from ghost_config.GhostConfigHandler import PostToGhostGhostClient
from images.ImageHandler import ImageHandler
from tags.TagHandler import TagHandler


class PostToGhostFileHandler(object):
    def _get_metadata_and_markdown(self):
        with open(self._path, 'r') as fin:
            is_metadata_found = False
            raw_metadata = ""
            metadata = {}
            markdown = ""
            for line in fin:
                if is_metadata_found:
                    markdown += line
                else:
                    raw_metadata += line
                    try:
                        metadata = json.loads(raw_metadata)
                        is_metadata_found = True
                    except json.decoder.JSONDecodeError:
                        pass
            if not is_metadata_found:
                markdown = raw_metadata
        return metadata, markdown

    def __init__(self):
        self._ghost_client = PostToGhostGhostClient()
        self._image_handler = ImageHandler(ghost_client=self._ghost_client)

    def _get_post_dict(self, path):
        self._path = path
        self._absolute_filename = os.path.abspath(path)
        self._base_dir = os.path.dirname(self._absolute_filename)
        self._receipt = Receipt(self._absolute_filename)

        metadata, markdown = self._get_metadata_and_markdown()
        self._tag_handler = TagHandler(ghost_client=self._ghost_client)
        self._metadata_handler = MetadataHandler(
            base_dir=self._base_dir, metadata=metadata, image_handler=self._image_handler, tag_handler=self._tag_handler)
        self._markdown_handler = MarkdownHandler(
            base_dir=self._base_dir, markdown=markdown, image_handler=self._image_handler)

        post_dict = self._receipt
        post_dict['markdown'] = self._markdown_handler.processed_markdown
        post_dict.update(**self._metadata_handler.processed_metadata)
        return post_dict

    def post_to_ghost(self, path):
        post_dict = self._get_post_dict(path=path)
        if "id" in post_dict:
            post = self._ghost_client.posts.update(**post_dict)
        else:
            post = self._ghost_client.posts.create(**post_dict)
        self._receipt.save_receipt(receipt_data=post)
