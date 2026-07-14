import pandas as pd
from openpyxl import load_workbook
import os
from config import Config


class FlexibleExcelParser:
    """
    Flexible Excel Parser - সব ধরনের Excel ফরম্যাট সাপোর্ট করে
    কলামের নাম যাই হোক না কেন, খুঁজে বের করবে!
    """
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.column_mapping = {}
        self.load_excel()
    
    def load_excel(self):
        """Excel ফাইল লোড করুন"""
        try:
            self.df = pd.read_excel(self.file_path, sheet_name=0)
            self._detect_columns()
        except Exception as e:
            raise Exception(f"Excel লোড করতে ত্রুটি: {str(e)}")
    
    def _detect_columns(self):
        """কলামগুলো ডিটেক্ট করুন - ফ্লেক্সিবল ম্যাচিং"""
        columns = [str(col).strip().lower() for col in self.df.columns]
        
        # প্রয়োজনীয় কলাম খুঁজুন
        required_mappings = {
            'class': Config.REQUIRED_COLUMNS['class'],
            'shift': Config.REQUIRED_COLUMNS['shift'],
            'exam': Config.REQUIRED_COLUMNS['exam'],
            'roll': Config.REQUIRED_COLUMNS['roll'],
            'name': Config.REQUIRED_COLUMNS['name']
        }
        
        # প্রতিটি প্রয়োজনীয় কলামের জন্য ম্যাপিং খুঁজুন
        for key, possible_names in required_mappings.items():
            for col_idx, col in enumerate(columns):
                for possible_name in possible_names:
                    if possible_name.lower() in col or col in possible_name.lower():
                        self.column_mapping[key] = self.df.columns[col_idx]
                        break
                if key in self.column_mapping:
                    break
        
        # চেক করুন সব প্রয়োজনীয় কলাম পেয়েছি কিনা
        required_keys = ['class', 'shift', 'exam', 'roll', 'name']
        missing = [k for k in required_keys if k not in self.column_mapping]
        
        if missing:
            raise Exception(f"এই কলামগুলো পাওয়া যায়নি: {', '.join(missing)}")
        
        # বাকি কলামগুলো বিষয় হিসেবে ধরুন
        used_columns = set(self.column_mapping.values())
        self.subject_columns = [col for col in self.df.columns if col not in used_columns]
    
    def get_classes(self):
        """সব ক্লাস পান (ইউনিক)"""
        return sorted(self.df[self.column_mapping['class']].unique().astype(str))
    
    def get_shifts(self, class_name):
        """নির্দিষ্ট ক্লাসের সব শিফট পান"""
        class_data = self.df[self.df[self.column_mapping['class']].astype(str) == str(class_name)]
        return sorted(class_data[self.column_mapping['shift']].unique().astype(str))
    
    def get_exams(self, class_name, shift_name):
        """নির্দিষ্ট ক্লাস ও শিফটের সব পরীক্ষা পান"""
        filtered_data = self.df[
            (self.df[self.column_mapping['class']].astype(str) == str(class_name)) &
            (self.df[self.column_mapping['shift']].astype(str) == str(shift_name))
        ]
        return sorted(filtered_data[self.column_mapping['exam']].unique().astype(str))
    
    def get_students(self, class_name, shift_name, exam_name):
        """নির্দিষ্ট ক্লাস, শিফট ও পরীক্ষার সব শিক্ষার্থী পান"""
        filtered_data = self.df[
            (self.df[self.column_mapping['class']].astype(str) == str(class_name)) &
            (self.df[self.column_mapping['shift']].astype(str) == str(shift_name)) &
            (self.df[self.column_mapping['exam']].astype(str) == str(exam_name))
        ]
        
        students = []
        for idx, row in filtered_data.iterrows():
            students.append({
                'roll': str(row[self.column_mapping['roll']]),
                'name': str(row[self.column_mapping['name']])
            })
        
        return students
    
    def get_result(self, class_name, shift_name, exam_name, roll_number):
        """শিক্ষার্থীর রেজাল্ট পান (রোল নম্বর দিয়ে)"""
        filtered_data = self.df[
            (self.df[self.column_mapping['class']].astype(str) == str(class_name)) &
            (self.df[self.column_mapping['shift']].astype(str) == str(shift_name)) &
            (self.df[self.column_mapping['exam']].astype(str) == str(exam_name)) &
            (self.df[self.column_mapping['roll']].astype(str) == str(roll_number))
        ]
        
        if filtered_data.empty:
            return None
        
        row = filtered_data.iloc[0]
        
        result = {
            'class': str(row[self.column_mapping['class']]),
            'shift': str(row[self.column_mapping['shift']]),
            'exam': str(row[self.column_mapping['exam']]),
            'roll': str(row[self.column_mapping['roll']]),
            'name': str(row[self.column_mapping['name']]),
            'subjects': {}
        }
        
        # সব বিষয়ের মার্কস যোগ করুন
        for subject in self.subject_columns:
            mark = row[subject]
            if pd.notna(mark):
                try:
                    result['subjects'][str(subject)] = float(mark)
                except:
                    result['subjects'][str(subject)] = str(mark)
        
        return result
    
    def get_result_by_name(self, class_name, shift_name, exam_name, student_name):
        """শিক্ষার্থীর রেজাল্ট পান (নাম দিয়ে)"""
        filtered_data = self.df[
            (self.df[self.column_mapping['class']].astype(str) == str(class_name)) &
            (self.df[self.column_mapping['shift']].astype(str) == str(shift_name)) &
            (self.df[self.column_mapping['exam']].astype(str) == str(exam_name)) &
            (self.df[self.column_mapping['name']].astype(str).str.lower() == str(student_name).lower())
        ]
        
        if filtered_data.empty:
            return None
        
        row = filtered_data.iloc[0]
        
        result = {
            'class': str(row[self.column_mapping['class']]),
            'shift': str(row[self.column_mapping['shift']]),
            'exam': str(row[self.column_mapping['exam']]),
            'roll': str(row[self.column_mapping['roll']]),
            'name': str(row[self.column_mapping['name']]),
            'subjects': {}
        }
        
        # সব বিষয়ের মার্কস যোগ করুন
        for subject in self.subject_columns:
            mark = row[subject]
            if pd.notna(mark):
                try:
                    result['subjects'][str(subject)] = float(mark)
                except:
                    result['subjects'][str(subject)] = str(mark)
        
        return result
    
    def get_subjects(self):
        """সব বিষয় পান"""
        return [str(col) for col in self.subject_columns]


class DataCache:
    """ডাটা ক্যাশ - পারফরম্যান্সের জন্য"""
    
    def __init__(self):
        self.cache = {}
        self.parser = None
    
    def load_data(self, file_path):
        """ফাইল লোড করুন এবং ক্যাশ করুন"""
        self.parser = FlexibleExcelParser(file_path)
        self.cache['classes'] = self.parser.get_classes()
        return self.parser
    
    def get_parser(self):
        """পার্সার পান"""
        return self.parser
    
    def get_classes(self):
        """ক্যাশড ক্লাস পান"""
        return self.cache.get('classes', [])
    
    def clear(self):
        """ক্যাশ ক্লিয়ার করুন"""
        self.cache = {}
        self.parser = None
