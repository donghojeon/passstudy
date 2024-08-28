changing_filename.py 설명
파일 기능: changing_filename.py 스크립트는 특정 디렉토리 내의 파일 이름을 간결하고 규칙적인 형식으로 변경합니다. 예를 들어, 파일 이름에 특정 패턴('-sorted-uniq')이 포함되어 있다면 이를 기반으로 파일 이름을 변경합니다.

주요 기능:

파일 이름에 '-sorted-uniq'가 포함된 파일을 대상으로 합니다.
파일 이름에서 첫 번째 부분을 추출하여 새로운 파일 이름을 생성합니다.
소문자로 시작하면 <base_name>_small.csv로 변경합니다.
대문자로 시작하면 <base_name>_large.csv로 변경합니다.
숫자로 시작하면 <base_name>_number.csv로 변경합니다.
변경된 파일 이름을 출력하고 실제 파일 이름을 변경합니다.
사용 예시: 이 스크립트는 directory 경로에 있는 파일들의 이름을 지정된 규칙에 따라 변경하는데 사용됩니다. 예를 들어, a-sorted-uniq.csv 파일은 a_small.csv로 변경됩니다.


noiseClean.py 설명
파일 기능: noiseClean.py 스크립트는 주어진 CSV 파일들에서 불필요한 데이터를 제거하고, 데이터를 정리한 후 pickle 파일로 저장합니다. 이 과정에서 특정 유효하지 않은 문자들을 필터링하여 데이터를 정리합니다.

주요 기능:

is_string_valid(input_string):

주어진 문자열이 유효한지 확인합니다. 문자열의 모든 문자가 허용된 문자 집합(AVAILABLE_CHARS)에 포함되어 있는지 검증합니다.
유효하지 않은 경우 NaN으로 대체합니다.
process_file(file, input_dir, output_dir, colnames):

지정된 CSV 파일을 읽고, 노이즈를 제거한 후 pickle 포맷으로 저장합니다.
NaN 데이터를 제거하고, 각 열의 값을 검증하여 유효하지 않은 데이터를 제거합니다.
처리된 파일을 output_dir에 저장하며, 이미 존재하는 파일은 처리를 스킵합니다.
display_cleaned_file_sizes(file, output_dir):

처리된 pickle 파일의 데이터 크기를 확인하고 출력합니다.
main():

스크립트의 메인 함수로, 지정된 디렉토리 내의 모든 CSV 파일을 처리하고 정리된 데이터를 pickle 파일로 저장합니다.
데이터 전처리가 완료된 후, 각 pickle 파일의 크기를 출력합니다.
사용 예시: 이 스크립트는 /rawdata/ 디렉토리에 있는 CSV 파일들을 대상으로 작동하며, 노이즈 제거 후의 파일들은 /noiseCleaned/ 디렉토리에 pickle 파일로 저장됩니다. 전처리된 데이터의 크기를 확인할 수 있습니다.

