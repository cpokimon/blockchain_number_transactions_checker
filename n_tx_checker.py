from telegram import Bot
from time import sleep
from blockchain import blockexplorer

# Add your wallet address here.
ADDRESS = 'your wallet address'
# Add your telegram bot token here.
API_TOKEN = 'your telegram bot token'
# Add your telegram chat_ or group_id here.
CHAT_ID = 'your chat id'
# Set check interval here (seconds)
# Script will check address every CHECK_INTERVAL seconds.
CHECK_INTERVAL = 600
# Set connection delay
# If server will stopped due to error script restarts in CONNECTION_DELAY seconds.
CONNECTION_DELAY = 60
CURRENCY_NAME = 'BTC'
# Set messages that will used when server start and stop(due to error)
TEXT = {
    'SERVER_START': 'СЕРВЕР ЗАПУЩЕН',
    'CURRENT_STATE': 'ТЕКУЩЕЕ СОСТОЯНИЕ',
    'SERVER_STOP': '!!!!!!ОШИБКА СЕРВЕРА!!!!!! Проверьте доступность Blockchain API. Повторный запуск через {} секунд...'.format(CONNECTION_DELAY),
    'NEW_TRANSACTION': 'НОВАЯ ТРАНЗАКЦИЯ',
}


def get_text(n_tx, final_balance, currency_name):
    return ('Транзакций сейчас: {}. Итоговый баланс: {} {}.'.format(n_tx, final_balance, currency_name))


def get_final_balance(address_data):
    return (address_data.final_balance / 100000000)


def checker(address: str = ADDRESS,
            api_token: str = API_TOKEN,
            chat_id: str = CHAT_ID,
            currency_name: str = CURRENCY_NAME,
            check_interval: int = CHECK_INTERVAL,
            text: dict = TEXT,
            connection_delay: int = CONNECTION_DELAY):

    bot = Bot(token=api_token)
    bot.sendMessage(chat_id=chat_id,
                    text=text['SERVER_START'])
    try:
        address_data = blockexplorer.get_address(address, offset=0)
        previous_n_tx = address_data.n_tx
        final_balance = get_final_balance(address_data=address_data)
        bot.sendMessage(chat_id=chat_id,
                        text=text['CURRENT_STATE'] + ' ' + get_text(n_tx=previous_n_tx,
                                                             final_balance=final_balance,
                                                             currency_name=currency_name))
        while True:
            address_data = blockexplorer.get_address(address, offset=0)
            current_n_tx = address_data.n_tx
            if current_n_tx > previous_n_tx:
                previous_n_tx = current_n_tx
                final_balance = get_final_balance(address_data=address_data)
                bot.sendMessage(chat_id=chat_id, text=text['NEW_TRANSACTION'] + ' ' + get_text(n_tx=current_n_tx,
                                                                                        final_balance=final_balance,
                                                                                        currency_name=currency_name))
            sleep(check_interval)
    finally:
        bot.sendMessage(chat_id=chat_id, text=text['SERVER_STOP'])
        sleep(connection_delay)
        checker()

if __name__ == '__main__':
    checker()
