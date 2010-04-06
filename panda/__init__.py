import hashlib, hmac, base64
from datetime import datetime, tzinfo, timedelta
import urllib, httplib

class Panda(object):
    def __init__(self, cloud_id, access_key, secret_key, api_host='api.pandastream.com', api_port=80):
        self.cloud_id = cloud_id
        self.access_key = access_key
        self.secret_key = secret_key
        self.api_host = api_host
        self.api_port = api_port
        self.api_version = 2

    def signed_params(self, verb, request_uri, params={}, timestamp_str=None):
        auth_params = params.copy()
        auth_params['cloud_id'] = self.cloud_id
        auth_params['access_key'] = self.access_key
        auth_params['timestamp'] = timestamp_str or generate_timestamp()
        additional_args = auth_params.copy()
        additional_args.update(auth_params)
        auth_params['signature'] = generate_signature(verb, request_uri, self.api_host, self.secret_key, additional_args)
        return auth_params

    def api_url(self):
        return 'http://' + self.api_host_and_port() + self.api_path()

    def api_host_and_port(self):
        ret = self.api_host
        if str(self.api_port) != '80':
            ret += ':' + self.api_host
        return ret

    def api_path(self):
        return '/v' + str(self.api_version)

    def get(self, request_path, params={}):
        return self._http_request('GET', request_path, params)

    def post(self, request_path, params={}):
        return self._http_request('POST', request_path, {}, params)

    def put(self, request_path, params={}):
        return self._http_request('PUT', request_path, {}, params)

    def delete(self, request_path, params={}):
        return self._http_request('DELETE', request_path, params)

    def _http_request(self, verb, path, query={}, data={}):
        verb = verb.upper()
        path = canonical_path(path)
        suffix = ''
        signed_data = None
        headers = {}

        if verb == 'POST' or verb == 'PUT':
            signed_data = self._signed_query(verb, path, data)
            headers = {"Content-type": "application/x-www-form-urlencoded"}
        else:
            signed_query_string = self._signed_query(verb, path, query)
            suffix = '?' + signed_query_string

        url = self.api_path() + path + suffix

        http = httplib.HTTPConnection(self.api_host, self.api_port)
        http.request(verb, url, signed_data, headers)
        return http.getresponse().read()

    def _signed_query(self, verb, request_path, params={}, timestamp=None):
        return dict2query(self.signed_params(verb, request_path, params, timestamp))


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

def canonical_path(path):
    return '/' + path.strip(' \t\n\r\0\x0B/')

def dict2query(d):
    pairs = []
    for k, v in d.iteritems():
        pairs.append(urlescape(k) + '=' + urlescape(v))
    return '&'.join(pairs)

def generate_timestamp():
    return datetime.now(UTC()).isoformat()

class UTC(tzinfo):
    """UTC"""

    def utcoffset(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return timedelta(0)
