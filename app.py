from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Resend API Key from .env
RESEND_API_KEY = os.getenv("RESEND_API_KEY")

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        customer_email = data.get('email')
        customer_name = data.get('customer_name')
        order_id = data.get('order_id')
        order_date = data.get('order_date')
        expiry_date = data.get('expiry_date')
        total_amount = data.get('total_amount')

        if not all([customer_email, customer_name, order_id, order_date, expiry_date, total_amount]):
            return jsonify({"error": "Missing required fields"}), 400

        # Email Content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #333;">
            <h2 style="color: #4CAF50;">Order Confirmation</h2>
            <p>Dear <strong>{customer_name}</strong>,</p>
            <p>Thank you for shopping with <strong>Pot It Up</strong>! Your order has been successfully placed.</p>

            <h3>Order Details:</h3>
            <table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">
                <tr style="background-color: #f2f2f2;">
                    <th style="padding: 10px; border: 1px solid #ddd;">Order ID</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Order Date</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Expiry Date</th>
                    <th style="padding: 10px; border: 1px solid #ddd;">Total Amount</th>
                </tr>
                <tr>
                    <td style="padding: 10px; border: 1px solid #ddd;">{order_id}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{order_date}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">{expiry_date}</td>
                    <td style="padding: 10px; border: 1px solid #ddd;">₹{total_amount}</td>
                </tr>
            </table>

            <p><strong>Note:</strong> This order is non-refundable and non-exchangeable.</p>
            <p>For any queries, contact us at <a href="mailto:potitupspprt@gmail.com">potitupspprt@gmail.com</a>.</p>

            <p>Best Regards,<br>
            <strong>Pot It Up Team</strong></p>
        </body>
        </html>
        """

        # Resend API Request
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        email_data = {
            "from": "onboarding@resend.dev",  # Must be a verified sender in Resend
            "to": [customer_email],
            "subject": f"Order Confirmation - {order_id}",
            "html": html_content
        }
        
        response = requests.post(url, json=email_data, headers=headers)

        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Email sent successfully"})
        else:
            return jsonify({"status": "error", "message": response.text}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)