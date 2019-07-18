# pexpuller
Get gateway participant history from a Pexip management node

## Store credentials in OS environment:
```
export USER="admin"
export PASSWORD="password"
export MGR_ADDRESS="mgr.customer.com"
```
## usage: 
```
main.py [-h]
               [-s {conference,ivr,waiting_room,insufficient_capacity_screen,insufficient_licenses_screen,invalid_license_screen,presentation,two_stage_dialing,gateway,lecture,test_call}]
               [-c CUSTOMER] [-d]

Pexip History db downloader

optional arguments:
  -h, --help            show this help message and exit
  -s {conference,ivr,waiting_room,insufficient_capacity_screen,insufficient_licenses_screen,invalid_license_screen,presentation,two_stage_dialing,gateway,lecture,test_call}, 
  --service_type {conference,ivr,waiting_room,insufficient_capacity_screen,insufficient_licenses_screen,invalid_license_screen,presentation,two_stage_dialing,gateway,lecture,test_call}
  Service Type (default: gateway)
  
  -c CUSTOMER, --customer CUSTOMER
                        Customer domain filter (default: None)
                        
  -d, --debug           Turn on debug mode. (default: False)
```
