import requests
from datetime import datetime
from Code.Logging.Logger import loggerSetup

paymentsLogger = loggerSetup('paymentsLogger_PaymentsGenerator', 'Code/Logging/Payments/payments.log')

URL = """https://paymentslambda.azurewebsites.net/api/HttpPaymentsHandler?code={}"""
FUNCTION_KEY = """lE1Qt9uJnAM9X2scZGBHBKZV_PPaSTrgaatxFQ-8Y2ecAzFuQn8U8w=="""


transactionID = 7
licensePlate = "EP726GG"
amount = 15.00

timeInString = "25/11/2022 10:50:00"
timeIn = datetime.strptime(timeInString,"%d/%m/%Y %H:%M:%S").timestamp()

paymentTimeString = "12/11/2022 10:55:30"
paymentTime = datetime.strptime(paymentTimeString,"%d/%m/%Y %H:%M:%S").timestamp()

paramaters = {
    "transactionID":transactionID,
    "licensePlate":licensePlate,
    "amount":amount,
    "timeIn":timeIn,
    "paymentTime":paymentTime
}

paymentsLogger.info("TEST: Sending payments....")
try:
    r = requests.post(URL.format(FUNCTION_KEY), data=paramaters)
    paymentsLogger.info(f"TEST: Payment transferred with status code: {r.status_code} - {r.text}")
except Exception as e:
    paymentsLogger.error(f"TEST: Error sending payment:{e}")