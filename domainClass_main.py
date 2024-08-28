import os
from domainClass_function import process_file
from concurrent.futures import ProcessPoolExecutor

def main():
    data_dir = './noiseCleanedtemp/'
    domain_dir = './DomainSeparated/'

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

    with ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_file, filename, data_dir, domain_dir) for filename in pickle_files]

        for future in futures:
            future.result()  # 에러 처리를 위해 결과를 수집

if __name__ == "__main__":
    main()
