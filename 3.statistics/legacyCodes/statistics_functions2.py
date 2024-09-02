import os
import pandas as pd
import gc
import logging
from complexity_analysis import classify_password_complexity, calculate_complexity_statistics

def process_pickle_file(pickle_file):
    """단일 pickle 파일을 로드하여 통계를 계산합니다."""
    try:
        logging.info(f"Loading pickle file: {pickle_file}")
        data = pd.read_pickle(pickle_file)

        # ID 및 PW 통계 계산
        unique_ids = set(data['ID'].unique())
        unique_passwords = set(data['PW'].unique())
        total_id_length = data['ID'].str.len().sum()
        total_pw_length = data['PW'].str.len().sum()
        domain_size = len(data)

        # 비밀번호 복잡도 분석
        complexity_stats = calculate_complexity_statistics(data['PW'])

        # 도메인 이름을 추출 (pickle 파일명에서 확장자 제거)
        domain_name = os.path.splitext(os.path.basename(pickle_file))[0]

        # 메모리 해제
        del data
        gc.collect()

        # 통계 결과 반환
        return {
            'Domain Name': domain_name,
            'Domain Size': domain_size,
            'Unique IDs': unique_ids,
            'Unique Passwords': unique_passwords,
            'Total ID Length': total_id_length,
            'Total PW Length': total_pw_length,
            'Complexity Stats': complexity_stats  # 복잡도 통계 추가
        }

    except Exception as e:
        logging.error(f"Failed to process {pickle_file}: {e}")
        return None

def aggregate_folder_statistics(folder_results):
    """여러 pickle 파일의 통계 결과를 집계합니다."""
    if not folder_results:
        return {}

    domain_count = len(folder_results)
    all_unique_ids = set()
    all_unique_passwords = set()
    total_id_length = 0
    total_pw_length = 0
    domain_sizes = {}
    aggregated_complexity_stats = {}

    for result in folder_results:
        if result is None:
            continue

        all_unique_ids.update(result['Unique IDs'])
        all_unique_passwords.update(result['Unique Passwords'])
        total_id_length += result['Total ID Length']
        total_pw_length += result['Total PW Length']
        domain_name = result['Domain Name']
        domain_size = result['Domain Size']
        domain_sizes[domain_name] = domain_size

        # 복잡도 통계 집계
        for level, stats in result['Complexity Stats'].items():
            if level not in aggregated_complexity_stats:
                aggregated_complexity_stats[level] = stats
            else:
                aggregated_complexity_stats[level]['count'] += stats['count']
                aggregated_complexity_stats[level]['total_length'] += stats['total_length']

    # 상위 10개 도메인 계산
    top_domains = sorted(domain_sizes.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'Domain Count': domain_count,
        'Unique ID Count': len(all_unique_ids),
        'Unique Password Count': len(all_unique_passwords),
        'Average ID Length': total_id_length / len(all_unique_ids) if all_unique_ids else 0,
        'Average PW Length': total_pw_length / len(all_unique_passwords) if all_unique_passwords else 0,
        'Top 10 Domains': top_domains,
        'Aggregated Complexity Stats': aggregated_complexity_stats  # 집계된 복잡도 통계 추가
    }

def save_to_excel(all_stats, output_file):
    """통계 데이터를 엑셀 파일로 저장합니다."""
    try:
        stats_data = []
        complexity_data = []

        for stats in all_stats:
            row = {
                'Folder': stats['Folder'],
                'Domain Count': stats['Domain Count'],
                'Unique ID Count': stats['Unique ID Count'],
                'Unique Password Count': stats['Unique Password Count'],
                'Average ID Length': stats['Average ID Length'],
                'Average PW Length': stats['Average PW Length'],
                'Top 10 Domains': ", ".join([f"{domain}: {count}" for domain, count in stats['Top 10 Domains']])
            }
            stats_data.append(row)

            # 복잡도 통계 데이터를 별도 시트로 저장
            for level, complexity_stats in stats['Aggregated Complexity Stats'].items():
                complexity_row = {
                    'Folder': stats['Folder'],
                    'Complexity Level': level,
                    'Count': complexity_stats['count'],
                    'Total Length': complexity_stats['total_length'],
                    'Average Length': complexity_stats['total_length'] / complexity_stats['count'] if complexity_stats['count'] > 0 else 0
                }
                complexity_data.append(complexity_row)

        # Pandas DataFrame으로 변환
        df_stats = pd.DataFrame(stats_data)
        df_complexity = pd.DataFrame(complexity_data)

        # 엑셀 파일로 저장
        with pd.ExcelWriter(output_file) as writer:
            df_stats.to_excel(writer, sheet_name='Summary', index=False)
            df_complexity.to_excel(writer, sheet_name='Complexity Stats', index=False)

        logging.info(f"Statistics successfully saved to {output_file}")

    except Exception as e:
        logging.error(f"Failed to save statistics to {output_file}: {e}")
