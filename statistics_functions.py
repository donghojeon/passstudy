import os
import pandas as pd
import gc

def process_pickle_file(pickle_file):
    """단일 pickle 파일을 로드하여 통계를 계산합니다."""
    data = pd.read_pickle(pickle_file)

    # ID 및 PW 통계 계산
    unique_ids = set(data['ID'].unique())
    unique_passwords = set(data['PW'].unique())
    total_id_length = data['ID'].str.len().sum()
    total_pw_length = data['PW'].str.len().sum()

    # pickle 파일 내 데이터 수
    domain_size = len(data)

    # 도메인 이름을 추출 (pickle 파일명에서 확장자 제거)
    domain_name = os.path.splitext(os.path.basename(pickle_file))[0]

    # 메모리 해제
    del data
    gc.collect()

    # 통계 결과 반환
    return {
        'Unique IDs': unique_ids,
        'Unique Passwords': unique_passwords,
        'Total ID Length': total_id_length,
        'Total PW Length': total_pw_length,
        'Domain Size': domain_size,
        'Domain Name': domain_name  # 도메인 이름 추가
    }


def aggregate_folder_statistics(folder_results):
    """여러 pickle 파일의 통계 결과를 집계합니다."""
    domain_count = len(folder_results)
    all_unique_ids = set()
    all_unique_passwords = set()
    total_id_length = 0
    total_pw_length = 0
    domain_sizes = {}

    for result in folder_results:
        all_unique_ids.update(result['Unique IDs'])
        all_unique_passwords.update(result['Unique Passwords'])
        total_id_length += result['Total ID Length']
        total_pw_length += result['Total PW Length']
        domain_name = result['Domain Name']
        domain_size = result['Domain Size']
        domain_sizes[domain_name] = domain_size

    # 상위 10개 도메인 계산
    top_domains = sorted(domain_sizes.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'Domain Count': domain_count,
        'Unique ID Count': len(all_unique_ids),
        'Unique Password Count': len(all_unique_passwords),
        'Average ID Length': total_id_length / sum(len(result['Unique IDs']) for result in folder_results) if folder_results else 0,
        'Average PW Length': total_pw_length / sum(len(result['Unique Passwords']) for result in folder_results) if folder_results else 0,
        'Top 10 Domains': top_domains  # 도메인 이름과 크기 페어 추가
    }


def save_to_excel(all_stats, output_file):
    """통계 데이터를 엑셀 파일로 저장합니다."""
    # 엑셀 파일로 저장할 데이터 준비
    stats_data = []
    for stats in all_stats:
        row = {
            'Folder': stats['Folder'],
            'Domain Count': stats['Domain Count'],
            'Unique ID Count': stats['Unique ID Count'],
            'Unique Password Count': stats['Unique Password Count'],
            'Average ID Length': stats['Average ID Length'],
            'Average PW Length': stats['Average PW Length'],
            # 수정된 부분: Top 10 Domains 출력 형식 변경
            'Top 10 Domains': ", ".join([f"{domain}: {count}" for domain, count in stats['Top 10 Domains']])
        }
        stats_data.append(row)

    # Pandas DataFrame으로 변환
    df = pd.DataFrame(stats_data)

    # 엑셀 파일로 저장
    df.to_excel(output_file, index=False)
