from flask import Flask, request, jsonify
import stripe

app = Flask(__name__)

STRIPE_SECRET_KEY = 'sk_test_51PsKOHJcBlvi9WwwJqNK5L9GWvXfVDHw0IrBmx7FVB9FzOJ36PXZ8G90wnN3p3tujdyuQxMQ1XmNM1qZCoVBLSBQ00aGHysn6o'
stripe.api_key = STRIPE_SECRET_KEY

@app.route('/webhook', methods=['POST'])
def stripe_webhook():
    print('111111')
    # payload = request.get_data(as_text=True)
    # sig_header = request.headers.get('Stripe-Signature')
    # event = None

    # try:
    #     event = stripe.Webhook.construct_event(
    #         payload, sig_header, 'whsec_CLr5y05tT85p3riiMsk6DypsDnBhqRXk'
    #     )
    # except ValueError as e:
    #     return jsonify({'error': str(e)}), 400
    # except stripe.error.SignatureVerificationError as e:
    #     return jsonify({'error': str(e)}), 400

    # if event['type'] == 'invoice.payment_succeeded':
    #     print('Payment succeeded:', event['data']['object'])
    # elif event['type'] == 'invoice.payment_failed':
    #     print('Payment failed:', event['data']['object'])

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5678,ssl_context=('/www/tg_pay_test/fullchain.pem','/www/tg_pay_test/privkey.key'))
    # app.run(host="0.0.0.0",port=3000)
