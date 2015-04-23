import json

class PandaModel(dict):
    def __init__(self, json_attr = None, *arg, **kwarg):
        if json_attr:          
            super(PandaModel, self).__init__(json_attr, *arg, **kwarg)
        else:
            super(PandaModel, self).__init__(*arg, **kwarg)

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)

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
