import os
import multiprocessing

def calculate_directory_size(path):
    """
    디렉토리 크기를 계산합니다.
    """
    total_size = 0
    for entry in os.scandir(path):
        if entry.is_dir() and entry.name != "System Volume Information":
            total_size += calculate_directory_size(entry.path)
        else:
            total_size += entry.stat().st_size
    return total_size

def get_directory_sizes(path):
    """
    지정된 경로의 모든 하위 디렉토리 크기를 계산하여 딕셔너리 형태로 반환합니다.
    """
    with multiprocessing.Pool() as pool:
        directory_sizes = {path: pool.apply_async(calculate_directory_size, args=(path,)).get()}
        for entry in os.scandir(path):
            if entry.is_dir() and entry.name != "System Volume Information":
                directory_sizes[entry.path] = pool.apply_async(calculate_directory_size, args=(entry.path,)).get()
    return directory_sizes

def old_get_directory_sizes(path):
    """
    지정된 경로의 모든 하위 디렉토리 크기를 계산하여 딕셔너리 형태로 반환합니다.
    """
    directory_sizes = {path: pool.apply_async(calculate_directory_size, args=(path,)).get()}
    for entry in os.scandir(path):
        if entry.is_dir() and entry.name != "System Volume Information":
            directory_sizes[entry.path] = pool.apply_async(calculate_directory_size, args=(entry.path,)).get()
    return directory_sizes

def main():
    """
    메인 함수입니다. 사용자로부터 경로를 입력받아 디렉토리 크기를 계산하고 출력합니다.
    """
    path = input("디렉토리 경로를 입력하세요: ")
    directory_sizes = get_directory_sizes(path)

    # 내림차순 정렬
    sorted_sizes = sorted(directory_sizes.items(), key=lambda item: item[1], reverse=True)

    print("\n디렉토리별 사용 용량 (내림차순):")
    for directory, size in sorted_sizes:
        print(f"{directory}: {size / 1024**3:.2f} GB")

if __name__ == "__main__":
    main()
