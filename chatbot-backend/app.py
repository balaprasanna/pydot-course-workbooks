TOKEN = "PLACE YOUR TOKEN HERE...."

import botogram
from datetime import datetime, timedelta
bot = botogram.create(TOKEN)

from balautil import requestutil as R
import pandas as pd
import matplotlib.pyplot as plt

def get_exchangerate_from_api(src,target):
    url = f"https://api.exchangeratesapi.io/latest?symbols={target}&base={src}"
    data = R.Get(url)
    value = data['rates'][target]
    return value

def get_last_10_days_dates():
    end_date = datetime.now()
    start_date = end_date - timedelta(days=10)
    start_date = start_date.isoformat().split("T")[0]
    end_date = end_date.isoformat().split("T")[0]
    return start_date,end_date

def get_exchangerate_history_from_api(src,target,start_date,end_date):
    url = f"https://api.exchangeratesapi.io/history?start_at={start_date}&end_at={end_date}&base={src}&symbols={target}"
    data = R.Get(url)
    return data

@bot.command("hello")
def hello_command(chat, message, args):
    """Say hello to the world!"""
    print(args)

    if len(args) >= 1:
        chat.send( " ".join(args))
    else:
        chat.send("Hello world")

@bot.command("time")
def time_command(chat, message, args):
    """Say the current time of the machine"""
    print(args)
    chat.send(f"Current time: {str(datetime.now())}")

@bot.command("exchangerate")
def get_exchange_rate(chat,message,args):
    """Find the exchange rate.. """
    
    if len(args) != 2:
        chat.send("USAGE info: /exchnagerate <USD> <SGD>")
        return

    src = args[0]
    target = args[1]

    exchangerate = get_exchangerate_from_api(src,target)
    resp = f"1 {src} = {exchangerate} {target}"
    chat.send(resp)

# /history INR SGD
@bot.command("history")
def get_history(chat,message,args):
    """Find the exchange rate history and plot it.. """
    
    if len(args) != 2:
        chat.send("USAGE info: /history <USD> <SGD>")
        return

    src = args[0]
    target = args[1]

    start_date,end_date = get_last_10_days_dates()
    history_data = get_exchangerate_history_from_api(src,target,start_date,end_date)
    pd.DataFrame(history_data['rates']).T.plot(kind="line", figsize=(13,5))
    location = r"C:\Users\balap\Desktop\teaching\pydot27\botbackend\history.png"
    plt.savefig(location)

    ## how to send the image..
    chat.send_photo(location)

if __name__ == "__main__":
    bot.run()