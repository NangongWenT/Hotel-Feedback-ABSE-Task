"""
文件解析工具
"""
import csv
import pandas as pd
import json
import io
from pathlib import Path

def parse_csv(file_path, text_column=None):
    """
    解析CSV文件
    返回: 文本列表
    """
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        
        # 如果没有指定列，尝试自动检测
        if text_column is None:
            # 常见的文本列名
            possible_columns = ['text', 'comment', 'review', 'feedback', 'content', '评论', '反馈', '内容']
            for col in possible_columns:
                if col in df.columns:
                    text_column = col
                    break
            
            # 如果还没找到，使用第一列
            if text_column is None:
                text_column = df.columns[0]
        
        texts = df[text_column].dropna().astype(str).tolist()
        return texts
        
    except Exception as e:
        raise ValueError(f"CSV解析失败: {str(e)}")

def parse_excel(file_path, text_column=None, sheet_name=0):
    """
    解析Excel文件
    返回: 文本列表
    """
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        
        # 如果没有指定列，尝试自动检测
        if text_column is None:
            possible_columns = ['text', 'comment', 'review', 'feedback', 'content', '评论', '反馈', '内容']
            for col in possible_columns:
                if col in df.columns:
                    text_column = col
                    break
            
            if text_column is None:
                text_column = df.columns[0]
        
        texts = df[text_column].dropna().astype(str).tolist()
        return texts
        
    except Exception as e:
        raise ValueError(f"Excel解析失败: {str(e)}")

def parse_txt(file_path):
    """
    解析TXT文件（每行一条）
    返回: 文本列表
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            texts = [line.strip() for line in f if line.strip()]
        return texts
    except Exception as e:
        raise ValueError(f"TXT解析失败: {str(e)}")

def parse_file(file_path, text_column=None):
    """
    根据文件类型自动解析
    返回: 文本列表
    """
    file_path = Path(file_path)
    suffix = file_path.suffix.lower()
    
    if suffix == '.csv':
        return parse_csv(file_path, text_column)
    elif suffix in ['.xlsx', '.xls']:
        return parse_excel(file_path, text_column)
    elif suffix == '.txt':
        return parse_txt(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {suffix}")

def parse_uploaded_file(file, text_column=None):
    """
    解析上传的文件对象（Flask FileStorage）
    返回: 反馈数据列表，每个元素包含 {'text': ..., 'hotel_name': ..., 'rating': ...}
    """
    filename = file.filename.lower()
    
    if filename.endswith('.csv'):
        return parse_uploaded_csv(file, text_column)
    elif filename.endswith('.txt'):
        return parse_uploaded_txt(file)
    elif filename.endswith('.json'):
        return parse_uploaded_json(file)
    else:
        raise ValueError(f"不支持的文件类型: {filename}")

def parse_uploaded_csv(file, text_column=None):
    """解析上传的CSV文件"""
    try:
        # 尝试不同的编码
        content = file.read()
        file.seek(0)  # 重置文件指针
        
        # 尝试UTF-8
        try:
            content_str = content.decode('utf-8')
        except:
            try:
                content_str = content.decode('gbk')
            except:
                content_str = content.decode('utf-8', errors='ignore')
        
        # 检测分隔符
        first_line = content_str.split('\n')[0] if '\n' in content_str else content_str
        delimiter = ';' if ';' in first_line else ','
        
        df = pd.read_csv(io.StringIO(content_str), delimiter=delimiter, encoding='utf-8')
        
        # 自动检测文本列
        if text_column is None:
            possible_columns = ['text', 'review', 'comment', 'feedback', 'content', 
                             '评论', '反馈', '内容', 'Review', 'Text', 'Comment']
            for col in possible_columns:
                if col in df.columns:
                    text_column = col
                    break
            if text_column is None:
                text_column = df.columns[0]
        
        # 检测酒店名称列
        hotel_column = None
        hotel_columns = ['hotel_name', 'hotel', '酒店', 'Hotel', 'Hotel Name']
        for col in hotel_columns:
            if col in df.columns:
                hotel_column = col
                break
        
        # 检测评分列
        rating_column = None
        rating_columns = ['rating', 'score', '评分', 'Rating', 'Score']
        for col in rating_columns:
            if col in df.columns:
                rating_column = col
                break
        
        results = []
        for _, row in df.iterrows():
            text = str(row[text_column]).strip()
            if not text or text == 'nan':
                continue
            
            feedback_data = {'text': text}
            if hotel_column and hotel_column in row:
                feedback_data['hotel_name'] = str(row[hotel_column]).strip()
            if rating_column and rating_column in row:
                try:
                    rating = float(row[rating_column])
                    if 1 <= rating <= 5:
                        feedback_data['rating'] = rating
                except:
                    pass
            
            results.append(feedback_data)
        
        return results
    except Exception as e:
        raise ValueError(f"CSV解析失败: {str(e)}")

def parse_uploaded_txt(file):
    """解析上传的TXT文件（每行一条评论）"""
    try:
        content = file.read()
        file.seek(0)
        
        try:
            content_str = content.decode('utf-8')
        except:
            try:
                content_str = content.decode('gbk')
            except:
                content_str = content.decode('utf-8', errors='ignore')
        
        lines = [line.strip() for line in content_str.split('\n') if line.strip()]
        return [{'text': line} for line in lines]
    except Exception as e:
        raise ValueError(f"TXT解析失败: {str(e)}")

def parse_uploaded_json(file):
    """解析上传的JSON文件"""
    try:
        content = file.read()
        file.seek(0)
        
        try:
            content_str = content.decode('utf-8')
        except:
            content_str = content.decode('utf-8', errors='ignore')
        
        data = json.loads(content_str)
        
        if isinstance(data, list):
            results = []
            for item in data:
                if isinstance(item, dict):
                    text = item.get('text') or item.get('review') or item.get('comment') or ''
                    if text:
                        feedback_data = {'text': str(text).strip()}
                        if 'hotel_name' in item or 'hotel' in item:
                            feedback_data['hotel_name'] = str(item.get('hotel_name') or item.get('hotel', '')).strip()
                        if 'rating' in item or 'score' in item:
                            try:
                                rating = float(item.get('rating') or item.get('score', 0))
                                if 1 <= rating <= 5:
                                    feedback_data['rating'] = rating
                            except:
                                pass
                        results.append(feedback_data)
            return results
        else:
            raise ValueError("JSON文件必须是数组格式")
    except Exception as e:
        raise ValueError(f"JSON解析失败: {str(e)}")

