import json
import logging
from functools import partial

logger = logging.getLogger(__name__)

class Retriever(object):
    def __init__(self, panda, model_type, path):
        self.panda = panda
        self.path = path
        self.model_type = model_type

    def all(self): 
        json_data = self.panda.get("{0}.json".format(self.path))
        return [self.model_type(self.panda, json_attr) for json_attr in json.loads(json_data)]

    def find(self, val):
        json_data = self.panda.get("{0}/{1}.json".format(self.path, val))
        return self.model_type(self.panda, json.loads(json_data))

    def where(self, pred):
        json_data = self.panda.get("{0}.json".format(self.path))
        return [self.model_type(self.panda, json_attr) for json_attr in json.loads(json_data) if pred(json_attr)]

class PandaModel(dict):
    def __init__(self, panda, json_attr = None, *arg, **kwarg):
        self.panda = panda
        if json_attr:          
            super(PandaModel, self).__init__(json_attr, *arg, **kwarg)
        else:
            super(PandaModel, self).__init__(*arg, **kwarg)

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)

class Video(PandaModel):
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Video, self).__init__(panda, json_attr, *args, **kwargs)
        self.panda = panda
        self.encodings = Retriever(panda, Encoding, "/videos/{}/encodings".format(self.get("id"))).all
        self.metadata = partial(Retriever(panda, Metadata, "/videos/{}".format(self.get("id"))).find, "metadata")

class Cloud(PandaModel):
    def videos(self):
        pass

    def profiles(self):
        pass

class Encoding(PandaModel):
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Encoding, self).__init__(panda, json_attr, *args, **kwargs)
        self.video = partial(Retriever(self.panda, Video, "/videos").find, self.get("video_id"))
        self.profile = partial(Retriever(self.panda, Profile, "/profiles").find, self.get("profile_id"))
    
class Profile(PandaModel):
    pass

class Notification(PandaModel):
    pass

class Metadata(PandaModel):
    pass
