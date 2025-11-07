"""
导出工具
"""
import csv
import pandas as pd
from io import StringIO
from models import Feedback, AspectSentiment

def export_feedbacks_to_csv(feedbacks):
    """
    将反馈列表导出为CSV格式
    返回: CSV字符串
    """
    output = StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow([
        'ID', '用户ID', '文本', '语言', '情感标签', '情感分数', 
        '创建时间', '方面', '方面情感'
    ])
    
    # 写入数据
    for feedback in feedbacks:
        aspects_str = ', '.join([
            f"{a.aspect_name}:{a.sentiment_label}" 
            for a in feedback.aspects
        ])
        
        writer.writerow([
            feedback.id,
            feedback.user_id,
            feedback.text,
            feedback.original_language,
            feedback.sentiment_label,
            feedback.sentiment_score,
            feedback.created_at.isoformat() if feedback.created_at else '',
            aspects_str,
            ''
        ])
    
    return output.getvalue()

def export_feedbacks_to_excel(feedbacks, file_path):
    """
    将反馈列表导出为Excel格式
    """
    data = []
    for feedback in feedbacks:
        aspects_str = ', '.join([
            f"{a.aspect_name}:{a.sentiment_label}" 
            for a in feedback.aspects
        ])
        
        data.append({
            'ID': feedback.id,
            '用户ID': feedback.user_id,
            '文本': feedback.text,
            '语言': feedback.original_language,
            '情感标签': feedback.sentiment_label,
            '情感分数': feedback.sentiment_score,
            '创建时间': feedback.created_at.isoformat() if feedback.created_at else '',
            '方面': aspects_str
        })
    
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False, engine='openpyxl')

