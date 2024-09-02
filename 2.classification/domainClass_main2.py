import os
import multiprocessing
from domainClass_function2 import process_file
from concurrent.futures import ProcessPoolExecutor


def main():
    data_dir = './noiseCleanedTmp/'
    domain_dir = './domainSeparated4/'

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
    max_workers = max(2, cpu_count - 12)  # 코어 수에서 1을 뺀 값 사용, 최소값 2 보장

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_file, filename, data_dir, domain_dir) for filename in pickle_files]

        for future in futures:
            future.result()  # 에러 처리를 위해 결과를 수집

if __name__ == "__main__":
    main()