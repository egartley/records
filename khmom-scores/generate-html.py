from datetime import datetime
import csv
import math


class Song:
    def __init__(self, songtype, title, series, beginner, standard, proud):
        self.songtype = songtype
        self.title = title
        self.series = series
        self.beginner = beginner
        self.standard = standard
        self.proud = proud

def get_series_nav_html():
    content = ""
    lastseries = ""
    i = 0
    for song in song_list:
        if not song.series == lastseries:
            lastseries = song.series
            content += "<a href=\"#qn-s" + str(i) + "\">" + song.series.replace("Bra?", "Bra&#9733;") + "</a><br>\n"
            i += 1
    return content

last_series = ""
series_index = 0
song_list = []
datestring = datetime.today().strftime("%B %e, %Y at %I:%M %p")
if "at 0" in datestring:
    datestring = datestring.replace("at 0", "at ")
pageheader = "---\npermalink: /records/khmom-scores/\nlayout: wnesenior\ntitle: Kingdom Hearts Melody of Memory Scores\nbase_url: /records/\nlast_updated: "
pageheader += datestring + "\n---\n\n"
signaturehtml = "<!-- Generated by https://github.com/egartley/records !-->\n"
signaturehtml += "<link href=\"/resources/css/khmom-scores-style.css\" rel=\"stylesheet\" type=\"text/css\">\n"
signaturehtml += "<p>These are my current scores in the game <i>Kingdom Hearts Melody of Memory</i> for PlayStation. Each song "
signaturehtml += "has the score listed for the three difficulties along with the stage type next to the title. For the most part, the "
signaturehtml += "awkward capitialization and formatting of the titles has been perserved from the game.</p>\n"
listinghtml = "<div class=\"songcard-container flex col\">\n"

# build list from csv
with open("khmom-scores.csv", mode="r") as tfblcsv:   
  file = csv.reader(tfblcsv)
  firstline = True
  for gl in file:
      if firstline:
          firstline = False
          continue
      song = Song(str(gl[3]), str(gl[2]), str(gl[0]), int(gl[4]), int(gl[5]), int(gl[6]))
      song_list.append(song)

# build navigate by series html
oldlh = listinghtml
prepend = "<h2 style=\"display:inline\">Navigate by Series</h2><p id=\"navseries\">" + get_series_nav_html() + "\n"
listinghtml = prepend + oldlh

# build listing html
for song in song_list:
    start = "<div class=\"songcard flex col\">"
    if not last_series == song.series:
        last_series = song.series
        start += "<span class=\"qn-link\" id=\"qn-s" + str(series_index) + "\"></span>"
        series_index += 1
    content = "<span class=\"songcard-title flex\">" + song.title
    if not song.songtype == "Field":
        content += "<span class=\"songcard-" + song.songtype.lower() + "\">" + song.songtype + "</span>"
    content += "</span><span class=\"songcard-series\">" + song.series + "</span><div class=\"songcard-scores flex\">"
    content += "<span class=\"songcard-beginner\">" + str(song.beginner) + "</span><span class=\"songcard-standard\">" + str(song.standard) + "</span>"
    content += "<span class=\"songcard-proud\">" + str(song.proud) + "</span>"
    content += "</div>"
    end = "</div>\n"
    listinghtml += start + content + end
listinghtml += "</div>\n"

# output file
with open("khmom-scores.html", mode="w") as outfile:
    outfile.write(pageheader + signaturehtml + listinghtml)

print("Done!")