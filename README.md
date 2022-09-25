# Diary

URL: [school-diary-service.herokuapp.com][diary]

This project is a school diary web service. 

> Note: it is using SQLite database, which is disk driven. It means that all your changes will are deleted every hour, sorry but thats how Heroku and SQLite work together :(
>
> However, you can always clone the project and run server locally, we will leave the instruction bellow


The site has three sections
- Admin
- Teacher
- Student

All of them work together as a team. 

1) First you need to log in to admin account and connect to school (both of them can be created only from our dev side, so if you have to use existing ones)
2) After that you can create groups, teachers, students and many more
3) UI is simple socwe hope yiu will get used to it
4) To create student and teacher account you need a secret key which you can download at Export pages of Admin panel

## Telegram Bot notifications

You can set up telegram notifications and customize them later in account settings

To link the chat to diary cpmplete three easy steps:
1) Log in to your fresh new Diary account in browser
2) Tap *Message bot*
3) Answer bots questions

That's it ✅ Now you can reload web page and select which notifications you want to get (you can always turn them off if you want)

> Bot can ignore your `/start` message, again big thanks to heroku base sub :( To fix it just open [this url][bot] and wait untill it loads (404 is also OK), then try messaging again

## Running localy

- Clone project
- Set up python and its dependancies `pip install -r 'requirements.txt'`
- Add .env (*Warning! For telegram alerts add your bot token, same is for posgresql, only thing which is available is HASH secret key*)
- Make DB migrations `alembic upgrade head` or [download our base][db_url]
- Start the server!


## P.S
We hope that you will like this project :) We are still young and ready to get better and better. If you found that something is not working or want to say something you can find mail adress in footer on every page

>p.s. 2: a bit money for coffee is also appreciated ✨

[db_url]:<www.ru>
[diary]:<school-diary-service.herokuapp.con>
[bot]:<diary-telegram.herokuapp.com>
