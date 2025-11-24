"""
方面提取服务（严格限制为6个核心方面）
"""
import re

# 严格限制的酒店评论方面（只保留指定的六个）
COMMON_ASPECTS = {
    '房间': ['房间', '客房', '卧室', '床', '床铺', 'room', 'bedroom', '睡眠', '睡觉'],
    '位置': ['位置', '地点', '交通', '地铁', '商圈', 'location', 'position', 'traffic'],
    '价格': ['价格', '费用', '性价比', '贵', '便宜', 'price', 'cost', 'value'],
    '服务': ['服务', '前台', '服务员', '工作人员', '态度', 'service', 'staff', 'reception'],
    '餐饮': ['餐饮', '早餐', '食物', '餐厅', '吃饭', 'food', 'breakfast', 'restaurant', 'dining'],
    '设施': ['设施', '设备', 'WiFi', '网络', '电梯', '空调', '泳池', '健身房', 'facility', 'equipment', 'wifi']
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