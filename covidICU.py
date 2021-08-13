import discord
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import random



TOKEN = 'YOUR TOKEN HERE'
KEY = 'YOUR API KEY HERE'


client = discord.Client()

command = '!COVID:'


@client.event

async def on_ready():
    await client.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = "scanning COVID data sources..."))

@client.event
async def on_message(message):
    if message.content.startswith(command):
        state = message.content.replace(command, '')


        try:
            url = 'https://api.covidactnow.org/v2/state/{}.timeseries.json?apiKey={}'.format(state, KEY)
            response = requests.get(url).json()
            data = pd.DataFrame(response['metricsTimeseries'])
            colors = ['blue', 'red', 'green', 'black', 'magenta', 'orange', 'firebrick']
            fig, ax = plt.subplots()
            ax.plot(data['date'], data['icuCapacityRatio'], color = random.choice(colors))
            fmt_qtr_year = mdates.MonthLocator(interval=3)
            ax.xaxis.set_major_locator(fmt_qtr_year)
            ax.set_xlabel('Date')
            ax.set_ylabel('ICU Capacity Ratio')
            ax.set_title('ICU Capacity by Date in {}'.format(state))

            plt.savefig('covid.png')
            file = discord.File("covid.png", filename = "covid.png")

            await message.channel.send("covid.png", file = file)
            await message.channel.send(embed = discord.Embed(title = "Data Source:", description = "Covid Act Now (https://covidactnow.org/data-api)"))
        except KeyError:
            await message.channel.send(embed = discord.Embed(title = "Error!", description =
            "Please try again using the two letter state code.", color = 0xdc2f02))





client.run(TOKEN)
