import os
import pandas as pd
import pickle

# 디렉토리 경로 설정
directory_path = 'noiseCleanedTmp'
max_file_size = 300 * 1024 * 1024  # 300MB in bytes

# 디렉토리 내의 모든 .pickle 파일을 검색
for filename in os.listdir(directory_path):
    if filename.endswith('.pickle'):
        file_path = os.path.join(directory_path, filename)
        
        # 파일 크기 확인
        file_size = os.path.getsize(file_path)
        
        if file_size > max_file_size:
            print(f"Processing large file: {filename}, size: {file_size / (1024 * 1024):.2f} MB")

            # 파일을 DataFrame으로 로드
            with open(file_path, 'rb') as f:
                df = pickle.load(f)
            
            # 파일을 나누기 위해 필요한 덩어리 수 계산
            num_chunks = file_size // max_file_size + 1
            chunk_size = len(df) // num_chunks
            
            # DataFrame을 나누고 각 덩어리를 새 파일로 저장
            for i in range(num_chunks):
                start_index = i * chunk_size
                end_index = (i + 1) * chunk_size if i < num_chunks - 1 else len(df)
                
                # DataFrame의 부분을 선택
                df_chunk = df.iloc[start_index:end_index]
                
                # 새로운 파일 이름 생성
                new_filename = f"{filename.split('.pickle')[0]}_{i+1}.pickle"
                new_file_path = os.path.join(directory_path, new_filename)
                
                # DataFrame 덩어리를 새로운 pickle 파일로 저장
                with open(new_file_path, 'wb') as new_f:
                    pickle.dump(df_chunk, new_f)
                
                print(f"Saved {new_filename}, chunk size: {len(df_chunk)} rows")

        else:
            print(f"File {filename} is already under the size limit: {file_size / (1024 * 1024):.2f} MB")
