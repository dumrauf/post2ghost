import json

from ghost_client import Ghost

from settings import CONFIG_FILE


class PostToGhostGhostClient(Ghost):
    @staticmethod
    def _get_config():
        with open(CONFIG_FILE, "r") as f:
            ghost_config = json.load(f)
        return ghost_config

    def __init__(self):
        config = self._get_config()
        super(PostToGhostGhostClient, self).__init__(
            base_url=config['base_url'],
            client_id=config['client_id'],
            client_secret=config['client_secret'],
        )
        self.login(username=config['username'],
                   password=config['password'])
