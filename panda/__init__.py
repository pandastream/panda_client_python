from request import PandaRequest
from models import Video, Cloud, Encoding, Profile, Notification, GroupRetriever, SingleRetriever, PandaError
import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())

class Panda(object):
    def __init__(self, cloud_id, access_key, secret_key, api_host='api.pandastream.com', api_port=443):
        self.cloud_id = cloud_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_host = api_host
        self.api_port = api_port
        self.api_version = 2

        self.videos = GroupRetriever(self, Video)
        self.clouds = GroupRetriever(self, Cloud)
        self.encodings = GroupRetriever(self, Encoding)
        self.profiles = GroupRetriever(self, Profile)
        self.notifications = SingleRetriever(self, Notification)

    def credentials(self):
        cred = [
            'cloud_id', 
            'access_key',
            'secret_key', 
            'api_host', 
            'api_port',
            'api_version'
        ]
        return {key: self.__dict__[key] for key in cred }

    def get(self, request_path, params={}):
        return PandaRequest('GET', request_path, self.credentials(), params).send()

    def post(self, request_path, params={}):
        return PandaRequest('POST', request_path, self.credentials(), params).send()

    def put(self, request_path, params={}):
        return PandaRequest('PUT', request_path, self.credentials(), params).send()

    def delete(self, request_path, params={}):
        return PandaRequest('DELETE', request_path, self.credentials(), params).send()
