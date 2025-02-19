# icon-pack
[xg-icons](https://github.com/verkyer/xg-icons) 的 Python 重构版本，解决了 NAS 部署的权限问题！
容器内的`端口`和`路径`有变化，注意修改！
## 界面展示
![image](https://github.com/verkyer/xg-icons/blob/main/demo.png)
## 参照Yaml
- ghcr
```
services:
  icons-pack:
    container_name: icons-pack
    image: ghcr.io/verkyer/icon-pack:latest
    ports:
      - "28080:5000"
    volumes:
      - ./images:/app/images #图标目录
    environment:
      - SITE_NAME=icons-pack #网站标题
      #- LOGO_IMG=favicon.ico  # 设置站点logo（路径或网址）
```
- dockerhub
```
services:
  icons-pack:
    container_name: icons-pack
    image: verky/icon-pack:latest
    ports:
      - "28080:5000"
    volumes:
      - ./images:/app/images #图标目录
    environment:
      - SITE_NAME=icons-pack #网站标题
      #- LOGO_IMG=favicon.ico  # 设置站点logo（路径或网址）
```
JPG、PNG图标，需要放到`/images/分组目录`文件下；
例如`/images/docker/1.png`，才会显示在首页`docker`分类下面。
## 环境变量
- `SITE_NAME`：网站标题，留空则默认显示；
- `LOGO_IMG`：网站logo和网页标签小图标，网址或根目录下的文件。