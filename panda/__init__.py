from request import PandaRequest
from models import Video, Cloud, Encoding, Profile, Notification
import json

class Retriever(object):
    def __init__(self, panda, path):
        self.panda = panda
        self.path = path

    def all(self):
        return [Video(json_attr) for json_attr in json.loads(self.panda.get(self.path.format("", "")))]

    def find(self, val):
        return Video(self.panda.get(self.path.format("/", val)))

class Panda(object):
    def __init__(self, cloud_id, access_key, secret_key, api_host='api.pandastream.com', api_port=443):
        self.cloud_id = cloud_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_host = api_host
        self.api_port = api_port
        self.api_version = 2

        self.videos = Retriever(self, "/videos{}{}.json")
        self.clouds = Retriever(self, "/clouds{}{}.json")
        self.encodings = Retriever(self, "/encodings{}{}.json")
        self.profiles = Retriever(self, "/profiles{}{}.json")
        self.notifications = Retriever(self, "/notifications{}{}.json")

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
