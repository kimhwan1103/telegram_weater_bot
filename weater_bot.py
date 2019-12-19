from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import requests
from bs4 import BeautifulSoup

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

print("토큰 설정...")
TOKEN = '1033104962:AAG68iE_1RTp_9EXX5P8C0D-XlFA698abtA'
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

def echo(update, context):
    user_says= " ".join(context.args)
    update.message.reply_text(user_says)

def start(update, context):
    context.bot.send_message(chat_id = update.effective_chat.id, text = "안녕하세요 %s님 저는 날씨및 미세먼지를 알려줘는 챗봇이에요!\n기본 명령어를 알고 싶으시면 '/help'를 입력하세요!!") % update.message.chat.first_name

def temp(update, context):
    user_says= " ".join(context.args)
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="+user_says+"+날씨+&oquery=날씨"
    html = get_url(url)
    soup = BeautifulSoup(html, "html.parser")
    water_str = get_water(soup)
    for text in water_str:
        update.message.reply_text(user_says+"의 날씨는"+text+"도")

def dust(update, context):
    user_says= " ".join(context.args)
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query="+user_says+"미세먼지+&oquery=날씨"
    html = get_url(url)
    soup = BeautifulSoup(html, "html.parser")
    water_str = get_dust(soup)
    for text in water_str:
        update.message.reply_text(user_says+"의 미세먼지"+text+"㎍/m³")



def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warn('Update "%s" caused error "%s"'%(update, error))

def main():
    print("실행중")
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start",start))

    dp.add_handler(CommandHandler("temp", temp))

    dp.add_handler(CommandHandler("dust", dust))

    dp.add_handler(CommandHandler("echo", echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
