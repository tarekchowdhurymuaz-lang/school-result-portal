import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from config import Config, get_config
from utils.excel_parser import FlexibleExcelParser, DataCache
import traceback

# Flask App তৈরি করুন
app = Flask(__name__)

# Config লোড করুন
config = get_config()
app.config.from_object(config)

# Upload folder তৈরি করুন যদি না থাকে
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Global data cache
data_cache = DataCache()
current_file = None


@app.route('/')
def index():
    """মূল পেজ"""
    return render_template('index.html')


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Excel ফাইল আপলোড করুন"""
    global current_file, data_cache

    try:
        if 'file' not in request.files:
            return jsonify({'error': 'কোনো ফাইল পাঠানো হয়নি'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'কোনো ফাইল নির্বাচিত হয়নি'}), 400

        # ফাইল এক্সটেনশন চেক করুন
        if not allowed_file(file.filename):
            return jsonify({'error': 'শুধুমাত্র .xlsx বা .xls ফাইল অনুমোদিত'}), 400

        # ফাইল সেভ করুন
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parser লোড করুন
        try:
            parser = data_cache.load_data(filepath)
            current_file = filepath

            return jsonify({
                'success': True,
                'message': 'ফাইল সফলভাবে আপলোড হয়েছে',
                'filename': filename
            })
        except Exception as e:
            return jsonify({'error': f'ফাইল পার্স করতে ত্রুটি: {str(e)}'}), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/classes', methods=['GET'])
def get_classes():
    """সব ক্লাস পান"""
    try:
        if not data_cache.get_parser():
            return jsonify({'error': 'প্রথমে ফাইল আপলোড করুন'}), 400

        parser = data_cache.get_parser()
        classes = parser.get_classes()

        return jsonify({
            'success': True,
            'classes': classes
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/shifts/<class_name>', methods=['GET'])
def get_shifts(class_name):
    """নির্দিষ্ট ক্লাসের শিফট পান"""
    try:
        parser = data_cache.get_parser()
        if not parser:
            return jsonify({'error': 'প্রথমে ফাইল আপলোড করুন'}), 400

        shifts = parser.get_shifts(class_name)

        return jsonify({
            'success': True,
            'shifts': shifts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/exams/<class_name>/<shift_name>', methods=['GET'])
def get_exams(class_name, shift_name):
    """নির্দিষ্ট ক্লাস ও শিফটের পরীক্ষা পান"""
    try:
        parser = data_cache.get_parser()
        if not parser:
            return jsonify({'error': 'প্রথমে ফাইল আপলোড করুন'}), 400

        exams = parser.get_exams(class_name, shift_name)

        return jsonify({
            'success': True,
            'exams': exams
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<class_name>/<shift_name>/<exam_name>', methods=['GET'])
def get_students(class_name, shift_name, exam_name):
    """শিক্ষার্থীর তালিকা পান"""
    try:
        parser = data_cache.get_parser()
        if not parser:
            return jsonify({'error': 'প্রথমে ফাইল আপলোড করুন'}), 400

        students = parser.get_students(class_name, shift_name, exam_name)

        return jsonify({
            'success': True,
            'students': students
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/result', methods=['POST'])
def get_result():
    """শিক্ষার্থীর ফলাফল পান"""
    try:
        parser = data_cache.get_parser()
        if not parser:
            return jsonify({'error': 'প্রথমে ফাইল আপলোড করুন'}), 400

        data = request.json
        class_name = data.get('class')
        shift_name = data.get('shift')
        exam_name = data.get('exam')
        roll = data.get('roll')
        name = data.get('name')

        # রোল নম্বর দিয়ে সার্চ করুন যদি দেওয়া থাকে
        if roll:
            result = parser.get_result(class_name, shift_name, exam_name, roll)
        elif name:
            result = parser.get_result_by_name(class_name, shift_name, exam_name, name)
        else:
            return jsonify({'error': 'রোল নম্বর বা নাম দিন'}), 400

        if not result:
            return jsonify({'error': 'শিক্ষার্থী খুঁজে পাওয়া যায়নি'}), 404

        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def allowed_file(filename):
    """ফাইল এক্সটেনশন চেক করুন"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'পেজ পাওয়া যায়নি'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'সার্ভার ত্রুটি'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)