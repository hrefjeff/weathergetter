'''

Python 3.7 Lambda Function on AWS

'''

import os
import json
from datetime import datetime
from urllib.request import urlopen

apikey = os.environ['apikey']  # api key used to access openweather API
site = os.environ['openweatherendpoint']  # URL of the openweather RESTful interface

right_now = str(datetime.now())

def validate(res):
    '''Return False to trigger the canary

    Currently this simply checks whether the EXPECTED string is present.
    However, you could modify this to perform any number of arbitrary
    checks on the contents of SITE.
    '''
    return 'temp_max' in res


def lambda_handler(event, context):
    zip = event['zip']
    reqstring = f"{site}zip={zip},us&appid={apikey}&units=imperial"

    try:
        with urlopen(reqstring) as response:
            parsed_response = response.read().decode('utf-8')
            
            if not validate(parsed_response):
                raise Exception('Validation failed. Response does not contain temperature information.')
            
            return {
                'statusCode' : 200,
                'body' : json.loads(json.dumps(parsed_response))
            }
            
    except:
        print('Check failed!')
        raise
    finally:
        print('Check complete at {}'.format(right_now))
