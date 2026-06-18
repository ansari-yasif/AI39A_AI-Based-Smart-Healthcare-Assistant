"""app/routes/chat_routes.py — AI Health Assistant chat endpoint"""
from flask import Blueprint
from app.controllers.chat_controller import ChatController

chat_bp = Blueprint('chat', __name__, url_prefix='/chat')

# No login_required — guests can use the chatbot (controller handles personalization)
@chat_bp.route('/ask', methods=['POST'])
def ask():
    return ChatController.ask()
