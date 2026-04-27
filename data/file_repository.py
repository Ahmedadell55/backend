# data/file_repository.py
"""
Repository للتعامل مع الملفات المحلية (.dar)
حفظ وتحميل المشاريع على القرص الصلب
"""

import json
import os
from typing import Dict, Any, List
from core import settings
from core import FileOperationError


class FileRepository:
    """كل عمليات الملفات المحلية (المشاريع)"""
    
    def __init__(self):
        self.projects_dir = settings.PROJECTS_DIR
        self._ensure_directory()
    
    def _ensure_directory(self):
        """تأكد إن مجلد المشاريع موجود"""
        os.makedirs(self.projects_dir, exist_ok=True)
    
    def save_project(self, filename: str, data: Dict[str, Any]) -> str:
        """
        حفظ مشروع في ملف
        """
        try:
            if not filename.endswith(".dar"):
                filename += ".dar"
            
            filepath = os.path.join(self.projects_dir, filename)
            
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return filepath
        except Exception as e:
            raise FileOperationError(filename, "save", str(e))
    
    def load_project(self, filename: str) -> Dict[str, Any]:
        """
        تحميل مشروع من ملف
        """
        try:
            if not filename.endswith(".dar"):
                filename += ".dar"
            
            filepath = os.path.join(self.projects_dir, filename)
            
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Project {filename} not found")
            
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError as e:
            raise FileOperationError(filename, "load", str(e))
        except Exception as e:
            raise FileOperationError(filename, "load", str(e))
    
    def list_projects(self) -> List[str]:
        """
        قائمة بكل المشاريع المحفوظة
        """
        try:
            files = [f for f in os.listdir(self.projects_dir) if f.endswith(".dar")]
            return sorted(files)
        except Exception as e:
            raise FileOperationError("", "list", str(e))
    
    def delete_project(self, filename: str) -> bool:
        """
        حذف ملف مشروع
        """
        try:
            if not filename.endswith(".dar"):
                filename += ".dar"
            
            filepath = os.path.join(self.projects_dir, filename)
            
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            raise FileOperationError(filename, "delete", str(e))