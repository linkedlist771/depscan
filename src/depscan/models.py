# dependencies_finder.py
from pathlib import Path
import ast
from typing import Set, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os
from .package_mapping import get_package_name

class DependencyFinder:
    def __init__(self, src_paths: list[str], workers: int = None, no_save: bool = False):
        self.src_paths = src_paths
        self.workers = workers or os.cpu_count()
        self.third_party_imports: Set[str] = set()
        self.no_save = no_save
        self.local_modules: Set[str] = set()
        
    def find_imports_in_file(self, file_path: Path) -> Set[str]:
        """分析单个文件中的导入"""
        encodings = ['utf-8-sig', 'utf-8', 'latin1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                break
            except UnicodeDecodeError:
                continue
                
        if content is None:
            print(f"Warning: Could not decode file {file_path} with any supported encoding")
            return set()
            
        imports = set()
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                # 处理 import xxx 语句
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name.split('.')[0])
                
                # 处理 from xxx import yyy 语句 
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except Exception as e:
            print(f"Error parsing {file_path}: {str(e)}")
            
        return imports

    async def process_files(self) -> Tuple[Set[str], Set[Path]]:
        """并行处理所有文件"""
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            # 获取所有 Python 文件
            python_files = self.get_python_files()
            
            print(f"\nScanning {len(python_files)} Python files... 🔍")
            
            # 并行处理文件
            tasks = []
            for file_path in python_files:
                task = loop.run_in_executor(
                    executor,
                    self.find_imports_in_file,
                    file_path
                )
                tasks.append(task)
                
            # 等待所有任务完成
            results = await asyncio.gather(*tasks)
            
            # 合并结果
            all_imports = set()
            for imports in results:
                all_imports.update(imports)
            # 排除标准库和本地模块
            stdlib_modules = self.get_stdlib_modules()
            third_party = {
                get_package_name(imp) for imp in all_imports 
                if imp not in stdlib_modules and imp not in self.local_modules
            }
            
            return third_party, python_files

    def get_python_files(self) -> Set[Path]:
        """获取所有 Python 文件的路径，并记录本地模块名"""
        python_files = set()
        for src in self.src_paths:
            path = Path(src)
            if path.is_file() and path.suffix == '.py':
                python_files.add(path)
                self.local_modules.add(path.stem)
            elif path.is_dir():
                for py_file in path.rglob('*.py'):
                    python_files.add(py_file)
                    self.local_modules.add(py_file.stem)
                    # 如果是__init__.py文件，将其所在文件夹名也加入local_modules
                    if py_file.name == '__init__.py':
                        self.local_modules.add(py_file.parent.name)
        return python_files

    @staticmethod
    def get_stdlib_modules() -> Set[str]:
        """获取 Python 标准库模块列表"""
        import sys
        stdlib_modules = set(sys.builtin_module_names)
        stdlib_modules.update({
            'functools', 'json', 'pathlib', 'typing', 'collections',
            'urllib', 'tempfile', 'copy', 'warnings', 'contextlib',
            'io', 'os', 're', 'shutil', 'traceback', 'types',
            'uuid', 'zipfile', 'gzip', 'tarfile', 'fnmatch',
            'glob', 'pickle', 'hashlib', 'importlib', 'inspect',
            'distutils', 'html'
        })
        return stdlib_modules

    def save_requirements(self, dependencies: Set[str]) -> str:
        """Save dependencies to requirements file and return the filename used"""
        if self.no_save:
            return None
            
        # Determine which requirements file to use
        if not Path('requirements.txt').exists():
            filename = 'requirements.txt'
        elif not Path('requirements-depscan.txt').exists():
            filename = 'requirements-depscan.txt'
        else:
            filename = 'requirements-depscan.txt'
            
        # Write dependencies to file
        with open(filename, 'w') as f:
            for dep in sorted(dependencies):
                f.write(f"{dep}\n")
                
        return filename

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('src', nargs='+', help='Source file(s) or directory')
    parser.add_argument('--workers', type=int, help='Number of workers')
    parser.add_argument('--no-save', action='store_true', help='Do not save requirements file')
    args = parser.parse_args()
    
    finder = DependencyFinder(args.src, args.workers, args.no_save)
    
    loop = asyncio.get_event_loop()
    third_party_deps, scanned_files = loop.run_until_complete(finder.process_files())
    
    # 美化输出
    print("\nFound dependencies in:")
    for file in sorted(scanned_files):
        print(f"- {file}")
    
    print(f"\nDiscovered {len(third_party_deps)} third-party dependencies:")
    for dep in sorted(third_party_deps):
        print(f"- {dep}")
    
    # Save requirements file
    if not args.no_save:
        filename = finder.save_requirements(third_party_deps)
        print(f"\nSaved dependencies to {filename} 💾")
        
    print(f"\nAll done! ✨ 🔍 ✨")
    print(f"Scanned {len(scanned_files)} files, found {len(third_party_deps)} dependencies.")

if __name__ == '__main__':
    main()