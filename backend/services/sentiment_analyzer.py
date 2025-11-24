"""
Sentiment Analysis Service (Full Version)
Integrates Qwen2 models with strict English aspect mapping and robust error handling.
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
    """
    Professional Sentiment Analyzer based on Qwen2.
    Supports strict 6-aspect classification and English output.
    """
    
    # 1. Standard White-list (English)
    ALLOWED_ASPECTS = {'Room', 'Location', 'Price', 'Service', 'Food', 'Facilities'}
    
    # 2. Comprehensive Aspect Mapping (Chinese/English -> Standard English)
    ASPECT_MAPPING = {
        # Room Related
        'room': 'Room', 'rooms': 'Room', 'bedroom': 'Room', 'suite': 'Room', 
        'accommodation': 'Room', 'bed': 'Room', 'beds': 'Room', 'sleep': 'Room', 
        'sleeping': 'Room', 'cleanliness': 'Room', 'clean': 'Room', 'cleaning': 'Room',
        'noise': 'Room', 'soundproof': 'Room', 'space': 'Room', 'spacious': 'Room',
        '房间': 'Room', '客房': 'Room', '卧室': 'Room', '床': 'Room', '卫生': 'Room', 
        '睡眠': 'Room', '隔音': 'Room', '空间': 'Room',
        
        # Location Related
        'location': 'Location', 'position': 'Location', 'place': 'Location', 'area': 'Location', 
        'loc': 'Location', 'neighborhood': 'Location', 'accessibility': 'Location',
        'traffic': 'Location', 'transport': 'Location', 'view': 'Location', # View often relates to location
        '位置': 'Location', '交通': 'Location', '地点': 'Location', '周边': 'Location', 
        '景色': 'Location', '风景': 'Location',
        
        # Price Related
        'price': 'Price', 'cost': 'Price', 'value': 'Price', 'money': 'Price', 
        'expensive': 'Price', 'cheap': 'Price', 'rate': 'Price', 'rates': 'Price',
        'booking': 'Price', 'deposit': 'Price',
        '价格': 'Price', '性价比': 'Price', '费用': 'Price', '贵': 'Price', '便宜': 'Price',
        
        # Service Related
        'service': 'Service', 'staff': 'Service', 'services': 'Service', 'personnel': 'Service',
        'reception': 'Service', 'check-in': 'Service', 'checkin': 'Service', 'crew': 'Service',
        'manager': 'Service', 'attitude': 'Service', 'response': 'Service',
        '服务': 'Service', '前台': 'Service', '态度': 'Service', '人员': 'Service', '管理': 'Service',
        
        # Food Related
        'food': 'Food', 'breakfast': 'Food', 'meal': 'Food', 'meals': 'Food',
        'dining': 'Food', 'restaurant': 'Food', 'drink': 'Food', 'drinks': 'Food',
        'catering': 'Food', 'bar': 'Food', 'lunch': 'Food', 'dinner': 'Food',
        '餐饮': 'Food', '早餐': 'Food', '吃饭': 'Food', '食物': 'Food', '餐厅': 'Food',
        
        # Facilities Related
        'facility': 'Facilities', 'facilities': 'Facilities', 'amenities': 'Facilities', 
        'equipment': 'Facilities', 'wifi': 'Facilities', 'internet': 'Facilities', 
        'pool': 'Facilities', 'gym': 'Facilities', 'parking': 'Facilities', 
        'elevator': 'Facilities', 'lift': 'Facilities', 'bathroom': 'Facilities',
        'shower': 'Facilities', 'toilet': 'Facilities', 'lobby': 'Facilities',
        '设施': 'Facilities', '设备': 'Facilities', '网络': 'Facilities', '泳池': 'Facilities',
        '电梯': 'Facilities', '浴室': 'Facilities', '停车场': 'Facilities'
    }
    
    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.device = Config.DEVICE
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load model with robust error handling and device checking"""
        cache_dir = Config.MODEL_CACHE_DIR
        os.makedirs(cache_dir, exist_ok=True)
        
        # Check local path
        model_local_path = Path(cache_dir) / self.model_name.replace('/', '--')
        if not (model_local_path.exists() and (model_local_path / 'model.safetensors').exists()):
            raise FileNotFoundError(f"Model not found at local path: {model_local_path}. Please download it first.")
            
        model_path = str(model_local_path)
        print(f"Loading model from: {model_path}")
        print(f"Target Device: {self.device}")
        
        if self.device == 'cuda':
            print(f"GPU detected: {torch.cuda.get_device_name(0)}")
            vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"Total VRAM: {vram:.2f} GB")
        
        try:
            # 1. Load Tokenizer
            print("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=True,
                local_files_only=True
            )
            print("✅ Tokenizer loaded.")
            
            # 2. Load Model
            print("Loading model weights (this may take time)...")
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
            
            # Ensure model is on correct device
            if self.device == 'cuda':
                if not hasattr(self.model, 'device') or str(self.model.device) == 'cpu':
                    self.model = self.model.to('cuda')
                print(f"Model loaded on GPU: {next(self.model.parameters()).device}")
            else:
                self.model = self.model.to('cpu')
                print(f"Model loaded on CPU")
            
            self.model.eval()
            
            # Memory usage report
            if self.device == 'cuda':
                allocated = torch.cuda.memory_allocated(0) / 1024**3
                print(f"✅ Model loaded successfully! VRAM Used: {allocated:.2f} GB")
            else:
                print(f"✅ Model loaded successfully!")
                
        except Exception as e:
            error_msg = f"❌ Critical Error loading model: {str(e)}"
            print(error_msg)
            print(traceback.format_exc())
            raise RuntimeError(f"Failed to load model: {str(e)}")
    
    def analyze(self, text):
        """
        Analyze overall sentiment (Simple version).
        Returns: {'label': 'very_positive/...', 'score': float}
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not initialized.")
        
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are a sentiment analysis assistant. Analyze the overall sentiment of the review."
                },
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of this hotel review. Choose one: very_positive, positive, neutral, negative, very_negative.\n\nReview: {text}\n\nSentiment:"
                }
            ]
            
            text_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer(text_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=15, temperature=0.1, do_sample=False)
            
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            response = response.strip().lower()
            
            label, score = self._parse_sentiment_response(response)
            return {'label': label, 'score': score}
            
        except Exception as e:
            print(f"Analyze Error: {str(e)}")
            raise RuntimeError(f"Analyze failed: {str(e)}")
    
    def _parse_sentiment_response(self, response):
        """
        Helper: Convert text response to standardized label and score.
        Handles both English and Chinese potential outputs for robustness.
        """
        response_lower = response.lower()
        
        # Very Positive
        if any(x in response_lower for x in ['very_positive', 'very positive', 'excellent', 'perfect', '极好', '非常满意']):
            return 'very_positive', 0.95
        # Positive
        elif any(x in response_lower for x in ['positive', 'good', 'nice', 'great', '满意', '正面']):
            if 'very' not in response_lower:
                return 'positive', 0.75
            return 'very_positive', 0.95
        # Negative
        elif any(x in response_lower for x in ['negative', 'bad', 'poor', 'terrible', '负面', '差']):
            if 'very' in response_lower or 'extremely' in response_lower:
                return 'very_negative', 0.1
            return 'negative', 0.3
        # Very Negative explicit
        elif any(x in response_lower for x in ['very_negative', 'very negative', 'awful', 'worst']):
            return 'very_negative', 0.1
        # Neutral fallback
        return 'neutral', 0.5
    
    def analyze_with_aspects(self, text):
        """
        Complex Analysis: Extracts 6 specific aspects, sentiment, evidence, and reasoning.
        Output is strictly in English.
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded.")
        
        try:
            # Improved Prompt for strict JSON output and English content
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert hotel feedback analyst. Your task is to extract specific aspects from reviews and evaluate their sentiment. IMPORTANT: All your responses must be in English, including all explanations and reasoning."
                },
                {
                    "role": "user",
                    "content": f"""Analyze the following hotel review.

Review Text: "{text}"

Instructions:
1. **Identification**: Identify specific mentions related to these 6 categories ONLY:
   - Room (cleanliness, comfort, size, noise, bed)
   - Location (proximity, view, neighborhood)
   - Price (value, cost, deposit)
   - Service (staff, check-in, attitude)
   - Food (breakfast, restaurant, drinks)
   - Facilities (wifi, pool, gym, parking, elevator)

2. **Classification**: Map any identified point to one of the 6 categories above. Ignore irrelevant points.

3. **Sentiment**: Rate each identified aspect as: very_positive, positive, neutral, negative, or very_negative.

4. **Reasoning**: Write a brief summary (1-2 sentences) in English explaining the overall impression.

5. **Output**: Return a valid JSON object. Do not include markdown formatting like ```json.

IMPORTANT: All text in your response MUST be in English, including the explanation field.

JSON Structure:
{{
  "overall": "sentiment_label",
  "aspects": {{
    "CategoryName": "sentiment_label"
  }},
  "reasoning": "English summary here",
  "aspect_details": [
    {{
      "aspect": "CategoryName",
      "sentiment": "sentiment_label",
      "evidence": "Quote from text",
      "explanation": "Brief explanation in English"
    }}
  ]
}}
"""
                }
            ]
            
            text_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer(text_prompt, return_tensors="pt").to(self.device)
            
            # Generate with slightly higher max tokens for detailed JSON
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=600,
                    temperature=0.1, # Low temp for deterministic output
                    do_sample=False
                )
            
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            
            # Parse the result
            result = self._parse_aspects_response(response)
            return result
            
        except Exception as e:
            print(f"Aspect Analysis Failed: {str(e)}")
            raise RuntimeError(f"Failed to analyze aspects: {str(e)}")
    
    def _parse_aspects_response(self, response):
        """
        Robustly parses the LLM response, handling JSON errors and enforcing English keys.
        """
        response = response.strip()
        data = None
        
        # Strategy 1: Direct JSON load
        try:
            # Clean up potential markdown wrappers
            clean_resp = response.replace('```json', '').replace('```', '').strip()
            data = json.loads(clean_resp)
        except json.JSONDecodeError:
            # Strategy 2: Regex extraction of JSON object
            try:
                match = re.search(r'\{.*\}', response, re.DOTALL)
                if match:
                    data = json.loads(match.group())
            except:
                pass
        
        # If JSON parsing completely fails, use fallback regex extraction
        if not data:
            print(f"⚠️ JSON parsing failed. Raw response: {response[:100]}...")
            return self._fallback_regex_extraction(response)
            
        return self._extract_and_normalize_data(data)
    
    def _fallback_regex_extraction(self, text):
        """Fallback method using Regex to find patterns like 'Room': 'positive'"""
        aspect_sentiments = {}
        
        # Regex for "Key": "Value"
        matches = re.findall(r'["\']?(\w+)["\']?\s*[:：]\s*["\']?([a-zA-Z_]+)["\']?', text)
        for k, v in matches:
            if k.lower() in ['overall', 'reasoning']: continue
            aspect_sentiments[k] = v
            
        # Construct a basic data object
        data = {
            'overall': 'neutral',
            'aspects': aspect_sentiments,
            'reasoning': 'Analysis generated via fallback extraction.'
        }
        return self._extract_and_normalize_data(data)

    def _extract_and_normalize_data(self, data):
        """
        Core Logic: Mapping raw LLM output to Standard English 6 Aspects.
        """
        # 1. Overall Sentiment
        overall_raw = data.get('overall', 'neutral')
        if isinstance(overall_raw, dict): overall_raw = overall_raw.get('label', 'neutral')
        overall_label, overall_score = self._parse_sentiment_score(str(overall_raw))
        
        # 2. Reasoning (Ensure it exists)
        reasoning = data.get('reasoning', 'No detailed reasoning provided.')
        
        # 3. Aspects Mapping
        # Merge 'aspects' and 'aspect_sentiments' keys just in case
        raw_aspects = data.get('aspects', {})
        if not raw_aspects:
            raw_aspects = data.get('aspect_sentiments', {})
            
        final_aspects = {}
        final_details = []
        
        # Process simple key-value pairs
        for aspect, sentiment in raw_aspects.items():
            mapped_key = self._map_to_standard_aspect(str(aspect))
            if mapped_key:
                label, _ = self._parse_sentiment_score(str(sentiment))
                final_aspects[mapped_key] = label

        # Process detailed aspect_details if available
        raw_details = data.get('aspect_details', [])
        if isinstance(raw_details, list):
            for detail in raw_details:
                if not isinstance(detail, dict): continue
                
                raw_name = detail.get('aspect', '')
                mapped_key = self._map_to_standard_aspect(str(raw_name))
                
                if mapped_key:
                    s_label, _ = self._parse_sentiment_score(str(detail.get('sentiment', 'neutral')))
                    # Ensure consistency: Update final_aspects map
                    final_aspects[mapped_key] = s_label
                    
                    final_details.append({
                        'aspect': mapped_key,
                        'sentiment': s_label,
                        'evidence': detail.get('evidence', 'Mentioned in review'),
                        'explanation': detail.get('explanation', ''),
                        'keywords': detail.get('keywords', [])
                    })
        
        return {
            'sentiment': {'label': overall_label, 'score': overall_score},
            'aspect_sentiments': final_aspects,
            'reasoning': reasoning,
            'aspect_details': final_details
        }

    def _map_to_standard_aspect(self, input_str):
        """
        Maps an input string (Chinese or English) to one of the 6 Allowed Aspects.
        Returns None if no match found.
        """
        key = input_str.strip().lower()
        
        # 1. Direct Exact Match
        for allowed in self.ALLOWED_ASPECTS:
            if key == allowed.lower():
                return allowed
                
        # 2. Dictionary Lookup
        if key in self.ASPECT_MAPPING:
            return self.ASPECT_MAPPING[key]
            
        # 3. Fuzzy Match (Substring)
        # e.g. "hotel location" -> contains "location" -> Location
        for map_k, map_v in self.ASPECT_MAPPING.items():
            if map_k in key:
                return map_v
                
        return None

    def analyze_aspect(self, text, aspect):
        """
        Single aspect analysis (Legacy support).
        """
        if not self.model: raise RuntimeError("Model not loaded")
        
        try:
            messages = [
                {"role": "system", "content": "Analyze sentiment for a specific aspect."},
                {"role": "user", "content": f"Review: {text}\nAspect: {aspect}\nSentiment (very_positive/positive/neutral/negative/very_negative):"}
            ]
            text_prompt = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            inputs = self.tokenizer(text_prompt, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(**inputs, max_new_tokens=15)
            
            response = self.tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
            label, score = self._parse_sentiment_score(response)
            return {'label': label, 'score': score}
        except:
            return {'label': 'neutral', 'score': 0.5}

    def _parse_sentiment_score(self, text):
        """Internal helper to normalize score"""
        t = text.lower()
        if 'very_positive' in t: return 'very_positive', 0.95
        if 'positive' in t: return 'positive', 0.75
        if 'very_negative' in t: return 'very_negative', 0.1
        if 'negative' in t: return 'negative', 0.3
        return 'neutral', 0.5