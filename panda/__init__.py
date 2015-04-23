from request import PandaRequest

class Retriever(object):
    def __init__(self, name):
        self.name = name

    def all(self):
        return "return all %s" % self.name

    def find(self, val):
        return "return %s with val %s" % (self.name, val)

class Panda(object):
    def __init__(self, cloud_id, access_key, secret_key, api_host='api.pandastream.com', api_port=443):
        self.cloud_id = cloud_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_host = api_host
        self.api_port = api_port
        self.api_version = 2

        self.video = Retriever("video")
        self.cloud = Retriever("cloud")
        self.encoding = Retriever("encoding")
        self.profile = Retriever("profile")
        self.notification = Retriever("notification")

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

