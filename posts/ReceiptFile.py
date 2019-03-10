import json

from settings import RECEIPT_FILE_SUFFIX


class Receipt(dict):
    def _get_receipt_file(self):
        return "{path}.{suffix}".format(path=self._path, suffix=RECEIPT_FILE_SUFFIX)

    def _get_receipt(self):
        try:
            with open(self._get_receipt_file(), "r") as f:
                receipt_data = f.read()
        except EnvironmentError:
            receipt_data = '{}'
        json_receipt_data = json.loads(receipt_data)
        return json_receipt_data

    def __init__(self, path):
        self._path = path
        existing_receipt = self._get_receipt()
        super(Receipt, self).__init__(**existing_receipt)

    def save_receipt(self, receipt_data):
        with open(self._get_receipt_file(), "w") as f:
            json_data = json.dumps(receipt_data, indent=2, sort_keys=True)
            f.write(json_data)
