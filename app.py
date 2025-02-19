from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import re
import logging

# 显式指定 static_folder 为 'static' 文件夹
app = Flask(__name__, template_folder='.', static_folder='static')
app.logger.setLevel(logging.ERROR)

BASE_DIR = 'images'
# LOGO_IMG = 'favicon.ico'  #  移除此处默认值，从环境变量获取
SITE_NAME = os.environ.get('SITE_NAME', 'xg-icons')
COPYRIGHT = os.environ.get('COPYRIGHT', 'Created by <a href="https://github.com/verkyer/xg-icons" target="_blank" rel="noopener noreferrer">@xg-icons</a>.')

def is_valid_path(path, base_dir):
    base_path = os.path.realpath(base_dir)
    file_path = os.path.realpath(path)
    return file_path.startswith(base_path)

def custom_filename_sort(filename):
    """自定义文件名排序函数"""
    match = re.match(r'^(.*?)-(\d+)\.', filename)
    if match:
        base_name, number_str = match.groups()
        number = int(number_str)
        return (base_name, number)
    else:
        base_name = os.path.splitext(filename)[0]
        return (base_name, 0)


def get_icon_data(base_dir):
    icon_data = {}
    try:
        categories = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith('.')]
    except OSError as e:
        app.logger.error(f"Could not read categories directory: {e}")
        return {}

    for category in categories:
        category_path = os.path.join(base_dir, category)
        try:
            images = [img for img in os.listdir(category_path) if re.search(r'\.(jpg|jpeg|png|gif)$', img, re.IGNORECASE)]
        except OSError as e:
            app.logger.warning(f"Could not read images in category '{category}': {e}")
            continue

        images.sort(key=custom_filename_sort)

        category_icons = []
        for image in images:
            image_path_relative = os.path.join(BASE_DIR, category, image)
            image_path_full = os.path.join(category_path, image)

            if is_valid_path(image_path_full, BASE_DIR):
                icon_name = os.path.splitext(image)[0]
                category_icons.append({
                    'imagePath': image_path_relative,
                    'iconName': icon_name,
                    'category': category
                })
        icon_data[category] = category_icons
    return icon_data

@app.route('/')
def index():
    icon_data = get_icon_data(BASE_DIR)
    categories = sorted(icon_data.keys())
    logo_img = os.environ.get('LOGO_IMG', 'favicon.ico') # 从环境变量获取，默认值可以是 static 目录下的 favicon.ico
    return render_template('template.html',
                           siteName=SITE_NAME,
                           logoImg=logo_img, # 传递 logoImg 变量的值，而不是直接使用 url_for
                           iconData=icon_data,
                           categories=categories,
                           copyright=COPYRIGHT)

# 新增 logo 路由
@app.route('/logo')
def logo():
    logo_img_path = os.environ.get('LOGO_IMG', 'favicon.ico')

    # 优先判断是否是 URL
    if logo_img_path.startswith(('http://', 'https://')):
        return redirect(logo_img_path) # 如果是 URL，直接重定向

    # 然后判断是否是根目录下的文件
    if os.path.isfile(logo_img_path):
        return send_from_directory('.', logo_img_path)

    # 再判断是否是 images 目录下的文件
    images_dir_logo_path = os.path.join('images', logo_img_path)
    if os.path.isfile(images_dir_logo_path) and is_valid_path(images_dir_logo_path, BASE_DIR):
        return send_from_directory('.', images_dir_logo_path) # 注意这里仍然用 '.'，因为 images 目录是相对于根目录的

    # 最后 fallback 到 static 目录
    return send_from_directory(app.static_folder, logo_img_path)


# 静态文件路由，确保可以访问 static 文件夹下的文件 (保持不变)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)


@app.route('/<path:filename>')
def send_icon(filename):
    if not is_valid_path(filename, BASE_DIR):
        return "File not found", 404
    return send_from_directory('.', filename)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)