# main.py

import os
from domainClass_function import process_file

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

    # 디렉토리 내 모든 pickle 파일을 순차적으로 처리
    for filename in sorted(os.listdir(data_dir)):
        if filename.endswith('.pickle'):
            process_file(filename, data_dir, domain_dir)

if __name__ == "__main__":
    main()
