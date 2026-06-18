<<<<<<< HEAD
<<<<<<< HEAD
=======
"""app/routes/chat_routes.py — AI Health Assistant chat endpoint"""
>>>>>>> 81bc593f977b6d351097a86ace2710ed19f359e1
=======
"""app/routes/chat_routes.py — AI Health Assistant chat endpoint"""
>>>>>>> Saksham-Shrestha
from flask import Blueprint
from app.controllers.chat_controller import ChatController

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

<<<<<<< HEAD
<<<<<<< HEAD
# ✅ No login_required – guests can use the chatbot
@chat_bp.route('/ask', methods=['POST'])
def ask():
    return ChatController.ask()
=======
# No login_required — guests can use the chatbot (controller handles personalization)
@chat_bp.route('/ask', methods=['POST'])
def ask():
    return ChatController.ask()
>>>>>>> 81bc593f977b6d351097a86ace2710ed19f359e1
=======
# No login_required — guests can use the chatbot (controller handles personalization)
@chat_bp.route('/ask', methods=['POST'])
def ask():
    return ChatController.ask()
>>>>>>> Saksham-Shrestha
