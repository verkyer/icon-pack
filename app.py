from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import re
import logging

# 显式指定 static_folder 为 'static' 文件夹
app = Flask(__name__, template_folder='.', static_folder='static')
app.logger.setLevel(logging.ERROR)

BASE_DIR = 'images'

# 默认值：
SITE_NAME = os.environ.get('SITE_NAME', 'icon-pack')
COPYRIGHT = os.environ.get('COPYRIGHT', 'Created by <a href="https://github.com/verkyer/icon-pack" target="_blank" rel="noopener noreferrer">@icon-pack</a>.')

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
        # 获取分类列表并进行排序
        categories = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith('.')])
    except OSError as e:
        app.logger.error(f"Could not read categories directory: {e}")
        return {}

    for category in categories:  # 按照排序后的分类顺序处理
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
        icon_data[category] = category_icons  # 使用排序后的分类作为键
    return icon_data

@app.route('/')
def index():
    icon_data = get_icon_data(BASE_DIR)
    categories = list(icon_data.keys())  # 获取排序后的分类列表
    logo_img = os.environ.get('LOGO_IMG', 'favicon.ico')
    return render_template('template.html',
                           siteName=SITE_NAME,
                           logoImg=logo_img,
                           iconData=icon_data,
                           categories=categories,
                           copyright=COPYRIGHT)

# 新增 logo 路由
@app.route('/logo')
def logo():
    logo_img_path = os.environ.get('LOGO_IMG', 'favicon.ico')
    if logo_img_path.startswith(('http://', 'https://')):
        return redirect(logo_img_path)
    if os.path.isfile(logo_img_path):
        return send_from_directory('.', logo_img_path)
    images_dir_logo_path = os.path.join('images', logo_img_path)
    if os.path.isfile(images_dir_logo_path) and is_valid_path(images_dir_logo_path, BASE_DIR):
        return send_from_directory('.', images_dir_logo_path)
    return send_from_directory(app.static_folder, logo_img_path)

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
