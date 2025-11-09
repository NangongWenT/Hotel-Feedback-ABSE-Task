"""
语言检测工具
"""
import re

def detect_language(text):
    """
    检测文本语言
    返回: 'zh' 或 'en'
    """
    if not text:
        return 'zh'
    
    # 中文字符正则
    chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
    
    # 统计中文字符数
    chinese_chars = len(chinese_pattern.findall(text))
    total_chars = len(text.replace(' ', '').replace('\n', ''))
    
    # 如果中文字符占比超过30%，认为是中文
    if total_chars > 0 and chinese_chars / total_chars > 0.3:
        return 'zh'
    else:
        return 'en'

