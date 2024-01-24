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
