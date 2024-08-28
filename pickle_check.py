import pandas as pd

def analyze_pickle_file(file_path):
    # .pickle 파일을 불러옵니다.
    try:
        data = pd.read_pickle(file_path)
    except Exception as e:
        print(f"Error reading the pickle file: {e}")
        return

    # 데이터의 길이(행의 수)를 출력합니다.
    length = len(data)
    print(f"Number of rows in the data: {length}")
    
    # 간단한 통계를 출력합니다.
    print("\nBasic statistics:")
    print(data.describe(include='all'))
    
    # 데이터의 첫 몇 줄을 출력합니다.
    print("\nFirst few rows of the data:")
    print(data.head())

    # 데이터프레임의 전체 정보
    print("\nDataFrame Information:")
    print(data.info())

def main():
    # 파일명을 사용자로부터 입력받습니다.
    file_path = input("Enter the path to the pickle file: ")
    
    # 입력받은 파일명으로 분석을 수행합니다.
    analyze_pickle_file(file_path)

if __name__ == '__main__':
    main()