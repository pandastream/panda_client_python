import json
import logging

logger = logging.getLogger(__name__)

class Retriever(object):
    def __init__(self, panda, model_type, path = None):
        self.panda = panda
        self.model_type = model_type
        if path:
            self.path = path
        else:
            self.path = model_type.path

    def new(self, *args, **kwargs):
        return self.model_type(self.panda, *args, **kwargs)

    def create(self, *args, **kwargs):
        return self.new(*args, **kwargs).create()    

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

class AbstractPandaModel(dict):
    def __init__(self, panda, json_attr = None, new=False, *arg, **kwarg):
        self.panda = panda
        if json_attr:          
            super(AbstractPandaModel, self).__init__(json_attr, *arg, **kwarg)
        else:
            super(AbstractPandaModel, self).__init__(*arg, **kwarg)

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)

class BasicPandaModel(AbstractPandaModel):
    def dup(self):
        copy = self.copy()
        del copy["id"]
        return copy

    def save(self):
        return self.create()

    def create(self):
        return self.panda.post("{0}.json".format(self.path), self)

    def delete(self):
        return self.panda.delete("{0}/{1}.json".format(self.path, self["id"]))

class UpdatablePandaModel(BasicPandaModel):
    changed_values = {}

    def save(self):
        return self.update()

    def update(self):
        put_path = "{0}/{1}.json".format(self.path, self["id"])
        ret = type(self)(self.panda, json.loads(self.panda.put(put_path, self.changed_values)))
        if "error" not in ret:
            self.changed_values = {}
        return ret

    def __setitem__(self, key, val):
        self.changed_values[key] = val
        super(UpdatablePandaModel, self).__setitem__(key, val)

class Video(BasicPandaModel):
    path = "/videos"
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Video, self).__init__(panda, json_attr, *args, **kwargs)

        self.encodings = GroupRetriever(panda, Encoding, "/videos/{0}/encodings".format(self["id"])).all
        self.metadata = SingleRetriever(panda, Metadata, "/videos/{0}/metadata".format(self["id"])).get

class Cloud(UpdatablePandaModel):
    path = "/clouds"

class Encoding(BasicPandaModel):
    path = "/encodings"
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Encoding, self).__init__(panda, json_attr, *args, **kwargs)
        self.video = SingleRetriever(self.panda, Video, "/videos/{0}".format(self["video_id"])).get

        key = self["profile_name"] or self["profile_id"]
        self.profile = SingleRetriever(self.panda, Video, "/profiles/{0}".format(key)).get

class Profile(UpdatablePandaModel):
    path = "/profiles"

class Notification(UpdatablePandaModel):
    path = "/notifications"

    def save(self):
        tmp = dict(self)
        for event in tmp["events"]:
            tmp["events"][event] = str(tmp["events"][event]).lower()
        return Notification(self.panda.put("/notifications.json", tmp))

    def delete(self):
        pass

    def dup(self):
        return self.copy()

class Metadata(AbstractPandaModel):
    pass
