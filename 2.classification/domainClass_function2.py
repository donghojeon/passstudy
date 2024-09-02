import os
import pandas as pd
import gc
import re
import time
from continent_mapping import continent_mapping
from multiprocessing import Lock

# Well-known TLDs
well_known_tlds = ["com", "org", "net", "int", "edu", "gov", "mil", "arpa"]

# 파일 접근을 제어하기 위한 Lock 생성
lock = Lock()

def get_continent_by_country_code(code):
    """국가 코드에 따라 대륙을 반환."""
    code = code.upper()
    for continent, countries in continent_mapping.items():
        if code in countries:
            return continent
    return None

def is_well_known_tld(tld):
    """도메인이 well-known TLD인지 확인."""
    return tld.lower() in well_known_tlds

def find_valid_suffix(domain_parts):
    """도메인의 모든 부분을 확인하여 유효한 국가 코드 또는 TLD를 찾음."""
    for part in domain_parts:
        part = part.lower()
        if is_well_known_tld(part) or get_continent_by_country_code(part):
            return part
    return None

def process_file(filename, data_dir, domain_dir):
    """파일을 처리하여 도메인을 분류하고 상태를 로깅합니다."""
    file_path = os.path.join(data_dir, filename)
    print(f"Starting processing file: {filename}")
    start_time = time.time()  # 작업 시작 시간 기록

    try:
        data = pd.read_pickle(file_path)
        print(f"Successfully loaded file: {filename}")
    except Exception as e:
        print(f"Failed to load file: {filename}. Error: {e}")
        return
    
    processed_data = {}  # 메모리 내에서 처리 데이터 저장

    # 도메인별 데이터 처리
    for domain, group in data.groupby('Domain'):
        domain = domain.lower()
        domain_parts = domain.split('.')
        valid_suffix = find_valid_suffix(domain_parts)
        folder = 'UNKNOWN' if not valid_suffix or len(domain_parts[-1]) > 20 else (get_continent_by_country_code(valid_suffix) if not is_well_known_tld(valid_suffix) else 'TLD/' + valid_suffix.upper())

        safe_domain = f"{domain_parts[0]}_{valid_suffix if valid_suffix else 'unknown'}"
        safe_domain = re.sub(r'[^a-z0-9._]', '_', safe_domain)
        domain_file = os.path.join(domain_dir, folder, f"{safe_domain}.pickle")
        
        if domain_file not in processed_data:
            processed_data[domain_file] = group
        else:
            processed_data[domain_file] = pd.concat([processed_data[domain_file], group])

    # 결과 데이터 저장
    for domain_file, df in processed_data.items():
        with lock:
            try:
                if os.path.exists(domain_file):
                    existing_data = pd.read_pickle(domain_file)
                    df = pd.concat([existing_data, df])
                df.to_pickle(domain_file)
                print(f"Saved file to: {domain_file}")
            except Exception as e:
                print(f"Error saving data to {domain_file}: {e}")

    # 메모리 해제
    del data
    gc.collect()
    total_time = time.time() - start_time  # 총 작업 시간 계산
    print(f"Finished processing file: {filename} in {total_time:.2f} seconds")
