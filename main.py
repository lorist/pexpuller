import logging  
from logging.config import fileConfig
from datetime import datetime, date, timedelta
import pytz
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import os
fileConfig('logging_config.ini')  
log = logging.getLogger()

'''
Run this first to store credentials in the OS
export USER="admin"
export PASSWORD="password"
export MGR_ADDRESS="mgr.customer.com"
'''
# Configuration loaded from config.ini file
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

class PexPuller():

    def __init__(self, args):
        log.debug("Initilizing object.")
        # From command line
        self.service_type = args.service_type
        self.filter = args.filter
        self.customer = args.customer
        # From config
        self.last_downloaded = config["Settings"]["last_downloaded"]
        self.now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
        self.user = os.environ.get('USER')
        self.password = os.environ.get('PASSWORD')
        self.mgr_address = os.environ.get('MGR_ADDRESS')


    def pex_pull(self, ):
        log.info("Getting participant history JSON for {}".format(self.customer))
        ## Write current time to config file as last_downloaded:
        if self.now != self.last_downloaded:
            config["Settings"]["last_downloaded"] = self.now
            log.info('Setting start time to: %s', self.now)

            try:
                with open("config.ini", "w") as cfg:
                    config.write(cfg)
            except IOError:
                log.error('error writing to config file')
                pass

        from mgr_api import MgrPull
        calls = MgrPull(service_type= self.service_type,
                    customer= self.customer,
                    filter = self.filter,
                    start = self.last_downloaded,
                    now= self.now,
                    user= self.user,
                    password= self.password,
                    mgr_address= self.mgr_address)
        # log.debug("Content = %s", calls)
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
    parser.add_argument('-f', '--filter', help='Filter on. eg. remote_alias', default='service_tag')
    parser.add_argument('-c', '--customer', help='Customer domain filter')
    parser.add_argument( "-d", "--debug", action="store_true", help = "Turn on debug mode." )
    requiredNamed = parser.add_argument_group('required named arguments')
    args = parser.parse_args()
    return args

def main():
    log.info("Excecuting app...")
    # create_db()
    args = parse_arguments()
    for arg, value in sorted(vars(args).items()):
        log.info("Argument %s: %r", arg, value)

    if args.debug:
        log.setLevel(logging.DEBUG)
    try:
        pexPuller = PexPuller(args)
        result = pexPuller.pex_pull()

        # all data:        
        all_data = pd.read_json(result)
        # abbeviated data:
        abr_data = all_data.drop(["av_id", "call_uuid", "conference", "conversation_id", "media_node", "media_streams", "parent_id", "presentation_id", "proxy_node", "resource_uri", "signalling_node", "local_alias",  "remote_port"], axis=1)

        # Process concurrent
        active_events= []
        for i in abr_data.index:
            active_events.append(len(abr_data[(abr_data["start_time"]<=abr_data.loc[i,"start_time"]) & (abr_data["end_time"]> abr_data.loc[i,"start_time"])]))
        abr_data['activecalls'] = pd.Series(active_events)

        # add customer column to db
        abr_data['customer'] = args.customer
        engine = create_engine('sqlite:///' + 'pexhistory.db', echo=False)

        abr_data.to_sql('participantHist', con=engine, index=False, if_exists='append')

    except KeyboardInterrupt as ex:
        log.warning("Terminated by user.")


if __name__ == "__main__":
    main()
