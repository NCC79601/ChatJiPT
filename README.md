![](img/ChatJiPT-logo.svg)

![version](https://img.shields.io/badge/version-0%2E1-yellow?style=flat-square) [![developer](https://img.shields.io/badge/developer-zhw-blue?style=flat-square)](https://github.com/NCC79601) ![wechat](https://img.shields.io/badge/WeChat-v3%2E9%2E9%2E27-g?style=flat-square&logo=wechat) ![windows](https://img.shields.io/badge/Windows-10%20%2F%2011-blue?style=flat-square&logo=windows)

## 1. 环境搭建

以 Windows 为例，使用 Conda 进行 Python 虚拟环境的管理，执行：

```shell
conda create -n langchain python=3.11.7
conda activate langchain
```

接下来安装依赖项，执行：

```shell
cd frontend
pip install -r requirements.txt
cd ../backend
pip install -r requirements.txt 
pip install -r requirements_api.txt
pip install -r requirements_webui.txt  
cd ..
conda install jq
```

### 2. 未完待续