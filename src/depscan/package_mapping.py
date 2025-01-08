"""
Package name mapping for Python imports.

This module provides a mapping between common import names and their corresponding
PyPI package names. This is useful because sometimes the name used to import a package
is different from the name used to install it via pip.

Example:
    Import name 'PIL' maps to PyPI package name 'pillow'
    Import name 'cv2' maps to PyPI package name 'opencv-python'
"""

PACKAGE_NAME_MAPPING = {
    # 图像处理
    'PIL': 'pillow',
    'cv2': 'opencv-python',
    
    # 科学计算
    'sklearn': 'scikit-learn',
    'skimage': 'scikit-image',
    'nx': 'networkx',
    
    # 数据处理
    'bs4': 'beautifulsoup4',
    'yaml': 'pyyaml',
    
    # 深度学习
    'tf': 'tensorflow',
    'torch': 'pytorch',
    'mx': 'mxnet',
    'paddle': 'paddlepaddle',
    
    # 数据库
    'psycopg2': 'psycopg2-binary',
    'pymysql': 'PyMySQL',
    
    # UI相关
    'tk': 'tkinter',
    'wx': 'wxPython',
    'qt': 'PyQt5',
    
    # 系统相关
    'win32com': 'pywin32',
    'winreg': 'pywin32',
    
    # 科学计算
    'np': 'numpy',
    'pd': 'pandas',
    'plt': 'matplotlib',
    
    # 网络相关
    'urllib3': 'urllib3',
    'requests': 'requests',
    'aiohttp': 'aiohttp',
    
    # 文本处理
    'docx': 'python-docx',
    'pptx': 'python-pptx',
    'xlrd': 'xlrd',
    'xlwt': 'xlwt',
    'openpyxl': 'openpyxl',
    
    # 音视频处理
    'cv': 'opencv-python',
    'imageio': 'imageio',
    'moviepy': 'moviepy',
    
    # 其他常用
    'dotenv': 'python-dotenv',
    'jwt': 'PyJWT',
    'redis': 'redis-py',
    'magic': 'python-magic',
    'ldap': 'python-ldap',
    'crypto': 'pycrypto',
    'cryptography': 'cryptography',
    'dateutil': 'python-dateutil',
    'h5py': 'h5py',
    'yaml': 'PyYAML',
    'toml': 'toml',
    'ujson': 'ujson',
    'msgpack': 'msgpack-python',
    'zmq': 'pyzmq',
}

def get_package_name(import_name: str) -> str:
    """
    Get the PyPI package name for a given import name.
    
    Args:
        import_name: The name used in the import statement
        
    Returns:
        The corresponding PyPI package name, or the original import name if no mapping exists
    """
    return PACKAGE_NAME_MAPPING.get(import_name, import_name) 