# performance testing for BlockMagic
# test application: BlockMagic Payment Tracker

import datetime,os,json
import requests as http
from statistics import mean, stdev, median, mode

global use_cases

use_cases = {
	"create_account":"http://api.click-meter.com:5000/payment-tracker/create-account",
	"push_receipt":'http://api.click-meter.com:5000/payment-tracker/push-receipt/{"from":"phil","to":"mary","amount":400,"key":"be52b8fbc0fea0ca3783481b806266e5"}',
	"query_payments":'http://api.click-meter.com:5000/payment-tracker/payment-summary/{"key":"be52b8fbc0fea0ca3783481b806266e5","payer":"phil","payee":"*","from_date":"6/16/2018","to_date":"6/16/2018"}'
}

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
	try:
		result["mean"] = mean(data)
	except:
		pass
	try:
		result["median"] = median(data)
	except:
		pass
	try:
		result["mode"] = mode(data)
	except:
		pass
	try:
		result["stdev"] = stdev(data)
	except:
		pass
	return result


def test_rig(rounds=50):
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
