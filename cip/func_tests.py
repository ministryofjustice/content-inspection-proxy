import os
import traceback
import yaml
import requests
from tests import soap_requests

with open('config/test_config.yaml') as cfg_file:
    config = yaml.load(cfg_file.read())

methods = {
    'get': requests.get,
    'post': requests.post,
    'head': requests.head,
}

soap_req_map = {
    'check_prisoner_info': soap_requests.soap_checkPrisonerInfo,
    'get_available_timeslots': soap_requests.soap_getAvailableTimeSlots1,
    'book_visit': soap_requests.soap_bookVisit_fixed,
}

total = len(config['test_targets'])
fail = 0

DEBUG = os.environ.get('DEBUG', False)

for target in config['test_targets']:
    try:
        print 'Testing {}... '.format(target['name']),
        url = '{}{}'.format(config['base_url'], target['url']) \
            if target['url'][0] == '/' else target['url']
        headers = config.get('base_headers', {})
        headers.update(target.get('headers', {}))

        try:
            data = soap_req_map[target['data']]
        except KeyError:
            print 'Request {} not found for test {}.'.format(
                target['data'], target['method'])
            fail += 1
            continue

        try:
            fn = methods[target['method']]
            x = fn(url, headers=headers, data=data)
        except KeyError:
            print 'Test {} uses unsupported method {}'.format(
                target['name'], target['method'])
            fail += 1
            continue

        if x.status_code == target['success']:
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

print 'Failed: {} out of {}'.format(fail, total)
if fail:
    print 'Rerun with env variable DEBUG set in order to see diagnostic output'