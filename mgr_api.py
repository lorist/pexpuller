import logging
import requests
from requests.auth import HTTPBasicAuth
import json

log = logging.getLogger(__name__)

class MgrPull():  
    def __init__(self, **kwargs):
        # self.customer = params.get('customer')
        self.values = kwargs['mgr_address']
        self.service_type = kwargs['service_type']
        self.customer = kwargs['customer']
        self.start = kwargs['start']
        self.now = kwargs['now']
        self.user = kwargs['user']
        self.password = kwargs['password']
        self.mgr_address = kwargs['mgr_address']

    def get_result(self):
        # example of doing some stuffs
        url = "https://%s/api/admin/history/v1/participant/?limit=5000&has_media=True&service_type=%s&remote_alias__contains=%s" % (self.mgr_address, self.service_type, self.customer)
        response = requests.get(url, auth=HTTPBasicAuth(self.user, self.password))

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            logging.info("Request error: {}".format(str(e)))
            return "Error: " + str(e)

        # Must have been a 200 status code
        json_obj = response.json()
        content = json.dumps(json_obj['objects'], indent = 4,sort_keys=True)
        logging.info("Request OK")
        return content
        # return str(participantUrl)
