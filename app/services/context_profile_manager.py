import os
import json
from pathlib import Path
from urllib.parse import urlparse
import re
from datetime import datetime

def sanitize_filename(text: str) -> str:
    """
    Chuyển đổi text thành filename-friendly string.
    Loại bỏ ký tự đặc biệt, thay thế khoảng trắng bằng dấu gạch ngang.
    """
    # Chuyển thành chữ thường
    text = text.lower()
    # Loại bỏ dấu tiếng Việt (Vietnamese diacritics)
    vietnamese_map = {
        'à': 'a', 'á': 'a', 'ả': 'a', 'ã': 'a', 'ạ': 'a',
        'ă': 'a', 'ằ': 'a', 'ắ': 'a', 'ẳ': 'a', 'ẵ': 'a', 'ặ': 'a',
        'â': 'a', 'ầ': 'a', 'ấ': 'a', 'ẩ': 'a', 'ẫ': 'a', 'ậ': 'a',
        'đ': 'd',
        'è': 'e', 'é': 'e', 'ẻ': 'e', 'ẽ': 'e', 'ẹ': 'e',
        'ê': 'e', 'ề': 'e', 'ế': 'e', 'ể': 'e', 'ễ': 'e', 'ệ': 'e',
        'ì': 'i', 'í': 'i', 'ỉ': 'i', 'ĩ': 'i', 'ị': 'i',
        'ò': 'o', 'ó': 'o', 'ỏ': 'o', 'õ': 'o', 'ọ': 'o',
        'ô': 'o', 'ồ': 'o', 'ố': 'o', 'ổ': 'o', 'ỗ': 'o', 'ộ': 'o',
        'ơ': 'o', 'ờ': 'o', 'ớ': 'o', 'ở': 'o', 'ỡ': 'o', 'ợ': 'o',
        'ù': 'u', 'ú': 'u', 'ủ': 'u', 'ũ': 'u', 'ụ': 'u',
        'ư': 'u', 'ừ': 'u', 'ứ': 'u', 'ử': 'u', 'ữ': 'u', 'ự': 'u',
        'ỳ': 'y', 'ý': 'y', 'ỷ': 'y', 'ỹ': 'y', 'ỵ': 'y'
    }
    for vietnamese_char, latin_char in vietnamese_map.items():
        text = text.replace(vietnamese_char, latin_char)
    # Thay thế khoảng trắng và ký tự đặc biệt bằng dấu gạch ngang
    text = re.sub(r'[^\w\s-]', '', text)
    # Thay thế khoảng trắng bằng dấu gạch ngang
    text = re.sub(r'[-\s]+', '-', text)
    # Loại bỏ dấu gạch ngang ở đầu và cuối
    text = text.strip('-')
    return text

def extract_novel_name_from_url(url: str) -> str:
    """
    Trích xuất tên truyện từ URL.
    Ví dụ: https://metruyencv.com/truyen/cau-tha-tai-ban-dau-thanh-ma-mon-lam-nhan-tai/chuong-100
    Trả về: cau-tha-tai-ban-dau-thanh-ma-mon-lam-nhan-tai
    """
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    # Tìm phần chứa tên truyện (thường là phần sau "truyen/")
    if 'truyen' in path_parts:
        truyen_index = path_parts.index('truyen')
        if truyen_index + 1 < len(path_parts):
            novel_name = path_parts[truyen_index + 1]
            return novel_name
    
    return ""

def get_novel_profile_path(novel_name: str, base_dir: str = "novel-profiles") -> Path:
    """
    Tạo đường dẫn cho profile file.
    Format: novel-profiles/[novel_name]_profiles.json
    """
    sanitized_name = sanitize_filename(novel_name)
    profile_filename = f"{sanitized_name}_profiles.json"
    return Path(base_dir) / profile_filename

def create_json_profile(novel_name: str, novel_url: str = "") -> dict:
    """
    Tạo cấu trúc JSON profile cơ bản.
    """
    return {
        "novel_info": {
            "novel_name": novel_name,
            "novel_url": novel_url,
            "created_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "last_updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        },
        "metadata": {
            "chapters_processed": 0,
            "total_characters": 0,
            "editing_style": "default"
        },
        "characters": {
            "character_relations": {},
            "pronoun_consistency": {}
        },
        "history": []
    }

def check_and_create_profile(novel_name: str, novel_url: str = "") -> Path:
    """
    Kiểm tra và tạo profile file nếu chưa tồn tại.
    
    Args:
        novel_name: Tên truyện
        novel_url: URL của truyện (tùy chọn, để ghi vào profile)
    
    Returns:
        Path: Đường dẫn đến profile file
    """
    # Tạo thư mục novel-profiles nếu chưa tồn tại
    profile_dir = Path("novel-profiles")
    profile_dir.mkdir(exist_ok=True)
    
    # Tạo đường dẫn profile file (sử dụng .json thay vì .txt)
    sanitized_name = sanitize_filename(novel_name)
    profile_filename = f"{sanitized_name}_profiles.json"
    profile_path = Path("novel-profiles") / profile_filename
    
    # Kiểm tra nếu file đã tồn tại
    if profile_path.exists():
        print(f"[PROFILE] Profile file đã tồn tại: {profile_path}")
        return profile_path
    
    # Tạo profile JSON mới
    print(f"[PROFILE] Tạo profile file mới: {profile_path}")
    
    # Tạo cấu trúc JSON
    profile_data = create_json_profile(novel_name, novel_url)
    
    # Ghi file JSON
    with open(profile_path, 'w', encoding='utf-8') as f:
        json.dump(profile_data, f, ensure_ascii=False, indent=2)
    
    print(f"[PROFILE] Đã tạo profile file: {profile_path}")
    
    return profile_path

def update_profile_stats(profile_path: Path, chapters_count: int = 1, characters_count: int = 0):
    """
    Cập nhật thống kê trong profile file (JSON format).
    """
    if not profile_path.exists():
        return
    
    try:
        # Đọc file JSON
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        # Cập nhật last_updated
        profile_data["novel_info"]["last_updated"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Cập nhật chapters_processed
        profile_data["metadata"]["chapters_processed"] += chapters_count
        
        # Cập nhật total_characters
        profile_data["metadata"]["total_characters"] += characters_count
        
        # Ghi file JSON
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)
        
        print(f"[PROFILE] Đã cập nhật profile: {profile_path}")
        
    except Exception as e:
        print(f"[PROFILE ERROR] Không thể cập nhật profile {profile_path}: {e}")

def add_character_relation(profile_path: Path, character_name: str, relation_data: dict):
    """
    Thêm thông tin quan hệ nhân vật vào profile.
    
    Args:
        profile_path: Đường dẫn đến profile file
        character_name: Tên nhân vật
        relation_data: Dữ liệu quan hệ {related_character: relationship_type, ...}
    """
    if not profile_path.exists():
        return
    
    try:
        # Đọc file JSON
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        # Thêm hoặc cập nhật thông tin nhân vật
        if character_name not in profile_data["characters"]["character_relations"]:
            profile_data["characters"]["character_relations"][character_name] = {}
        
        # Cập nhật quan hệ
        profile_data["characters"]["character_relations"][character_name].update(relation_data)
        
        # Ghi file JSON
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)
        
        print(f"[PROFILE] Đã cập nhật thông tin nhân vật cho: {character_name}")
        
    except Exception as e:
        print(f"[PROFILE ERROR] Không thể cập nhật thông tin nhân vật {profile_path}: {e}")

def update_pronoun_consistency(profile_path: Path, character_name: str, pronouns: list):
    """
    Cập nhật thông tin xưng hô nhất quán cho nhân vật.
    
    Args:
        profile_path: Đường dẫn đến profile file
        character_name: Tên nhân vật
        pronouns: Danh sách các xưng hô được sử dụng
    """
    if not profile_path.exists():
        return
    
    try:
        # Đọc file JSON
        with open(profile_path, 'r', encoding='utf-8') as f:
            profile_data = json.load(f)
        
        # Cập nhật xưng hô
        profile_data["characters"]["pronoun_consistency"][character_name] = pronouns
        
        # Ghi file JSON
        with open(profile_path, 'w', encoding='utf-8') as f:
            json.dump(profile_data, f, ensure_ascii=False, indent=2)
        
        print(f"[PROFILE] Đã cập nhật xưng hô cho nhân vật: {character_name}")
        
    except Exception as e:
        print(f"[PROFILE ERROR] Không thể cập nhật xưng hô {profile_path}: {e}")

def get_profile_data(profile_path: Path) -> dict:
    """
    Đọc và trả về dữ liệu profile.
    
    Args:
        profile_path: Đường dẫn đến profile file
        
    Returns:
        dict: Dữ liệu profile
    """
    if not profile_path.exists():
        return {}
    
    try:
        with open(profile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[PROFILE ERROR] Không thể đọc profile {profile_path}: {e}")
        return {}

def format_character_info_for_prompt(profile_data: dict) -> str:
    """
    Format thông tin nhân vật cho prompt.
    
    Args:
        profile_data: Dữ liệu profile
        
    Returns:
        str: Thông tin nhân vật đã format
    """
    if not profile_data:
        return "No character information available."
    
    lines = []
    
    # Character pronouns
    if profile_data.get("characters", {}).get("pronoun_consistency"):
        lines.append("Current Character Pronouns:")
        for character, pronouns in profile_data["characters"]["pronoun_consistency"].items():
            pronouns_str = ", ".join(pronouns) if isinstance(pronouns, list) else str(pronouns)
            lines.append(f"- {character}: {pronouns_str}")
        lines.append("")
    
    # Character relations
    if profile_data.get("characters", {}).get("character_relations"):
        lines.append("Character Relationships:")
        for character, relations in profile_data["characters"]["character_relations"].items():
            if relations:
                relations_str = "; ".join([f"{rel_char} ({rel_type})" for rel_char, rel_type in relations.items()])
                lines.append(f"- {character}: {relations_str}")
        lines.append("")
    
    return "\n".join(lines) if lines else "No character information available."

def parse_ai_response_for_pronouns(ai_response: str) -> dict:
    """
    Parse kết quả từ AI để extract thông tin xưng hô mới và nhân vật mới.
    
    Args:
        ai_response: Kết quả từ AI
        
    Returns:
        dict: Thông tin xưng hô và nhân vật mới
    """
    result = {
        "new_pronouns": {},
        "new_characters": {}
    }
    
    # Parse new/changed pronouns
    pronouns_section = extract_section(ai_response, "### New/Changed Pronouns", "### New Characters")
    if pronouns_section and "None" not in pronouns_section:
        lines = pronouns_section.strip().split('\n')
        for line in lines:
            if line.startswith("- "):
                parts = line[2:].split(":")
                if len(parts) >= 2:
                    character_name = parts[0].strip()
                    pronouns = parts[1].strip()
                    # Parse pronouns list
                    pronoun_list = [p.strip() for p in pronouns.split(",") if p.strip()]
                    if pronoun_list:
                        result["new_pronouns"][character_name] = pronoun_list
    
    # Parse new characters
    characters_section = extract_section(ai_response, "### New Characters", None)
    if characters_section and "None" not in characters_section:
        lines = characters_section.strip().split('\n')
        for line in lines:
            if line.startswith("- "):
                parts = line[2:].split(":")
                if len(parts) >= 2:
                    character_name = parts[0].strip()
                    description = parts[1].strip()
                    result["new_characters"][character_name] = description
    
    return result

def extract_section(text: str, start_marker: str, end_marker: str = None) -> str:
    """
    Trích xuất section từ text dựa trên markers.
    
    Args:
        text: Văn bản đầu vào
        start_marker: Marker bắt đầu
        end_marker: Marker kết thúc (nếu None thì đến hết text)
        
    Returns:
        str: Section được trích xuất
    """
    start_index = text.find(start_marker)
    if start_index == -1:
        return ""
    
    start_index += len(start_marker)
    
    if end_marker:
        end_index = text.find(end_marker, start_index)
        if end_index == -1:
            end_index = len(text)
    else:
        end_index = len(text)
    
    return text[start_index:end_index].strip()

def update_profile_from_ai_response(profile_path: Path, ai_response: str):
    """
    Update profile từ kết quả AI response.
    
    Args:
        profile_path: Đường dẫn đến profile file
        ai_response: Kết quả từ AI
    """
    if not profile_path.exists():
        return
    
    try:
        # Parse AI response
        parsed_data = parse_ai_response_for_pronouns(ai_response)
        
        # Update new pronouns
        for character, pronouns in parsed_data["new_pronouns"].items():
            update_pronoun_consistency(profile_path, character, pronouns)
        
        # Update new characters (basic implementation - can be enhanced)
        if parsed_data["new_characters"]:
            # For now, we'll just log new characters
            print(f"[PROFILE] New characters detected: {list(parsed_data['new_characters'].keys())}")
            # In future, we can add more detailed character tracking
            
    except Exception as e:
        print(f"[PROFILE ERROR] Không thể update profile từ AI response {profile_path}: {e}")
