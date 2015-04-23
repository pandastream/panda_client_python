import json

class PandaModel(dict):
    def __init__(self, init_json = None, *arg, **kwarg):
        if init_json:            
            super(PandaModel, self).__init__(json.loads(init_json) ,*arg, **kwarg)
        else:
            super(PandaModel, self).__init__(*arg, **kwarg)

    def to_json(self):
        return json.dumps(self)

    def all(self):
        pass

    def find(self, val):
        pass

    def delete(self):
        pass

class Video(PandaModel):
    def encodings(self):
        pass

class Cloud(PandaModel):
    def videos(self):
        pass

    def profiles(self):
        pass

class Encoding(PandaModel):
    def video(self):
        pass

class Profile(PandaModel):
    pass

class Notification(PandaModel):
    pass
