import logging
import stripe
from telegram import Update, LabeledPrice, ReplyKeyboardMarkup,ShippingOption
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, PreCheckoutQueryHandler


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

async def pre_checkout_query(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    await context.bot.answer_pre_checkout_query(query.id, ok=True)

async def successful_payment(update: Update, context: CallbackContext) -> None:
    payment = update.message.successful_payment
    await update.message.reply_text('感谢您的付款！')

def main() -> None:
    # 创建 Application 对象
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # 添加处理器
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('pay', request_invoice))
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, request_invoice))
    application.add_handler(PreCheckoutQueryHandler(pre_checkout_query))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    # 启动机器人
    application.run_polling()

if __name__ == '__main__':
    main()
