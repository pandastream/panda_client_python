import hashlib, hmac, base64
from datetime import datetime
import urllib

class Panda(object):
    def __init__(self, cloud_id, access_key, secret_key, api_host='api.pandastream.com', api_port=80):
        self.cloud_id = cloud_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_host = api_host
        self.api_port = api_port

    def signed_params(self, verb, request_uri, params={}, timestamp_str=None):
        auth_params = params.copy()
        auth_params['cloud_id'] = self.cloud_id
        auth_params['access_key'] = self.access_key
        auth_params['timestamp'] = timestamp_str or datetime.now().isoformat()
        additional_args = auth_params.copy()
        additional_args.update(auth_params)
        auth_params['signature'] = generate_signature(verb, request_uri, self.api_host, self.secret_key, additional_args)
        return auth_params

def generate_signature(verb, request_uri, host, secret_key, params={}):
    query_string = canonical_querystring(params)

    string_to_sign = (
        verb.upper() + "\n" +
        host.lower() + "\n" +
        request_uri + "\n" +
        query_string
    )
    signature = hmac.new(secret_key, string_to_sign, hashlib.sha256).digest()
    return base64.b64encode(signature).strip()

def canonical_querystring(params):
    ordered_params = sorted([(k, v) for k, v in params.iteritems()])
    assign_strs = map(lambda pair: urlescape(pair[0]) + '=' + urlescape(pair[1]), ordered_params)
    return '&'.join(assign_strs)

def urlescape(s):
    s = unicode(s)
    return urllib.quote(s).replace("%7E", "~").replace(' ', '%20')