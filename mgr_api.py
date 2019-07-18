import logging
import requests
from requests.auth import HTTPBasicAuth
import json
import sys

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
        url = "https://%s/api/admin/history/v1/participant/?limit=5000&has_media=True&call_direction=in&service_type=%s&remote_alias__contains=%s&end_time__gte=%s&end_time__lt=%s" % (self.mgr_address, self.service_type, self.customer, self.start, self.now)
        response = requests.get(url, auth=HTTPBasicAuth(self.user, self.password))
        json_obj = []
        try:
            response.raise_for_status()
            json_obj = response.json()
        except requests.exceptions.HTTPError as e:
            # Whoops it wasn't a 200
            log.info("Request error: {}".format(str(e)))
            return "Error: " + str(e)

        # Must have been a 200 status code
        if json_obj:
	        total_count = json_obj['meta']['total_count']
	        if total_count > 0:
	        	content = json.dumps(json_obj['objects'], indent = 4,sort_keys=True)
	        	log.info("Got results. %s", total_count)
	        	return content
	        else:
	        	log.info("No calls during these times")
	        	sys.exit()
