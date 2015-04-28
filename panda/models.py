import json
import logging

class Retriever(object):
    def __init__(self, panda, model_type, path = None):
        self.panda = panda
        self.model_type = model_type
        if path:
            self.path = path
        else:
            self.path = model_type.path

    def new(self, *args, **kwargs):
        return self.model_type(self.panda, new=True, *args, **kwargs)

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
    def __init__(self, panda, json_attr = None, new=False, *arg, **kwarg):
        self.panda = panda
        self.new = new
        self.changed_values = {}
        if json_attr:          
            super(PandaModel, self).__init__(json_attr, *arg, **kwarg)
        else:
            super(PandaModel, self).__init__(*arg, **kwarg)

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)
 
    def __setitem__(self, key, val):
        self.changed_values[key] = val
        super(PandaModel, self).__setitem__(key, val)

    def dup(self):
        copy = self.copy()
        del copy["id"]
        return copy

    def save(self):
        if self.new:
            self.create()
        else:
            self.update()

    def create(self):
        ret = type(self)(self.panda, json.loads(self.panda.post(self.path, self.changed_values)))
        if "error" not in ret:
            self.changed_values = {}
            self.new = False
        return ret

class Updatable(object):
    def update(self):
        put_path = "{0}/{1}.json".format(self.path, self["id"])
        ret = type(self)(self.panda, json.loads(self.panda.put(put_path, self.changed_values)))
        if "error" not in ret:
            self.changed_values = {}
        return ret

class Video(PandaModel):
    path = "/videos"
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Video, self).__init__(panda, json_attr, *args, **kwargs)

        self.encodings = GroupRetriever(panda, Encoding, "/videos/{0}/encodings".format(self["id"])).all
        self.metadata = SingleRetriever(panda, Metadata, "/videos/{0}/metadata".format(self["id"])).get

        self["cloud_id"] = panda.cloud_id

class Cloud(PandaModel, Updatable):
    path = "/clouds"

class Encoding(PandaModel):
    path = "/encodings"
    def __init__(self, panda, json_attr = None, *args, **kwargs):
        super(Encoding, self).__init__(panda, json_attr, *args, **kwargs)
        self.video = SingleRetriever(self.panda, Video, "/videos/{0}".format(self["video_id"])).get

        # TODO: consider the case when user provide profile_id instead
        self.profile = SingleRetriever(self.panda, Video, "/profiles/{0}".format(self["profile_name"])).get

class Profile(PandaModel, Updatable):
    path = "/profiles"

class Notification(PandaModel, Updatable):
    path = "/notifications"

    def save(self):
        return Notification(self.panda.put("/notifications.json", self))


class Metadata(PandaModel):
    pass
