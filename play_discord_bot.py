import vk_api
from vk_api.longpoll import VkLongPoll,VkEventType
from vk_api.keyboard  import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import sqlite3
import random
money=0

#конект к вк
mytoken="28346e0451768e4fa2a8607f8f8eda7d7e592e89f468ae9c39fe3fe78953f67a393cccb572529de691df3"
avtorizatia=vk_api.VkApi(token=mytoken)
longpoll=VkLongPoll(avtorizatia)
# БД
db=sqlite3.connect('server.db')
cur=db.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userID BIGINT,
        cash BIGINT
)""")
db.commit()

## начальная клавиатура
keyboard_Nachalo=VkKeyboard(one_time=True)
keyboard_Nachalo.add_button("Играть",color=VkKeyboardColor.POSITIVE)
keyboard_Nachalo.add_line()
keyboard_Nachalo.add_button("Игры от medved075",color=VkKeyboardColor.SECONDARY)
keyboard_Nachalo.add_line()
keyboard_Nachalo.add_openlink_button("YouTube",link="https://www.youtube.com/channel/UCyuR6I9fkBMMvXoCKVaMsNA")

##игра
keyboard_game=VkKeyboard(one_time=True)
keyboard_game.add_button("Клик",color=VkKeyboardColor.POSITIVE)
keyboard_game.add_line()
keyboard_game.add_button("Казино",color=VkKeyboardColor.NEGATIVE)
keyboard_game.add_button("Баланс",color=VkKeyboardColor.SECONDARY)
keyboard_game.add_line()
keyboard_game.add_button("Назад",color=VkKeyboardColor.PRIMARY)
#мои игры
keyboard_myGame=VkKeyboard(one_time=False)
keyboard_myGame.add_button("Fly bird Fly",color=VkKeyboardColor.POSITIVE)
keyboard_myGame.add_line()
keyboard_myGame.add_button("ByGone DEMO VR",color=VkKeyboardColor.SECONDARY)
keyboard_myGame.add_line()
keyboard_myGame.add_button("Stone ball adventure",color=VkKeyboardColor.POSITIVE)
keyboard_myGame.add_line()
keyboard_myGame.add_button("Назад",color=VkKeyboardColor.PRIMARY)

#начальная клава
def write_key_menu(sender,message):
    avtorizatia.method('messages.send',{'user_id':sender,"message": message,"random_id":get_random_id(),"keyboard":keyboard_Nachalo.get_keyboard()})

def write_key_game(sender,message):
    avtorizatia.method('messages.send',{'user_id':sender,"message": message,"random_id":get_random_id(),"keyboard":keyboard_game.get_keyboard()})
def write_key_my_game(sender,message):
    avtorizatia.method('messages.send',{'user_id':sender,"message": message,"random_id":get_random_id(),"keyboard":keyboard_myGame.get_keyboard()})

for event in longpoll.listen():
    if event.type==VkEventType.MESSAGE_NEW and event.to_me and event.text:
       reseived_message = event.text
       sender=event.user_id
       if reseived_message=="Играть":
           cur.execute(f"SELECT userID FROM users WHERE userID='{sender}'")
           if cur.fetchone() is None:
               cur.execute(f"INSERT INTO users VALUES ('{sender}','{0}')")
               db.commit()
               write_key_game(sender, "запись есть")
               write_key_menu(486192476,"Новый пользователь ID:"+sender)
           else:
               write_key_game(sender, "В игре")
               ###
       # мои игры
       elif reseived_message=="Игры от medved075":
            write_key_my_game(sender,"Добро пожаловать в игры разработчика medved075, Какую игру вы хотите выбрать?")
       elif reseived_message=="Fly bird Fly":
           write_key_my_game(sender,"Название: Fly bird Fly"+"\n"+
                             "Описание: Помоги потерявшейся птице не столкнутся со стаей птиц. Это первая игра от medved075"+"\n"+
                             "Ссылки на скачивание:"+"\n"+"AppGallery: https://appgallery.huawei.com/app/C104567695?sharePrepath=ag&locale=ru_RU&source=appshare&subsource=C104567695&shareTo=com.android.bluetooth&shareFrom=appmarket"+"\n"+
                             "GameJolt: https://gamejolt.com/games/fly_bird_fly/634443")
       elif reseived_message=="ByGone DEMO VR":
           write_key_my_game(sender,"Название: ByGone DEMO VR"+"\n"+"Описание: Игра в виртуальной реальности(VR) в жанре horror. Для игры понадобится всего лишь ваш телефон и cardboard. Приятной игры !"+"\n"+
                             "Ссылки на скачивание:"+"\n"+"AppGallry: https://appgallery.huawei.com/app/C104762829?sharePrepath=ag&locale=ru_RU&source=appshare&subsource=C104762829&shareTo=com.android.bluetooth&shareFrom=appmarket"+"\n"+
                             "GameJolt: https://gamejolt.com/games/ByGone/647391")
       elif reseived_message == "Stone ball adventure":
           write_key_my_game(sender,"Название: Stone ball adventure"+"\n"+"Описание: 3D платформер про каменного шара, в игре насчитывается более 50 уровней. В настоящее время игра находится в разработке.")
        ####GAME
       elif reseived_message=="Клик":
           cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
           for i in cur.fetchone():
                pass
           cur.execute(f"UPDATE users SET cash={i+1} WHERE userID='{sender}'")
           db.commit()
           cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
           for i in cur.fetchone():
               pass
           write_key_game(sender, "Вы получили одну монету💰"+"\n"+"Ваш баланс:"+str(i))
       elif reseived_message == "Баланс":
           cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
           for i in cur.fetchone():
               pass
           write_key_game(sender,"Ваш баланс составляет:"+"\n"+str(i)+"💰")
       elif reseived_message=="Назад":
           write_key_menu(sender,"Добро пожаловать в главное меню")
       elif reseived_message=="Казино":
           cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
           for i in cur.fetchone():
               pass
           if i>=50:
               cur.execute(f"UPDATE users SET cash={i - 50} WHERE userID='{sender}'")
               db.commit()
               r=random.randint(1,10)
               if r>=8:
                   cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
                   for i in cur.fetchone():
                       pass
                   cur.execute(f"UPDATE users SET cash={i + 150} WHERE userID='{sender}'")
                   db.commit()
                   cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
                   for i in cur.fetchone():
                       pass
                   write_key_game(sender, "Вы выйграли 150 монет 💰💰💰" + "\n" + "Ваш баланс:" + str(i))
               else:
                   cur.execute(f"SELECT cash FROM users WHERE userID='{sender}'")
                   for i in cur.fetchone():
                       pass
                   write_key_game(sender, "вы проиграли ⛔💰⛔" + "\n" + "Ваш баланс:" + str(i))
           else:
               write_key_game(sender,"у вас нет денег"+"\n"+"нужно 50 монет")

       elif reseived_message=="medved075 bd":
           cur.execute(f"SELECT * FROM users")
           for i in cur.fetchall():
               print(i)
               write_key_menu(486192476,str(i))

       else:
           write_key_menu(sender,"Такой команды нет")
           print(sender)
           for i in cur.execute("SELECT * FROM users "):
               print(i)
