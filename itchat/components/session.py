import requests

from retrying import retry

from .. import config

def load_session(core):
    core.s = Session()

def retry_on_exception(exception):
    if isinstance(exception, requests.exceptions.HTTPError):
        status_code = exception.response.status_code
        if status_code == 503:
            return True
    elif isinstance(exception, requests.exceptions.Timeout):
        return True
    return False

class Session():
    def __init__(self):
        self.s = requests.Session()
        self.cookies = self.s.cookies

    @retry(wait_fixed=1000, retry_on_exception=retry_on_exception)
    def get(self, url, **kwargs):
        kwargs['timeout'] = config.TIMEOUT
        resp = self.s.get(url, **kwargs)
        resp.raise_for_status()
        return resp

    @retry(wait_fixed=1000, retry_on_exception=retry_on_exception)
    def post(self, url, **kwargs):
        kwargs['timeout'] = config.TIMEOUT
        resp = self.s.post(url, **kwargs)
        resp.raise_for_status()
        return resp
