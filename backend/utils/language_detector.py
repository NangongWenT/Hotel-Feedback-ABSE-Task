
import re

def detect_language(text):

    if not text:
        return 'zh'
    
 
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    
   
    chinese_chars = len(chinese_pattern.findall(text))
    total_chars = len(text.replace(' ', '').replace('\n', ''))
 
    if total_chars > 0 and chinese_chars / total_chars > 0.3:
        return 'zh'
    else:
        return 'en'

