import requests
from datetime import datetime

URL = """https://sendpaymentscode.azurewebsites.net/api/PaymentsReceiverHTTP?code={}"""
FUNCTION_KEY = """qutLVUJeqUP1Fiomlo2irHjq6D1BO2fI0FN_c9gh2uUNAzFu_GJDXg=="""


transactionID = 6
licensePlate = "EP726GG"
amount = 15.00

timeInString = "12/11/2022 10:50:00"
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

print("Sending payments....")
try:
    r = requests.post(URL.format(FUNCTION_KEY), data=paramaters)
    print(f"Payment transferred with status code: {r.status_code}\n{r.text}")
except Exception as e:
    print(f"Errore sending payment:\n{e}")