from datetime import datetime
from pathlib import Path
import re

class JournalWriter:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.template = self._load_template()
    
    def _load_template(self):
        """Load the journal template"""
        return """---
cssclasses:
  - "{day_name}"
  - cards
  - daily
reading: false
EarlyWakeUp: "False"
productivity: 0
journal: Personal
journal-start-date: {date}
journal-end-date: {date}
journal-section: day
---
#dailyjournal 
# DAILY NOTE
---
### _{formatted_date}_
## Daily Journal
## <font color="#d99694">Essence: </font>

[[<{yesterday_date}> | Yesterday]] | [[<{tomorrow_date}> | Tomorrow ]]

>[!multi-column]
>>[!todo]- Tasks Due Today 
>>```tasks not done 
>>due {date} 
>>hide due date```
>
>>[!danger]- Overdue Tasks
>>```tasks
>>not done 
>>due < {date} 
>>hide due date```
>
>>[!success]- Completed Tasks
>>```tasks
>>done {date}```

![[Calendar View]]

---

#### Habits Checkouts


> [!multi-column]
> 
>>```meta-bind
>>INPUT[progressBar(title(Productivity),minValue(0),maxValue(100)):productivity]
>>```



>>[!important] Other Habits
>>> [!multi-column]
>>>```meta-bind
>>>INPUT[toggle(title(Early Wake Up),offValue(false), onValue(true)):EarlyWakeUp]
>>>```
>>>
>>>```meta-bind
>>>INPUT[toggle(title(Reading),offValue(false), onValue(true)):reading]
>>>```



---
# New Tasks

# Logs
{journal_content}
"""
    
    def create_journal_entry(self, content, date=None):
        """Create a journal entry with the given content"""
        if date is None:
            date = datetime.now()
        
        # Format dates
        date_str = date.strftime('%Y-%m-%d')
        day_name = date.strftime('%A')
        formatted_date = date.strftime('%A, %B %d, %Y')
        
        # Calculate yesterday and tomorrow
        from datetime import timedelta
        yesterday = date - timedelta(days=1)
        tomorrow = date + timedelta(days=1)
        yesterday_str = yesterday.strftime('%Y-%m-%d')
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        
        # Fill in the template
        journal_text = self.template.format(
            day_name=day_name,
            date=date_str,
            formatted_date=formatted_date,
            yesterday_date=yesterday_str,
            tomorrow_date=tomorrow_str,
            journal_content=content
        )
        
        # Create filename in YYYY-MM-DD format
        filename = date.strftime('%Y-%m-%d') + '.md'
        filepath = self.vault_path / filename
        
        # Check if file already exists
        if filepath.exists():
            # Append to existing file under Logs section
            with open(filepath, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Find the Logs section and append
            if '# Logs' in existing_content:
                # Add timestamp for multiple entries
                timestamp = datetime.now().strftime('%H:%M')
                new_entry = f"\n##### Time - {timestamp}\n{content}\n"
                
                updated_content = existing_content.replace(
                    '# Logs\n',
                    f'# Logs\n{new_entry}'
                )
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
            else:
                # Just append at the end
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write(f"\n\n{content}")
        else:
            # Create new file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(journal_text)
        
        return filepath
    
    def get_todays_entry_path(self):
        """Get the path to today's journal entry"""
        today = datetime.now()
        filename = today.strftime('%Y-%m-%d') + '.md'
        return self.vault_path / filename
