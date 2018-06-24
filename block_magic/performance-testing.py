# performance testing for BlockMagic
# test application: BlockMagic Payment Tracker

import datetime,os,json
import requests as http       # you may need to `pip install` this
from statistics import mean, stdev, median, mode       # you may need to `pip install` this

global use_cases, test_api_key, battery_of_tests, all_tests

test_api_key = "c42c8084d97975bc5822465ece68f57a"

def text_date_today():
	today = datetime.datetime.today()
	mm = str(today.month)
	dd = str(today.day)
	yyyy = str(today.year)
	return mm+"/"+dd+"/"+yyyy

use_cases = {
	"create_account":"http://api.click-meter.com:5000/payment-tracker/create-account",
	"push_receipt":'http://api.click-meter.com:5000/payment-tracker/push-receipt/{"from":"phil","to":"mary","amount":400,"key":"%s"}' % test_api_key,
	"query_payments":'http://api.click-meter.com:5000/payment-tracker/payment-summary/{"key":"%s","payer":"phil","payee":"*","from_date":"%s","to_date":"%s"}' % (test_api_key, text_date_today(), text_date_today())
}

battery_of_tests = {"mean":mean,"median":median,"mode":mode,"stdev":stdev}
all_tests = battery_of_tests.keys()

def time_it(url):
	start = datetime.datetime.today()
	http.get(url)
	return (datetime.datetime.today() - start).seconds

def reliability(url):
	if http.get(url).status_code == 200:
		return 1
	else:
		return 0

def battery(data):
	result = {}
	for test in all_tests:
		try:
			result[test] = battery_of_tests[test](data)
		except:
			pass
	return result

def test_rig(rounds=100):
	test_results = {"data":{"response_time":{},"reliability":{}},"analysis":{"response_time":{},"reliability":{}}}
	for case in use_cases:
		test_results["data"]["response_time"][case] = []
		test_results["data"]["reliability"][case] = []
		i = 0
		while i < rounds:
			test_results["data"]["response_time"][case].append(time_it(use_cases[case]))
			test_results["data"]["reliability"][case].append(reliability(use_cases[case]))
			i+=1
		test_results["analysis"]["response_time"][case] = battery(test_results["data"]["response_time"][case])
		test_results["analysis"]["reliability"][case] = battery(test_results["data"]["reliability"][case])
	return test_results


print test_rig()
