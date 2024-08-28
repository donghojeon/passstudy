import os

def shorten_filenames(directory):
    """Rename files to a shorter format like a_small.csv."""
    for filename in os.listdir(directory):
        if '-sorted-uniq' in filename:
            base_name = filename.split('-')[0]  # 'a' 추출
            if base_name.islower():
                new_name = f"{base_name}_small.csv"
            elif base_name.isupper():
                new_name = f"{base_name}_large.csv"
            elif base_name.isdigit():
                new_name = f"{base_name}_number.csv"
                
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, new_name)

            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

# 경로를 적절히 설정하세요
directory = '/mnt/pentapass/updated_codes/passdata'
shorten_filenames(directory)
