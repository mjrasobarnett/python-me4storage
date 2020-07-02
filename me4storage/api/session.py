import logging
import requests
import distutils
import hashlib

from pprint import pformat
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from me4storage.common.exceptions import LoginError, ApiError, ApiStatusError
from me4storage.models.status import Status

logger = logging.getLogger(__name__)

class Session:

    def __init__(self,
                 baseurl,
                 port,
                 username,
                 password,
                 verify,
                 timeout = 30,
                 ):

        logger.debug("Init class Session")
        self.baseurl = baseurl
        self.port = port
        self.username = username
        self.password = password
        self.verify = verify
        self.timeout = timeout

        logger.debug("Session params:\n"
                "\tbaseurl: {}\n"
                "\tport: {}\n"
                "\tusername: {}\n"
                "\tpassword: {}\n"
                "\tverify: {}"
                .format(self.baseurl,
                        self.port,
                        self.username,
                        self.password,
                        self.verify))

        # If verify is false, disable all requests InsecureRequestWarning
        # instances, which produce annoying warning messages on the console
        if self.verify == False:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        # Login to the api and get session token
        self.session_token = None
        self._login()

        # Set authorization token in session headers
        self.headers = {
                "datatype": "json",
                "sessionKey": self.session_token,
                }

        self.session = requests.Session()

    def _login(self):
        """
        Login to the API and store the session token

        POST to the auth/login endpoint with the provided username and
        password. The response contains the parameter 'token' which is
        stored and then used in all future API calls to authenticate.
        """

        auth_string = hashlib.sha256(f'{self.username}_{self.password}'.encode('utf-8')).hexdigest()
        endpoint_path = f'login/{auth_string}'
        url = self._build_url(endpoint_path)

        response = requests.get(
                url,
                verify = self.verify,
                headers = { "datatype": "json",},
                )

        logger.debug("Response:\n{}".format(response.text))
        logger.debug("Headers:\n{}".format(response.headers))
        response.raise_for_status()

        response_body = response.json()

        try:
            self.session_token = response_body['status'][0]['response']
        except Exception as e:
            logger.error("Unable to login, unexpected output in "
                         f"response: \n{response.text}")
            raise LoginError("No session token received")

    def _build_url(self, endpoint):
        url = f"{self.baseurl}:{self.port}/api/{endpoint}"
        logger.debug(f"url: {url}")
        return url

    @staticmethod
    def _raise_status(response):
        """
        Check response body for 'status' object, and check that
        this shows a successfuly return code.

        If not raise ApiStatusError exception
        """
        try:
            status_responses = response['status']
        except Exception as e:
            logger.error("Unable to parse API response status object. "
                         f"Response: \n{response.text}")
            raise ApiError("Unexpected status in response")

        for status_response in status_responses:
            status = Status(status_response)
            if status.return_code != 0:
                raise ApiStatusError(f"Operation failed. rc: {status.return_code}. Response: {status.response}", response)

    def _get(self, url, params={}):

        logger.debug("HTTP GET: {}".format(url))
        response = self.session.get(url,
                                    verify=self.verify,
                                    headers=self.headers,
                                    params=params,
                                    timeout=self.timeout,
                                    )
        # Throw exception if bad request (a 4XX client error or 5XX server error)
        response.raise_for_status()

        # Decode response from json
        response_body = response.json()
        logger.debug("Response:\n{}".format(pformat(response_body)))
        logger.debug("Headers:\n{}".format(response.headers))

        # Accorindg to Dell API guidelines all API responses
        # contain a 'status' object, that we should check that
        # the operation was successful
        self._raise_status(response_body)

        return response_body


    def get_object(self, endpoint, params={}):
        """ Get a single object from API """

        url = self._build_url(endpoint)
        data = self._get(url, params)
        if isinstance(data, list):
            raise RuntimeError(f'Bad object URL \'{url}\': expected an object, '
                               f'got a collection of objects')
        return data
