import random
import os
import logging
import requests
from bs4 import BeautifulSoup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

print("토큰 설정...")
TOKEN = TOKEN #토큰을 넣어주세요 input token 
print("토큰 설정완료!")

def get_url(url):
    req = requests.get(url)
    req.encoding = 'utf8'
    html = req.text
    return html

def get_water(soup):
    water_str = soup.find('span', {"class":"todaytemp"})
    return water_str

def get_dust(soup):
    dust = soup.find('em', {"class" : "main_figure"})
    return dust


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def start(update, context):
    text = ("안녕하세요 %s님 저는 날씨및 미세먼지를 알려줘는 챗봇이에요!\n기본 명령어를 알고 싶으시면 '/help'를 입력하세요!!") % update.message.chat.first_name
    update.message.reply_text(text)

def help(update, context):
    text = ("'/temp' = 현재 온도를 알려줍니다.\n'/dust' = 미세먼지를 알려줍니다.")
    update.message.reply_text(text)

def query(msg):
    return msg

def response(bot, update): 
    chat_id = update.message.chat_id 
    user = update.message.from_user 
    user_name = "%s%s" %(user.last_name, user.first_name) 
    r_msg = query(update.message.text) 
    bot.sendMessage(chat_id, text=r_msg)

       

def main():
    
    print("실행중...")
    updater = Updater(TOKEN, use_context=True)
    
    
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler([Filters.text], response))
    
    updater.start_polling()
    
    updater.idle()
    

if __name__ == '__main__':
    main()

