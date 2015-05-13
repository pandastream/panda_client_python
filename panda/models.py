import json
import logging
from requests import post
from functools import wraps
from os import stat

logger = logging.getLogger(__name__)

class PandaError(Exception):
    pass

def error_check(func):
    @wraps(func)
    def check(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            if "error" in res:
                logger.error(res["message"])
                raise PandaError(res["message"])
        except Exception as e:
            logger.error(e)
            raise
        return res
    return check

class Retriever(object):
    def __init__(self, panda, model_type, path = None):
        self.panda = panda
        self.model_type = model_type
        if path:
            self.path = path
        else:
            self.path = model_type.path

class GroupRetriever(Retriever):
    @error_check
    def _all(self, **kwargs):
        json_data = self.panda.get("{0}.json".format(self.path), kwargs)
        return json.loads(json_data)

    @error_check
    def new(self, *args, **kwargs):
        return self.model_type(self.panda, *args, **kwargs)

    @error_check
    def create(self, *args, **kwargs):
        return self.new(*args, **kwargs).create(**kwargs)

    @error_check
    def find(self, val, **kwargs):
        json_data = self.panda.get("{0}/{1}.json".format(self.path, val), **kwargs)
        return self.model_type(self.panda, json.loads(json_data))

    def all(self, **kwargs):
        return [self.model_type(self.panda, json_attr) for json_attr in self._all(**kwargs)]

    def where(self, pred, **kwargs):
        return [self.model_type(self.panda, json_attr) for json_attr in self._all(**kwargs) if pred(json_attr)]

class SingleRetriever(Retriever):
    @error_check
    def get(self, **kwargs):
        json_data = self.panda.get("{0}.json".format(self.path), **kwargs)
        return self.model_type(self.panda, json.loads(json_data))

    @error_check
    def post(self, **kwargs):
        json_data = self.panda.post("{0}.json".format(self.path), **kwargs)
        return self.model_type(self.panda, json.loads(json_data))

class PandaDict(dict):
    def __init__(self, panda, json_attr = None, new=False, *arg, **kwarg):
        self.panda = panda
        if json_attr:
            super(PandaDict, self).__init__(json_attr, *arg, **kwarg)
        else:
            super(PandaDict, self).__init__(*arg, **kwarg)

    def to_json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)

class PandaModel(PandaDict):
    def __init__(self, *args, **kwargs):
        super(PandaModel, self).__init__(*args, **kwargs)
        self.setdefault("id")

    def dup(self):
        copy = self.copy()
        del copy["id"]
        return copy

    @error_check
    def save(self):
        return self.create()

    @error_check
    def create(self, **kwargs):
        json_data = self.panda.post("{0}.json".format(self.path), kwargs)
        return self.__class__(self.panda, json.loads(json_data))

    @error_check
    def delete(self, **kwargs):
        json_data = self.panda.delete("{0}/{1}.json".format(self.path, self["id"]), kwargs)
        return self.__class__(self.panda, json.loads(json_data))

class UpdatablePandaModel(PandaModel):
    changed_values = {}

    @error_check
    def save(self):
        return self.update()

    @error_check
    def update(self):
        put_path = "{0}/{1}.json".format(self.path, self["id"])
        ret = type(self)(self.panda, json.loads(self.panda.put(put_path, self.changed_values)))
        if "error" not in ret:
            self.changed_values = {}
        return ret

    def __setitem__(self, key, val):
        self.changed_values[key] = val
        super(UpdatablePandaModel, self).__setitem__(key, val)

class UploadSession(object):
    def __init__(panda, file_name):
        self.panda = panda
        self.file_name = file_name
        self.file_size = stat(file_name).st_size
        data = panda.post('/videos/upload.json', {
            "file_size": self.file_size,
            "file_name": file_name})
        self.location = json.loads(data)["location"]
        self.status = "initialized"
        self.video = None
        self.error_message = None

    def _read_chunks(self):
        i = 0
        while True:
            data = file_object.read(CHUNK_SIZE)
            if not data:
                break
            yield (data, i)
            i = i+1

    def start(self, pos=0):
        self.status = "processing"
        with open(file_name) as f:
            try:
                for chunk, i in read_chunks(f):
                    index = i * CHUNK_SIZE

                    res = post(self.location, headers = {
                        'Content-Type': 'application/octet-stream',
                        'Cache-Control': 'no-cache',
                        'Content-Range': "bytes {0}-{1}/{2}".format(pos + index, pos + index+CHUNK_SIZE-1, self.file_size),
                        'Content-Length': str(CHUNK_SIZE)
                    }, data=chunk)
                    if res.status_code == 200:
                        self.video = Video.new(self.panda, json_attr=res.json())
                    else:
                        self.status = "error"
                        break
            except Exception as e:
                self.status = "error"
                self.error_message = str(e)

    def resume(self):
        res = post(self.location, headers = {
            'Content-Type': 'application/octet-stream',
            'Cache-Control': 'no-cache',
            'Content-Range': "bytes */{0}".format(self.file_size),
            'Content-Length': "0"
        })
        pos = res["Range"].split("-")[0]

    def abort(self):
        if status != "success":
            self.status = "aborted"
            self.error_message = None

class Video(PandaModel):
    path = "/videos"

    def encodings(self):
        return GroupRetriever(self.panda, Encoding, "/videos/{0}/encodings".format(self["id"])).all()

    def metadata(self):
        return SingleRetriever(self.panda, Metadata, "/videos/{0}/metadata".format(self["id"])).get()

class Cloud(UpdatablePandaModel):
    path = "/clouds"

class Encoding(PandaModel):
    path = "/encodings"

    def video(self):
        return SingleRetriever(self.panda, Video, "/videos/{0}".format(self["video_id"])).get()

    def profile(self):
        key = self["profile_name"] or self["profile_id"]
        return SingleRetriever(self.panda, Video, "/profiles/{0}".format(key)).get()

    def cancel(self):
        return SingleRetriever(self.panda, PandaDict, "/encodings/{0}/cancel.json".format(self["id"])).post()

    def retry(self):
        return SingleRetriever(self.panda, PandaDict, "/encodings/{0}/retry.json".format(self["id"])).post()

class Profile(UpdatablePandaModel):
    path = "/profiles"

class Notifications(UpdatablePandaModel):
    path = "/notifications"

    @error_check
    def update(self):
        tmp = dict(self)
        for event in tmp["events"]:
            tmp["events"][event] = str(tmp["events"][event]).lower()
        return Notifications(self.panda.put("/notifications.json", tmp))

    def delete(self):
        raise AttributeError("Notification instance has no attribute 'delete'")

    def dup(self):
        return self.copy()

class Metadata(PandaDict):
    pass
