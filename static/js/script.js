/* ===================================
   জাভাস্ক্রিপ্ট - স্কুল রেজাল্ট পোর্টাল
   =================================== */

// গ্লোবাল ভেরিয়েবল
let currentClass = null;
let currentShift = null;
let currentExam = null;
let allClasses = [];
let uploadedFileName = null;

// ফাইল আপলোড ফাংশন
async function uploadFile() {
    const fileInput = document.getElementById('excelFile');
    const file = fileInput.files[0];
    const statusMessage = document.getElementById('uploadStatus');

    if (!file) {
        showError(statusMessage, 'দয়া করে একটি ফাইল নির্বাচন করুন');
        return;
    }

    // ফর্মডাটা তৈরি করুন
    const formData = new FormData();
    formData.append('file', file);

    try {
        showLoading(statusMessage);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            showSuccess(statusMessage, 'ফাইল সফলভাবে আপলোড হয়েছে ✓');
            uploadedFileName = data.filename;
            
            // ক্লাসগুলো লোড করুন
            await loadClasses();
            
            // সার্চ সেকশন প্রদর্শন করুন
            document.getElementById('searchSection').style.display = 'block';
        } else {
            showError(statusMessage, data.error || 'আপলোড ব্যর্থ হয়েছে');
        }
    } catch (error) {
        showError(statusMessage, 'নেটওয়ার্ক ত্রুটি: ' + error.message);
    }
}

// ক্লাস লোড করুন
async function loadClasses() {
    try {
        const response = await fetch('/api/classes');
        const data = await response.json();

        if (data.success) {
            allClasses = data.classes;
            const classSelect = document.getElementById('classSelect');
            classSelect.innerHTML = '<option value="">-- ক্লাস নির্বাচন করুন --</option>';
            
            data.classes.forEach(cls => {
                const option = document.createElement('option');
                option.value = cls;
                option.textContent = cls;
                classSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('ক্লাস লোড ত্রুটি:', error);
    }
}

// ক্লাস পরিবর্তন ইভেন্ট
async function onClassChange() {
    const classSelect = document.getElementById('classSelect');
    currentClass = classSelect.value;

    if (!currentClass) {
        document.getElementById('shiftGroup').style.display = 'none';
        return;
    }

    // শিফট লোড করুন
    try {
        const response = await fetch(`/api/shifts/${currentClass}`);
        const data = await response.json();

        if (data.success) {
            const shiftSelect = document.getElementById('shiftSelect');
            shiftSelect.innerHTML = '<option value="">-- শিফট নির্বাচন করুন --</option>';
            
            data.shifts.forEach(shift => {
                const option = document.createElement('option');
                option.value = shift;
                option.textContent = shift;
                shiftSelect.appendChild(option);
            });

            document.getElementById('shiftGroup').style.display = 'block';
            document.getElementById('examGroup').style.display = 'none';
            document.getElementById('searchGroup').style.display = 'none';
        }
    } catch (error) {
        console.error('শিফট লোড ত্রুটি:', error);
    }
}

// শিফট পরিবর্তন ইভেন্ট
async function onShiftChange() {
    const shiftSelect = document.getElementById('shiftSelect');
    currentShift = shiftSelect.value;

    if (!currentShift) {
        document.getElementById('examGroup').style.display = 'none';
        return;
    }

    // পরীক্ষা লোড করুন
    try {
        const response = await fetch(`/api/exams/${currentClass}/${currentShift}`);
        const data = await response.json();

        if (data.success) {
            const examSelect = document.getElementById('examSelect');
            examSelect.innerHTML = '<option value="">-- পরীক্ষা নির্বাচন করুন --</option>';
            
            data.exams.forEach(exam => {
                const option = document.createElement('option');
                option.value = exam;
                option.textContent = exam;
                examSelect.appendChild(option);
            });

            document.getElementById('examGroup').style.display = 'block';
            document.getElementById('searchGroup').style.display = 'none';
        }
    } catch (error) {
        console.error('পরীক্ষা লোড ত্রুটি:', error);
    }
}

// পরীক্ষা পরিবর্তন ইভেন্ট
function onExamChange() {
    const examSelect = document.getElementById('examSelect');
    currentExam = examSelect.value;

    if (currentExam) {
        document.getElementById('searchGroup').style.display = 'block';
        clearSearchFields();
    } else {
        document.getElementById('searchGroup').style.display = 'none';
    }
}

// ফলাফল সার্চ করুন
async function searchResult() {
    const rollInput = document.getElementById('rollInput').value.trim();
    const nameInput = document.getElementById('nameInput').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    if (!rollInput && !nameInput) {
        showErrorAlert(errorMessage, 'দয়া করে রোল নম্বর বা নাম দিন');
        return;
    }

    try {
        const requestBody = {
            class: currentClass,
            shift: currentShift,
            exam: currentExam
        };

        if (rollInput) {
            requestBody.roll = rollInput;
        } else {
            requestBody.name = nameInput;
        }

        const response = await fetch('/api/result', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();

        if (data.success) {
            displayResult(data.result);
            errorMessage.style.display = 'none';
        } else {
            showErrorAlert(errorMessage, data.error || 'শিক্ষার্থী খুঁজে পাওয়া যায়নি');
        }
    } catch (error) {
        showErrorAlert(errorMessage, 'নেটওয়ার্ক ত্রুটি: ' + error.message);
    }
}

// ফলাফল প্রদর্শন করুন
function displayResult(result) {
    // হেডার তথ্য সেট করুন
    document.getElementById('studentName').textContent = result.name;
    document.getElementById('studentInfo').textContent = 
        `রোল: ${result.roll} | ক্লাস: ${result.class} | শিফট: ${result.shift}`;

    // মার্কস কার্ড তৈরি করুন
    const marksContainer = document.getElementById('marksContainer');
    marksContainer.innerHTML = '';

    Object.entries(result.subjects).forEach(([subject, mark]) => {
        const card = document.createElement('div');
        card.className = 'mark-card ' + getMarkStatus(mark);
        
        card.innerHTML = `
            <div class="subject-name">${subject}</div>
            <div class="subject-mark">${mark}</div>
        `;

        marksContainer.appendChild(card);
    });

    // রেজাল্ট সেকশন দেখান
    document.getElementById('resultSection').style.display = 'block';
    
    // উপরে স্ক্রল করুন
    document.getElementById('resultSection').scrollIntoView({ behavior: 'smooth' });
}

// মার্ক স্ট্যাটাস নির্ধারণ করুন
function getMarkStatus(mark) {
    if (typeof mark === 'number') {
        if (mark >= 80) return 'excellent';
        if (mark >= 60) return 'good';
        return 'average';
    }
    return '';
}

// নতুন সার্চ রিসেট করুন
function resetSearch() {
    document.getElementById('resultSection').style.display = 'none';
    clearSearchFields();
    document.getElementById('classSelect').focus();
}

// সার্চ ফিল্ড ক্লিয়ার করুন
function clearSearchFields() {
    document.getElementById('rollInput').value = '';
    document.getElementById('nameInput').value = '';
}

// ইউটিলিটি ফাংশন - স্ট্যাটাস মেসেজ দেখান
function showSuccess(element, message) {
    element.textContent = message;
    element.className = 'status-message success';
    element.style.display = 'block';
}

function showError(element, message) {
    element.textContent = '❌ ' + message;
    element.className = 'status-message error';
    element.style.display = 'block';
}

function showLoading(element) {
    element.innerHTML = '<span class="loading"></span> আপলোড হচ্ছে...';
    element.className = 'status-message';
    element.style.display = 'block';
}

function showErrorAlert(element, message) {
    element.textContent = '⚠️ ' + message;
    element.style.display = 'block';
}

// পেজ লোড হলে
document.addEventListener('DOMContentLoaded', function() {
    // কোনো প্রারম্ভিক সেটআপ প্রয়োজন হলে এখানে করুন
    console.log('স্কুল রেজাল্ট পোর্টাল লোড হয়েছে');
});
