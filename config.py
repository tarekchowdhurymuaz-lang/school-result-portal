import os
from datetime import timedelta

# Flask Configuration
class Config:
    """Base configuration"""
    
    # App settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Cache settings (in-memory caching)
    CACHE_TIMEOUT = 3600  # 1 hour
    
    # Excel parsing settings
    REQUIRED_COLUMNS = {
        'class': ['class', 'ক্লাস', 'শ্রেণী', 'standard', 'grade'],
        'shift': ['shift', 'শিফট', 'session', 'সেশন'],
        'exam': ['exam', 'পরীক্ষা', 'test', 'পরীক্ষার নাম', 'examination'],
        'roll': ['roll', 'রোল', 'roll no', 'রোল নম্বর', 'roll number', 'student id'],
        'name': ['name', 'নাম', 'student name', 'শিক্ষার্থী', 'student', 'students name']
    }


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True  # HTTPS only


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'test_uploads')


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


# Get configuration based on environment
def get_config():
    """Get configuration based on FLASK_ENV"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])
