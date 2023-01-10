# Diary

[ИНСТРУКЦИЯ НА РУССКОМ][ru]

URL: [diary-fusm.onrender.com][diary]

This project is a school diary web service. 

>You can always clone the project and run the server locally, we will leave the instructions bellow


The site has three sections
- Admin
- Teacher
- Student

All of them work together as a team. 

1) First you need to log in to admin account and connect to your school (both of them can be created only from our dev side, so if you have to use existing ones)
2) After that you can create groups, teachers, students and many more
3) The UI is simple so we hope you will get used to it
4) To create student and teacher accounts you need a secret key which you can download from the Export pages of the Admin panel


## Logins and passwords

We highly recommend to try the project on your machine, because when everyone tries to use one account, nothing good happens 

### Schools:

| Name | City   |
|------|--------|
| 1534 | Moscow |
| 1234 | Omsk   |
| 1111 | Kiev   |

### Admins: 
| Login          | Password  |
|----------------|-----------|
| 1534@admin.com | Admin1534 |
| 1234@admin.com | Admin1234 |

### Teachers:
| Login                                      | Password        |
|--------------------------------------------|-----------------|
| surname_from_teachers_list@teacher1534.com | Teacher12345678 |

> Babenko, Gusev, Antonova, Shumilov, Kuntina, Leonteva, Malygin, Chernov, Chirikov, Pchelintsev, Sharapova, Marchenkova
> 
> *all in lowercase

###  Students: 
| Login                                   | Password        |
|-----------------------------------------|-----------------|
| any_surname_from_class_list@student.com | Student12345678 |

> Log in to any teacher account and open classbook, chose any surname from the list
>
> *all in lowercase


## Telegram Bot notifications

You can set up telegram notifications and customize them later in account settings

To link the chat to diary complete three easy steps:
1) Log in to your fresh new Diary account in your browser
2) Tap *Message bot*
3) Answer the bots questions

That's it ✅ Now you can reload the web page and select which notifications you want to get (you can always turn them off if you want)

> Bot can ignore your `/start` message, again big thanks to heroku base sub :( To fix it just open [this url][bot] and wait untill it loads (404 is also OK), then try messaging again

## Running localy

- Clone project
- Set up python and its dependancies `pip install -r 'requirements.txt'`
- Add .env (*Warning! For telegram alerts add your bot token, same is for posgresql, the only thing which is available is HASH secret key*)
- Make DB migrations `alembic upgrade head` or [download our base][db]
- Start the server!


## P.S
We hope that you will like this project :) We are still young and ready to get better and better. If you found that something is not working or want to say something you can find feedback form in the footer of every page

>p.s. 2: a bit of money for coffee is also appreciated ✨

[diary]:<https://diary-fusm.onrender.com>
[bot]:<https://diary-telegram.herokuapp.com>
[ru]:<README_RU.md>
[db]:<https://disk.yandex.ru/d/3tiUdF4uz4Xgtw>
