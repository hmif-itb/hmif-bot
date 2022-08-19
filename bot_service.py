from bot import HMIFLineBotApi
import datetime
from flask import current_app
from gcal_service import GcalService
from linebot.models import TextSendMessage
from replies import reply_help, reply_help_deadline, reply_help_seminar, reply_help_ujian
from utils import (
    text_contains,
    get_source_id,
    count_days_to_end_of_semester,
)


class BotService:
    @classmethod
    def init_bot(cls, bot_config):
        cls.__hmif_bot = HMIFLineBotApi(bot_config)

    def __init__(self, event, message: str):
        '''
        event: Line Bot event from webhook
        '''
        if self.__hmif_bot is None:
            raise ValueError('the bot is not initialized')

        self.__event = event
        self.__message = message

    # public methods (ORDER ALPHABETICALLY)
    def reply(self):
        if self.__message.startswith('help hmif bot'):
            return self.__send_help()

        if text_contains(self.__message, ['ada', 'apa', 'aja'], series=True, max_len=75):
            return self.__send_gcal_event()

        if self.__message == '/uid':
            source_id = get_source_id(self.__event)
            try:
                self.__hmif_bot.reply_message(self.__event.reply_token, TextSendMessage(source_id))
            except Exception:
                current_app.logger.error('reply - message: /uid', exc_info=True)
            return

    # private helper methods (ORDER ALPHABETICALLY)
    def __send_help(self):
        if self.__message == 'help hmif bot deadline':
            response = TextSendMessage(text=reply_help_deadline)
        elif self.__message == 'help hmif bot seminar' or self.__message == 'help hmif bot sidang':
            response = TextSendMessage(text=reply_help_seminar)
        elif self.__message == 'help hmif bot ujian':
            response = TextSendMessage(text=reply_help_ujian)
        else:
            # defaults to 'help hmif bot'
            response = TextSendMessage(text=reply_help)

        try:
            current_app.logger.info('__send_help - message : %s - response : %s', self.__message,
                                    response)
            self.__hmif_bot.reply_message(self.__event.reply_token, response)
        except Exception:
            current_app.logger.error('__send_help - message : %s', self.__message, exc_info=True)

    def __send_gcal_event(self):
        today = datetime.date.today()
        title = ""
        start_date = None
        days = None

        if text_contains(self.__message, ['bulan', 'ini'], series=True):
            title = "Timeline HMIF - Bulan Ini"
            start_date = today
            days = 30
        elif text_contains(self.__message, ['minggu', 'ini'], series=True):
            title = "Timeline HMIF - Minggu Ini"
            start_date = today
            days = 7
        elif text_contains(self.__message, ['minggu', 'depan'], series=True):
            title = "Timeline HMIF - Minggu Depan"
            start_date = today + \
                datetime.timedelta(days=(7 - today.weekday() - 1))
            days = 7
        elif text_contains(self.__message, ['hari', 'ini'], series=True):
            title = "Timeline HMIF - Hari Ini"
            start_date = today
            days = 0
        elif text_contains(self.__message, ['besok'], series=True):
            title = "Timeline HMIF - Besok"
            start_date = today + datetime.timedelta(days=1)
            days = 0
        elif text_contains(self.__message, ['sejauh', 'ini'], series=True):
            title = "Timeline HMIF - Deadline Sejauh Ini"
            start_date = today
            days = count_days_to_end_of_semester(today)

        source_id = get_source_id(self.__event)
        events = GcalService.get_events(self.__message, source_id, start_date=start_date, days=days)

        try:
            current_app.logger.info('__send_gcal_event - message : %s - events count : %s',
                                    self.__message, len(events))
            self.__hmif_bot.send_events(self.__event, title, events)
        except Exception:
            current_app.logger.error('__send_gcal_event - message %s', self.__message,
                                     exc_info=True)
            self.__hmif_bot.reply_message(self.__event.reply_token,
                                          TextSendMessage(text='Gagal mendapatkan jadwal'))
