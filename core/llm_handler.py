import ollama
from datetime import datetime

class LLMHandler:
    def __init__(self, model='llama3.1'):
        self.model = model
        self.conversation_history = []
        self.style_instructions = ""
    
    def set_style_instructions(self, instructions):
        """Set writing style instructions from analyzed journals"""
        self.style_instructions = instructions
    
    def start_conversation(self):
        """Start a new journaling conversation"""
        self.conversation_history = []
        
        # Friendly, varied greetings
        greetings = [
            "Hey! How was your day?",
            "Hi there! What's been going on today?",
            "Hey! Tell me about your day",
            "What's up? How did today go?",
            "Hey! Anything interesting happen today?"
        ]
        
        import random
        greeting = random.choice(greetings)
        
        self.conversation_history.append({
            'role': 'assistant',
            'content': greeting
        })
        
        return greeting
    
    def chat(self, user_message):
        """Continue the conversation"""
        self.conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        
        # Check if user wants to end
        end_phrases = ['that\'s all', 'that is all', 'done', 'finished', 'nothing else', 'bye', 'end']
        if any(phrase in user_message.lower() for phrase in end_phrases):
            response = "Got it! Let me write up your journal entry now."
            self.conversation_history.append({
                'role': 'assistant',
                'content': response
            })
            return response, True  # True means conversation ended
        
        # System prompt for natural conversation
        system_prompt = """You are a friendly journaling companion. Have a natural, casual conversation to help the person journal about their day.

Guidelines:
- Ask follow-up questions naturally based on what they share
- Show genuine interest and empathy
- Don't be formulaic or robotic
- Keep responses brief (1-2 sentences)
- Let the conversation flow naturally
- Don't ask multiple questions at once
- React to what they say before asking more
- Be warm and supportive
- If they mention something interesting, dig deeper
- Don't force structure - just chat naturally"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': system_prompt}
                ] + self.conversation_history
            )
            
            assistant_message = response['message']['content']
            
            self.conversation_history.append({
                'role': 'assistant',
                'content': assistant_message
            })
            
            return assistant_message, False
            
        except Exception as e:
            return f"Sorry, I'm having trouble connecting. Make sure Ollama is running. Error: {str(e)}", False
    
    def generate_journal_entry(self):
        """Generate a journal entry from the conversation"""
        # Extract just the user's messages
        user_messages = [msg['content'] for msg in self.conversation_history if msg['role'] == 'user']
        conversation_content = '\n\n'.join(user_messages)
        
        generation_prompt = f"""Based on this conversation, write a journal entry in the person's authentic voice.

Style Instructions:
{self.style_instructions}

The journal entry should:
- Be written in first person
- Capture the essence and details shared
- Feel like it was written by the person themselves
- Maintain their natural voice and storytelling style
- Include specific moments, feelings, and thoughts mentioned
- Use the same casual, narrative flow they naturally use

Conversation:
{conversation_content}

Write the journal entry now (just the content, no meta-commentary):"""

        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'system', 'content': 'You are a skilled writer who transforms conversations into authentic journal entries.'},
                    {'role': 'user', 'content': generation_prompt}
                ]
            )
            
            return response['message']['content']
            
        except Exception as e:
            # Fallback: just combine user messages
            return conversation_content
