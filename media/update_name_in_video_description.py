# pip install ffmpeg-python
# 
# Обходит каталог, который указан в константе, выбирает все видео файлы и 
# заполняет в описании файла наименование по имени файла без расширения

import os
import subprocess
from mutagen.mp4 import MP4

# Константы
VIDEO_DIR = "/media/lastinm/1C_COURCES/ПЛАТФОРМА 1С/РАЗРАБОТЧИК 1С/МОДУЛЬ 5. СКД/СКД - ОБЯЗАТЕЛЬНОЕ К ПРОСМОТРУ"  # Основной каталог для обработки
MAX_DEPTH = 1  # Максимальная глубина вложенности (0 - только основной каталог)
VIDEO_EXTENSIONS = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')  # Поддерживаемые форматы
USE_FFMPEG = True  # Использовать ffmpeg для не-MP4 файлов

def update_video_metadata():
    """Обходит каталоги и обновляет метаданные видеофайлов"""
    processed_files = 0
    errors = 0
    
    for depth, (root, dirs, files) in enumerate(os.walk(VIDEO_DIR)):
        # Контроль глубины обхода
        if MAX_DEPTH > 0 and depth >= MAX_DEPTH:
            del dirs[:]  # Прекращаем углубляться
            continue
        
        for file in files:
            if not file.lower().endswith(VIDEO_EXTENSIONS):
                continue
                
            file_path = os.path.join(root, file)
            filename_without_ext = os.path.splitext(file)[0]
            
            try:
                # Обработка MP4 файлов
                if file.lower().endswith('.mp4'):
                    video = MP4(file_path)
                    video["\xa9nam"] = filename_without_ext  # Название
                    video["\xa9cmt"] = filename_without_ext  # Комментарий
                    video.save()
                    processed_files += 1
                    print(f"✓ Успешно: {file_path}")
                
                # Обработка других форматов через ffmpeg
                elif USE_FFMPEG:
                    temp_file = f"{file_path}.temp"
                    
                    cmd = [
                        'ffmpeg',
                        '-i', file_path,
                        '-c', 'copy',
                        '-metadata', f'title={filename_without_ext}',
                        '-metadata', f'comment={filename_without_ext}',
                        '-loglevel', 'error',
                        '-y',
                        temp_file
                    ]
                    
                    subprocess.run(cmd, check=True)
                    os.replace(temp_file, file_path)
                    processed_files += 1
                    print(f"✓ Обработан (ffmpeg): {file_path}")
                
            except subprocess.CalledProcessError as e:
                errors += 1
                print(f"× Ошибка ffmpeg: {file_path} - {str(e)}")
            except Exception as e:
                errors += 1
                print(f"× Ошибка обработки: {file_path} - {str(e)}")
    
    print(f"\nИтог: обработано {processed_files} файлов, ошибок: {errors}")

if __name__ == "__main__":
    update_video_metadata()