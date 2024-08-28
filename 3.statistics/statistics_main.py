import os
from statistics_functions import process_pickle_file, save_to_excel, aggregate_folder_statistics
from concurrent.futures import ProcessPoolExecutor

def main():
    base_dir = './DomainSeparated/'
    output_file = './domain_statistics.xlsx'

    # TLD 하위 폴더 및 대륙별 폴더 목록
    target_folders = ['TLD/COM', 'TLD/NET', 'TLD/EDU', 'TLD/GOV', 'TLD/INT', 'TLD/MIL', 'TLD/ORG'] + \
                     ['AFRICA', 'ASIA', 'EUROPE', 'N_AMERICA', 'S_AMERICA', 'OCEANIA']

    all_stats = []

    # 각 폴더 내의 pickle 파일을 병렬 처리
    with ProcessPoolExecutor() as executor:
        for folder in target_folders:
            folder_path = os.path.join(base_dir, folder)
            pickle_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.pickle')]

            # 각 pickle 파일에 대해 병렬 처리
            futures = {executor.submit(process_pickle_file, pickle_file): pickle_file for pickle_file in pickle_files}

            # 각 pickle 파일에 대한 통계 결과 수집
            folder_results = [future.result() for future in futures]

            # 폴더별 통계를 집계
            folder_stats = aggregate_folder_statistics(folder_results)
            folder_stats['Folder'] = folder  # 폴더 이름 추가
            all_stats.append(folder_stats)

    # 엑셀 파일로 저장
    save_to_excel(all_stats, output_file)

if __name__ == "__main__":
    main()
