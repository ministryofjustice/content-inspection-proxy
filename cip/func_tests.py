import os
import traceback
import sys
import yaml
import time
import requests
from tests import soap_requests

cfg = 'func_tests/test.yaml'\
    if 'CIP_FT_CFG' not in os.environ else os.environ['CIP_FT_CFG']

with open(cfg) as cfg_file:
    config = yaml.load(cfg_file.read())
methods = {
    'get': requests.get,
    'post': requests.post,
    'head': requests.head,
}

soap_req_map = {
    'check_prisoner_info': soap_requests.soap_checkPrisonerInfo,
    'check_prisoner_info_domis': soap_requests.soap_checkPrisonerInfo_domis,
    'check_domis_prisoner_info': soap_requests.soap_domis_checkPrisonerInfo,
    'get_available_timeslots': soap_requests.soap_getAvailableTimeSlots1,
    'get_domis_available_timeslots': soap_requests.soap_domis_getAvailableTimeSlots1,
    'book_visit': soap_requests.soap_bookVisit_fixed,
}

if 'CIP_FT_BASE_URL' in os.environ:
    config['base_url'] = os.environ['CIP_FT_BASE_URL']

total = len(config['fixtures'])
fail = 0

DEBUG = os.environ.get('DEBUG', False)

for fixture in config['fixtures']:
    try:
        print 'Testing {}... '.format(fixture['name'])
        url = '{}{}'.format(config['base_url'], fixture['url']) \
            if fixture['url'][0] == '/' else fixture['url']
        print "url: {}".format(url)
        headers = config.get('base_headers', {})
        headers.update(fixture.get('headers', {}))

        try:
            data = soap_req_map[fixture['data']]
        except KeyError:
            data = ""

        try:
            fn = methods[fixture['method']]
            x = fn(url, headers=headers, data=data)
        except KeyError:
            print 'Test {} uses unsupported method {}'.format(
                fixture['name'], fixture['method'])
            fail += 1
            continue

        if x.status_code == fixture['success']:
            print 'SUCCESS'
        else:
            print 'FAIL'
            if DEBUG:
                print 'Status Code: ', x.status_code
                print 'Headers: ', x.headers
                print 'Payload: ', x.text

            fail += 1
    except Exception, e:
        print 'FAIL'
        fail += 1
        if DEBUG:
            print traceback.format_exc()

    # Temporarily extending existing dictionary with sleep.
    # Otherwise we should have had to extend DSL to with different token for sleep and different for request.
    # ..and this convinces me that next DSL extension should force us to migrate to i.e. nosetests or cucumber.
    # Anything but not our DSL.
    if 'sleep' in fixture.keys():
        time.sleep(fixture['sleep'])
    print


print '\n\nFailed: {} out of {}'.format(fail, total)
if fail:
    if not DEBUG:
        print 'Rerun with env variable DEBUG set in order to see diagnostic output'
    sys.exit(1)
