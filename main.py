import urllib
import json
from urllib import request
import requests as reqs
import webbrowser
from PIL import Image

username = str(input("User: "))

page = reqs.get("https://www.instagram.com/" + username + "/?__a=1")
parsed_json = (json.loads(page.text))

print(parsed_json["graphql"]["user"]["username"])
print(parsed_json["graphql"]["user"]["full_name"])
person = parsed_json["graphql"]["user"]
print(person["biography"])

all_posts = person["edge_owner_to_timeline_media"]["edges"]


willNPage = person["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
cntLoaded = len(all_posts)
end_c = person["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
while willNPage:
    posts = reqs.get("https://instagram.com/graphql/query/?query_id=17888483320059182&id=" + person["id"] + "&first=" + str(cntLoaded) + "&after=" + str(end_c))
    posts = json.loads(posts.text)
    posts = posts["data"]["user"]
    willNPage = posts["edge_owner_to_timeline_media"]["page_info"]["has_next_page"]
    for i in posts["edge_owner_to_timeline_media"]["edges"]:
        all_posts.append(i)
    cntLoaded = len(all_posts)
    end_c = posts["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]

mx_likes = 0
most_liked_post = None
for i in all_posts:
    mx_likes = max(i["node"]["edge_media_preview_like"]["count"], mx_likes)
    if (mx_likes == i["node"]["edge_media_preview_like"]["count"]):
        most_liked_post = i
print ("Most liked photo has " + str(mx_likes) + " likes")

cnt_vid = 0
cnt_photo = 0
for i in all_posts:
    if (i["node"]["is_video"] == True):
        cnt_vid+=1
    else:
        cnt_photo+=1
print("Videos: " + str(cnt_vid))
print("Photos: " + str(cnt_photo))

print(most_liked_post["node"]["display_url"])

image = reqs.get(most_liked_post["node"]["thumbnail_src"])

with open("img.jpg", "wb") as f:
	f.write(image.content)

with open('photo.html','wb') as f:
	message = """
	<html>
	<head></head>
	<body><img src="img.jpg"/></body>
	</html>
	"""
	f.write(message.encode())
	

webbrowser.open_new_tab('photo.html')

urllib.request.urlretrieve('https://scontent-arn2-2.cdninstagram.com/v/t51.2885-15/e35/70520495_611316476064605_3167318308265959634_n.jpg?_nc_ht=scontent-arn2-2.cdninstagram.com&_nc_cat=105&_nc_ohc=F_ET5kcBB6oAX_KUNmm&oh=8f7481482355049ebe9ce31e816b29d7&oe=5E96D5AE', 'C:/Users/Alexey.Admin/Desktop')