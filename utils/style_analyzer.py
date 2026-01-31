import os
import re
from pathlib import Path
from collections import Counter

class StyleAnalyzer:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.style_profile = {
            'common_phrases': [],
            'avg_paragraph_length': 0,
            'uses_emojis': False,
            'tone': 'casual',  # casual, formal, mixed
            'formatting_preferences': [],
            'sample_entries': []
        }
    
    def analyze_existing_journals(self):
        """Analyze existing journal entries to learn writing style"""
        journal_files = list(self.vault_path.glob('*.md'))
        
        if not journal_files:
            return self.style_profile
        
        all_text = []
        emoji_count = 0
        
        for file in journal_files[:10]:  # Analyze last 10 entries
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Extract content after "# Logs" section
                    logs_match = re.search(r'# Logs\n(.*)', content, re.DOTALL)
                    if logs_match:
                        journal_text = logs_match.group(1)
                        all_text.append(journal_text)
                        
                        # Count emojis
                        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags
                            "]+", flags=re.UNICODE)
                        emoji_count += len(emoji_pattern.findall(journal_text))
                        
                        # Store sample
                        if len(self.style_profile['sample_entries']) < 3:
                            self.style_profile['sample_entries'].append(journal_text[:500])
            except Exception as e:
                continue
        
        if all_text:
            combined = '\n'.join(all_text)
            
            # Detect emoji usage
            self.style_profile['uses_emojis'] = emoji_count > 5
            
            # Analyze tone (simple heuristic)
            casual_markers = len(re.findall(r'\b(like|yeah|damn|lol|omg|btw)\b', combined, re.IGNORECASE))
            self.style_profile['tone'] = 'casual' if casual_markers > 3 else 'neutral'
            
            # Detect formatting preferences
            if '==' in combined:
                self.style_profile['formatting_preferences'].append('highlight_text')
            if re.search(r'^>', combined, re.MULTILINE):
                self.style_profile['formatting_preferences'].append('blockquotes')
            if re.search(r'^\*\*', combined, re.MULTILINE):
                self.style_profile['formatting_preferences'].append('bold')
        
        return self.style_profile
    
    def get_style_instructions(self):
        """Generate instructions for LLM based on analyzed style"""
        instructions = []
        
        if self.style_profile['uses_emojis']:
            instructions.append("Use emojis naturally to express emotions (especially 😭, ☺️, 😅)")
        
        if self.style_profile['tone'] == 'casual':
            instructions.append("Write in a very casual, conversational, stream-of-consciousness style")
            instructions.append("Use informal language and internal thoughts")
        
        if 'highlight_text' in self.style_profile['formatting_preferences']:
            instructions.append("Use ==highlighted text== for important phrases or dialogue")
        
        if 'blockquotes' in self.style_profile['formatting_preferences']:
            instructions.append("Use blockquotes (>) for nested thoughts or context")
        
        instructions.append("Write detailed narrative storytelling with self-aware commentary")
        instructions.append("Include specific details, internal feelings, and moment-by-moment descriptions")
        
        return '\n'.join(instructions)
