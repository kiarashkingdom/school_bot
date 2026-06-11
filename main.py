import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from Texts import texts,commands
from DML import insert_into_admin,insert_into_daily_queue,insert_into_files,insert_into_teachers
from DQL import  get_teachers,get_admin, get_file_by_id
import os
import jdatetime
import logging
from config import *

log_filename = f'bot_{jdatetime.date.today().strftime("%Y_%m_%d")}.log'
logging.basicConfig(level=logging.INFO, filename=log_filename , format="%(asctime)s - %(levelname)s- %(message)s ", encoding='utf-8')
logging.critical('Bot started successfully ✅')

telebot.apihelper.API_URL = 'https://tapi.bale.ai/bot{0}/{1}' #وصل کردن به بله
telebot.apihelper.FILE_URL= 'https://tapi.bale.ai/file/bot{0}/{1}'

os.makedirs('Data', exist_ok=True) #ساخت فولدر دیتا
database={} #{cid:[name,...]}
user_steps_sign_up={}  #{cid: 'step' }
user_steps_log_in={}  #{cid: 'step' }
user_steps={}

bot = telebot.TeleBot(API_TOKEN)

hideboard = ReplyKeyboardRemove()

def listener(messages):   
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: {m.text}")
        elif m.content_type == 'photo':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: New photo recieved")
        elif m.content_type == 'document':
            print(f"{m.chat.first_name} [{str(m.chat.id)}]: New document recieved")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    if data.startswith('week_'):
        week_offset = int(data.split('_')[1])
        user_steps[f'week_{cid}'] = week_offset
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(texts[ 'saturday'], callback_data='day_1'), InlineKeyboardButton(texts[ 'sunday'], callback_data='day_2'),InlineKeyboardButton(texts[ 'monday'], callback_data='day_3'))
        markup.add(InlineKeyboardButton(texts[ 'tuesday'], callback_data='day_4'), InlineKeyboardButton(texts[ 'wednesday'], callback_data='day_5'),InlineKeyboardButton(texts[ 'thursday'], callback_data='day_6'))
        markup.add(InlineKeyboardButton(texts[ 'friday'], callback_data='day_7'))
        bot.edit_message_text(texts['📅 Select day:'], cid, mid, reply_markup=markup)
    elif data.startswith('day_'):
        day_num = data.split('_')[1]
        days = {'1': 'شنبه', '2': 'یکشنبه', '3': 'دوشنبه', '4': 'سه‌شنبه', '5': 'چهارشنبه', '6': 'پنجشنبه', '7': 'جمعه'}
        day_name = days[day_num]
        user_steps[f'day_{cid}'] = day_name
        bot.answer_callback_query(call_id, f'روز {day_name} انتخاب شد')
        
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton('زنگ 1', callback_data='period_1'),
            InlineKeyboardButton('زنگ 2', callback_data='period_2'),
            InlineKeyboardButton('زنگ 3', callback_data='period_3'),
            InlineKeyboardButton('زنگ 4', callback_data='period_4')
        )
        bot.edit_message_text(f'📅 روز {day_name}\n⏰ حالا زنگ را انتخاب کن:', cid, mid, reply_markup=markup)
    
    elif data.startswith('period_'):
        period_num = data.split('_')[1]
        day_name = user_steps[f'day_{cid}']
        week_offset = user_steps[f'week_{cid}']
        miladi_date = persian_weekday_to_miladi(day_name, week_offset)
        folder_name = miladi_date.strftime("%Y-%m-%d")
        folder_path = os.path.join('Data', folder_name)
        bot.answer_callback_query(call_id, f'زنگ {period_num} انتخاب شد')
        bot.edit_message_text(f' زنگ {period_num} انتخاب شد', cid, mid)
        if os.path.exists(folder_path):
            all_items = os.listdir(folder_path)
            files = []
            for item in all_items:
                full_path = os.path.join(folder_path, item)
                if os.path.isfile(full_path):
                    files.append(item)
            for filename in files:
                file_path = os.path.join(folder_path, filename)
                fid = int(filename.split('.')[0])
                file_info = get_file_by_id(fid)
                caption = f"📄 {file_info['file_name']}\n🏫 {file_info['class_name']}"
                with open(file_path, 'rb') as f:
                    bot.send_document(cid, f, caption=caption)
            user_steps.pop(f'day_{cid}', None)
            user_steps.pop(f'week_{cid}', None)
        else:
            bot.send_message(cid,texts['file_not_found'])

    


# start Handler
@bot.message_handler(commands=['start'])
def send_welcome(message):
    cid = message.chat.id
    first_name = message.chat.first_name
    logging.critical(f'User {first_name} (CID: {cid}) started the bot')
    bot.send_message(cid, f'سلام {first_name} عزیز به ربات علامه حلی 8 خوش آمدید❤')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(texts['sign up'], texts['log in'])
    keyboard.add('/help')
    bot.send_message(cid, texts[ 'choose log in if you have account, and sign up for creating a new account ⚠️'], reply_markup=keyboard, reply_to_message_id=message.message_id)

#help Handler
@bot.message_handler(commands=['help'])
def command_help_handler(message):
    cid = message.chat.id
    text = "**📚 راهنمای ربات علامه حلی 8**\n"
    for command, desc in commands.items():
        text += f'✅ /{command} : {desc}\n'
    bot.send_message(cid, text)

#handler support
@bot.message_handler(commands=['support'])
def command_support_handler(message):
    cid = message.chat.id
    bot.send_message(cid, 'اگه رمز خود را فراموش کردین به این آیدی پیام بدین: @kiarashkingdom')

#add_admin
@bot.message_handler(commands=['insert_into_admin'])
def get_admin_info(message):
    cid= message.chat.id
    bot.send_message(cid, texts['send_admin_info'])
    user_steps[cid] = 'admin' 
@bot.message_handler(func= lambda message: user_steps.get(message.chat.id) == 'admin')
def add_admin(message):
    try:
        cid=message.chat.id
        lines = message.text.strip().split('\n')
        CID = lines[0].split(':')[-1].strip()
        name = lines[1].split(':')[-1].strip()
        lastname = lines[2].split(':')[-1].strip()
        phone = lines[3].split(':')[-1].strip()
        username=lines[4].split(':')[-1].strip()
        password=lines[5].split(':')[-1].strip()
        insert_into_admin(CID,name,lastname,phone,username,password)
        logging.info(f'New admin added: {name} {lastname} (CID: {CID})')
        bot.send_message(cid, f"✅ ادمین {name} {lastname} با موفقیت اضافه شد!")
    except Exception as e:
        logging.error(f"Error adding admin: {str(e)}")
        bot.send_message(cid, f"❌ خطا در اضافه کردن ادمین\nلطفا فرمت اطلاعات را چک کنید.")
    
    finally:
        user_steps.pop(cid, None)


#sign up Handler
@bot.message_handler(func=lambda message: message.text == texts['sign up'])
def sign_up_handler(message):
    cid = message.chat.id
    if get_teachers(cid) is None and get_admin(cid) is None:
        bot.send_message(cid, texts['enter your name: '], reply_markup=hideboard)
        user_steps_sign_up[cid] = 'name'
    else:
        bot.send_message(cid, texts['you signed up before ❌'])

@bot.message_handler(func= lambda message: user_steps_sign_up.get(message.chat.id) == 'name')
def step_name_handler(message):
    cid = message.chat.id
    first_name = message.text.strip()
    database.setdefault(cid,list())
    database[cid].append(first_name)
    bot.send_message(cid, texts['enter your last name: '])
    user_steps_sign_up[cid] = "last_name"

@bot.message_handler(func= lambda message: user_steps_sign_up.get(message.chat.id) == 'last_name')
def step_last_name_handler(message):
    cid = message.chat.id
    last_name = message.text.strip()
    database[cid].append(last_name)
    bot.send_message(cid, texts['enter your password: '])
    user_steps_sign_up[cid] = "password"

@bot.message_handler(func= lambda message: user_steps_sign_up.get(message.chat.id) == 'password')
def step_password_handler(message):
    cid = message.chat.id
    password = message.text.strip()
    database[cid].append (password)
    bot.send_message(cid, texts['enter your username: '])
    user_steps_sign_up[cid] = "username"

@bot.message_handler(func= lambda message: user_steps_sign_up.get(message.chat.id) == 'username')
def step_username_handler(message):
    cid = message.chat.id
    username = message.text.strip()
    database[cid].append (username)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('ارسال شماره تلفن', request_contact=True))
    bot.send_message(cid, texts['enter your phone number: '], reply_markup=markup)
    user_steps_sign_up[cid] = "phone_number"

@bot.message_handler(content_types=['contact'] , func= lambda message: user_steps_sign_up.get(message.chat.id) == 'phone_number')
def step_phone_number_handler(message):
    cid = message.chat.id
    contact_info = message.contact
    phone_number = contact_info.phone_number
    user_id = contact_info.user_id
    if user_id == cid:
        database[cid].append (phone_number)
        bot.send_message(cid, texts['sign up completed ✅'], reply_markup=hideboard)
        name = database[cid][0] 
        last_name = database[cid][1]
        password = database[cid][2]
        username=database[cid][3]
        phone = database[cid][4]
        insert_into_teachers(cid, name, last_name, phone, username, password)
        logging.info(f'New user registered: {name} {last_name} (CID: {cid})')
        database.pop(cid, None)
        user_steps_sign_up.pop(cid, None)
    else:
        bot.send_message(cid, texts['please share your correct number'])

#log in Handler
@bot.message_handler(func=lambda message: message.text == texts['log in'])
def log_in_handler(message):
    cid=message.chat.id
    if get_teachers(cid) is not None or get_admin(cid) is not None :
        bot.send_message(cid, texts['enter your username: '], reply_markup=hideboard)
        user_steps_log_in[cid] = 'username'
    else:
        bot.send_message(cid, texts["you don't have acount"], reply_markup=hideboard)

@bot.message_handler(func= lambda message: user_steps_log_in.get(message.chat.id) == 'username')
def log_in_name_handler(message):
    cid = message.chat.id
    username = message.text.strip()
    teacher = get_teachers(cid)
    admin = get_admin(cid)
    if teacher and teacher['username'] == username:
        bot.send_message(cid, texts['enter your password: '])
        user_steps_log_in[cid] = "password"
    elif admin and admin['username'] == username:
        bot.send_message(cid, texts['enter your password: '])
        user_steps_log_in[cid] = "password"
    else:
        bot.send_message(cid, texts['username is not correct'])

@bot.message_handler(func=lambda message: user_steps_log_in.get(message.chat.id) == 'password')
def log_in_password_handler(message):
    cid = message.chat.id
    password = message.text.strip()
    teacher = get_teachers(cid)
    admin = get_admin(cid)
    if teacher and teacher['password'] == password:
        bot.send_message(cid, f"{teacher['name']} {teacher['last_name']} خوش آمدی 🎉")
        logging.info(f'Login successful: {teacher["name"]} {teacher["last_name"]} (CID: {cid}) - Teacher')
        user_steps_log_in.pop(cid, None)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(texts['upload_file'],texts['logout'])
        keyboard.add(texts['profile'])
        bot.send_message(cid, texts[ 'please choose one'], reply_markup=keyboard, reply_to_message_id=message.message_id)
        
    elif admin and admin['password'] == password:
        bot.send_message(cid, f"{admin['name']} {admin['last_name']} (ادمین) خوش آمدی 🎉")
        logging.info(f'Login successful: {admin["name"]} {admin["last_name"]} (CID: {cid}) - Admin')
        user_steps_log_in.pop(cid, None)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(texts['schedule'],texts['logout'])
        keyboard.add(texts['profile'])
        bot.send_message(cid, texts[ 'please choose one'], reply_markup=keyboard, reply_to_message_id=message.message_id)
    else:
        bot.send_message(cid, texts['password is not correct'])

# handler profile
@bot.message_handler(func=lambda message: message.text == texts['profile'])
def command_profile_handler(message):
    cid = message.chat.id
    admin = get_admin(cid)
    teacher = get_teachers(cid)
    if admin is not None:
        text = '👤 **پروفایل شما**\n\n'
        text += f'نام: {admin["name"]}\n'
        text += f'فامیلی: {admin["last_name"]}\n'
        text += f'نام کاربری: {admin["username"]}\n'
        text += f'شماره تماس: {admin["phone"]}'
        bot.send_message(cid, text)
    elif teacher is not None:
        text = '👤 **پروفایل شما**\n\n'
        text += f'نام: {teacher["name"]}\n'
        text += f'فامیلی: {teacher["last_name"]}\n'
        text += f'نام کاربری: {teacher["username"]}\n'
        text += f'شماره تماس: {teacher["phone"]}'
        bot.send_message(cid, text)
    else:
        bot.send_message(cid, texts["you don't have acount"])

#schedule Handler 
@bot.message_handler(func=lambda message: message.text == texts['schedule'])
def command_schedule_handler(message):
    cid = message.chat.id
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('این هفته', callback_data='week_0'),InlineKeyboardButton('هفته آینده', callback_data='week_1'))
    bot.send_message(cid, texts['which weekend'], reply_markup=markup)

# Handle log out 
@bot.message_handler(func=lambda message: message.text == texts['logout'])
def logout_handler(message):
    cid = message.chat.id
    user_steps.pop(cid, None)
    user_steps_sign_up.pop(cid, None)
    user_steps_log_in.pop(cid, None)
    logging.info(f'User logged out: {cid}')
    database.pop(cid, None)

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(texts['sign up'], texts['log in'])
    keyboard.add('/help')
    
    bot.send_message(cid, texts['logout_success'], reply_markup=keyboard)

#upload Handler 
@bot.message_handler(func=lambda message: message.text == texts['upload_file'])
def upload_file_start(message):
    cid = message.chat.id
    if get_teachers(cid) is not None:
        bot.send_message(cid, texts['send_file_info'])
        user_steps[cid] = 'AP' 
    else:
        bot.send_message(cid, texts['only_teachers'])

#  photos Handler
@bot.message_handler(content_types= ['photo'])
def photo_get_handler(message):
    cid=message.chat.id
    teacher = get_teachers(cid)
    if message.caption is not None:
        if user_steps.get(cid) == 'AP' and get_teachers(cid) is not None:
            file_info = message.caption.split('\n')
            file_name = file_info[0].split(':')[-1].strip()
            class_name = file_info[1].split(':')[-1].strip()
            display_date = file_info[2].split(':')[-1].strip()
            period = file_info[3].split(':')[-1].strip()
            parts = display_date.split('/')
            y = int(parts[0])
            m = int(parts[1])
            d = int(parts[2])
            miladi_date = jdatetime.date(y, m, d).togregorian()
            fid = insert_into_files(teacher['CID'],file_name , class_name , period , miladi_date)
            logging.info(f'File uploaded: {file_name} by {teacher["name"]} (FID: {fid})')
            insert_into_daily_queue(fid, miladi_date)

            folder_name = miladi_date.strftime("%Y-%m-%d") 
            save_path = os.path.join('Data', folder_name)
            os.makedirs(save_path, exist_ok=True)
            file_id = message.photo[-1].file_id
            file_infoo = bot.get_file(file_id)
            extension = 'jpg' 
            file_path=file_infoo.file_path
            content = bot.download_file(file_path)
            with open(os.path.join(save_path, f"{fid}.{extension}"), 'wb') as f:
                f.write(content)
            bot.send_message(cid,texts['upload_success'])
            user_steps.pop(cid, None)
        else:
            bot.send_message(cid, texts['please_select_command'])
    else:
        bot.send_message(cid,texts['please_send_caption'])

#  Documents Handler
@bot.message_handler(content_types=['document'])
def content_document_handler(message):
    cid=message.chat.id
    teacher = get_teachers(cid)
    if message.caption is not None:
        if user_steps.get(cid) == 'AP' and get_teachers(cid) is not None:
            file_info = message.caption.split('\n')
            file_name = file_info[0].split(':')[-1].strip()
            class_name = file_info[1].split(':')[-1].strip()
            display_date = file_info[2].split(':')[-1].strip()
            period = file_info[3].split(':')[-1].strip()
            parts = display_date.split('/')
            y = int(parts[0])
            m = int(parts[1])
            d = int(parts[2])
            miladi_date = jdatetime.date(y, m, d).togregorian()
            fid = insert_into_files(teacher['CID'],file_name , class_name , period , miladi_date)
            logging.info(f'File uploaded: {file_name} by {teacher["name"]} (FID: {fid})')
            insert_into_daily_queue(fid, miladi_date)

            folder_name = miladi_date.strftime("%Y-%m-%d") 
            save_path = os.path.join('Data', folder_name)
            os.makedirs(save_path, exist_ok=True)
            file_id = message.document.file_id
            file_infoo=bot.get_file(file_id)
            file_path=file_infoo.file_path
            extension = message.document.file_name.split('.')[-1]
            content=bot.download_file(file_path)
            with open(os.path.join(save_path, f"{fid}.{extension}"), 'wb') as f:
                f.write(content)
            bot.send_message(cid,texts['upload_success'])
            user_steps.pop(cid, None)
        else:
            bot.send_message(cid, texts['please_select_command'])
    else:
        bot.send_message(cid,texts['please_send_caption'])

# other messages Handler
@bot.message_handler(func=lambda message: True) # اگه کاربر پیام دیگری وارد کرد اخطار بده بهش
def echo_message(message):
    bot.reply_to(message, texts['please use keyboard buttons'])

def persian_weekday_to_miladi(weekday_name, week_offset=0):
    today = jdatetime.date.today()
    days_code = {'شنبه': 0, 'یکشنبه': 1, 'دوشنبه': 2, 'سه‌شنبه': 3,  'چهارشنبه': 4, 'پنجشنبه': 5, 'جمعه': 6}
    target_code = days_code[weekday_name]
    today_code = today.weekday()
    if today_code >= target_code:
        if week_offset==0:
            diff = target_code - today_code
        elif week_offset==1:
            diff = 7 + (target_code - today_code)
    else:
        if week_offset==0:
            diff = today_code - target_code
        elif week_offset==1:
            diff = 7 + (today_code - target_code)
    target_shamsi = today + jdatetime.timedelta(days=diff)
    return target_shamsi.togregorian()

bot.infinity_polling()

