import random
import csv
#from hashlib import sha256
colors = ['blue', 'red', 'green', 'purple', 'white',
          'black', 'yellow', 'orange', 'indigo', 'gold', 'silver']
mention = '<@!711586603105124364>'
games = ['pubg', 'fortnite', 'GTA 4', 'minecraft', 'rust']
consoles = ['xbox one', 'xbox 360', 'ps4', 'ps2', 'playstation']
platforms = ['console', 'PC', 'phone']
ps = ['idk', 'not sure', 'ps4', 'ps3', 'some form of playstaion']
activitys = ['reading', 'homework', 'gaming', 'not much', 'nothing']
like_or_not = ['not really', 'kinda', 'a bit', 'yeah!! do you?']


def format_out(res, message):
    res = res.replace("<@USER>", message.author.mention)
    #res.replace(":D", )
    res = res.replace("<RAND_GAME>", random.choice(games))
    res = res.replace("<RAND_GAME_PLATFORM>", random.choice(platforms))
    res = res.replace("<RAND_CONSOLE>", random.choice(consoles))
    res = res.replace("<RANDOM_PS>", random.choice(ps))
    if "<USER_FAV_COLOR>" in res:
        ucolor = random.choice(colors)
        with open('colours.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',',
                                 quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in readCSV:
                if row[0] == message.author.name:
                    print("found user ", message.author.name,
                          "'s fav colour (", row[1], ")")
                    ucolor = row[1]
        res = res.replace("<USER_FAV_COLOR>", ucolor)
    res = res.replace("<USER_NAME>", message.author.name)
    res = res.replace("<SHRUG>", '¯\_(ツ)_/¯')
    res = res.replace("<RAND_LIKE_OR_NOT>", random.choice(like_or_not))
    if "<RANDOM_ACTIVITY>" in res:
        rand_activity = random.choice(activitys)
        if "and <RANDOM_ACTIVITY>" in res:
            if rand_activity == 'nothing':
                res = res.replace("and <RANDOM_ACTIVITY>", "")
        res = res.replace("<RANDOM_ACTIVITY>", rand_activity)
    res = res.replace("<SAD>", "😢")
    return res
