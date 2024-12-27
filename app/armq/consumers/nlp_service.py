import asyncio
import json
from uuid import UUID

import aio_pika
from aiogram import Bot

from app.tg_bot.keyboards.for_exhibit import get_comment_and_photo_kb
from app.tg_bot.keyboards.strings import negative_comment_answer, positive_comment_answer, neutral_comment_answer
from app.config_reader import config
from app.database.connection import session
from app.database.cruds import DatabaseCRUDS
from app.logs.logs import logging
from app.services.bert_service import BertClassifier


class NLPConsumer:
    def __init__(self):
        self.comment_classifier = BertClassifier(config.NLP_MODEL_PATH, config.TOKENIZER_DIR_NAME)
        TOKEN = config.BOT_TOKEN.get_secret_value()
        self.bot = Bot(token=TOKEN)
        asyncio.run(self.run())

    async def run(self):
        logging.info(f'ARMQ_URL: {config.ARMQ_URL}')
        self.connection = await aio_pika.connect_robust(
            config.ARMQ_URL
        )
        # Creating channel
        self.channel = await self.connection.channel()

        # Declaring queue
        queue = await self.channel.declare_queue(
            config.NLP_QUEUE_NAME, auto_delete=False
        )
        await queue.consume(self.comment_classify_task)

        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await self.connection.close()

    async def comment_classify_task(
            self,
            message: aio_pika.abc.AbstractIncomingMessage,
    ) -> None:
        async with message.process(ignore_processed=True):
            async with session() as db:
                crud_methods = DatabaseCRUDS(db)
                message_body_json: dict = json.loads(message.body)
                try:
                    model_res = self.comment_classifier.get_sentiment_onnx(message_body_json['message'])
                except Exception as err:
                    logging.error(err)
                    await self.bot.send_message(message_body_json['tg_id'],
                                                'Произошла ошибка определения тональности комментария')
                    return

                comment_id = UUID(message_body_json['comment_id'])
                await crud_methods.update_comment_sentiment(comment_id, model_res)
                if model_res == 0:
                    await self.bot.send_message(message_body_json['tg_id'],
                                                negative_comment_answer,
                                                reply_markup=get_comment_and_photo_kb(message_body_json['exhibit_id']))
                elif model_res == 1:
                    await self.bot.send_message(message_body_json['tg_id'],
                                                neutral_comment_answer,
                                                reply_markup=get_comment_and_photo_kb(message_body_json['exhibit_id']))
                else:
                    await self.bot.send_message(message_body_json['tg_id'],
                                                positive_comment_answer,
                                                reply_markup=get_comment_and_photo_kb(message_body_json['exhibit_id']))


def start_consumers():
    logging.info(f'ARMQ_URL: {config.ARMQ_URL}')
    NLPConsumer()
