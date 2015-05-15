Panda client, Python
====================

This simple Python library provides a low-level interface to the REST API of [**Panda**](https://www.pandastream.com), the online video encoding service.

Setup
-----

This module has been tested with Python 2.5, 2.6 and 2.7.

You can install it using `easy_install`:

```bash
easy_install panda
```

Alternatively you can use `pip`:

```bash
pip install panda
```

A third option is to install the module directly from github repository:

```
git clone https://github.com/pandastream/panda_client_python
cd panda_client_python
python setup.py  install
```

Usage
-----
To use the module, import it into your application and then create an instance of Panda object using credentials you can obtain from your account panel at the Panda website:
```python
from panda import Panda

panda = Panda(
    api_host='api.pandastream.com',
    access_key='your-access-key',
    secret_key='your-secret-key',
    api_port=443, ## enables https
)
```
Now you can use this object to work with your Panda account. There are 6 types of objects that you can interact with:
* Cloud - represents a single cloud that can have multiple videos and profiles
* Profile - contains settings used to determine how should videos be processed
* Video - a single input video you want to process using Panda
* Encoding - a single processed output. One video can have multiple output encodings
* Notifications - contains settings used to determine how can you be notified about encoding progress
* Metadata - contains extracted data from the input video whe calculate before the encoding process

First you have to select the cloud. In order to do so, you have to provide its ID, which you can obtain from your account panel in the Panda website. Since all credentials are kept as class attributes, you can provide it easily:

```python
from panda import Panda

panda = Panda(
    api_host='api.pandastream.com',
    access_key='your-access-key',
    secret_key='your-secret-key',
    api_port=443, ## enables https
)

panda.cloud_id = 'your-cloud-id'
```

You'd usually want to use a handy shortcut and pass that value directly to object constructor:

```python
from panda import Panda

panda = Panda(
    api_host='api.pandastream.com',
    cloud_id='your-panda-cloud-id,
    access_key='your-access-key',
    secret_key='your-secret-key',
    api_port=443, ## enables https
)
```

In order to retrieve informations about the given cloud you can use either a REST GET call (using `panda.get()` method) or a wrapper called `panda.clouds.find()`:

```python
from panda import Panda, PandaError

panda = Panda(
    api_host = "api-eu.pandastream.com",
    api_port = "443",
    cloud_id = "1297b11ca25dd3ce3ea64513eda642be",
    access_key = "7042a47b8d1adeaf25b1",
    secret_key = "b92ca4b065badf0ca9c4",
)

# simple API
try:
    cloud = panda.clouds.find("1297b11ca25dd3ce3ea64513eda642be")
    print(cloud["id"])
    print("") 
    print(cloud.to_json(indent=2))
except PandaError as e:
    print(e)

print("-----")

# REST AI
import json    
try:
    cloud = json.loads(panda.get("/clouds/1297b11ca25dd3ce3ea64513eda642be.json"))
    print(cloud["id"])
    print("")
    print(json.dumps(cloud, indent=2))
expect (TypeError, ValueError) as e: # handle JSON erros
    print(e)
```

Result:

```json
1297b11ca25dd3ce3ea64513eda642be

{
  "s3_videos_bucket": "mariusz-bucket", 
  "id": "1297b11ca25dd3ce3ea64513eda642be", 
  "name": "pies", 
  "url": "http://mariusz-bucket.s3.amazonaws.com/", 
  "created_at": "2014/11/05 13:45:14 +0000", 
  "s3_private_access": false, 
  "updated_at": "2015/04/28 12:37:03 +0000"
}
-----
1297b11ca25dd3ce3ea64513eda642be

{
  "s3_videos_bucket": "mariusz-bucket", 
  "s3_private_access": false, 
  "url": "http://mariusz-bucket.s3.amazonaws.com/", 
  "created_at": "2014/11/05 13:45:14 +0000", 
  "updated_at": "2015/04/28 12:37:03 +0000", 
  "id": "1297b11ca25dd3ce3ea64513eda642be", 
  "name": "pies"
}
```

There is also a shortcut method `cloud_details()`, which allows you to reveive informations about the cloud which id you assigned to a Panda object:

```python
panda.cloud_id = "1297b11ca25dd3ce3ea64513eda642be"
try:
    details = panda.cloud_details()
    print(details.to_json(indent=2))
except PandaError as e:
    print(e)
```

Result:

```json
{
  "s3_videos_bucket": "mariusz-bucket", 
  "id": "1297b11ca25dd3ce3ea64513eda642be", 
  "name": "pies", 
  "url": "http://mariusz-bucket.s3.amazonaws.com/", 
  "created_at": "2014/11/05 13:45:14 +0000", 
  "s3_private_access": false, 
  "updated_at": "2015/05/11 14:12:14 +0000"
}
```

If you want to get all your clouds you can use either `panda.get()` with a "/clouds.json" routine or a wrapper method - `panda.clouds.all()`. For example, if you want to iterate over all your clouds to retrieve all your videos you can use following code:

```python
from panda import Panda, PandaError

panda = Panda(
    api_host = "api-eu.pandastream.com",
    api_port = "443",
    access_key = "7042a47b8d1adeaf25b1",
    secret_key = "b92ca4b065badf0ca9c4",
)

# simple API
try:
    clouds = panda.clouds.all()
    for cloud in clouds:
        panda.cloud_id = cloud["id"] # use that cloud
        for video in panda.videos.all(): # get all videos of selected clud
            print(video.to_json(indent=2))
except PandaError as e:
    print(e)

print("=============")

# REST API
import json    

try:
    clouds = json.loads(panda.get("/clouds.json"))
    for cloud in clouds:
        panda.cloud_id = cloud["id"]
        videos = json.loads(panda.get("/videos.json"))
        for video in videos:
            print(json.dumps(video, indent=2))
expect (TypeError, ValueError) as e: # handle JSON erros
    print(e)
``` 

These two examples provide a general idea about working with Panda module. You can either use a REST API to retrieve JSON strings or you can use wrapper objects to retrieve dictionary-like objects. Using simpler API is recommended as you don't have to worry about remembering proper REST path, exceptions messages are more verbose and you don't have to parse returned JSON output on your own in order to query for selected parameters. Returnrd object, besides basic dictionary abilities, also contains some additional methods:

object type | provided methods
------------ | -------------
Cloud</br>Profile | `to_json()`, `dup()`, `create()`, `delete()`, `save()`, `reload()`
Video</br>Encoding | `to_json()`, `dup()`, `create()`, `delete()`, `reload()`
Notifications | `to_json()`, `dup()`, `save()`, `reload()`
Metadata | `to_json()`

Summary of these methods:
* `to_json()` - turns object into a JSON string using inderlying `json.dump()` call
* `dup()` - copies object (same as dictionary built-in method `copy()`) and also remove the "id" parameter, which needs to be unique
* `create()` - saves object into the database using POST request
* `save()` - updates object using PUT request
* `delete()` - deletes object using DEL request
* `reload()` - retrieve actual version of an object using another GET request

In order to get these objects you can use following retriever fields of Panda object:

retriever | provided methods
------------ | -------------
Panda.clouds</br>Panda.videos</br>Panda.encodings</br>Panda.profiles | `all()`, `find()`, `where()`, `new()`, `create()`
Panda.notifications | `get()`

Summary of these methods: 
* `all()` - retrieves all objects of the given type
* `find()` - retrieves a single object of the given type and ID
* `where()` - retrieves a subset of all objects of the given type that pass provided predicate. WARNING: this is only a convenience method as it doesn't optimize database query - all objects of given type are retrieved and then filtered
* `new()` - create a new instance of the given type. Parameters to be inserted are passed as a named arguments.
* `create()` - create a new instance of the given type and then calls its `create()` method to save it into the database
* `get()` - retrieves single object of the given type

Some objects also have special methods that allows them to retrieve objects related to them:
* `Video.encodings()` - retrieves all encodings of the given video 
* `Video.metadata()` - retrives metadata of the given video (the only way to get such an object)
* `Encoding.video()` - retrieves a Video object of the given encoding

Simple API Examples
------------------ 
Exception handling are usually ommited for brevity.

Retrieve various objects and count them:
```python
import panda_client_python.panda as panda
import json

panda = panda.Panda(
    api_host = "api-eu.pandastream.com",
    api_port = "443",
    cloud_id = "1297b11ca25dd3ce3ea64513eda642be",
    access_key = "7042a47b8d1adeaf25b1",
    secret_key = "b92ca4b065badf0ca9c4",
)

print("videos")
videos = panda.videos.all()
for video in videos:
    print(video.to_json(indent=2))

print("\nclouds")
clouds = panda.clouds.all()
for cloud in clouds:
    print(cloud.to_json(indent=2))

print("\nencodings")
encodings = panda.encodings.all()
for encoding in encodings:
    print(encoding.to_json(indent=2))

print("\nprofiles")
profiles = panda.profiles.all()
for profile in profiles:
    print(profile.to_json(indent=2))

print("videos: ", len(panda.videos.all()))
print("clouds: ", len(panda.clouds.all()))
print("encodings: ", len(panda.encodings.all()))
print("profiles", len(panda.profiles.all()))
```

Retrieve a subset of all objects:
```python
encodings = panda.encodings.where(lambda e: e["fps"] < 30)
for encoding in encodings:
    print(encoding.to_json(indent=2))
```

Retrieve all encodings of a video:
```python
video = panda.videos.find("71857d3a21b765ad585a151b9618c583")
encodings = video.encodings()
for encoding in encodings:
    print(encoding.to_json(indent=2))
```

Retrieve failed encodings of a video:
```python
video = panda.videos.find("71857d3a21b765ad585a151b9618c583")
encodings = video.encodings(status="fail") # could be also "success" or "processing"
for encoding in encodings:
    print(encoding.to_json(indent=2))
```

Retrieve metadata of a video:
```python
video = panda.videos.find("71857d3a21b765ad585a151b9618c583")
metadata = video.metadata()
print(metadata.to_json(indent=2))
```

Retrieve notifications of a video:
```python
notifications = panda.notifications.get()
print(notifications.to_json(indent=2))
```

Update profile name:
```python
prf = panda.profiles.find("2bda90c140d0f79030c45c3dec5ed196")
print(prf["name"])

prf["name"] = "{0}0".format(prf["name"])
prf.save()

prf = panda.profiles.find("2bda90c140d0f79030c45c3dec5ed196")
print(prf["name"])
```

Update notification details:
```python
notif = panda.notifications.get()
print(notif.to_json(indent=2))
notif["events"] = {
    "video_created": False,
    "video_encoded": False,
    "encoding_progress": not notif["events"]["encoding_progress"],
    "encoding_completed": True
}
notif.save()

notif = panda.notifications.get()
print(notif.to_json(indent=2))
```

Create and then delete a profile:
```python
panda.profiles.create(preset_name="h264", name="MyProfile")

prof = panda.profiles.find("MyProfile")
print(prof.to_json(indent=2))

prof.delete()

try:
    prof = panda.profiles.find("MyProfile") # it should fail with PandaError now
    print(prof.to_json(indent=2))
except PandaError as e:
    print(e)
```

Create a video:
```python
print(len(panda.videos.all()))
panda.videos.create(source_url="http://s3.amazonaws.com/marcins-bucket/t.mp4")
print(len(panda.videos.all()))
```

More examples and descriptions of optional named parameters are avilable at [**Panda API documentation**](https://www.pandastream.com/docs#api).

REST API Examples
----------------

Retrieve a list of all your videos:

```python
panda.get('/videos.json')
```

Retrieve a list of profiles you have defined for your account:

```python
panda.get('/profiles.json')
```

Create a new profile:

```python
panda.post('/profiles.json', {
    'title':    'My custom profile',
    'category': 'desktop',
    'extname':  'mp4',
    'width':    320,
    'height':   240,
    'command':  'ffmpeg -i $input_file$ -f mp4 -b 128k $resolution_and_padding$ -y $output_file',
});
```

Upload a video:

```python
panda.post('/videos.json', {
    'source_url': 'http://example.com/path/to/video.mp4',
});
```

Check the status of each encoding (one per profile):

```python
panda.get('/videos/VIDEO_ID/encodings.json');
```

Remove video and profile:

```python
panda.delete('/videos/VIDEO_ID.json');
panda.delete('/profiles/PROFILE_ID.json');
```

Resumable uploads
---------------------

You can upload a local video using `panda.videos.create(file="file.mp4")`. This will attempt to upload an entire file using a single POST request. This is undesirable for big files because if the connection broke, the entire uploading process ends up failing. It's very upsetting to retry sending a 5GB file just because something went wrong after readhing 95% mark. Therefore for a local files, especially big ones, it's good to use resumable upload approach. First you have to get an session object using `Panda.upload_session()` method, passing a file as an argument. Then you can start your uploading using its `start()` method. If the connection broke the exception will be raised and then you can decide what to do with your session object using `abort()` or `resume()` method. Current status of the process can be viewed by `status` attribute which can have one of following values:
* `initialized` - session ready to start
* `uploading` - uploading started
* `error` - something went wrong. You can see the details using `error_message` attribute
* `uploaded` - uploading completed
* `aborted` - uploading canceled
* `interrupted` - stopped by user during an interactive session

An example:

```python
us = panda.upload_session("file.mp4")

retry_count = 0
try:
    us.start()
except Exception as e:
    while retry_count < 5 and us.status != "success":
        try:
            time.sleep(5)            
            us.resume()
        except Exception as e:
            retry_count += 1
```


Generating signatures
---------------------

All requests to your Panda cloud are signed using HMAC-SHA256, based on a timestamp and your Panda secret key. This is handled transparently. However, sometimes you will want to generate only this signature, in order to make a request by means other than this library. This is the case when using the [JavaScript panda_uploader](https://github.com/pandastream/panda_uploader).

To do this, a method `signed_params()` is provided:

```
panda.signed_params('POST', '/videos.json')
# => {'access_key': '8df50af4-074f-11df-b278-1231350015b1',
# 'cloud_id': 'your-cloud-id',
# 'signature': 'LejCdm0O83+jk6/Q5SfGmk14WTO1pB6Sh6Z5eA2w5C0=',
# 'timestamp': '2010-02-26T15:01:46.221513'}

panda.signed_params('GET', '/videos.json', {"some_params": "some_value"})
# => {'access_key': '8df50af4-074f-11df-b278-1231350015b1',
#  'cloud_id': 'your-cloud-id',
#  'signature': 'uHnGZ+kI9mT3C4vW71Iop9z2N7UKCv38v2l2dvREUIQ=',
#  'some_param': 'some_value',
#  'timestamp': '2010-02-26T15:04:27.039620'}
```
