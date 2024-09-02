import pandas as pd

def count_chars_bit(password):
    """비밀번호의 문자 유형을 비트마스크로 계산하여 복잡도 레벨을 반환합니다."""
    upper, lower, number, special = 0, 0, 0, 0
    
    for char in password:
        if 'A' <= char <= 'Z':
            upper = 0b100
        elif 'a' <= char <= 'z':
            lower = 0b1
        elif '0' <= char <= '9':
            number = 0b10
        else:
            special = 0b1000

    # 비트마스크 합산 결과 반환
    return upper + lower + number + special

def classify_password_complexity(password_list):
    """비밀번호 목록을 16가지 복잡도 레벨로 분류합니다."""
    complexity_levels = {
        0b0001: 'lowonly',
        0b0010: 'numonly',
        0b0100: 'uponly',
        0b1000: 'spconly',
        0b0011: 'lownum',
        0b0101: 'uplow',
        0b0110: 'upnum',
        0b1001: 'spclow',
        0b1010: 'spcnum',
        0b1100: 'spcup',
        0b0111: 'upnumlow',
        0b1011: 'spcnumlow',
        0b1101: 'spcuplow',
        0b1110: 'spcupnum',
        0b1111: 'all'
    }

    classified_passwords = {level: [] for level in complexity_levels.values()}
    
    for password in password_list:
        complexity_bit = count_chars_bit(password)
        complexity_level = complexity_levels.get(complexity_bit, 'unknown')
        classified_passwords[complexity_level].append(password)
    
    return classified_passwords

def calculate_complexity_statistics(password_series):
    """각 복잡도 레벨별로 비밀번호의 빈도, 평균 길이, 최대/최소 길이 등을 계산합니다."""
    classified_passwords = classify_password_complexity(password_series)
    
    complexity_stats = {}
    
    for level, passwords in classified_passwords.items():
        if passwords:
            lengths = [len(pw) for pw in passwords]
            complexity_stats[level] = {
                'count': len(passwords),
                'total_length': sum(lengths),
                'max_length': max(lengths),
                'min_length': min(lengths)
            }
        else:
            complexity_stats[level] = {
                'count': 0,
                'total_length': 0,
                'max_length': 0,
                'min_length': 0
            }
    
    return complexity_stats
