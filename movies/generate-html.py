from datetime import datetime
import csv
import math


class Movie:
    def __init__(self, title, year, length, rating):
        self.title = title
        self.year = year
        self.length = length
        self.rating = rating


def get_quicknav_html():
    start = "<h2>Quick Navigation</h2>\n<p>\n"
    end = "</p>\n"
    links = "<a class=\"qn-link\" href=\"#qn-num\">#</a>\n"
    for letter in alphabet:
        links += "<a class=\"qn-link\" href=\"#qn-" + letter + "\">" + letter.upper() + "</a>\n"
    return start + links + end

def get_quicknav_anchor(letter):
    return "qn-" + letter

def get_listing_html(movie, qnid):
    start = "<tr"
    if len(qnid) > 0:
        start += " id=\"" + qnid[-4:] + "\">"
    else:
        start += ">"
    content = "<td>" + movie.title + "</td>"
    content += "<td>" + str(movie.year) + "</td>"
    content += "<td>" + movie.rating + "</td>"
    content += "<td>" + movie.length + "</td>"
    end = "</tr>\n"
    return start + content + end


alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
datestring = datetime.today().strftime("%B %e, %Y at %I:%M %p")
if "at 0" in datestring:
    # change formatting for times with a single digit hour
    datestring = datestring.replace("at 0", "at ")
pageheader = "---\npermalink: /records/movies/\nlayout: greystone\ntitle: Movie Records\nlast_updated: "
pageheader += datestring + "\n---\n\n"
signaturehtml = "<!-- Generated by https://github.com/egartley/records !-->\n"
signaturehtml += "<link href=\"/resources/css/rLzoDOi3W5sFgVCX/records-style.css\" rel=\"stylesheet\" type=\"text/css\">\n"
listinghtml = "<h2>All Movies Watched</h2>\n<table>\n<tr><th>Title</th><th>Year</th><th>Rating</th><th>Length</th></tr>\n"

alphabet_index = 0
lastletter = ""
nummode = True
movie_list = []

# build list of movie objects from csv
with open("movies.csv", mode="r") as moviescsv:   
  file = csv.reader(moviescsv)
  first = True
  for gl in file:
      if first:
          first = False
          continue
      # Title,Year,Length,Rating
      movie_list.append(Movie(str(gl[0]), int(gl[1]), str(gl[2]), str(gl[3])))

# sort alphabetically by game title
movie_list = sorted(movie_list, key=lambda movie: movie.title)

# build non-listing html
quicknavhtml = get_quicknav_html()

# build listing html
for movie in movie_list:
    lastletter = movie.title[0:1].upper()
    tempqn = ""
    # check if finished with numbered titles
    if nummode and lastletter.isalpha():
        # finished with numbered titles, output quick link nav for A
        nummode = False
        tempqn += get_quicknav_anchor(alphabet[alphabet_index])
    if not nummode:
        while not alphabet[alphabet_index].upper() == lastletter:
            # output quick nav link for the new letter
            alphabet_index += 1
            tempqn += get_quicknav_anchor(alphabet[alphabet_index])
    # proceed with regular listing html for current movie
    listinghtml += get_listing_html(movie, tempqn)

# add remaining quick nav links
#while alphabet_index < len(alphabet) - 1:
    #alphabet_index += 1
    #listinghtml += get_quicknav_anchor(alphabet[alphabet_index]) + "\n"
listinghtml += "</table>\n"
with open("movies.html", mode="w") as outfile:
    outfile.write(pageheader + signaturehtml + quicknavhtml + listinghtml)

print("Done!")