
"""
현재 경로에 특정 파일이나 디렉토리가 존재하는지를 확인하기 위해 import os를 사용
파일을 이동이나 복사하기 위해 shutil 모듈을 사용하였음
파일 탐색기에서의 잘라내기 기능을 구현함
cut_file 함수는 잘라낼 파일의 경로와 붙여넣을 경로를 매개변수로 함
이때 붙여넣을 경로에 입력이 잘못됐을 경우 에러를 발생시킴
b_is_exit 변수를 0으로 초기화하고
1을 입력하였을때 잘라내기 기능이 구현되도록 함수를 작성하였음
favorites : 즐겨찾기 목록
addFavorite() : 원하는 파일을 즐겨찾기에 추가하는 함수
showFavorites() : 즐겨찾기 안의 파일 목록을 순서대로 출력하는 함수
"""

import os
import shutil
import hashlib
import time
import function
import tkinter as tk
from tkinter import filedialog, messagebox

# 파일 관리 시스템
# - 중복 파일 탐지 및 삭제: 주어진 디렉토리에서 중복 파일을 찾아내고, 중복된 파일을 삭제합니다.
# - 파일 이름 변경: 사용자가 지정한 파일의 이름을 변경합니다.
# - 파일 메타데이터 관리: 파일의 생성 시간, 수정 시간, 파일 크기를 출력합니다.

def manage_metadata(file_path):
    """
    주어진 파일의 메타데이터를 관리합니다.
    """
    # 파일 생성 및 수정 시간 가져오기
    created_time = os.path.getctime(file_path)
    modified_time = os.path.getmtime(file_path)

    # 생성 및 수정 시간을 사람이 읽기 쉬운 형식으로 변환
    created_time_readable = time.ctime(created_time)
    modified_time_readable = time.ctime(modified_time)

    # 파일 크기 가져오기
    file_size = os.path.getsize(file_path)

    # 파일 메타데이터 출력
    print(f"File: {file_path}")
    print(f"Created Time: {created_time_readable}")
    print(f"Modified Time: {modified_time_readable}")
    print(f"Size: {file_size} bytes")

def find_duplicates(directory):
    """
    주어진 디렉토리에서 중복 파일을 찾아내고 중복된 파일의 경로를 반환합니다.
    """
    duplicates = {}
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            # 파일 경로 생성
            filepath = os.path.join(dirpath, filename)
            # 파일 내용의 해시 값 계산
            with open(filepath, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()
            # 해시 값을 이용하여 중복 파일 확인
            if file_hash in duplicates:
                duplicates[file_hash].append(filepath)
            else:
                duplicates[file_hash] = [filepath]
    # 중복된 파일만 반환
    return {hash: paths for hash, paths in duplicates.items() if len(paths) > 1}

def remove_duplicates(duplicates):
    """
    중복된 파일을 삭제합니다.
    """
    for _, duplicate_paths in duplicates.items():
        for path in duplicate_paths[1:]:
            # 중복된 파일 삭제
            os.remove(path)
            print(f"Deleted: {path}")

# 지정한 파일을 삭제하는 함수
def delete_file(path):
    """
    파일의 경로를 받아 해당 파일을 삭제
    
    Args:
        path (str): 삭제할 파일의 경로
    
    Returns:
        None
    """
    if os.path.exists(path):
        os.remove(path)
        print(f"{path} 파일이 삭제되었습니다.")
    else:
        print(f"{path} 파일이 존재하지 않습니다.")

def search_file(root_directory, target_filename):
    """
    특정 파일을 파일 시스템에서 검색하는 함수입니다.
    :param root_directory: 검색을 시작할 루트 디렉토리
    :param target_filename: 검색할 파일의 이름
    :return: 파일의 경로 리스트 (파일이 여러 개일 경우)
    """
    matched_files = []

    for dirpath, dirnames, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename == target_filename:
                matched_files.append(os.path.join(dirpath, filename))

    return matched_files

"""
    입력한 경로의 디렉토리 내 파일 크기를 KB, MB처럼 사람이 읽기쉽게 변환하여 보여주는 함수
    매개변수 size_in_bytes: 바이트 단위의 파일 크기
    리턴값 str: 사람이 읽기 쉬운 형식으로 변환된 파일 크기
"""
def get_human_readable_size(size_in_bytes):

    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024

"""
    주어진 디렉토리의 파일 크기를 사람이 읽기 쉬운 형식으로 출력
    매개변수 directory: 디렉토리 경로
    파일 사이즈 출력
"""
def display_file_sizes(directory):
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                size_in_bytes = os.path.getsize(file_path)
                human_readable_size = get_human_readable_size(size_in_bytes)
                print(f"{filename}: {human_readable_size}")
    except Exception as e:
        print(f"Error: {e}")

"""
Moves a file from the source path to the destination path.
@Param
    source : The source file path.
    destination : The destination file path.
@Return
    None
@Raises
    Prints an error message if the operation fails.
"""
def move_file(source, destination):
    try:
        shutil.move(source, destination)
        print(f"Moved file from {source} to {destination}")
    except Exception as e:
        print(f"Error moving file: {e}")

"""
Creates a directory at the specified path.
@Param
    directory_path : The path where the new directory should be created.
@Return
    None
@Raises
    Prints an error message if the operation fails.
"""
def create_directory(directory_path):
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Created directory {directory_path}")
    except Exception as e:
        print(f"Error creating directory: {e}")

"""
Lists all files in the specified directory.
@Param
    directory : The directory path to list files from.
@Return
    A list of filenames in the directory.
@Raises
    Prints an error message if the operation fails and returns an empty list.
"""
def list_files(directory):
    try:
        files = os.listdir(directory)
        print(f"Files in {directory}: {files}")
        return files
    except Exception as e:
        print(f"Error listing files: {e}")
        return []

"""
Gets the parent directory of the specified path.
@Param
    path : The file or directory path.
@Return
    The parent directory path.
"""
def getParentDir(path):
    return os.path.dirname(path)

def copyFile(src, dest):
    try:
        shutil.copy(src, dest)
        print(f"파일이 성공적으로 복사되었습니다: {dest}")
    except Exception as e:
        print(f"파일 복사 중 오류가 발생했습니다: {e}")

def cut_file(source, destination):
    try:
        shutil.move(source, destination)
        print(f"{source} 파일이 {destination}으로 잘라내기 되었습니다.")
    except Exception as e:
        print(f"파일을 이동하는 중 오류가 발생했습니다: {e}")

def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def create_and_write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

favorites = []
def addFavorite():
    path = input("즐겨찾기에 추가할 파일 경로를 입력하세요: ")
    favorites.append(path)
    print("즐겨찾기에 추가되었습니다.")

def showFavorites():
    if not favorites:
        print("현재 즐겨찾기 목록이 비어있습니다.")
    else:
        print("즐겨찾기 목록:")
        for i, favorite in enumerate(favorites, 1):
            print(f"{i}. {favorite}")

 # 파일 시스템을 관리할 리스트
file_system = []

def add_file(file_name):
    """파일을 파일 시스템에 추가합니다."""
    file_system.append(file_name)
    print(f"파일 '{file_name}'이(가) 추가되었습니다.")

def list_files(order='asc'):
    """파일을 저장한 순서대로 나열합니다.
    order: 'asc'는 오름차순, 'desc'는 내림차순
    """
    if order == 'asc':
        sorted_files = file_system
    elif order == 'desc':
        sorted_files = list(reversed(file_system))
    else:
        print("정렬 순서는 'asc' 또는 'desc' 중 하나여야 합니다.")
        return

    for file in sorted_files:
        print(file)

b_is_exit = False

while not b_is_exit:
    func = input("기능 입력 (? 입력시 도움말) : ")

    if func == "1":
        source = input("잘라낼 파일의 경로를 입력하세요: ")
        destination = input("붙여넣을 경로를 입력하세요: ")
        cut_file(source, destination)
        print("잘라내기 완료")

    elif func == "2":
        print("기능 2 실행.")
        # Add functionality for option 2 here

    elif func == "3":
        print("기능 3 실행.")
        # Add functionality for option 3 here

    elif func == "복사":
        src = input("복사할 파일의 경로를 입력하세요: ")
        dest = input("복사할 위치를 입력하세요: ")
        copyFile(src, dest)

    elif func == "?":
        print("도움말: 1을 입력하여 잘라내기(이동)하거나 2, 3을 입력하여 기능을 선택하거나 '복사'를 입력하여 파일을 복사하거나 '종료'를 입력하여 종료합니다.")

    elif func.lower() == "종료":
        b_is_exit = True
        print("프로그램을 종료합니다.")

    else:
        print("알 수 없는 입력입니다. 다시 시도해주세요.")

# 파일 목록과 고정된 파일을 저장할 리스트 초기화
file_list = []  # 파일 목록을 저장할 리스트
pinned_file = None  # 고정된 파일을 저장할 변수

# 파일 추가 함수
def add_file():
    global file_list
    file_path = filedialog.askopenfilename()  # 파일 선택 다이얼로그 열기
    if file_path:
        file_list.append(file_path)  # 선택한 파일을 리스트에 추가
        update_file_listbox()  # 리스트박스를 업데이트

# 파일을 상단에 고정하는 함수
def pin_file():
    global pinned_file, file_list
    selected_file = file_listbox.get(tk.ACTIVE)  # 현재 선택된 파일 가져오기
    if selected_file:
        pinned_file = selected_file  # 선택된 파일을 고정 파일로 설정
        update_file_listbox()  # 리스트박스를 업데이트

# 리스트박스를 업데이트하는 함수
def update_file_listbox():
    global pinned_file, file_list
    file_listbox.delete(0, tk.END)  # 리스트박스 초기화
    if pinned_file:
        file_listbox.insert(tk.END, f"[PINNED] {pinned_file}")  # 고정된 파일을 상단에 표시
    for file in file_list:
        if file != pinned_file:
            file_listbox.insert(tk.END, file)  # 고정되지 않은 파일을 나머지에 표시

# 파일 고정을 해제하는 함수
def unpin_file():
    global pinned_file
    pinned_file = None  # 고정된 파일 해제
    update_file_listbox()  # 리스트박스를 업데이트

# GUI 설정
root = tk.Tk()
root.title("파일 고정 앱")  # 윈도우 제목 설정

# 파일 목록을 표시하는 리스트박스
file_listbox = tk.Listbox(root, width=50, height=15)
file_listbox.pack(pady=10)

# 파일 추가 버튼
add_button = tk.Button(root, text="파일 추가", command=add_file)
add_button.pack(side=tk.LEFT, padx=5)

# 파일 고정 버튼
pin_button = tk.Button(root, text="파일 고정", command=pin_file)
pin_button.pack(side=tk.LEFT, padx=5)

# 파일 고정 해제 버튼
unpin_button = tk.Button(root, text="파일 고정 해제", command=unpin_file)
unpin_button.pack(side=tk.LEFT, padx=5)

# 메인 루프 실행
root.mainloop()

def classify_files_by_extension(source_directory, destination_directory):
    """
    파일 형식에 따라 파일을 분류하여 이동하는 함수

    :param source_directory: 파일들이 있는 소스 디렉토리
    :param destination_directory: 분류된 파일들을 저장할 목적지 디렉토리
    """
    # 소스 디렉토리에서 모든 파일과 디렉토리 가져오기
    for item in os.listdir(source_directory):
        item_path = os.path.join(source_directory, item)
        
        # 파일인 경우에만 처리
        if os.path.isfile(item_path):
            # 파일 확장자 가져오기
            file_extension = os.path.splitext(item)[1][1:].lower()  # 확장자에서 점(.) 제거하고 소문자로 변환
            if file_extension:  # 확장자가 있는 경우
                # 목적지 디렉토리 경로 만들기
                extension_dir = os.path.join(destination_directory, file_extension)
                os.makedirs(extension_dir, exist_ok=True)  # 확장자 디렉토리 생성 (이미 있으면 무시)
                
                # 파일을 목적지 디렉토리로 이동
                shutil.move(item_path, os.path.join(extension_dir, item))
                print(f"Moved: {item} -> {extension_dir}")

                # 파일 목록과 고정된 파일을 저장할 리스트 초기화
file_list = []  # 파일 목록을 저장할 리스트
pinned_file = None  # 고정된 파일을 저장할 변수

# 파일 추가 함수
def add_file():
    global file_list
    file_path = filedialog.askopenfilename()  # 파일 선택 다이얼로그 열기
    if file_path:
        file_list.append(file_path)  # 선택한 파일을 리스트에 추가
        update_file_listbox()  # 리스트박스를 업데이트

# 파일을 상단에 고정하는 함수
def pin_file():
    global pinned_file, file_list
    selected_file = file_listbox.get(tk.ACTIVE)  # 현재 선택된 파일 가져오기
    if selected_file:
        pinned_file = selected_file  # 선택된 파일을 고정 파일로 설정
        update_file_listbox()  # 리스트박스를 업데이트

# 리스트박스를 업데이트하는 함수
def update_file_listbox():
    global pinned_file, file_list
    file_listbox.delete(0, tk.END)  # 리스트박스 초기화
    if pinned_file:
        file_listbox.insert(tk.END, f"[PINNED] {pinned_file}")  # 고정된 파일을 상단에 표시
    for file in file_list:
        if file != pinned_file:
            file_listbox.insert(tk.END, file)  # 고정되지 않은 파일을 나머지에 표시

# 파일 고정을 해제하는 함수
def unpin_file():
    global pinned_file
    pinned_file = None  # 고정된 파일 해제
    update_file_listbox()  # 리스트박스를 업데이트

# GUI 설정
root = tk.Tk()
root.title("파일 고정 앱")  # 윈도우 제목 설정

# 파일 목록을 표시하는 리스트박스
file_listbox = tk.Listbox(root, width=50, height=15)
file_listbox.pack(pady=10)

# 파일 추가 버튼
add_button = tk.Button(root, text="파일 추가", command=add_file)
add_button.pack(side=tk.LEFT, padx=5)

# 파일 고정 버튼
pin_button = tk.Button(root, text="파일 고정", command=pin_file)
pin_button.pack(side=tk.LEFT, padx=5)

# 파일 고정 해제 버튼
unpin_button = tk.Button(root, text="파일 고정 해제", command=unpin_file)
unpin_button.pack(side=tk.LEFT, padx=5)

# 메인 루프 실행
root.mainloop()