import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 38.630280
MY_LNG = -90.200310

def iss_is_near():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_position = (iss_longitude, iss_latitude)

    if (MY_LAT - 5) < iss_latitude < (MY_LAT + 5) and (MY_LNG - 5) < iss_longitude < (MY_LNG + 5):
        return True

def send_email():
    with smtplib.SMTP(host="smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user="carnasci89@gmail.com", password="cxauozxphpreajme")
        connection.sendmail(
            to_addrs="carnasci89@gmail.com",
            from_addr="carnasci89@gmail.com",
            msg="Subject:Look up!\n\nISS is within view."
        )

def is_night():
    parameters = {
        "lat":MY_LAT,
        "lng":MY_LNG,
        "formatted":0,
    }

    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    time.sleep(60)
    if iss_is_near() and is_night():
        send_email()