import cv2
import os
import numpy as np
from PIL import Image

def convert_png_to_jpg(image_path):
    # 打开PNG文件
    with Image.open(image_path) as img:
        # 转换为RGB模式
        rgb_img = img.convert('RGB')
        # 构建新的JPG文件名
        jpg_image_path = image_path.rsplit('.', 1)[0] + '.jpg'
        # 保存为JPG格式
        rgb_img.save(jpg_image_path, 'JPEG')
        print(f"文件 {image_path} 已转换为 {jpg_image_path}")

def process_image_in_directory(directory):
    # 获取目录中的所有文件名
    files = os.listdir(directory)
    if len(files) != 1:
        print("目录中没有文件或有多于一个文件")
        return

    image_file = files[0]
    image_path = os.path.join(directory, image_file)

    if image_file.endswith(".png"):
        convert_png_to_jpg(image_path)
    elif image_file.endswith(".jpg") or image_file.endswith(".jpeg"):
        print(f"文件 {image_path} 无需转换")
    else:
        print(f"文件 {image_path} 不是有效的图像文件")


def get_image_filename(folder_path):
    """
    获取指定文件夹中的一张图片的文件名

    参数:
    folder_path (str): 文件夹路径

    返回:
    str: 图片文件名, 如果没有找到图片文件则返回None
    """
    # 支持的图片文件扩展名
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 获取文件的扩展名
        ext = os.path.splitext(filename)[1].lower()
        # 如果文件是图片文件，则返回文件名
        if ext in image_extensions:
            return os.path.splitext(filename)[0]
    
    # 如果没有找到图片文件，则返回None
    return None


def video_to_images(video_path, output_folder, target_size=(320, 480)):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Unable to open video file")
        return

    # 获取视频帧率和总帧数
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 读取并保存每一帧图片
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

         # 调整图片大小
        resized_frame = cv2.resize(frame, target_size)

        # 将帧保存为图片文件
        image_path = f"{output_folder}/frame_{frame_count:05d}.jpg"
        cv2.imwrite(image_path, resized_frame)

        frame_count += 1

    # 关闭视频文件
    cap.release()
    print(f"Video to images conversion completed. Total frames: {frame_count}")

def create_subfolder(parent_folder, subfolder_name):
    """
    在指定的文件夹中创建一个子文件夹

    参数:
    parent_folder (str): 父文件夹路径
    subfolder_name (str): 子文件夹名称

    返回:
    str: 新创建的子文件夹路径
    """
    # 构建子文件夹的完整路径
    subfolder_path = os.path.join(parent_folder, subfolder_name)

    # 如果子文件夹不存在，则创建它
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
        print(f"子文件夹 '{subfolder_path}' 创建成功")
    else:
        print(f"子文件夹 '{subfolder_path}' 已经存在")

    return subfolder_path

def extract_first_frame(video_path, output_path):
    """
    从视频中提取第一帧并保存为图片

    参数:
    video_path (str): 视频文件路径
    output_path (str): 保存图片的路径

    返回:
    bool: 成功返回True，失败返回False
    """
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    
    # 检查视频是否成功打开
    if not cap.isOpened():
        print("Error: Unable to open video file:", video_path)
        return False

    # 读取第一帧
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to read the first frame from video:", video_path)
        return False

    # 保存第一帧为图片
    cv2.imwrite(output_path, frame)
    
    # 关闭视频文件
    cap.release()
    return True

def merge_frames_and_save(video1_path, video2_path, output_path):
    """
    提取两个视频的第一帧，将它们左右拼接成一张图片并保存

    参数:
    video1_path (str): 第一个视频文件路径
    video2_path (str): 第二个视频文件路径
    output_path (str): 保存拼接图片的路径
    """
    # 提取第一个视频的第一帧
    first_frame_path_1 = "/tmp/first_frame_1.jpg"
    if not extract_first_frame(video1_path, first_frame_path_1):
        return
    
    # 提取第二个视频的第一帧
    first_frame_path_2 = "/tmp/first_frame_2.jpg"
    if not extract_first_frame(video2_path, first_frame_path_2):
        return
    
    # 读取第一帧图片
    first_frame_1 = cv2.imread(first_frame_path_1)
    first_frame_2 = cv2.imread(first_frame_path_2)

    # 检查是否成功读取图片
    if first_frame_1 is None or first_frame_2 is None:
        print("Error: Unable to read extracted frames")
        return
    
    # 获取图片尺寸
    height, width, _ = first_frame_1.shape

    # 调整第二帧的大小以匹配第一帧
    first_frame_2 = cv2.resize(first_frame_2, (width, height))

    # 将两张图片左右拼接成一张新的图片
    merged_image = np.concatenate([first_frame_1, first_frame_2], axis=1)

    # 保存拼接后的图片
    cv2.imwrite(output_path, merged_image)
    print(f"Merged image saved to {output_path}")


def merge_frames(first_frame_path, last_frame_path, output_path):
    # 读取第一帧和最后一帧图片
    first_frame = cv2.imread(first_frame_path)
    last_frame = cv2.imread(last_frame_path)

    # 获取图片尺寸
    height, width, _ = first_frame.shape

    # 将两张图片左右拼接成一张新的图片
    merged_image = np.concatenate([first_frame, last_frame], axis=1)

    # 保存拼接后的图片
    cv2.imwrite(output_path, merged_image)



# 设置视频文件路径和输出文件夹路径
#video_path = "/home/ubuntu/3d-photo-inpainting/video/Fig1_circle5.mp4"
#output_folder = "/home/ubuntu/imgToVideo/outImgs9"

# 指定目标图片大小或像素
#target_size = (320, 480)

# 调用函数进行视频转图片
#video_to_images(video_path, output_folder, target_size)

