# Useful bot
## BTL_Python_Nhom9

##### There are no more releases planned.
###### We might work on it sporadically  

#### Tested in python 3, 3.5, 3.6
---
A reddit bot template in python, using praw.  

---------


### To use:
You need to have your own api credentials. If you do not head [here](https://www.reddit.com/prefs/apps "reddit apps") and click create application -> script.  
**Add what is needed to botinfo.example.py then rename it to botinfo.py. If you do not fill all the info in then the script will not work.**  
Currently recommended that you enter the credentials in database via the cli. However it is good to start with the credentials in the botinfo.py because the cli will import them for you   
Fully tested releases are [here](https://github.com/coolaspie/useful_bot/releases "useful bot releases")   

``` 
pip install praw  
git clone https://github.com/thanhchauns2/BTL/Reddit-Bot.git  
```

To run:  
```    
python3 main.py
```
or
```
python3 cli.py
```
If you want to import the credentials for easier use:
```
python3.6 cli.py import
```
**To get any responses to messages, posts or comments you have to use the response add feature in the cli.**  
To get mutliple subreddit use the cli change subreddit and for the new subreddit do "subreddit1+subreddit2+etc"

---
#### Versions

No further versions available.

#### Currently:
* Replies to posts
* Replies to comments
* Reads messages and adds users who request blacklist or  unblacklisting 
* Replies to messages
* Respond to username mentions
* Create additional responses to messages
    * Delete created responses
* Templete for simple features
* CLI manual import with the import arguement
* Ability to have multiple comment/posts trigger words and responses
* Post and Command Responses all in a tables


---

#### Issues:

If you find one please submit it in the issues tab

---
