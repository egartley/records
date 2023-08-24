from datetime import datetime
import csv
import math


class Game:
    def __init__(self, title, year, platform, rating, hundo, plat, iconid, hours, playthroughs, dlc):
        self.title = title
        self.platform = platform
        self.rating = rating
        self.iconid = iconid
        if len(iconid) < 6:
            self.iconid = ("0" * (6 - len(iconid))) + self.iconid
        self.hundo = hundo
        self.plat = plat
        self.year = year
        self.hours = hours
        self.playthroughs = playthroughs
        self.dlc = dlc

def get_rating_html(rating):
    # convert numeric 5-star rating to html
    start = "<span class=\"gamecard-rating flex\">"
    fullstars = rating // 1
    hashalf = not rating // 1 == rating
    empties = 5 - math.ceil(rating)
    content = "<img src=\"/resources/png/wT9F00t1BuDE9wRx/sf.png\">" * int(fullstars)
    if hashalf:
        content += "<img src=\"/resources/png/wT9F00t1BuDE9wRx/sh.png\">"
    if empties > 0:
        content += "<img src=\"/resources/png/wT9F00t1BuDE9wRx/se.png\">" * int(empties)
    end = "</span>"
    return start + content + end

def get_playtext(game):
    # won't show number of playthroughs if only one
    # 0 = incomplete, -9 = abandoned, and -1 = in-progress
    hourstext = str(game.hours) + " hours"
    playthroughtext = ""
    if game.playthroughs == 0:
        playthroughtext = " (incomplete)"
    elif game.playthroughs == -9:
        playthroughtext = " (abandoned)"
    elif game.playthroughs == -1:
        playthroughtext = " (in-progress)"
    elif game.playthroughs > 1:
        playthroughtext = ", played " + str(game.playthroughs) + " times"
    return hourstext + playthroughtext

def get_listing_html(game):
    start = "<div class=\"gamecard flex card\">\n<div class=\"gamecard-outer flex\">\n<img id=\"i"
    start += game.iconid + "\" alt=\"icon\" src=\"/resources/png/B1cZjrwAuuPI9Cyd/blank.png\">\n"
    start += "<div class=\"gamecard-inner flex\">\n"    
    platform = game.platform
    # change displayed string if nintendo or ios
    if platform in ["DS", "3DS", "Switch", "Wii"]:
        platform = "Nintendo " + platform
    if platform == "iOS":
        platform = "Mobile (iOS)"
    content = "<span class=\"gamecard-subtext\">" + game.year + "</span>\n"
    content += "<span class=\"gamecard-subtext\">" + platform + "</span>\n"
    content += get_rating_html(game.rating) + "\n"
    content += "</div>\n</div>\n"
    content += "<span class=\"gamecard-title\">" + game.title
    if game.dlc:
        content += " <img id=\"dlc\" alt=\"dlc\" src=\"/resources/png/wT9F00t1BuDE9wRx/dlc.png\">"
    if game.hundo:
        content += " <img id=\"100\" alt=\"100\" src=\"/resources/png/wT9F00t1BuDE9wRx/100.png\">"
    if game.plat:
        content += "<img id=\"plat\" alt=\"plat\" src=\"/resources/png/wT9F00t1BuDE9wRx/plat.png\">"
    content += "</span>\n<span class=\"gamecard-playtext\" style=\"font-size:12px\">" + get_playtext(game) + "</span>"
    end = "</div>"
    return start + content + end

def get_icon_css(iconid):
    # gets the css rule for the iconid
    filename = "icons.png"
    if not iconid[1:2] == "0":
        # support icon sheets from 2 to 9
        filename = "icons" + str(int(iconid[1:2]) + 1) + ".png"
    x = int(iconid[4:6])
    x *= -64
    y = int(iconid[2:4])
    y *= -64
    return "img#i" + iconid + "{background:url(/resources/png/wT9F00t1BuDE9wRx/" + filename + ") " + str(x) + "px " + str(y) + "px}"

def calc_stats():
    for game in game_list:
        # rating
        rating_index = 6
        if game.rating == 5:
            rating_index = 0
        elif game.rating == 4.5:
            rating_index = 1
        elif game.rating == 4:
            rating_index = 2
        elif game.rating == 3.5:
            rating_index = 3
        elif game.rating == 3:
            rating_index = 4
        elif game.rating == 2.5:
            rating_index = 5
        stat_ratings[rating_index][1] += 1
        # platform
        platform_index = 6
        if game.platform in ["PlayStation", "PlayStation 4", "PlayStation 5", "PlayStation 4/5"]:
            platform_index = 0
        elif game.platform in ["PlayStation 1", "PlayStation 2"]:
            platform_index = 1
        elif game.platform in ["3DS", "DS", "DSi", "DSiWare"]:
            platform_index = 2
        elif game.platform == "Switch":
            platform_index = 3
        elif game.platform == "Wii":
            platform_index = 4
        elif game.platform == "PC":
            platform_index = 5
        # if none of the above clauses are met, then the "other" category is
        # assumed by platform_index being set to 6 initally
        stat_platforms[platform_index][1] += 1
        # completion
        if game.hundo:
            stat_completion[0][1] += 1
        if game.plat:
            stat_completion[1][1] += 1  

def get_single_stat_html(title, values):
    content = "<div class=\"stat\">\n<span class=\"bold\">" + title + "</span><br>\n"
    for v in values:
        content += v[0] + " (" + str(v[1]) + ")<br>\n"
    # substring on -5 to return without last "<br>\n"
    return content[:-5] + "</div>\n"

def get_stats_html():
    start = "<h2>Statistics</h2>\n<div class=\"stat-container\">\n"
    content = get_single_stat_html("Platforms", stat_platforms)
    content += get_single_stat_html("Ratings", stat_ratings)
    content += get_single_stat_html("Completion", stat_completion)
    end = "</div>\n<p>Total games: " + str(len(game_list)) + "</p>\n"
    return start + content + end


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
datestring = datetime.today().strftime("%B %e, %Y at %I:%M %p")
if "at 0" in datestring:
    # change formatting for times with a single digit hour
    datestring = datestring.replace("at 0", "at ")
pageheader = "---\npermalink: /records/games/\nlayout: greystone\ntitle: Game Records\nlast_updated: "
pageheader += datestring + "\n---\n\n"
signaturehtml = "<!-- Generated by https://github.com/egartley/records !-->\n"
signaturehtml += "<link href=\"/resources/css/rLzoDOi3W5sFgVCX/game-records-icons.css\" rel=\"stylesheet\" type=\"text/css\">\n"
signaturehtml += "<link href=\"/resources/css/rLzoDOi3W5sFgVCX/game-records-style.css\" rel=\"stylesheet\" type=\"text/css\">\n"
signaturehtml += "<script src=\"/resources/js/tktKmZk7PrGIDVqH/game-records.js\" type=\"application/javascript\"></script>\n"
signaturehtml += "<p>This is a record of every game I've played since 2006 or so. Each game has a rating out of 5, "
signaturehtml += "a rough estimate of total play time, and number of playthroughs (if more than one). Games that "
signaturehtml += "have been 100% completed include a tag next to the title, as well as those where I've gotten its platinum "
signaturehtml += "trophy on PSN. A vast majority of games were played on original hardware, but some of the older titles "
signaturehtml += "were emulated on PC.</p>\n"
signaturehtml += "<p>Click on a game to view more details about it. Some will have notes about how good or bad it was, why "
signaturehtml += "they may have been abandoned, and other things like that.</p>\n"
selecthtml = "<label for=\"sortby\">Sort games by:</label>\n<select name=\"sortby\" id=\"sortby\">\n"
selecthtml += "<option selected=\"selected\" value=\"titleAZ\">Title A-Z (Default)</option><option value=\"titleZA\">Title Z-A</option>\n"
selecthtml += "<option value=\"yearUp\">Year (Ascending)</option><option value=\"yearDown\">Year (Descending)</option>\n"
selecthtml += "<option value=\"ratingUp\">Rating (Ascending)</option><option value=\"ratingDown\">Rating (Descending)</option>\n"
selecthtml += "<option value=\"hoursUp\">Hours (Ascending)</option><option value=\"hoursDown\">Hours (Descending)</option></select>\n"
selecthtml += "<label for=\"filter\">Filter:</label><select name=\"filter\" id=\"filter\" style=\"margin-right:12px\">\n"
selecthtml += "<option selected=\"selected\" value=\"none\">None (Default)</option>\n"
selecthtml += "<option value=\"platform\">Platform</option><option value=\"rating\">Rating</option>\n"
selecthtml += "<option value=\"year\">Release Year</option><option value=\"hours\">Hours Played</option>\n"
selecthtml += "<option value=\"playthroughs\">Playthroughs</option><option value=\"hundo\">100% Completion</option>\n"
selecthtml += "<option value=\"plat\">Platinum Trophy</option></select>\n"
selecthtml += "<label class=\"filterby\" style=\"display:none\" for=\"filterby\">THISSHOULDNOTBEVISIBLE</label>\n"
selecthtml += "<select name=\"filterby\" class=\"filterby\" style=\"display:none\">\n"
selecthtml += "<option selected=\"selected\" value=\"itsnotworkingbud\">None (Default)</option>"
listinghtml = "<h2>All Games Played</h2>" + selecthtml + "\n<div class=\"gamecard-container flex\">\n"

game_list = []
iconcss = ""
stat_ratings = [["5 stars", 0], ["4.5 stars", 0], ["4 stars", 0], ["3.5 stars", 0],
                ["3 stars", 0], ["2.5 stars", 0], ["2 stars or below", 0]]
stat_platforms = [["PS4/PS5", 0], ["PS1/PS2", 0], ["3DS/DS/DSi", 0], ["Switch", 0],
                  ["Wii", 0], ["PC", 0], ["Other", 0]]
stat_completion = [["100% Complete", 0], ["Platinum Trophy", 0]]

# build list of game objects from csv
with open("games.csv", mode="r") as gamescsv:   
  file = csv.reader(gamescsv)
  first = True
  for gl in file:
      if first:
          first = False
          continue
      # Title,Company,Year,Platform,Rating,100%,Platinum,Icon ID,Hours Played,Playthroughs,DLC
      game = Game(str(gl[0]), str(gl[2]), str(gl[3]), float(gl[4]), int(gl[5]) == 1,
                  int(gl[6]) == 1, str(gl[7]), int(gl[8]), int(gl[9]), int(gl[10]) == 1)
      game_list.append(game)

# sort alphabetically by game title
game_list = sorted(game_list, key=lambda game: game.title)

# build non-listing html
calc_stats()
statshtml = get_stats_html()

# build listing html
for game in game_list:
    listinghtml += get_listing_html(game)
listinghtml += "</div>\n"
with open("games.html", mode="w") as outfile:
    outfile.write(pageheader + signaturehtml + statshtml + listinghtml)

iconcss = ""
for game in game_list:
    iconcss += get_icon_css(game.iconid)
with open("game-records-icons.css", mode="w") as outfile:
    outfile.write(iconcss)

print("Done!")
