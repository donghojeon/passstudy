import os
import multiprocessing
from domainClass_function import process_file
from concurrent.futures import ProcessPoolExecutor
import time

def main():
    data_dir = './noiseCleanedTmp/'
    domain_dir = './domainSeparated2/'

    # TLD와 대륙별 폴더 생성
    tld_folders = ['com', 'org', 'net', 'int', 'edu', 'gov', 'mil', 'arpa']
    continents = ['AFRICA', 'ASIA', 'S_AMERICA', 'N_AMERICA', 'EUROPE', 'OCEANIA']
    other_folders = ['UNKNOWN', 'GARBAGE']

    for folder in tld_folders:
        os.makedirs(os.path.join(domain_dir, 'TLD', folder.upper()), exist_ok=True)

    for continent in continents:
        os.makedirs(os.path.join(domain_dir, continent), exist_ok=True)

    for folder in other_folders:
        os.makedirs(os.path.join(domain_dir, folder), exist_ok=True)

    # 병렬 처리로 pickle 파일 처리
    pickle_files = [filename for filename in sorted(os.listdir(data_dir)) if filename.endswith('.pickle')]

    # CPU 코어 수에 따라 적절한 병렬 작업 수 설정
    cpu_count = multiprocessing.cpu_count()
    max_workers = max(2, cpu_count - 1)  # 코어 수에서 1을 뺀 값 사용, 최소값 2 보장

    start_time = time.time()  # 전체 작업 시작 시간 기록

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_file, filename, data_dir, domain_dir): filename for filename in pickle_files}

        # 주기적으로 작업 상태를 출력
        for i, future in enumerate(futures, 1):
            filename = futures[future]
            try:
                result = future.result()
                print(f"Completed processing: {filename}")
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
            
            if (i % 5 == 0) or (i == len(pickle_files)):
                elapsed_time = time.time() - start_time
                print(f"Processed {i} files out of {len(pickle_files)}. Elapsed time: {elapsed_time:.2f} seconds.")

    total_elapsed_time = time.time() - start_time  # 전체 작업 종료 시간 계산
    print(f"All files processed. Total elapsed time: {total_elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    main()
