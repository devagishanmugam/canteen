from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import telebot

app = Flask(__name__)
app.secret_key = "canteen_secret_key"  # Required for session storage

# Telegram Bot Setup
BOT_TOKEN = "7606446781:AAFOaf57M9ans99-dG8GrcsTtpG94Ntc7Zk"
USER_ID = 6681334553  # Replace with your actual Telegram ID  
bot = telebot.TeleBot(BOT_TOKEN)

items = [
    {"name": "Tea", "price": 15, "category": "Drinks", "image": "images/tea.jpg"},
    {"name": "Coffee", "price": 20, "category": "Drinks", "image": "images/coffee.jpg"},
    {"name": "Dosa", "price": 50, "category": "Meals", "image": "images/dosa.jpg"},
    {"name": "Idli", "price": 35, "category": "Meals", "image": "images/idli.jpg"},
    {"name": "Pani Puri", "price": 30, "category": "Snacks", "image": "images/panipuri.jpg"},
    {"name": "Sandwich", "price": 50, "category": "Snacks", "image": "images/sandwitch.jpg"},
    {"name": "Veg Rice", "price": 80, "category": "Meals", "image": "images/veg rice.jpg"},
    {"name": "Parato", "price": 40, "category": "Meals", "image": "images/parato.jpg"},
    {"name": "Tattu Vadai Set", "price": 30, "category": "Snacks", "image": "images/tattu vadai set.jpg"},
    {"name": "KitKat", "price": 30, "category": "Snacks", "image": "images/kitkat.jpg"},
    {"name": "Milky Bar", "price": 70, "category": "Snacks", "image": "images/milky bar.jpg"},
    {"name": "Dairy Milk", "price": 90, "category": "Snacks", "image": "images/dairy milk.jpg"},
    {"name": "Mojito", "price": 50, "category": "Drinks", "image": "images/mojito.jpg"},
    {"name": "Rose Milk", "price": 60, "category": "Drinks", "image": "images/rosemilk.jpg"},
    {"name": "Mango Juice", "price": 30, "category": "Drinks", "image": "images/mango juice.jpg"},
    {"name": "Orange Juice", "price": 40, "category": "Drinks", "image": "images/orange juice.jpg"},
    {"name": "Watermelon Juice", "price": 50, "category": "Drinks", "image": "images/watermelon juice.jpg"},
    
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.json
    if 'items' in data and len(data['items']) > 0:
        session['cart'] = data['items']  # Store cart items in session
        return jsonify({"redirect": url_for('confirm_order')}), 200
    return jsonify({"error": "No items in cart"}), 400

@app.route('/confirm_order')
def confirm_order():
    cart = session.get('cart', [])
    return render_template('confirm_order.html', cart=cart)  # Show confirm order page

@app.route('/final_checkout', methods=['POST'])
def final_checkout():
    data = request.json
    cart = session.get('cart', [])
    
    if not cart or not all(k in data for k in ['name', 'class', 'phone']):
        return jsonify({"error": "Missing details"}), 400
    
    # Prepare Telegram message
    message = f"\n\U0001F6D2 *New Order Checkout* \U0001F6D2\n\n"
    total_price = 0

    for item in cart:
        message += f"\U0001F37D *{item['name']}* - ₹{item['price']}\n"
        total_price += item['price']

    message += f"\n💰 *Total Amount: ₹{total_price}*\n"
    message += f"\n👤 *Customer Info:*\n📛 Name: {data['name']}\n📚 Class: {data['class']}\n📞 Phone: {data['phone']}"

    # Send order to Telegram
    bot.send_message(USER_ID, message, parse_mode="Markdown")

    # Clear cart after order confirmation
    session.pop('cart', None)
    return jsonify({"message": "Order placed successfully!"}), 200

@app.route('/getitems', methods=['GET'])
def get_items():
    return jsonify(items), 200

if __name__ == '__main__':
    app.run(debug=True)
