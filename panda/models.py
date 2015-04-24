import json
import logging

class Retriever(object):
    def __init__(self, panda, model_type, path):
        self.panda = panda
        self.path = path
        self.model_type = model_type

class GroupRetriever(Retriever):        
    def all(self): 
        json_data = self.panda.get("{0}.json".format(self.path))
        return [self.model_type(self.panda, json_attr) for json_attr in json.loads(json_data)]

    def find(self, val):
        json_data = self.panda.get("{0}/{1}.json".format(self.path, val))
        return self.model_type(self.panda, json.loads(json_data))

    def where(self, pred):
        json_data = self.panda.get("{0}.json".format(self.path))
        return [self.model_type(self.panda, json_attr) for json_attr in json.loads(json_data) if pred(json_attr)]

class SingleRetriever(Retriever):
    def get(self):
        json_data = self.panda.get("{0}.json".format(self.path))
        return self.model_type(self.panda, json.loads(json_data))

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
        self.encodings = GroupRetriever(panda, Encoding, "/videos/{}/encodings".format(self.get("id"))).all
        self.metadata = SingleRetriever(panda, Metadata, "videos/{}/metadata".format(self.get("id"))).get

class Cloud(PandaModel):
    def videos(self):
        pass

    def profiles(self):
        pass

class Encoding(PandaModel):
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Encoding, self).__init__(panda, json_attr, *args, **kwargs)
        self.video = SingleRetriever(self.panda, Video, "/videos/{}".format(self.get("video_id"))).get
        self.profile = SingleRetriever(self.panda, Video, "/profiles/{}".format(self.get("video_id"))).get
    
class Profile(PandaModel):
    pass

class Notification(PandaModel):
    pass

class Metadata(PandaModel):
    pass
