import os
import pandas as pd
import gc
import re
from continent_mapping import continent_mapping
from multiprocessing import Lock

# Well-known TLDs
well_known_tlds = [
    "com", "org", "net", "int", "edu", "gov", "mil", "arpa"
]

# 파일 접근을 제어하기 위한 Lock 생성
lock = Lock()

def get_continent_by_country_code(code):
    """국가 코드에 따라 대륙을 반환"""
    code = code.upper()
    for continent, countries in continent_mapping.items():
        if code in countries:
            return continent
    return None

def is_well_known_tld(tld):
    """도메인이 well-known TLD인지 확인"""
    return tld.lower() in well_known_tlds

def find_valid_suffix(domain_parts):
    """도메인의 모든 부분을 확인하여 유효한 국가 코드 또는 TLD를 찾음"""
    for part in domain_parts:
        part = part.lower()
        if is_well_known_tld(part) or get_continent_by_country_code(part):
            return part
    return None

def process_file(filename, data_dir, domain_dir):
    """파일을 처리하여 도메인을 분류"""
    print(f"Processing file: {filename}")
    file_path = os.path.join(data_dir, filename)

    try:
        data = pd.read_pickle(file_path)
    except UnicodeDecodeError:
        print(f"UnicodeDecodeError encountered. Trying with 'latin1' encoding for file: {filename}")
        data = pd.read_pickle(file_path, encoding='latin1')  # 'latin1'으로 재시도

    # 도메인별 데이터 저장
    for domain, group in data.groupby('Domain'):
        domain = domain.lower()
        domain_parts = domain.split('.')
        
        # 유효한 도메인 접미사를 찾음
        valid_suffix = find_valid_suffix(domain_parts)
        
        if valid_suffix:
            # 도메인의 유효한 접미사를 기준으로 저장 폴더를 결정
            if is_well_known_tld(valid_suffix):
                folder = os.path.join('TLD', valid_suffix.upper())
            else:
                folder = get_continent_by_country_code(valid_suffix)
                if folder is None:
                    folder = 'UNKNOWN'
        elif len(domain_parts[-1]) > 20:
            folder = 'GARBAGE'
        else:
            folder = 'UNKNOWN'
        
        # Safe domain name을 만들고 파일 저장
        safe_domain = f"{domain_parts[0]}.{valid_suffix}"
        safe_domain = re.sub(r'[^a-z0-9._]', '_', safe_domain)
        domain_file = os.path.join(domain_dir, folder, f"{safe_domain}.pickle")
        
        # Lock을 사용하여 파일 접근을 제어
        with lock:
            if os.path.exists(domain_file):
                try:
                    existing_data = pd.read_pickle(domain_file)
                    group = pd.concat([existing_data, group])
                except (EOFError, KeyError, ValueError):
                    print(f"Error reading {domain_file}. Skipping this file.")
                    continue  # 파일 읽기 오류가 발생하면 스킵
            
            group.to_pickle(domain_file)
    
    # 메모리 해제를 위해 데이터프레임 삭제
    del data
    gc.collect()
