from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging, json
from datetime import datetime
from pytz import timezone

from Pancake_NFT import pancake_nft
from Pancake_NFT import nft_web3

from config import params




def timetz(*args):
    return datetime.now(tz).timetuple()
    
tz = timezone("Asia/Shanghai")
logging.Formatter.converter = timetz

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def loadData():
   with open('./Pancake_NFT/rank.json', 'r') as f:
      raw = f.read()
   return json.loads(raw)

def returnDetail(token_id,price):
    raw = loadData()
    image = raw['data'][token_id]['image']['thumbnail']
    rarity = round(float(raw['data'][token_id]['rarity']),3)
    rank = raw['data'][token_id]['rank']
    attributes = ""
    for item in raw['data'][token_id]['attributes']:
        temp = item['traitType'] + ": " + item['value'] + " " + str(round(item['rarity']*100, 2)) + "%\n"
        attributes = attributes + temp
        
    result = "排名：" + str(rank) + "位\n" + \
             "编号：# " + token_id + \
             "只要 " + str(price) + " BNB\n\n" + \
             "属性：\n" + attributes + "\n" + image + "\n" + \
             "购买：\n" + "https://pancakeswap.finance/nfts/collections/0x0a8901b0e25deb55a87524f0cc164e9644020eba/" + token_id
    return result
    
def start(update:Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\! ',
    )
    


def nft_web3_callback(context: CallbackContext):
    print(context.job.context['events_filter'])
    if not context.job.context['events_filter']:
        context.job.context['events_filter'] = nft_web3.initEvent()
        
    res = nft_web3.returnHash(context.job.context['events_filter'])
    if res:
        order = 1
        queue = dict()
        for tx in res:
            temp = nft_web3.returnTransaction(tx)
            
            if temp:
                print(temp)
                print(context.job.context["ranking"].get(temp['tokenId'], None))
                if (temp['price'] <= context.job.context['customPrice'] and context.job.context["ranking"].get(temp['tokenId'], None) != None):
                    reply_msg = returnDetail(temp['tokenId'], temp['price'])
                    context.bot.send_message(chat_id=context.job.context['chat_id'],text = reply_msg)
            
    else:
        logging.info("No Latest Transaction.")
    
def nft_web3_rt(update: Update, context: CallbackContext):
    defaultRank = 5000
    defaultPrice = 6
    context.job = dict()
    jobDict = context.job
    jobDict["chat_id"] = update.message.chat_id
    jobDict['buf'] = dict()

    if len(context.args) == 0:
        customRank = defaultRank
        customPrice = defaultPrice
    elif len(context.args) == 1:
        customRank = defaultRank
        customPrice = context.args[0]
    elif len(context.args) == 2:
        customRank = context.args[0]
        customPrice = context.args[1]

    jobDict["customRank"] = customRank
    jobDict["customPrice"] = float(customPrice)

    reply_text = "监控白痴兔兔主人计划 已启动！\n监控排名：低于{}\n监控价格：低于{} BNB".format(customRank, customPrice)
    context.bot.send_message(chat_id=jobDict["chat_id"],
                             text=reply_text)  
    events_filter = nft_web3.initEvent()
    jobDict['events_filter'] = events_filter
    print(jobDict['events_filter'])
    
    raw_data = loadData()
    targetRanking = dict()
    for id_ in range(params['TOTAL_SUPPLY']):
        if(raw_data['data'][str(id_)]['rank'] < int(customRank)):
            targetRanking[str(id_)] = raw_data['data'][str(id_)]['rank']

    jobDict['ranking'] = targetRanking
    context.job_queue.run_repeating(nft_web3_callback, 10, first=1, context=jobDict)
    
def main(execuateType) -> None:
    if execuateType == "test":
        token = params['TEST_BOT_TOKEN']
    elif execuateType == "prod":
        token = params['PROD_BOT_TOKEN']
        
    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("nft", nft_web3_rt, pass_args=True))
    updater.start_polling()
    updater.idle()
    
    
if __name__ == '__main__':
    main('test')
