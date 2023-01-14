import json
from datetime import datetime, time

import discord
from discord.ext import commands
from discord.ext.tasks import loop

from twitch import get_notifications
from youtube import get_yt_notifications
from keep_alive import keep_alive

bot = commands.Bot(command_prefix="$")


@bot.command()
async def ping(ctx):
    await ctx.send("pong KFC :santa: \n server")


# check twitch streamers online eery 90 seconds
@loop(seconds=180)
async def check_twitch_online_streamers():
    channel = bot.get_channel(951993123079323748)

    if not channel:
      return

    notifications = get_notifications()

    for notification in notifications:
        embed = discord.Embed(title="{}".format(notification["title"]),
                              url="https://www.twitch.tv/{}".format(
                                  notification["user_name"]),
                              color=discord.Color.purple())
        embed.add_field(name="**Game:**",
                        value="{}".format(notification["game_name"]),
                        inline=True)
        embed.add_field(name="**Viewcount:**",
                        value="{}".format(notification["viewer_count"]),
                        inline=True)
        embed.set_image(url="{}".format(notification["thumbnail_url"].replace(
            "{width}", "400").replace("{height}", "225")))
        await channel.send(
            "@everyone Heylo CBtwt ** {} ** is now live! Go show them some love !"
            .format(notification["user_login"]),
            embed=embed)


# check youtube streamer online every 5 minutes
@loop(seconds=300)
async def check_yt_online_streamers():
    channel = bot.get_channel(951993123079323748)

    if not channel:
        return

    now = datetime.utcnow().time()
    time1, time2, time3, time4 = time(22, 0,
                                      0), time(23, 59,
                                               59), time(0, 0,
                                                         1), time(7, 0, 0)
    if ((now >= time1 and now <= time2) or (now >= time3 and now <= time4)):
        ytifications = get_yt_notifications()

        for ytification in ytifications:
            await channel.send(
                "@everyone What's up guys! {} is now live on Youtube! \n https://www.youtube.com/watch?v={}"
                .format(ytification["snippet"]["channelTitle"],
                        ytification["id"]["videoId"]))


with open("config.json") as config_file:
    config = json.load(config_file)

if __name__ == "__main__":
    check_twitch_online_streamers.start()
    # check_yt_online_streamers.start()
    keep_alive()
    bot.run(config["discord_token"])
