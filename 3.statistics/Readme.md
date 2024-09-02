아래는 statistics_main.py, statistics_functions.py, complexity_analysis.py 파일의 동작 과정을 텍스트와 블록 다이어그램을 사용하여 설명한 내용입니다. 



[statistics_main.py]
전체 통계 작업을 관리
1. main()
로깅 설정: setup_logging()을 호출하여 로그 파일을 설정합니다.
폴더 목록 설정: TLD 및 대륙별 폴더 목록을 설정합니다.
폴더별 통계 처리: process_folder()를 호출하여 각 폴더의 pickle 파일을 처리하고 통계를 생성합니다.
엑셀 파일 저장: save_to_excel()을 호출하여 통계 결과를 엑셀 파일로 저장합니다.

2.setup_logging()
프로그램의 실행 상태를 기록하기 위한 로그 설정을 수행

3.determine_max_workers()
시스템 CPU코어 수를 기반으로 병렬 작업에 사용할 'MAX_workers'수를 사용자의 의견으로 결정.
어떤 프로그램의 경우 전체 코어를 모두 사용하지 않더라도 memory를 모두 사용할 수 있기 떄문에 CPU코어 숫자는 경험적으로 결정하는 것이 좋아보인다.

4.process_foler(folder_path)
입력으로 받은 디렉토리 내의 모든 'pickle'파일을 병렬로 처리하고, 그 결과를 집계한다.
pickle 파일 목록 수집: 폴더 내 모든 pickle 파일을 리스트로 수집합니다.
병렬 처리: ProcessPoolExecutor를 사용하여 각 pickle 파일을 병렬로 처리합니다.
결과 수집 및 집계: 처리된 파일의 통계를 수집하고, aggregate_folder_statistics()를 통해 폴더 단위의 통계로 집계합니다.

[statistics_functions.py]
1.process_pickle_file(pickle_file)
개별 pickle 파일을 로드하여 ID, PW 통계를 계산하고, 비밀번호 복잡도 분석을 수행

