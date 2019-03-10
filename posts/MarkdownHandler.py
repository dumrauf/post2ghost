import os
import re

from images.utils import is_external_image

image_pattern = re.compile(r"!\[.*\]\(.*\)")
filename_pattern = re.compile(r"\(.*\)")


class MarkdownHandler(object):
    @staticmethod
    def _get_filename(image):
        filenames = filename_pattern.findall(image)
        filename = filenames[0][1:-1]
        filename_and_alt_text = filename.split(' ', 1)
        path = filename_and_alt_text[0]
        return path

    def _get_all_images_from_markdown(self):
        images = image_pattern.findall(self._markdown)
        image_paths = {}
        for image in images:
            path = self._get_filename(image=image)
            image_paths[path] = ""
        return image_paths

    def _upload_all_images(self, images):
        for key in images:
            if is_external_image(path=key):
                uploaded_path = key
            else:
                absolute_path = os.path.join(self._base_dir, key)
                uploaded_path = self._image_handler.upload_image(
                    path=absolute_path)
            images[key] = uploaded_path
        return images

    def _replace_images_in_original_markdown(self, images):
        replaced_markdown = self._markdown
        for key in sorted(images, key=len, reverse=True):
            original_path = key
            uploaded_path = images[key]
            replaced_markdown = replaced_markdown.replace(
                original_path, uploaded_path)
        return replaced_markdown

    def _process_images(self):
        images = self._get_all_images_from_markdown()
        images = self._upload_all_images(images=images)
        processed_markdown = self._replace_images_in_original_markdown(
            images=images)
        return processed_markdown

    def __init__(self, base_dir, markdown, image_handler):
        self._base_dir = base_dir
        self._markdown = markdown
        self._image_handler = image_handler
        processed_markdown = self._process_images()
        final_markdown = processed_markdown.strip()
        self.processed_markdown = final_markdown
