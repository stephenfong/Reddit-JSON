import json 
import urllib.request 

urllib.request.urlretrieve("https://www.reddit.com/r/hardwareswap/new/.json?limit=100", ".\Reddit Json\hws.json")

#file = open(r"C:\Users\Stephen\Desktop\hws.json", "r") # opens json file
file = open(".\Reddit Json\hws.json", "r")
data_dict = json.load(file) 

in_dict = data_dict['data']['children'][0]['data'] # indexes values in overall dict to get to inner dict

list_keys = ["link_flair_css_class", "title", "selftext", "author_flair_text","author","url","num_comments"]

def unlock(keys, dictionary): #function that finds the value of the corresponding key
    for key in keys:
        print(dictionary[key])

unlock(list_keys,in_dict)




