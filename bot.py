import re
import logging
import stripe
from telegram import Update, LabeledPrice, ReplyKeyboardMarkup, ShippingOption, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InlineKeyboardMarkup, InlineKeyboardButton, InputInvoiceMessageContent
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, PreCheckoutQueryHandler, InlineQueryHandler, CallbackQueryHandler


# 配置 Stripe 密钥
stripe.api_key = 'sk_test_51PsKOHJcBlvi9WwwJqNK5L9GWvXfVDHw0IrBmx7FVB9FzOJ36PXZ8G90wnN3p3tujdyuQxMQ1XmNM1qZCoVBLSBQ00aGHysn6o'

# 配置 Telegram 机器人
TELEGRAM_TOKEN = '7487357401:AAHRuJa0dmMj4Fk4c1wTg2wgu01q5xShV84'

# 配置支付提供者令牌
PAYMENT_PROVIDER_TOKEN = '284685063:TEST:NzBhNjk4ZjIyMjBl'


async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('欢迎使用机器人')


async def request_invoice(update: Update, context: CallbackContext) -> None:
    try:
        chat_id = update.message.chat.id
        # 发送发票
        await context.bot.send_invoice(
            chat_id,
            title='Test Invoice',  # 发票标题
            description='Description of the invoice',  # 发票描述
            payload='unique-invoice-payload',  # 发票负载
            provider_token=PAYMENT_PROVIDER_TOKEN,  # 支付提供者令牌
            currency='USD',  # 货币
            prices=[LabeledPrice(label='Test Product', amount=1000)],  # 商品项
            start_parameter='test-payment',  # 支付参数
            need_name=False,  # 是否需要客户姓名
            need_phone_number=False,  # 是否需要客户电话
            need_email=False,  # 是否需要客户电子邮件
            is_flexible=False,  # 发票是否可以修改
        )

    except Exception as e:
        await update.message.reply_text('创建发票时出现问题，请稍后再试。')

# 预付款查询监听（支付前检查）


async def pre_checkout_query(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    await context.bot.answer_pre_checkout_query(query.id, ok=True)

# 支付成功监听


async def successful_payment(update: Update, context: CallbackContext) -> None:
    payment = update.message.successful_payment
    await update.message.reply_text('感谢您的付款！')


async def inline_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query
    results = []

    if query == '':
        print(1)
        results.append(
            InlineQueryResultArticle(
                id='1',
                title='请输入支付信息',
                input_message_content=InputTextMessageContent('请提供支付相关的信息。'),
                thumbnail_url='https://space.yygogogo.com//storage/product/20240911/9a/bac2338f5fec5260c58a703ac5766126baf02d.png',  # 可选
                description='用于支付的内联查询'

            )
        )
    elif 'payment' in query:
        print(2)
        results.append(
            InlineQueryResultArticle(
                id='2',
                title='支付处理',
                input_message_content=InputTextMessageContent(
                    '处理支付请求: {}'.format(query)),
                thumbnail_url='https://space.yygogogo.com//storage/product/20240911/9a/bac2338f5fec5260c58a703ac5766126baf02d.png',  # 可选
                description='确认您的支付信息'
            )
        )
    else:
        print(3)
        results.append(
            # 返回文章结果
            # InlineQueryResultArticle(
            #     id='3',
            #     title='帮助',
            #     # input_message_content=InputTextMessageContent('请在查询中包含“payment”以处理支付。'),
            #     input_message_content=InputTextMessageContent('生成订单成功'),
            #     thumbnail_url='https://space.yygogogo.com//storage/product/20240911/9a/bac2338f5fec5260c58a703ac5766126baf02d.png',  # 可选
            #     description='帮助信息'
            # ),
            # InlineQueryResultArticle(
            #     id="3",  # 唯一ID
            #     title="点击生成发票",
            #     input_message_content=InputTextMessageContent(
            #         '点击下方按钮以生成支付发票。'),
            #     reply_markup=InlineKeyboardMarkup(
            #         [[InlineKeyboardButton(
            #             text="生成发票", callback_data='generate_invoice')]]
            #     )
            # )
            # 内联支付
            InlineQueryResultArticle(
                id="invoice_1",
                title="生成支付发票",
                thumbnail_url='https://space.yygogogo.com//storage/product/20240911/9a/bac2338f5fec5260c58a703ac5766126baf02d.png',
                # 返回内联发票
                input_message_content=InputInvoiceMessageContent(
                    title="支付商品",
                    description="这是一个测试发票",
                    payload="custom_payload",
                    provider_token=PAYMENT_PROVIDER_TOKEN,
                    currency="USD",
                    prices=[{"label": "商品", "amount": 1000}]  # 金额以最小货币单位表示
                ),
                # reply_markup=InlineKeyboardMarkup(
                #     [[InlineKeyboardButton(
                #         text="生成发票", callback_data='generate_invoice')]]
                # )
            )
        )
    await context.bot.answer_inline_query(update.inline_query.id, results)

# 处理回调按钮点击


async def button_callback(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.from_user.id
    # 发送发票
    if query.data == 'generate_invoice':
        await request_invoice(update, context)
        await query.answer()  # 确认按钮点击

# 处理消息并应用正则表达式过滤器


async def handle_message(update: Update, context: CallbackContext) -> None:
    print(5555555)
    try:
        message_text = update.message.text
        print(message_text)
        # 检查消息是否符合正则表达式
        if regex_filter(message_text, r'生成支付发票'):
            print(6666666)
            await request_invoice(update, context)
    except Exception as e:
        await update.message.reply_text("处理消息时发生错误，请稍后再试。")

# 自定义的正则表达式过滤器


def regex_filter(message_text, pattern):
    return re.search(pattern, message_text) is not None


def main() -> None:
    # 创建 Application 对象
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # 添加处理器
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('pay', request_invoice))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, request_invoice))
    # application.add_handler(MessageHandler(filters.TEXT, custom_message_handler))
    application.add_handler(CallbackQueryHandler(button_callback))
    # 处理所有文本消息，并在消息处理函数中应用正则表达式过滤器
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(PreCheckoutQueryHandler(pre_checkout_query))
    application.add_handler(MessageHandler(
        filters.SUCCESSFUL_PAYMENT, successful_payment))

    application.add_handler(InlineQueryHandler(inline_query))

    # 启动机器人
    application.run_polling()


if __name__ == '__main__':
    main()
