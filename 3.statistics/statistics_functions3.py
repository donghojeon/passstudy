import os
import pandas as pd
import gc
import datetime
import logging
from complexity_analysis import classify_password_complexity, calculate_complexity_statistics


def process_pickle_file(pickle_file):
    data = pd.read_pickle(pickle_file)

    unique_ids = set(data['ID'].unique())
    unique_passwords = set(data['PW'].unique())
    total_id_pw_number = len(data)  # ID/PW 쌍의 총 개수
    total_id_length = data['ID'].str.len().sum()
    total_pw_length = data['PW'].str.len().sum()
    domain_size = len(data)

    complexity_stats = calculate_complexity_statistics(data['PW'])

    type_counts = {key: stats['count'] for key, stats in complexity_stats.items()}

    lv1_count = sum(type_counts[key] for key in ['lowonly', 'numonly', 'uponly', 'spconly'])
    lv2_count = sum(type_counts[key] for key in ['lownum', 'uplow', 'upnum', 'spclow', 'spcnum', 'spcup'])
    lv3_count = sum(type_counts[key] for key in ['upnumlow', 'spcnumlow', 'spcuplow', 'spcupnum'])
    lv4_count = type_counts.get('all', 0)

    domain_name = os.path.splitext(os.path.basename(pickle_file))[0]

    del data
    gc.collect()

    return {
        'Domain Name': domain_name,
        'Domain Size': domain_size,
        'Total ID PW Number': total_id_pw_number,  # ID/PW 쌍의 총 개수
        'Unique IDs': unique_ids,
        'Unique Passwords': unique_passwords,
        'Total ID Length': total_id_length,
        'Total PW Length': total_pw_length,
        'Complexity Stats': complexity_stats,
        'Type Counts': type_counts,
        'Lv1 Count': lv1_count,
        'Lv2 Count': lv2_count,
        'Lv3 Count': lv3_count,
        'Lv4 Count': lv4_count
    }


def aggregate_folder_statistics(folder_results):
    domain_count = len(folder_results)
    all_unique_ids = set()
    all_unique_passwords = set()
    total_id_pw_number = 0  # ID/PW 쌍의 총 개수
    total_id_length = 0
    total_pw_length = 0
    domain_sizes = {}
    aggregated_complexity_stats = {}
    aggregated_type_counts = {key: 0 for key in [
        'lowonly', 'numonly', 'uponly', 'spconly',
        'lownum', 'uplow', 'upnum', 'spclow',
        'spcnum', 'spcup', 'upnumlow', 'spcnumlow',
        'spcuplow', 'spcupnum', 'all'
    ]}
    lv1_total = lv2_total = lv3_total = lv4_total = 0

    for result in folder_results:
        all_unique_ids.update(result['Unique IDs'])
        all_unique_passwords.update(result['Unique Passwords'])
        total_id_pw_number += result['Total ID PW Number']  # ID/PW 쌍의 총 개수 누적
        total_id_length += result['Total ID Length']
        total_pw_length += result['Total PW Length']
        domain_name = result['Domain Name']
        domain_size = result['Domain Size']
        domain_sizes[domain_name] = domain_size

        for level, stats in result['Complexity Stats'].items():
            if level not in aggregated_complexity_stats:
                aggregated_complexity_stats[level] = stats
            else:
                aggregated_complexity_stats[level]['count'] += stats['count']
                aggregated_complexity_stats[level]['total_length'] += stats['total_length']

        for key, count in result['Type Counts'].items():
            aggregated_type_counts[key] += count

        lv1_total += result['Lv1 Count']
        lv2_total += result['Lv2 Count']
        lv3_total += result['Lv3 Count']
        lv4_total += result['Lv4 Count']

    top_domains = sorted(domain_sizes.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        'Domain Count': domain_count,
        'Total ID PW Number': total_id_pw_number,  # 누적된 ID/PW 쌍의 총 개수
        'Unique ID Count': len(all_unique_ids),
        'Unique Password Count': len(all_unique_passwords),
        'Average ID Length': total_id_length / total_id_pw_number if total_id_pw_number else 0,  # 전체 ID 수로 나눔
        'Average PW Length': total_pw_length / total_id_pw_number if total_id_pw_number else 0,  # 전체 PW 수로 나눔
        'Top 10 Domains': top_domains,
        'Aggregated Complexity Stats': aggregated_complexity_stats,
        'Aggregated Type Counts': aggregated_type_counts,
        'Lv1 Total': lv1_total,
        'Lv2 Total': lv2_total,
        'Lv3 Total': lv3_total,
        'Lv4 Total': lv4_total
    }




def save_to_excel(all_stats, output_file):
    # 현재 날짜와 시간을 가져와 포맷팅
    now = datetime.datetime.now()
    formatted_time = now.strftime("%m%d_%H%M")  # "0901_1110" 형식으로 포맷팅

    # 파일 이름에 날짜와 시간을 추가
    output_file_with_timestamp = f"statistics_{formatted_time}.xlsx"

    stats_data = []
    complexity_data = []

    complexity_levels = [
        'lowonly', 'numonly', 'uponly', 'spconly',
        'lownum', 'uplow', 'upnum', 'spclow',
        'spcnum', 'spcup', 'upnumlow', 'spcnumlow',
        'spcuplow', 'spcupnum', 'all'
    ]

    for stats in all_stats:
        # Summary 시트를 위한 데이터
        stats_row = {
            'Folder': stats['Folder'],
            'Domain Count': stats['Domain Count'],
            'Total ID PW Number': stats['Total ID PW Number'],
            'Unique ID Count': stats['Unique ID Count'],
            'Unique Password Count': stats['Unique Password Count'],
            'Average ID Length': stats['Average ID Length'],
            'Average PW Length': stats['Average PW Length'],
            'Top 10 Domains': ", ".join([f"{domain}: {count}" for domain, count in stats['Top 10 Domains']]),
            'Lv1 PW Count': stats['Lv1 Total'],
            'Lv2 PW Count': stats['Lv2 Total'],
            'Lv3 PW Count': stats['Lv3 Total'],
            'Lv4 PW Count': stats['Lv4 Total']
        }
        stats_data.append(stats_row)

        # Complexity Stats 시트를 위한 데이터
        complexity_row = {'folder': stats['Folder']}
        for level in complexity_levels:
            complexity_row[f'{level}_count'] = stats['Aggregated Complexity Stats'].get(level, {}).get('count', 0)
            complexity_row[f'{level}_total_length'] = round(stats['Aggregated Complexity Stats'].get(level, {}).get('total_length', 0), 2)
            complexity_row[f'{level}_avg_length'] = round(stats['Aggregated Complexity Stats'].get(level, {}).get('total_length', 0) /
                                                        stats['Aggregated Complexity Stats'].get(level, {}).get('count', 1), 2) \
                                                        if stats['Aggregated Complexity Stats'].get(level, {}).get('count', 0) > 0 else 0
        complexity_data.append(complexity_row)

    df_stats = pd.DataFrame(stats_data)
    df_complexity = pd.DataFrame(complexity_data)

    # Complexity Stats 시트의 구조를 재구성
    complexity_formatted_data = []
    for index, row in df_complexity.iterrows():
        folder = row['folder']
        count_row = {key.split('_')[0]: row[key] for key in row.index if '_count' in key}
        length_row = {key.split('_')[0]: row[key.replace('count', 'total_length')] for key in row.index if '_count' in key}
        avg_length_row = {key.split('_')[0]: row[key.replace('count', 'avg_length')] for key in row.index if '_count' in key}
        
        # 각 폴더에 대해 3개의 행을 추가: count, total length, avg length
        complexity_formatted_data.append({**{'folder': f"{folder} count"}, **count_row})
        complexity_formatted_data.append({**{'folder': f"{folder} total length"}, **length_row})
        complexity_formatted_data.append({**{'folder': f"{folder} avg length"}, **avg_length_row})

    df_complexity_formatted = pd.DataFrame(complexity_formatted_data)

    with pd.ExcelWriter(output_file_with_timestamp) as writer:
        # Summary 시트 작성
        df_stats.to_excel(writer, sheet_name='Summary', index=False)

        # Complexity Stats 시트 작성
        df_complexity_formatted.to_excel(writer, sheet_name='Complexity Stats', index=False)

    logging.info(f"Statistics successfully saved to {output_file_with_timestamp}")
