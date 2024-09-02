import os
from statistics_functions2 import process_pickle_file, save_to_excel, aggregate_folder_statistics
from concurrent.futures import ProcessPoolExecutor, as_completed
import logging
import multiprocessing
import time

def setup_logging():
    logging.basicConfig(
        filename='statistics_processing.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def determine_max_workers():
    # CPU 코어 수를 기반으로 max_workers 설정 (시스템 리소스 보호를 위해 CPU 코어 수보다 적게 설정)
    cpu_count = multiprocessing.cpu_count()
    return max(2, cpu_count - 1)  # 최소 2개, 최대 CPU 코어 수 - 1

def process_folder(folder_path):
    pickle_files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith('.pickle')]
    folder_results = []

    with ProcessPoolExecutor(max_workers=determine_max_workers()) as executor:
        future_to_file = {executor.submit(process_pickle_file, file): file for file in pickle_files}

        for future in as_completed(future_to_file):
            file = future_to_file[future]
            try:
                result = future.result()
                folder_results.append(result)
                logging.info(f"Successfully processed {file}")
            except Exception as exc:
                logging.error(f"Error processing {file}: {exc}")

    # 폴더별 통계 집계 및 반환
    return aggregate_folder_statistics(folder_results)

def main():
    start_time = time.time()
    setup_logging()
    logging.info("Starting statistics processing...")

    base_dir = '../2.classification/domainSeparated4/'
    output_file = './domain_statistics.xlsx'


#    target_folders = [
#        'TLD/COM', 'TLD/NET', 'TLD/EDU', 'TLD/GOV', 'TLD/INT', 'TLD/MIL', 'TLD/ORG',
#        'AFRICA', 'ASIA', 'EUROPE', 'N_AMERICA', 'S_AMERICA', 'OCEANIA'
#    ]

    target_folders = [
        'TLD/EDU', 'TLD/GOV', 'TLD/INT', 'TLD/MIL', 'TLD/ORG',
        'AFRICA', 'ASIA', 'N_AMERICA', 'S_AMERICA', 'OCEANIA'
    ]

    all_stats = []

    for folder in target_folders:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            logging.info(f"Processing folder: {folder_path}")
            folder_stats = process_folder(folder_path)
            folder_stats['Folder'] = folder  # 폴더 이름 추가
            all_stats.append(folder_stats)
        else:
            logging.warning(f"Folder does not exist: {folder_path}")

    # 엑셀 파일로 저장
    save_to_excel(all_stats, output_file)
    logging.info(f"Statistics saved to {output_file}")
    logging.info("Statistics processing completed.")

    end_time = time.time()
    elapsed_time = end_time - start_time
    logging.info(f"Statistics processing completed in {elapsed_time:.2f} seconds.")
    print(f"Statistics processing completed in {elapsed_time:.2f} seconds.")
    
if __name__ == "__main__":
    main()
