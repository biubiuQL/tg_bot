import re
import logging
import stripe
from telegram import Update, LabeledPrice, ReplyKeyboardMarkup, ShippingOption, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, PreCheckoutQueryHandler, InlineQueryHandler


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
            InlineQueryResultArticle(
            id="3",  # 唯一ID
            title="点击生成发票",
            input_message_content=InputTextMessageContent('请点击生成支付发票。')
            )
            # 返回图片结果
            # InlineQueryResultPhoto(
            #     id='1',
            #     photo_url='https://space.yygogogo.com//storage/product/20240911/9a/bac2338f5fec5260c58a703ac5766126baf02d.png',  # 你的图片 URL
            #     thumbnail_url='https://space.yygogogo.com//storage/product/20240911/9a/bac2338f5fec5260c58a703ac5766126baf02d.png',  # 缩略图 URL
            #     title='示例图片',
            #     description='这是一个图片的例子',
            #     caption='这是图片的说明'
            # )
        )
    await context.bot.answer_inline_query(update.inline_query.id, results)


async def custom_message_handler(update: Update, context: CallbackContext) -> None:
    print("hao hao")
    message_text = update.message.text
    # 定义正则表达式模式
    pattern = '生成订单成功'
    # 使用正则表达式匹配消息内容
    if re.search(pattern, message_text):
        await request_invoice(update, context)


# 处理消息并应用正则表达式过滤器
async def handle_message(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    print(1111111)
    # 检查消息是否符合正则表达式
    if regex_filter(message_text, r'生成支付发票'):
        await request_invoice(update, context)

# 自定义的正则表达式过滤器
def regex_filter(pattern):
    return lambda message: re.search(pattern, message.text) is not None

def main() -> None:
    # 创建 Application 对象
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # 添加处理器
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('pay', request_invoice))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, request_invoice))
    # application.add_handler(MessageHandler(filters.TEXT, custom_message_handler))

    # 处理所有文本消息，并在消息处理函数中应用正则表达式过滤器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.add_handler(PreCheckoutQueryHandler(pre_checkout_query))
    application.add_handler(MessageHandler(
        filters.SUCCESSFUL_PAYMENT, successful_payment))

    application.add_handler(InlineQueryHandler(inline_query))

    # 启动机器人
    application.run_polling()


if __name__ == '__main__':
    main()
