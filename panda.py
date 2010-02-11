class Panda(object):
    def __init__(self, cloud_id, access_key, secret_key, api_host='api.pandastream.com', api_port=80):
        self.cloud_id = cloud_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_host = api_host
        self.api_port = api_port