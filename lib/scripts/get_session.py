import json
import os
import sys


def logger(x):
    return print(x, flush=True)


data = json.loads(sys.argv[1])

if data["username"] == "" or data["username"] is None:
    logger("Please enter a valid username.")
    exit()
if data["following_now"] is None:
    data["following_now"] = 0
if data["followers_now"] is None:
    data["followers_now"] = 0


if type(data["following_now"]) == str:
    data["following_now"] = int(data["following_now"])
if type(data["followers_now"]) == str:
    data["followers_now"] = int(data["followers_now"])


try:
    import pandas as pd
except ImportError:
    logger(
        "[ERROR] If you want to use telegram_reports, please type in console: 'pip3 install gramaddict[telegram-reports]'"
    )

sessionPath = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "accounts", data["username"]
)


class GenerateReports:
    def run(self, username, followers_now, following_now):
        self.followers_now = followers_now
        self.following_now = following_now
        self.time_left = None
        self.username = username

        def telegram_bot_sendtext(text):
            return logger(text)

        if username is None:
            logger("[ERROR] You have to specify an username for getting reports!")
            return None
        file = os.path.join(sessionPath, "sessions.json")
        if not os.path.exists(file):
            logger(
                "[ERROR] You have to run the bot at least once to generate a report!"
            )
            return None

        with open(file) as json_data:
            activity = json.load(json_data)

        aggActivity = []
        for session in activity:
            try:
                start = session["start_time"]
                finish = session["finish_time"]
                followed = session.get("total_followed", 0)
                unfollowed = session.get("total_unfollowed", 0)
                likes = session.get("total_likes", 0)
                watched = session.get("total_watched", 0)
                comments = session.get("total_comments", 0)
                pm_sent = session.get("total_pm", 0)
                followers = int(session.get("profile", 0).get("followers", 0))
                following = int(session.get("profile", 0).get("following", 0))
                aggActivity.append(
                    [
                        start,
                        finish,
                        likes,
                        watched,
                        followed,
                        unfollowed,
                        comments,
                        pm_sent,
                        followers,
                        following,
                    ]
                )
            except TypeError:
                continue

        df = pd.DataFrame(
            aggActivity,
            columns=[
                "start",
                "finish",
                "likes",
                "watched",
                "followed",
                "unfollowed",
                "comments",
                "pm_sent",
                "followers",
                "following",
            ],
        )
        df["date"] = df.loc[:, "start"].str[:10]
        df["duration"] = pd.to_datetime(df["finish"], errors="coerce") - pd.to_datetime(
            df["start"], errors="coerce"
        )
        df["duration"] = df["duration"].dt.total_seconds() / 60

        dailySummary = df.groupby(by="date").agg(
            {
                "likes": "sum",
                "watched": "sum",
                "followed": "sum",
                "unfollowed": "sum",
                "comments": "sum",
                "pm_sent": "sum",
                "followers": "max",
                "following": "max",
                "duration": "sum",
            }
        )
        if len(dailySummary.index) > 1:
            dailySummary["followers_gained"] = dailySummary["followers"].astype(
                int
            ) - dailySummary["followers"].astype(int).shift(1)
        else:
            dailySummary["followers_gained"] = dailySummary["followers"].astype(int)
        dailySummary.dropna(inplace=True)
        dailySummary["followers_gained"] = dailySummary["followers_gained"].astype(int)
        dailySummary["duration"] = dailySummary["duration"].astype(int)

        followers_before = int(df["followers"].iloc[-1])
        following_before = int(df["following"].iloc[-1])
        statString = {
            "Overview Followers": f"{followers_now} ({followers_now - followers_before:+})",
            "Overview Following": f"{following_now} ({following_now - following_before:+})",
            "Last Session Activity Botting": f'{str(df["duration"].iloc[-1].astype(int))}',
            "Last Session Activity Likes": f"{str(df['likes'].iloc[-1])}",
            "Last Session Activity Follows": f"{str(df['followed'].iloc[-1])}",
            "Last Session Activity Unfollows": f"{str(df['unfollowed'].iloc[-1])} ",
            "Last Session Activity Stories Watched": f"{str(df['watched'].iloc[-1])}",
            "Today Session Activity Botting": f"{str(dailySummary['duration'].iloc[-1])}",
            "Today Session Activity Likes": f"{str(dailySummary['likes'].iloc[-1])}",
            "Today Session Activity Follows": f"{str(dailySummary['followed'].iloc[-1])}",
            "Today Session Activity Unfollows": f"{str(dailySummary['unfollowed'].iloc[-1])}",
            "Today Session Activity Stories Watched": f"{str(dailySummary['watched'].iloc[-1])}",
            "Trends New Followers Today": f"{str(dailySummary['followers_gained'].iloc[-1])}",
            "Trends New Followers Past 3 days": f"{str(dailySummary['followers_gained'].tail(3).sum())}",
            "Trends New Followers Past week": f"{str(dailySummary['followers_gained'].tail(7).sum())}",
            "Weekly Average Followers per day": f"{str(round(dailySummary['followers_gained'].tail(7).mean(), 1))}",
            "Weekly Average Likes": f"{str(int(dailySummary['likes'].tail(7).mean()))}",
            "Weekly Average Follows": f"{str(int(dailySummary['followed'].tail(7).mean()))}",
            "Weekly Average Unfollows": f"{str(int(dailySummary['unfollowed'].tail(7).mean()))}",
            "Weekly Average Stories Watched": f"{str(int(dailySummary['watched'].tail(7).mean()))}",
            "Weekly Average Botting": f"{str(int(dailySummary['duration'].tail(7).mean()))}",
        }
        try:
            r = telegram_bot_sendtext(json.dumps(statString))
        except Exception as e:
            logger(f"[ERROR] Failed to flush data from telegram config : {e}")


generatedReports = GenerateReports()
generatedReports.run(
    username=data["username"],
    followers_now=data["followers_now"],
    following_now=data["following_now"],
)
