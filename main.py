from telegram.ext import Updater, MessageHandler, Filters, ConversationHandler
from telegram.ext import CallbackContext, CommandHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
import markovify
from user_statistic import Stat
from predict import pred
import numpy
import sys

markup1 = ReplyKeyboardMarkup([['/predict']], one_time_keyboard=True)

reply_keyboard = [['Мужчина', 'Женщина']]
markup3 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

reply_keyboard = [['да', 'нет']]
markup6 = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

user_data = Stat('SeasUp', 0, 0, 0, 0, 0, 0)


def send_anek(update, _):
    for i in range(3):
        with open("anek.txt", encoding='utf-8') as f:
            text = f.read()
        text_model = markovify.Text(text)
        a = text_model.make_sentence()
        if a:
            update.message.reply_text(a)


def send_welcome(update, _):

    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    print('User:', first_name)
    update.message.reply_text('Добро пожаловать! Этот бот создан для диагностики развития сердечнососудистых заболеваний '
                              'в ближайшие 10 лет\nИспользуйте для помощи:\n/help')
    return 1


def send_help(update, _):
    update.message.reply_text('Список команд:\n/help: помощь\n/predict: начать диагностику', reply_markup=markup1)


def prediction(update, _):
    update.message.reply_text('Для того, чтобы начать диагностику, следует сначала получить анализы '
                              'крови на количесво холестерина и сахара в крови')
    update.message.reply_text('Итак, приступим!\nДля начала введите ваш возраст:')
    return 2


def get_user_age(update, context):
    age = update.message.text
    if age.isdigit():
        context.user_data['age'] = int(age)
    else:
        context.user_data['age'] = 0

    global user_data
    try:
        user_data.get_age(context.user_data['age'])
    except:
        pass
    update.message.reply_text('Теперь введите ваш пол:', reply_markup=markup3)
    return 3


def get_user_sex(update, context):
    sex = update.message.text
    if sex == 'Женщина':
        context.user_data['sex'] = 0
    else:
        context.user_data['sex'] = 1

    global user_data
    try:
        user_data.get_sex(context.user_data['sex'])
    except:
        pass
    update.message.reply_text('Отлично! Если вы курите, то введите количество сигарет, которые вы '
                              'выкуриваете за день(0, если не курите)')
    return 4


def get_user_cigs(update, context):
    cigs = update.message.text
    if cigs.isdigit():
        context.user_data['cigs'] = int(cigs)
    else:
        context.user_data['cigs'] = 0

    global user_data
    try:
        user_data.get_cigs(context.user_data['cigs'])
    except:
        pass
    update.message.reply_text('Введите общий уровень холестерина в крови')
    return 5


def get_user_chol(update, context):
    chol = update.message.text.replace(',', '.')
    if chol.isdigit():
        context.user_data['chol'] = float(chol)
    else:
        context.user_data['chol'] = 5

    global user_data
    try:
        user_data.get_chol(context.user_data['chol'])
    except:
        pass
    update.message.reply_text('Принимаете ли вы в данный момент препараты, которые влияют на ваше '
                              'кровяное давление?', reply_markup=markup6)
    return 6


def get_user_bp(update, context):
    text = update.message.text
    if text == 'да':
        context.user_data['bp'] = 1
    else:
        context.user_data['bp'] = 0

    global user_data
    try:
        user_data.get_bp(int(context.user_data['bp']))
    except:
        pass
    update.message.reply_text('Введите общий уровень глюкозы в крови')
    return 7


def get_user_glucose(update, context):
    glucose = update.message.text.replace(',', '.')
    if glucose.isdigit():
        context.user_data['glucose'] = float(glucose)
    else:
        context.user_data['glucose'] = 5

    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    print(context.user_data)

    global user_data
    try:
        user_data.get_glucose(context.user_data['glucose'])
    except:
        pass
    update.message.reply_text('Отлично, все почти готово!')
    # print(chat_id, ':', *user_data.send_back())
    print(chat_id, '-', first_name, ':', user_data.predict_result()[0])
    # update.message.reply_text(user_data.predict_result()[0])
    if user_data.predict_result()[0] == 0:
        update.message.reply_text('С большой вероятностью риск развития ишемической болезни сердца '
                                  'у вас отсутствует')
    if user_data.predict_result()[0] == 1:
        update.message.reply_text('Предварительный анализ показывает что у вас есть риск развития '
                                  'ишемической болезни сердца')
    update.message.reply_text('Для уточнения результатов обязательно проконсультируйтесь со специалистом')
    return ConversationHandler.END


def stop(update, _):
    update.message.reply_text('Диагностика остановлена.', reply_keyboard=ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    updater = Updater('1003593379:AAEXv1sd57DbWDh0m7u-eQQSz3MYaddCVzE', use_context=True)

    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('predict', prediction)],

        states={
            1: [MessageHandler(Filters.text, prediction, pass_user_data=True)],
            2: [MessageHandler(Filters.text, get_user_age, pass_user_data=True)],
            3: [MessageHandler(Filters.text, get_user_sex, pass_user_data=True)],
            4: [MessageHandler(Filters.text, get_user_cigs, pass_user_data=True)],
            5: [MessageHandler(Filters.text, get_user_chol, pass_user_data=True)],
            6: [MessageHandler(Filters.text, get_user_bp, pass_user_data=True)],
            7: [MessageHandler(Filters.text, get_user_glucose, pass_user_data=True)]
        },

        fallbacks=[CommandHandler('stop', stop)]
    )

    dp.add_handler(CommandHandler('start', send_welcome))
    dp.add_handler(CommandHandler('help', send_help))
    dp.add_handler(CommandHandler('anek', send_anek))
    dp.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
