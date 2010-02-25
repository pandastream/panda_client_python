Panda client, Python
====================

This simple Python library provides a low-level interface to the REST API of [**Panda**](http://account.pandastream.com), the online video encoding service.


Setup
-----

This module has been tested with Python 2.5 and 2.6.

You can install it using `easy_install`:

    easy_install panda

To use the module, import it into your application. Then create an instance using your Panda details:

    import panda

    panda = panda.Panda(array(
      'api_host':   'api.pandastream.com',
      'cloud_id':   'your-panda-cloud-id',
      'access_key': 'your-access-key',
      'secret_key': 'your-secret-key',
    ));

Now you can use this instance to interact with your Panda cloud.


Examples
--------

Retrieve a list of all your videos:

    panda.get('/videos.json')

Before being able to encode videos, you need to define **encoding profiles**. You can retrieve a list of profiles you have defined for your account:

    panda.get('/profiles.json')

Initially though, this list will be empty. Solve this by creating a new profile:

    panda.post('/profiles.json', {
        'title':    'My custom profile',
        'category': 'desktop',
        'extname':  'mp4',
        'width':    320,
        'height':   240,
        'command':  'ffmpeg -i $input_file$ -f mp4 -b 128k $resolution_and_padding$ -y $output_file',
    });

From now on, any video that you upload will be encoded in all available profiles by default. Let's upload a video now:

    panda.post('/videos.json', {
        'source_url': 'http://example.com/path/to/video.mp4',
    });

It will take some time to encode, depending on the size of the video and other parameters. While you wait, you can check the status of each encoding (one per profile):

    panda.get('/videos/VIDEO_ID/encodings.json');

Eventually, the process will end and each profile will have a URL where you can retrieve the result from.

Finally, you may want to clean up after your tests:

    panda.delete('/videos/VIDEO_ID.json');
    panda.delete('/profiles/PROFILE_ID.json');
