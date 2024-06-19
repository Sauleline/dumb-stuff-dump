import xmltodict
import urllib3
import tabulate
import webbrowser
import os
import feedparser
from datetime import datetime
import time

def req(url):
    datajson = feedparser.parse(url)
    for j in range(config['items']):
        displayList.append({'item': datajson.entries[j], 'product': {'title': datajson.feed.title}})

feeds = []
displayList = []
http = urllib3.PoolManager()
displayTable = [["Index", "Title\nAuthor", "Release Date"]]
path = r"C:\Program Files\LibreWolf\librewolf.exe"
webbrowser.register('librewolf', None, webbrowser.BackgroundBrowser(path))

configRaw = open("Feeds/config.xml", "r")
config = dict(xmltodict.parse(configRaw.read()))
config = config['config']
config['ignored'] = config['ignored'].split(', ')
for i in range(len(config['ignored'])):
    config['ignored'][i] = config['ignored'][i].upper()
config['items'] = int(config['items'])
config['limit'] = int(config['limit'])
config['size'] = int(config['size'])
configRaw.close()

opml = open("Feeds/feeds.opml", "r")
feedDict = dict(xmltodict.parse(opml.read()))

for i in feedDict['opml']['body']['outline']:
    feeds.append({'url': i['@xmlUrl'], 'type': i['@type'].upper()})
opml.close()

for i in range(len(feeds)):
    if not feeds[i]['type'] in config['ignored']:
        req(feeds[i]['url'])

displayList = sorted(displayList, key=lambda d: d['item'].published_parsed, reverse=True)

for i in range(len(displayList)):
    if i < config['limit']:
        displayTable.append([i, displayList[i]['item']['title'] if 'title' in displayList[i]['item'] else "Image(s)", datetime.fromtimestamp(time.mktime(displayList[i]['item'].published_parsed))])
        displayTable.append(["", displayList[i]['product']['title'], ""])
        displayTable.append(tabulate.SEPARATING_LINE)
os.system('cls')
print(tabulate.tabulate(displayTable, headers="firstrow", maxcolwidths=[None, config['size'], None]))
print("\ntype help for help\n")
cmd = input()
if cmd == "new":
    newTitle = input("New Feed Name:\t")
    newURL = input("New Feed URL:\t")
    newType = input("New Feed Type: \t")
    opml = open("Feeds/feeds.opml", "r")
    arr = opml.readlines()
    opml.close()
    disp = '    <outline title="{}" xmlUrl="{}" type="{}" />\n'.format(newTitle, newURL, newType)
    arr.insert(-2, disp)
    opml = open("Feeds/feeds.opml", "w")
    opml.write("")
    opml.close()
    opml = open("Feeds/feeds.opml", "a")
    opml.writelines(arr)
    opml.close()
elif cmd == "delete":
    opml = open("Feeds/feeds.opml", 'r')
    arr = opml.readlines()
    opml.close()
    temp0 = arr.pop(0)
    temp1 = arr.pop(0)
    temp2 = arr.pop(0)
    temp3 = arr.pop()
    temp4 = arr.pop()
    testarr = []
    delete = input("Deleted Feed Title: \t")
    for i in range(len(arr)):
        testarr.append(arr[i].split('"')[1])
    if delete in testarr:
        arr.pop(testarr.index(delete))
    arr.insert(0, temp2)
    arr.insert(0, temp1)
    arr.insert(0, temp0)
    arr.append(temp4)
    arr.append(temp3)
    opml = open("Feeds/feeds.opml", "w")
    opml.write("")
    opml.close()
    opml = open("Feeds/feeds.opml", "a")
    opml.writelines(arr)
    opml.close()
elif "open" in cmd:
    cmd = cmd.split()
    webbrowser.get('librewolf').open_new(displayList[int(cmd[1])]['item'].link)
elif "download" in cmd:
    cmd = cmd.split()
    webbrowser.get('librewolf').open_new(displayList[int(cmd[1])]['item']['links'][0]['href'])
elif cmd == "exit":
    quit()
elif cmd == "count":
    print("You have {} feeds.".format(len(feeds)))
elif cmd == "list":
    feedlist = []
    print("Your feeds are: ")
    for i in feedDict['opml']['body']['outline']:
        feedlist.append([i['@type'], i['@title']])
    feedlist.append(tabulate.SEPARATING_LINE)
    print(tabulate.tabulate(feedlist, headers=['Type', 'Title']))
elif cmd == "help":
    inputs = [['new', 'Make a new feed'], ['delete', 'Deletes a feed'], ['open', 'Opens an index of an item'], ['download', 'Opens the download link of an item'], ['exit', 'Quits the program'], ['count', 'Shows how many feeds you have'], ['list', 'Shows a list of your feeds']]
    print(tabulate.tabulate(inputs, headers=['command', 'description']))
print("\nRefreshing...")
os.system("rss.py")
