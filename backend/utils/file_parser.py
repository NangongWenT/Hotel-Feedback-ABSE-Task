import csv
import io
import traceback


def parse_uploaded_file(file_storage):
    """
    [Ultimate Enhanced Version] Parse Uploaded Files
    Features:
    1. Automatically detects CSV delimiter (comma ',' or semicolon ';') <-- Fixed core issue
    2. Automatically handles BOM headers and multiple encoding formats
    3. Brute-force fuzzy matching for column names
    4. Enhanced error handling and detailed logging
    """
    filename = file_storage.filename.lower()
    print(f"📄 开始解析文件: {file_storage.filename}")

    # 1. Read binary data
    try:
        stream = file_storage.read()
        if not stream:
            print("❌ 上传文件为空，无法解析")
            return []
        print(f"📊 读取到文件大小: {len(stream)} 字节")
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}")
        return []

    # 2. Try to decode content - optimized encoding handling
    content = None
    encoding_used = 'utf-8'
    
    # Try multiple common encodings
    encodings = [
        ('utf-8-sig', 'UTF-8 (带BOM)'),
        ('gbk', 'GBK'),
        ('gb2312', 'GB2312'),
        ('latin-1', 'Latin-1'),
        ('utf-16', 'UTF-16')
    ]
    
    for encoding, desc in encodings:
        try:
            content = stream.decode(encoding)
            encoding_used = encoding
            print(f"✅ 成功使用编码: {desc} ({encoding})")
            break
        except UnicodeDecodeError:
            print(f"🔄 尝试编码 {desc} 失败，继续尝试")
        except LookupError:
            print(f"⚠️ 不支持的编码: {encoding}")
    
    # Fallback solution
    if content is None:
        try:
            print("⚠️ 所有标准编码尝试失败，使用忽略错误模式")
            content = stream.decode('utf-8', errors='replace')
            encoding_used = 'utf-8 (with replacement)'
        except:
            print("❌ 文件编码无法识别，无法继续解析")
            return []

    # 3. Convert to file object
    f = io.StringIO(content)

    # 4. [Key Step] Automatically detect delimiter - optimized logic
    delimiter = ','  
    try:
    
        sample = content[:2048]
        
        # Alternative 1: Use csv.Sniffer
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t', '|'])
            delimiter = dialect.delimiter
            print(f"🔍 csv.Sniffer 检测到分隔符: '{delimiter}'")
        except Exception as e:
            print(f"⚠️ csv.Sniffer 失败: {str(e)}，尝试备用方法")
            
            # Alternative 2: Count occurrences of possible delimiters in first line
            first_line = sample.split('\n')[0] if '\n' in sample else sample
            possible_delimiters = [';', ',', '\t', '|']
            max_count = 0
            
            for d in possible_delimiters:
                count = first_line.count(d)
                if count > max_count:
                    max_count = count
                    delimiter = d
            
            if max_count > 0:
                print(f"✅ 备用方法检测到分隔符: '{delimiter}' (出现 {max_count} 次)")
            else:
                print("⚠️ 无法自动检测分隔符，默认使用逗号")
    except Exception as e:
        print(f"❌ 分隔符检测失败: {str(e)}，默认使用逗号")

    try:
      
        f.seek(0)
        reader = csv.reader(f, delimiter=delimiter)

      
        try:
            headers = next(reader)
          
            headers = [h.strip().strip('"').strip("'") for h in headers]
            print(f"🔍 读取到表头: {headers} (共 {len(headers)} 列)")
        except StopIteration:
            print("❌ 文件内容为空或格式错误，无法读取表头")
            return []
        except Exception as e:
            print(f"❌ 读取表头失败: {str(e)}")
            return []

        # 5. Intelligently find text column index - enhanced matching logic
        clean_headers = [h.strip().lower() for h in headers]
        target_index = -1
        possible_keys = ['text', 'review', 'content', 'comment', 'body', '评论', '内容', '反馈', 'description']

        # Try exact matching and contains matching
        for i, header in enumerate(clean_headers):
            # Exact match
            if header in possible_keys:
                target_index = i
                print(f"✅ 精确命中列名: '{headers[i]}' (索引: {i})")
                break
        
        # If no exact match, try contains matching
        if target_index == -1:
            for i, header in enumerate(clean_headers):
                if any(key in header for key in possible_keys):
                    target_index = i
                    print(f"✅ 模糊命中列名: '{headers[i]}' (索引: {i})")
                    break

        # Fallback: If no keywords found, guess based on column count and common patterns
        if target_index == -1:
            if len(headers) == 1:
                target_index = 0
                print("⚠️ 仅找到一列，默认使用该列作为文本列")
            else:
                print(f"❌ 无法识别文本列。请确保CSV包含以下列名之一: {', '.join(possible_keys)}")
                print(f"   实际表头: {', '.join(headers)}")
                return []

        # 6. Extract data - enhanced error handling and data cleaning
        results = []
        empty_rows = 0
        invalid_rows = 0
        
        for row_idx, row in enumerate(reader):
            try:
                # Skip empty rows
                if not row or all(not cell.strip() for cell in row):
                    empty_rows += 1
                    continue

                # Check if index is valid
                if len(row) <= target_index:
                    print(f"⚠️ 行 {row_idx + 2} 列数不足，跳过该行")
                    invalid_rows += 1
                    continue

                # Get and clean text
                val = row[target_index].strip()
                # Filter invalid content
                if val and len(val) > 1 and val.lower() not in ['nan', 'none', 'null', 'n/a']:
                    results.append({'text': val})
                else:
                    invalid_rows += 1
            except Exception as e:
                print(f"❌ 处理第 {row_idx + 2} 行时出错: {str(e)}")
                invalid_rows += 1
                continue

        # Output statistics
        total_rows = row_idx + 1 if 'row_idx' in locals() else 0
        print(f"📊 解析统计: 总行数={total_rows}, 有效数据={len(results)}, 空行={empty_rows}, 无效行={invalid_rows}")
        
        if not results:
            print("❌ 未找到有效数据，请检查文件内容和列名是否正确")
            return []
            
        print(f"✅ 解析成功，共 {len(results)} 条有效数据")
        return results

    except Exception as e:
        print(f"❌ 解析过程发生未知错误: {str(e)}")
        print("📋 详细错误栈:")
        traceback.print_exc()
        return []
    finally:
        try:
            file_storage.seek(0)  # Reset file pointer
            print("🔄 文件指针已重置")
        except:
            print("⚠️ 重置文件指针失败")