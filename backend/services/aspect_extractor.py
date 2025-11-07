"""
方面提取服务（可选，用于提取常见方面）
"""
import re

# 常见的酒店评论方面
COMMON_ASPECTS = {
    '房间': ['房间', '客房', '卧室', '床', '床铺', 'room', 'bedroom'],
    '服务': ['服务', '前台', '服务员', '工作人员', 'service', 'staff', 'reception'],
    '位置': ['位置', '地点', '交通', 'location', 'position', 'traffic'],
    '价格': ['价格', '费用', '性价比', 'price', 'cost', 'value'],
    '设施': ['设施', '设备', 'WiFi', '网络', 'facility', 'equipment', 'wifi'],
    '餐饮': ['餐饮', '早餐', '食物', '餐厅', 'food', 'breakfast', 'restaurant'],
    '清洁': ['清洁', '卫生', '干净', 'clean', 'cleanliness', 'hygiene'],
    '环境': ['环境', '氛围', '安静', 'environment', 'atmosphere', 'quiet']
}

def extract_aspects_from_text(text):
    """
    从文本中提取可能涉及的方面
    返回: 方面名称列表
    """
    text_lower = text.lower()
    detected_aspects = []
    
    for aspect_name, keywords in COMMON_ASPECTS.items():
        for keyword in keywords:
            if keyword.lower() in text_lower:
                if aspect_name not in detected_aspects:
                    detected_aspects.append(aspect_name)
                break
    
    return detected_aspects

