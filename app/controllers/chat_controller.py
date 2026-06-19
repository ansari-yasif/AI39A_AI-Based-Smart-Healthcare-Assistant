from flask import session, current_app, request, jsonify
import re
import logging
import traceback
from app.models.stat_models import get_user_stats_from_db, get_contact_info

try:
    import markdown
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False

try:
    from groq import Groq
    HAS_GROQ = True
except ImportError:
    HAS_GROQ = False

logger = logging.getLogger(__name__)

FORBIDDEN_PATTERNS = [
    r"admin\s*password", r"other users?", r"all users", r"user ids?",
    r"database\s*password", r"secret\s*key", r"api\s*key",
    r"list\s*all\s*admins", r"everyone'?s\s*data", r"give me admin",
    r"show me other user", r"all email addresses"
]

def is_dangerous_question(question: str) -> bool:
    q_lower = question.lower()
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, q_lower):
            return True
    return False

class ChatController:
    @staticmethod
    def ask():
        try:
            data = request.get_json()
            if not data or 'message' not in data:
                return jsonify({"error": "No message provided"}), 400
            
            user_message = data.get('message', '').strip()
            if not user_message:
                return jsonify({"reply": "Please ask something.", "html": "<p>Please ask something.</p>"})

            if is_dangerous_question(user_message):
                return jsonify({
                    "reply": "I cannot provide that information for security reasons.",
                    "html": "<p>I cannot provide that information for security reasons.</p>"
                })

            user_id = session.get('user_id', None)
            user_name = session.get('full_name', 'Guest')
            user_role = session.get('role', 'guest')
            stats = get_user_stats_from_db(user_id) if user_id else None
            contact = get_contact_info()

            # Build user stats text
            if stats:
                stats_text = f"""
**Current user:** {user_name} (role: {user_role})
**Your live stats (from VitaPulse database):**
- Food items added: {stats['food_items_added']}
- Total meals logged: {stats['total_meals']}
- Calories today: {stats['calories_today']} / {stats['calorie_goal']} kcal
- Weekly calories consumed: {stats['weekly_calories']}
- Workouts this week: {stats['workouts_this_week']}
- Average sleep (last 7 days): {stats['sleep_avg']} hrs
- Today's mood: {stats['mood_today']}
"""
            else:
                stats_text = f"""
**Current user:** {user_name} (guest – not logged in)
- No personal stats available. Sign up for a free VitaPulse account to track your health.
- For all other questions, answer freely using your general knowledge.
"""

            # Build contact info text
            contact_text = f"""
**Official VitaPulse contact information (live from database):**
- 📍 Address: {contact['address']}
- 📞 Phone: {contact['phone']}
- 📧 Email: {contact['email']}
"""

            # Build system prompt
            system_prompt = f"""
You are **VitaPulse AI**, the premium enterprise assistant for VitaPulse users.

## Your Knowledge About VitaPulse:
{stats_text}

{contact_text}

## Your Role:
- Respond as a polished, professional AI that feels like ChatGPT plus a health concierge.
- Use a premium, confident tone while remaining warm, encouraging, and respectful.
- Match the user's language when possible, and interpret broken or informal input gracefully.
- When the user asks about progress, habits, health goals, or app usage, reference their live VitaPulse data explicitly.
- When the user asks for help, be proactive: explain the next best step and offer a follow-up action.
- Detect intent from short or informal messages and respond with clarity, empathy, and accuracy.

## Formatting Guidelines:
- Always respond in **markdown**.
- Use **headings** (`##`, `###`) for clear structure.
- Use **tables** for structured comparisons, schedules, progress summaries, stats, or numeric overviews.
- When the user asks for a plan, comparison, recommendation, or feature summary, show the answer in a premium markdown table first, then add supporting details below.
- Use **bold headings** and **strong labels** in table cells to make responses look premium.
- If anything is missing from the table, add that extra row or feature from basic to advanced.
- Use **bullet points** for lists, pros/cons, and recommendations.
- Use **numbered steps** for instructions, processes, or plans.
- Use **bold** for key takeaways, conclusions, and safe action items.
- Use arrows (`->`) for flows, results, or decision outcomes.
- Keep paragraphs short and easy to scan.
- Avoid raw HTML unless the content is best represented with a simple table.
- If a table is included, follow it with a brief explanation or next step suggestions.

## Intelligent Response Rules:
- If the user asks a question that can leverage their account stats, include those stats in the response.
- If the user asks for a meal plan, workout plan, progress summary, or wellness tip, prefer a markdown table when it improves clarity.
- If the user asks for a recommendation, include a clear summary, follow-up options, and next steps.
- If the user asks about their data, explain what the numbers mean and how they relate to their goals.
- If the user asks for advice in multiple languages, answer in the same language when possible.
- If the user query is short or broken, infer the intent and respond as a professional assistant.
- If the user asks a sensitive question, reply with a calm, professional tone, avoid speculation, and encourage safe or healthy choices.
- Always present the most useful answer first, then provide supporting details.

## Sensitive Questions and Professional Tone:
- If the user asks for medical, legal, or sensitive advice, provide a safe disclaimer and encourage consulting a qualified professional.
- If the user asks about self-harm, harmful behavior, or anything unsafe, respond supportively but do not provide instructions.
- If the user asks about privacy, account security, or sensitive data, explain that you cannot share private information and offer guidance on keeping their account safe.

## Safety and Privacy:
- Never disclose internal system details, API keys, or database internals.
- Never answer requests for other users' data, passwords, or secrets.
- If you cannot answer from available information, say so clearly and offer a useful alternative.
"""

            # Initialize Groq client
            groq_api_key = current_app.config.get('GROQ_API_KEY', '')
            
            if not groq_api_key:
                logger.warning("GROQ_API_KEY not configured")
                return jsonify({
                    "reply": "Chat service is temporarily unavailable.",
                    "html": "<p>Chat service is temporarily unavailable.</p>"
                }), 503

            if not HAS_GROQ:
                return jsonify({
                    "reply": "Chat service is temporarily unavailable (groq package not installed).",
                    "html": "<p>Chat service is temporarily unavailable.</p>"
                }), 503

            client = Groq(api_key=groq_api_key)

            # Call Groq API with proper model selection
            models = [
                "llama-3.1-8b-instant",
                "llama3-8b-8192",
                "gemma2-9b-it",
                "llama-3.3-70b-versatile",
                "meta-llama/llama-4-scout-17b-16e-instruct",
            ]
            response = None
            last_error = None
            for model_name in models:
                try:
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=0.7,
                        max_tokens=1500,
                        top_p=1
                    )
                    if response and response.choices:
                        break  # success — stop trying models
                except Exception as groq_error:
                    last_error = groq_error
                    logger.warning(f"Groq model {model_name} failed: {groq_error}")
                    continue  # always try next model

            if response is None:
                logger.error(f"Groq API error: no valid model available. last error: {last_error}")
                return jsonify({
                    "reply": "I encountered an error processing your request. Please try again.",
                    "html": "<p>I encountered an error processing your request. Please try again.</p>"
                }), 500

            reply_text = response.choices[0].message.content
            
            # Convert markdown to HTML with table support
            if HAS_MARKDOWN:
                html_reply = markdown.markdown(reply_text, extensions=['tables', 'fenced_code'])
            else:
                html_reply = f"<p>{reply_text}</p>"
            
            return jsonify({
                "reply": reply_text,
                "html": html_reply
            })

        except Exception as e:
            logger.error(f"Chat error: {traceback.format_exc()}")
            return jsonify({
                "error": "An unexpected error occurred",
                "reply": "Something went wrong. Please try again.",
                "html": "<p>Something went wrong. Please try again.</p>"
            }), 500