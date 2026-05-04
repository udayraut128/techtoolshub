from flask import Blueprint, render_template, request, current_app
from flask_mail import Message
from app.mail_config import mail

contact_bp = Blueprint('contact', __name__)


# 🔹 Contact Page + Form Handling
@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        user_message = request.form.get('message')

        # ✅ Basic validation
        if not name or not email or not user_message:
            return render_template(
                'contact.html',
                message="⚠️ All fields are required"
            )

        try:
            # ✅ Create email
            msg = Message(
                subject=f"New Contact Message from {name}",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[current_app.config['MAIL_USERNAME']]
            )

            # ✅ Email body
            msg.body = f"""
New Contact Form Submission

Name: {name}
Email: {email}

Message:
{user_message}
"""

            # ✅ Send mail
            mail.send(msg)

            return render_template(
                'contact.html',
                message="✅ Message sent successfully!"
            )

        except Exception as e:
            # 🔥 Print actual error in terminal
            print("MAIL ERROR:", e)

            return render_template(
                'contact.html',
                message="❌ Failed to send message. Check server logs."
            )

    return render_template('contact.html')


# 🧪 TEST ROUTE (IMPORTANT FOR DEBUGGING)
@contact_bp.route('/test-mail')
def test_mail():
    try:
        msg = Message(
            subject="Test Email from TechTools",
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[current_app.config['MAIL_USERNAME']]
        )

        msg.body = "✅ If you received this, mail is working!"

        mail.send(msg)

        return "✅ Test mail sent successfully!"

    except Exception as e:
        return f"❌ Error: {e}"