import json
import os
import datetime
from unittest import TestCase

from cloudburst.utils.utils import aws_paginator, datetime_handler

TEST_FILE = "test-fixtures/test_response.json"
MYPATH = os.path.dirname(os.path.abspath(__file__))
I = 0

class TestUtils(TestCase):
    def test_datetime_handler(self):
        data = {
            'now': datetime.datetime.now()
        }
        json.dumps(data, default=datetime_handler)
        self.assertRaises(TypeError, json.dumps, data)
        self.assertRaises(TypeError, datetime_handler, 'a')

    def test_aws_paginator(self):
        def fn():
            with open(os.path.join(MYPATH, "test-fixtures/test_response.json"), 'r') as tf:
                return json.loads(tf.read())
    
        responses = aws_paginator(fn)
        assert isinstance(responses, list)
        assert isinstance(responses[0], dict)
        
        self.assertRaises(ValueError, aws_paginator, fn, NextToken='a')

        def fn2(NextToken=None):
            # On first run, pass the response object with NextToken defined back
            if NextToken == None:
                with open(os.path.join(MYPATH, "test-fixtures/test_response_nexttoken.json"), 'r') as tf:
                    return json.loads(tf.read())
            # On the second run, pass the response object with no NextToken to
            # prevent an infinte loop
            else:
                return fn()

        responses = aws_paginator(fn2)
