import requests

try:
    from httplib import BadStatusLine
except ImportError:
    from http.client import BadStatusLine

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
    elif isinstance(exception, requests.exceptions.ConnectionError):
        try:
            if isinstance(exception.args[0].args[1], BadStatusLine):
                return True
        except:
            pass
    return False

class Session(requests.Session):
    def __init__(self):
        super().__init__()

        self.headers.update({ 'User-Agent': config.USER_AGENT })

    @retry(wait_fixed=1000, retry_on_exception=retry_on_exception)
    def request(self, method, url, **kwargs):
        kwargs['timeout'] = kwargs.get('timeout', config.TIMEOUT)
        resp = super().request(method, url, **kwargs)
        resp.raise_for_status()
        return resp
