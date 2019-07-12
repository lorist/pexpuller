import logging  
from logging.config import fileConfig
from datetime import datetime, date, timedelta
import pandas as pd

fileConfig('logging_config.ini')  
log = logging.getLogger()

# Configuration loaded from config.ini file
import configparser
config = configparser.ConfigParser()
config.read('config.ini')


class MainProgramObject():

    def __init__(self, args):
        log.debug("Initilizing object.")
        # From command line
        self.service_type = args.service_type
        self.customer = args.customer
        # From config file
        self.start = config["Settings"]["last_downloaded"]
        self.now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.user = config["Settings"]["user"]
        self.password = config["Settings"]["password"]
        self.mgr_address = config["Settings"]["mgr_address"]

    def some_logic(self, ):
        log.info("Getting participant history JSON for {}".format(self.customer))
        from mgr_api import MgrPull
        calls = MgrPull(service_type= self.service_type,
                    customer= self.customer,
                    start= self.start,
                    now= self.now,
                    user= self.user,
                    password= self.password,
                    mgr_address= self.mgr_address)
        return calls.get_result()


def parse_arguments():  
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
    service_type_list = [   "conference",
                            "ivr",
                            "waiting_room",
                            "insufficient_capacity_screen",
                            "insufficient_licenses_screen",
                            "invalid_license_screen",
                            "presentation",
                            "two_stage_dialing",
                            "gateway",
                            "lecture",
                            "test_call"
                        ]   
    parser = ArgumentParser(description="Pexip History db downloader", formatter_class=ArgumentDefaultsHelpFormatter)                
    parser.add_argument('-s', '--service_type', help='Service Type', default='gateway', choices=service_type_list)
    parser.add_argument('-c', '--customer', help='Customer domain filter')
    parser.add_argument( "-d", "--debug", action="store_true", help = "Turn on debug mode." )
    requiredNamed = parser.add_argument_group('required named arguments')
    # requiredNamed.add_argument('-f', '--file', help='CSV output file name', required=True)
    args = parser.parse_args()
    return args

def main():
    log.info("Excecuting app...")
    args = parse_arguments()
    for arg, value in sorted(vars(args).items()):
        log.info("Argument %s: %r", arg, value)

    
    if args.debug:
        log.setLevel(logging.DEBUG)
    try:
        # mainObj = MainProgramObject(args.arg1, args.barg2)
        mainObj = MainProgramObject(args)
        result = mainObj.some_logic()
        # all data:
        # pd.read_json(result).to_csv(args.customer + '-participant.csv')
        all_data = pd.read_json(result)
        # abbeviated data:
        abr_data = all_data.drop(["av_id", "call_uuid", "conference", "conversation_id", "id", 
                                  "media_node", "media_streams", "parent_id", "presentation_id",
                                  "proxy_node", "resource_uri", "signalling_node", "local_alias",
                                  "remote_address", "remote_port", "service_tag",], axis=1).to_csv(args.customer + '-participant.csv')

    except KeyboardInterrupt as ex:
        log.warning("Terminated by user.")

if __name__ == "__main__":  
    main()
