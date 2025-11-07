"""
情感分析服务
集成Qwen2系列模型（支持中英文情感分析）
"""
from transformers import AutoTokenizer, AutoModelForCausalLM, Qwen2ForCausalLM
import torch
import sys
from pathlib import Path
import traceback
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config
import os
import json
import re

class SentimentAnalyzer:
    """情感分析器"""
    
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.device = Config.DEVICE
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """加载模型"""
        cache_dir = Config.MODEL_CACHE_DIR
        os.makedirs(cache_dir, exist_ok=True)
        
        # 尝试使用本地路径（如果模型已下载）
        model_local_path = Path(cache_dir) / self.model_name.replace('/', '--')
        if not (model_local_path.exists() and (model_local_path / 'model.safetensors').exists()):
            raise FileNotFoundError(f"模型未在本地找到: {model_local_path}. 请确保模型已下载到 {cache_dir} 目录下。")
        model_path = str(model_local_path)
        print(f"使用本地模型路径: {model_path}")
        
        print(f"设备: {self.device}")
        if self.device == 'cuda':
            print(f"GPU: {torch.cuda.get_device_name(0)}")
            print(f"显存: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.2f} GB")
        
        try:
            # 加载 tokenizer
            print("加载 tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                local_files_only=True
            )
            print("✅ Tokenizer 加载成功")
            
            # 加载模型
            print("加载模型（这可能需要几分钟）...")
            load_kwargs = {
                'trust_remote_code': True,
                'local_files_only': True,
            }
            
            if self.device == 'cuda':
                load_kwargs['torch_dtype'] = torch.float16
                load_kwargs['device_map'] = 'auto'
                load_kwargs['low_cpu_mem_usage'] = True
            else:
                load_kwargs['torch_dtype'] = torch.float32
            
            self.model = Qwen2ForCausalLM.from_pretrained(
                model_path,
                **load_kwargs
            )
            
            # 确保模型在正确的设备上
            if self.device == 'cuda':
                # 如果使用device_map='auto'，模型应该已经在GPU上了
                # 但为了确保，我们检查一下
                if not hasattr(self.model, 'device') or str(self.model.device) == 'cpu':
                    self.model = self.model.to('cuda')
                print(f"模型已加载到GPU: {next(self.model.parameters()).device}")
            else:
                self.model = self.model.to('cpu')
                print(f"模型已加载到CPU")
            
            self.model.eval()
            
            if self.device == 'cuda':
                allocated = torch.cuda.memory_allocated(0) / 1024**3
                reserved = torch.cuda.memory_reserved(0) / 1024**3
                print(f"✅ 模型加载完成！")
                print(f"显存使用: {allocated:.2f} GB / {reserved:.2f} GB")
            else:
                print(f"✅ 模型加载完成！")
                
        except Exception as e:
            error_msg = f"❌ 模型加载失败: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            raise RuntimeError(f"模型加载失败，无法继续: {str(e)}")
    
    def analyze(self, text):
        """
        分析文本情感
        返回: {'label': 'very_positive/positive/neutral/negative/very_negative', 'score': float}
        五档情感：积极(very_positive)、正面(positive)、中立(neutral)、反面(negative)、消极(very_negative)
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("模型未加载，无法进行分析")
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的情感分析助手，专门分析酒店评论的整体情感倾向。请仔细分析评论的整体情感倾向，使用五档情感分类。"
                },
                {
                    "role": "user",
                    "content": f"请分析以下酒店评论的整体情感倾向，使用五档情感分类。\n\n五档情感分类：\n1. 积极(very_positive)：非常满意、极好、完美、超出预期等强烈积极情感\n2. 正面(positive)：不错、很好、满意、便捷、方便等正面情感\n3. 中立(neutral)：没有明确的情感倾向，或者积极和消极情感相当\n4. 反面(negative)：不太好、一般、有待改进等负面情感\n5. 消极(very_negative)：极差、很差、不满意、糟糕、非常差等强烈消极情感\n\n请只回答：very_positive、positive、neutral、negative 或 very_negative\n\n评论：{text}\n\n情感："
                }
            ]
            
            text_prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.tokenizer(text_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=15,
                    temperature=0.1,
                    do_sample=False,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            response = response.strip().lower()
            
            label, score = self._parse_sentiment_response(response)
            
            return {'label': label, 'score': score}
        except Exception as e:
            print(f"模型分析失败: {str(e)}")
            raise RuntimeError(f"情感分析失败: {str(e)}")
    
    def _parse_sentiment_response(self, response):
        """解析情感响应，返回标签和分数"""
        response_lower = response.lower()
        
        if 'very_positive' in response_lower or '非常积极' in response_lower or '极好' in response_lower:
            return 'very_positive', 0.9
        elif 'positive' in response_lower or '正面' in response_lower or '积极' in response_lower:
            if 'very' not in response_lower and '非常' not in response_lower:
                return 'positive', 0.7
            else:
                return 'very_positive', 0.9
        elif 'neutral' in response_lower or '中性' in response_lower or '中立' in response_lower:
            return 'neutral', 0.5
        elif 'negative' in response_lower or '反面' in response_lower or '负面' in response_lower:
            if 'very' not in response_lower and '非常' not in response_lower and '极' not in response_lower:
                return 'negative', 0.3
            else:
                return 'very_negative', 0.1
        elif 'very_negative' in response_lower or '非常消极' in response_lower or '极差' in response_lower:
            return 'very_negative', 0.1
        else:
            return 'neutral', 0.5
    
    def analyze_with_aspects(self, text):
        """
        一次性分析文本的所有方面及其情感，包含思考过程和证据
        返回: {
            'sentiment': {'label': '...', 'score': float},
            'aspect_sentiments': {'方面名': '情感标签', ...},
            'reasoning': '思考过程文本',
            'aspect_details': [
                {
                    'aspect': '方面名',
                    'sentiment': '情感标签',
                    'evidence': '原文证据',
                    'keywords': ['关键词1', '关键词2'],
                    'explanation': '解释说明'
                }
            ]
        }
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("模型未加载，无法进行分析")
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": "你是专业的酒店评论情感分析助手。你需要识别评论中的所有方面，分析每个方面的情感，并提供详细的思考过程和证据。"
                },
                {
                    "role": "user",
                    "content": f"""请分析以下酒店评论，识别所有被评价的方面，并给出每个方面的情感分类。

评论：{text}

要求：
1. 识别评论中所有被评价的方面（如：房间、服务、位置、餐饮、价格、设施等）
2. 对每个方面进行五档情感分类：very_positive（积极）、positive（正面）、neutral（中立）、negative（负面）、very_negative（消极）
3. 为每个方面提供：
   - 情感标签
   - 原文中的证据（引用的具体文字）
   - 关键词（影响情感判断的关键词）
   - 简要解释

请返回JSON格式：
{{
  "overall": "整体情感（very_positive/positive/neutral/negative/very_negative）",
  "aspects": {{
    "方面名": "情感标签"
  }},
  "reasoning": "整体思考过程说明",
  "aspect_details": [
    {{
      "aspect": "方面名",
      "sentiment": "情感标签",
      "evidence": "原文证据片段",
      "keywords": ["关键词1", "关键词2"],
      "explanation": "为什么是这个情感"
    }}
  ]
}}

结果："""
                }
            ]
            
            text_prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.tokenizer(text_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=500,
                    temperature=0.3,
                    do_sample=True,
                    top_p=0.9,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            response = response.strip()
            
            result = self._parse_aspects_response(response)
            
            return result
        except Exception as e:
            print(f"方面分析失败: {str(e)}")
            raise RuntimeError(f"方面情感分析失败: {str(e)}")
    
    def _parse_aspects_response(self, response):
        """解析模型返回的方面和情感JSON"""
        response = response.strip()
        
        # 方法1：尝试直接解析整个响应
        try:
            data = json.loads(response)
            return self._extract_from_json_data(data)
        except json.JSONDecodeError:
            pass
        
        # 方法2：查找JSON对象
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_str = response[start_idx:end_idx+1]
            try:
                data = json.loads(json_str)
                return self._extract_from_json_data(data)
            except json.JSONDecodeError:
                pass
        
        # 方法3：尝试提取代码块中的JSON
        code_block_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response, re.DOTALL)
        if code_block_match:
            json_str = code_block_match.group(1)
            try:
                data = json.loads(json_str)
                return self._extract_from_json_data(data)
            except json.JSONDecodeError:
                pass
        
        # 方法4：如果JSON解析失败，尝试从文本中提取
        aspect_sentiments = {}
        exclude_fields = {
            'aspect', 'aspect_details', 'aspects', 'evidence', 'explanation', 
            'keywords', 'reasoning', 'overall', 'sentiment', 'result',
            '思考', '分析', '说明', '结果', 'data', 'json', 'object'
        }
        
        aspect_patterns = [
            r'["\']?([^"\':,]+)["\']?\s*[:：]\s*["\']?([^"\',}]+)["\']?',
            r'(\w+)\s*[:：]\s*(\w+)'
        ]
        
        for pattern in aspect_patterns:
            matches = re.findall(pattern, response)
            for match in matches:
                aspect_name = match[0].strip()
                sentiment = match[1].strip()
                if (aspect_name and sentiment and 
                    aspect_name.lower() not in exclude_fields and
                    not aspect_name.startswith('_') and
                    len(aspect_name) <= 20):
                    label, _ = self._parse_sentiment_response(sentiment)
                    aspect_sentiments[aspect_name] = label
        
        overall_label, overall_score = self._parse_sentiment_response(response)
        
        return {
            'sentiment': {
                'label': overall_label,
                'score': overall_score
            },
            'aspect_sentiments': aspect_sentiments if aspect_sentiments else {}
        }
    
    def _extract_from_json_data(self, data):
        """从JSON数据中提取情感和方面信息，包括思考过程和证据"""
        # 提取整体情感
        overall = data.get('overall', 'neutral')
        if isinstance(overall, dict):
            overall = overall.get('label', 'neutral')
        overall_label, overall_score = self._parse_sentiment_response(str(overall))
        
        # 提取思考过程
        reasoning = data.get('reasoning', '')
        if not reasoning:
            reasoning = data.get('思考', '') or data.get('分析', '') or data.get('说明', '')
        
        # 提取方面情感
        aspects = data.get('aspects', {})
        if not isinstance(aspects, dict):
            aspects = {}
        
        exclude_fields = {
            'aspect', 'aspect_details', 'aspects', 'evidence', 'explanation', 
            'keywords', 'reasoning', 'overall', 'sentiment', 'result',
            '思考', '分析', '说明', '结果', 'data', 'json', 'object', 'format',
            'label', 'score', 'value', 'type', 'name', 'id', 'key', 'text'
        }
        
        aspect_sentiments = {}
        for aspect_name, sentiment in aspects.items():
            aspect_name_str = str(aspect_name).strip()
            
            if (aspect_name_str and 
                aspect_name_str.lower() not in exclude_fields and
                not aspect_name_str.startswith('_') and
                len(aspect_name_str) <= 20):
                if isinstance(sentiment, str):
                    label, _ = self._parse_sentiment_response(sentiment)
                    aspect_sentiments[aspect_name_str] = label
                elif isinstance(sentiment, dict):
                    label = sentiment.get('label', 'neutral')
                    aspect_sentiments[aspect_name_str] = label
        
        # 提取方面详细信息
        aspect_details = data.get('aspect_details', [])
        if not isinstance(aspect_details, list):
            aspect_details = []
        
        # 清理和验证aspect_details
        cleaned_aspect_details = []
        for detail in aspect_details:
            if isinstance(detail, dict):
                aspect_name = detail.get('aspect', '').strip()
                if (aspect_name and 
                    aspect_name.lower() not in exclude_fields and
                    not aspect_name.startswith('_') and
                    len(aspect_name) <= 20):
                    cleaned_aspect_details.append({
                        'aspect': aspect_name,
                        'sentiment': detail.get('sentiment', 'neutral'),
                        'evidence': detail.get('evidence', ''),
                        'keywords': detail.get('keywords', []),
                        'explanation': detail.get('explanation', '')
                    })
        
        result = {
            'sentiment': {
                'label': overall_label,
                'score': overall_score
            },
            'aspect_sentiments': aspect_sentiments
        }
        
        # 如果有思考过程或方面详情，添加到结果中
        if reasoning:
            result['reasoning'] = reasoning
        if cleaned_aspect_details:
            result['aspect_details'] = cleaned_aspect_details
        
        return result
    
    def analyze_aspect(self, text, aspect):
        """
        分析特定方面的情感（保留用于兼容性）
        aspect: 方面名称（中文，如'房间'、'服务'、'位置'等）
        返回: {'label': 'very_positive/positive/neutral/negative/very_negative', 'score': float}
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("模型未加载，无法进行分析")
        
        try:
            aspect_display = aspect
            
            messages = [
                {
                    "role": "system",
                    "content": "你是一个专业的情感分析助手，专门分析酒店评论中不同方面的情感倾向。请仔细分析评论中是否明确提到了指定方面，以及对该方面的情感倾向，使用五档情感分类。"
                },
                {
                    "role": "user",
                    "content": f"请分析以下酒店评论中关于\"{aspect_display}\"方面的情感倾向，使用五档情感分类。\n\n规则：\n1. 如果评论中没有明确提到\"{aspect_display}\"相关内容，回答：neutral\n2. 如果提到了\"{aspect_display}\"但没有明确的情感倾向，回答：neutral\n\n五档情感分类：\n- 积极(very_positive)：非常满意、极好、完美、超出预期等强烈积极情感\n- 正面(positive)：不错、很好、满意、便捷、方便等正面情感\n- 中立(neutral)：没有明确的情感倾向\n- 反面(negative)：不太好、一般、有待改进等负面情感\n- 消极(very_negative)：极差、很差、不满意、糟糕等强烈消极情感\n\n请只回答：very_positive、positive、neutral、negative 或 very_negative\n\n评论：{text}\n\n方面：{aspect_display}\n情感："
                }
            ]
            
            text_prompt = self.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            inputs = self.tokenizer(text_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=15,
                    temperature=0.1,
                    do_sample=False,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            response = response.strip().lower()
            
            label, score = self._parse_sentiment_response(response)
            
            return {'label': label, 'score': score}
        except Exception as e:
            print(f"方面分析失败: {str(e)}")
            raise RuntimeError(f"方面情感分析失败: {str(e)}")


