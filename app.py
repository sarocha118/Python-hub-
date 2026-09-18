import re
from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

# ==========================================
# 📚 DATA STORE (ข้อมูลบทเรียน & แบบฝึกหัด)
# ==========================================

LESSONS_DATA = [
    {
        "id": "intro",
        "title": "Python คืออะไร",
        "category": "🌱 Python พื้นฐาน",
        "keywords": ["python", "intro", "แนะนำ"],
        "desc": "ทำความรู้จักภาษา Python และประโยชน์ของการเรียนเขียนโค้ด",
        "syntax": "# เขียนโค้ด Python ในไฟล์ .py",
        "example_easy": 'print("Hello, Python!")',
        "example_med": 'name = "Python"\nprint(f"Welcome to {name}")',
        "example_adv": "import sys\nprint(sys.version)",
        "output": "Hello, Python!",
        "warning": "Python ให้ความสำคัญกับ Indentation (การเว้นวรรค) มาก",
        "task": 'เขียนคำสั่งแสดงข้อความ "Hello World"',
        "task_hint": 'ใช้คำสั่ง print("...")',
        "quiz": {
            "q": "ไฟล์โค้ด Python มักจะลงท้ายด้วยนามสกุลอะไร?",
            "options": [".py", ".html", ".cpp", ".js"],
            "ans": 0,
        },
    },
    {
        "id": "print",
        "title": "print()",
        "category": "🌱 Python พื้นฐาน",
        "keywords": ["print", "แสดงผล", "output"],
        "desc": "คำสั่งสำหรับแสดงผลข้อมูลออกทางหน้าจอ",
        "syntax": 'print(object, sep=" ", end="\\n")',
        "example_easy": 'print("Hello World")',
        "example_med": 'print("Hello", "Aem", sep=" - ")',
        "example_adv": 'print("Loading", end="..."); print("Done")',
        "output": "Hello World",
        "warning": "ข้อความต้องครอบด้วยเครื่องหมายอัญประกาศ '...' หรือ \"...\"",
        "task": "ให้ใช้ print() แสดงชื่อของตัวเอง",
        "task_hint": 'print("ชื่อของคุณ")',
        "quiz": {
            "q": "คำสั่ง print() ใช้ทำอะไร?",
            "options": [
                "รับข้อมูลจากผู้ใช้",
                "แสดงข้อความออกทางหน้าจอ",
                "วนซ้ำ",
                "แปลงชนิดข้อมูล",
            ],
            "ans": 1,
        },
    },
    {
        "id": "input",
        "title": "input()",
        "category": "🌱 Python พื้นฐาน",
        "keywords": ["input", "รับข้อมูล", "รับค่า", "user input"],
        "desc": "รับข้อมูลจากผู้ใช้ผ่านคีย์บอร์ด",
        "syntax": 'input("ข้อความคำถาม")',
        "example_easy": 'name = input("ชื่อของคุณ: ")',
        "example_med": 'name = input("Name: ")\nprint("Hello", name)',
        "example_adv": 'age = int(input("Age: "))\nprint(f"Next year: {age + 1}")',
        "output": "ชื่อของคุณ: Aem\nAem",
        "warning": "input() จะคืนค่าเป็น str (String) เสมอ ถ้าต้องการนำไปคำนวณต้องแปลงเป็น int() หรือ float() ก่อน",
        "task": "รับค่าอายุจากผู้ใช้ แล้วแปลงเป็น int",
        "task_hint": 'age = int(input("ใส่อายุ: "))',
        "quiz": {
            "q": "ค่าที่ได้จาก input() จะเป็นชนิดข้อมูลใดโดยเริ่มต้น?",
            "options": ["int", "float", "str", "bool"],
            "ans": 2,
        },
    },
    {
        "id": "if-else",
        "title": "if / elif / else",
        "category": "🔀 Conditions",
        "keywords": ["if", "elif", "else", "เงื่อนไข", "ตรวจสอบ"],
        "desc": "ใช้สำหรับตรวจสอบเงื่อนไขเพื่อตัดสินใจทำงานตามโค้ดที่กำหนด",
        "syntax": "if เงื่อนไข:\n    โค้ดที่ทำเมื่อเป็นจริง\nelif เงื่อนไข2:\n    โค้ดเมื่อเงื่อนไข2 เป็นจริง\nelse:\n    โค้ดกรณีอื่นๆ",
        "example_easy": 'score = 80\nif score >= 50:\n    print("Pass")',
        "example_med": 'age = 15\nif age >= 18:\n    print("Adult")\nelse:\n    print("Minor")',
        "example_adv": 'age = int(input("Age: "))\nif age >= 18:\n    print("ผู้ใหญ่")\nelif age >= 13:\n    print("วัยรุ่น")\nelse:\n    print("เด็ก")',
        "output": "วัยรุ่น",
        "warning": "อย่าลืมเครื่องหมาย : (colon) ท้ายบรรทัด if/elif/else และจัด Indentation ให้ถูกต้อง",
        "task": "รับอายุจากผู้ใช้ ถ้าอายุมากกว่าหรือเท่ากับ 18 ให้แสดงคำว่า 'ผู้ใหญ่'",
        "task_hint": 'age = int(input("อายุ: "))\nif age >= 18:\n    print("ผู้ใหญ่")',
        "quiz": {
            "q": "หากต้องการเช็คเงื่อนไขเพิ่มหลังจาก if ไม่ผ่าน ต้องใช้คำสั่งใด?",
            "options": ["else if", "elif", "then", "case"],
            "ans": 1,
        },
    },
    {
        "id": "for-loop",
        "title": "for / while",
        "category": "🔁 Loops",
        "keywords": ["for", "while", "loop", "วนซ้ำ", "range"],
        "desc": "ใช้ทำซ้ำคำสั่งเดิมตามจำนวนรอบหรือเงื่อนไขที่กำหนด",
        "syntax": "for i in range(จำนวนรอบ):\n    โค้ดทำซ้ำ\n\nwhile เงื่อนไข:\n    โค้ดทำซ้ำ",
        "example_easy": "for i in range(5):\n    print(i)",
        "example_med": 'fruits = ["apple", "banana"]\nfor f in fruits:\n    print(f)',
        "example_adv": "count = 0\nwhile count < 3:\n    print(count)\n    count += 1",
        "output": "0\n1\n2\n3\n4",
        "warning": "ระวังการเขียน while loop ที่ไม่มีวันจบ (Infinite Loop)",
        "task": "ใช้ for loop แสดงตัวเลข 0 ถึง 4 ออกทางหน้าจอ",
        "task_hint": "for i in range(5):\n    print(i)",
        "quiz": {
            "q": "range(3) จะสร้างลำดับตัวเลขใดบ้าง?",
            "options": ["1, 2, 3", "0, 1, 2", "0, 1, 2, 3", "1, 2"],
            "ans": 1,
        },
    },
    {
        "id": "list",
        "title": "List",
        "category": "📦 Data Structures",
        "keywords": ["list", "array", "รายการ", "ชุดข้อมูล"],
        "desc": "ตัวแปรชนิดเก็บชุดข้อมูลหลายค่าเรียงตามลำดับ",
        "syntax": 'my_list = [item1, item2, item3]\nmy_list.append("new_item")',
        "example_easy": 'nums = [1, 2, 3]\nprint(nums[0])',
        "example_med": 'items = ["A", "B"]\nitems.append("C")\nprint(items)',
        "example_adv": 'matrix = [[1, 2], [3, 4]]\nprint(matrix[1][0])',
        "output": "1",
        "warning": "Index ของ List เริ่มต้นที่ 0 ไม่ใช่ 1",
        "task": "สร้าง List เก็บชื่อผลไม้ 3 ชนิด แล้วแสดงผลตัวแรก",
        "task_hint": 'fruits = ["Apple", "Banana", "Orange"]\nprint(fruits[0])',
        "quiz": {
            "q": "สมาชิกตัวแรกใน List my_list มีดัชนี (Index) เป็นเท่าใด?",
            "options": ["1", "-1", "0", "0.1"],
            "ans": 2,
        },
    },
    {
        "id": "functions",
        "title": "def (Functions)",
        "category": "🛠️ Functions",
        "keywords": ["def", "function", "ฟังก์ชัน", "return", "parameter"],
        "desc": "การสร้างกลุ่มโค้ดทำงานเฉพาะทางที่สามารถเรียกใช้ซ้ำได้",
        "syntax": "def function_name(param):\n    # โค้ดทำงาน\n    return result",
        "example_easy": 'def say_hi():\n    print("Hi!")\n\nsay_hi()',
        "example_med": 'def add(a, b):\n    return a + b\n\nprint(add(5, 3))',
        "example_adv": 'def check_even(n):\n    return "Even" if n % 2 == 0 else "Odd"\n\nprint(check_even(4))',
        "output": "Hi!",
        "warning": "ฟังก์ชันจะไม่ทำงานจนกว่าจะมีการเรียกใช้งาน (Call Function)",
        "task": "เขียนฟังก์ชัน greet(name) ที่คืนค่าคำว่า Hello ตามด้วยชื่อ",
        "task_hint": 'def greet(name):\n    return "Hello " + name',
        "quiz": {
            "q": "คีย์เวิร์ดใดใช้ประกาศสร้างฟังก์ชันใน Python?",
            "options": ["function", "func", "def", "create"],
            "ans": 2,
        },
    },
]

CHEAT_SHEET = [
    {"cmd": "print()", "desc": "แสดงข้อมูลออกหน้าจอ"},
    {"cmd": "input()", "desc": "รับข้อมูลจากผู้ใช้"},
    {"cmd": "int()", "desc": "แปลงเป็นจำนวนเต็ม"},
    {"cmd": "float()", "desc": "แปลงเป็นทศนิยม"},
    {"cmd": "str()", "desc": "แปลงเป็นข้อความ (String)"},
    {"cmd": "len()", "desc": "หาความยาวของข้อมูล/จำนวนสมาชิก"},
    {"cmd": "range()", "desc": "สร้างลำดับช่วงตัวเลข"},
    {"cmd": "type()", "desc": "ตรวจสอบชนิดข้อมูล (Data Type)"},
]

LEARNING_PATH = [
    {"title": "🐣 Python 0", "desc": "ทำความรู้จัก Python", "id": "intro"},
    {"title": "📦 ตัวแปร & print", "desc": "การใช้งานตัวแปรและการแสดงผล", "id": "print"},
    {"title": "⌨️ input", "desc": "รับค่าข้อมูลจากผู้ใช้", "id": "input"},
    {"title": "🔀 if / else", "desc": "การเช็คเงื่อนไขทำตามโจทย์", "id": "if-else"},
    {"title": "🔁 Loops", "desc": "การวนซ้ำด้วย for และ while", "id": "for-loop"},
    {"title": "📋 List", "desc": "การจัดการชุดข้อมูลหลายตัว", "id": "list"},
    {"title": "🛠️ Functions", "desc": "การสร้างฟังก์ชันไว้ใช้ซ้ำ", "id": "functions"},
]

ACHIEVEMENTS = [
    {"id": "first_code", "title": "🏅 First Code", "desc": "เรียนจบเนื้อหาแรก"},
    {"id": "input_master", "title": "🏅 Input Master", "desc": "ผ่านบทเรียน input()"},
    {"id": "if_beginner", "title": "🏅 If Beginner", "desc": "ทำโจทย์ if/else สำเร็จ"},
    {"id": "quiz_pro", "title": "🏆 Python Beginner", "desc": "เก็บ XP ครบ 200 XP"},
]

# ==========================================
# 🌐 HTML TEMPLATE (Single Page Application)
# ==========================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="th" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🐍 Python Hub — เว็บรวมความรู้ Python</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#f0fdf4',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d',
                        }
                    }
                }
            }
        }
    </script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Sukhumvit Set', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .hide-scrollbar::-webkit-scrollbar { display: none; }
        .hide-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
    </style>
</head>
<body class="bg-gray-50 text-gray-800 dark:bg-gray-900 dark:text-gray-100 min-h-screen pb-20 md:pb-6 transition-colors duration-200">

    <header class="sticky top-0 z-40 bg-white/80 dark:bg-gray-800/80 backdrop-blur border-b border-gray-200 dark:border-gray-700 px-4 py-3">
        <div class="max-w-5xl mx-auto flex justify-between items-center">
            <div class="flex items-center space-x-2 cursor-pointer" onclick="nav('home')">
                <span class="text-2xl">🐍</span>
                <span class="font-bold text-xl text-brand-600 dark:text-brand-500">Python Hub</span>
            </div>
            
            <div class="flex items-center space-x-3">
                <div class="bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 px-3 py-1 rounded-full text-xs font-bold flex items-center space-x-1">
                    <span>⭐ XP</span>
                    <span id="user-xp">0</span>
                </div>
                <button onclick="toggleDarkMode()" class="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600">
                    <i id="theme-icon" class="fas fa-moon"></i>
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-5xl mx-auto p-4 md:p-6">

        <!-- 🏠 1. PAGE: HOME -->
        <section id="page-home" class="space-y-8">
            <div class="text-center py-10 space-y-4">
                <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight">🐍 Python Hub</h1>
                <p class="text-lg text-gray-600 dark:text-gray-400 max-w-xl mx-auto">ศูนย์รวมความรู้ Python สำหรับมือใหม่ เข้าใจง่าย ฝึกเขียนได้ในมือถือ</p>
                
                <div class="max-w-md mx-auto relative mt-6">
                    <div class="relative">
                        <input type="text" id="hero-search" oninput="handleSearch(this.value, 'hero-suggestions')" placeholder="ค้นหาบทเรียน เช่น input, if, loop..." 
                               class="w-full pl-10 pr-4 py-3 rounded-2xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-brand-500 shadow-sm">
                        <i class="fas fa-search absolute left-3 top-4 text-gray-400"></i>
                    </div>
                    <div id="hero-suggestions" class="absolute w-full mt-1 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-lg hidden z-50 overflow-hidden"></div>
                </div>

                <div class="flex justify-center space-x-3 pt-2">
                    <button onclick="nav('path')" class="bg-brand-600 hover:bg-brand-700 text-white font-bold px-5 py-2.5 rounded-xl shadow-md transition">🚀 เริ่มเรียน</button>
                    <button onclick="nav('lessons')" class="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 font-bold px-5 py-2.5 rounded-xl transition">📚 ดูหัวข้อทั้งหมด</button>
                </div>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
                <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div class="text-2xl font-bold text-brand-600 dark:text-brand-500">📚 10+</div>
                    <div class="text-xs text-gray-500">บทเรียนพื้นฐาน</div>
                </div>
                <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div class="text-2xl font-bold text-blue-500">🧪 100%</div>
                    <div class="text-xs text-gray-500">มีโจทย์ให้ฝึกทำ</div>
                </div>
                <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div class="text-2xl font-bold text-purple-500">🧠 Quiz</div>
                    <div class="text-xs text-gray-500">ทดสอบวัดความเข้าใจ</div>
                </div>
                <div class="bg-white dark:bg-gray-800 p-4 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                    <div class="text-2xl font-bold text-amber-500">📱 Mobile</div>
                    <div class="text-xs text-gray-500">ออกแบบสำหรับมือถือ</div>
                </div>
            </div>

            <div class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 space-y-4">
                <div class="flex justify-between items-center">
                    <h2 class="text-xl font-bold flex items-center gap-2">🗺️ เส้นทางการเรียนรู้ (Learning Path)</h2>
                    <button onclick="nav('path')" class="text-sm text-brand-600 dark:text-brand-400 hover:underline">ดูทั้งหมด →</button>
                </div>
                <div class="flex overflow-x-auto space-x-3 pb-2 hide-scrollbar" id="home-path-list"></div>
            </div>
        </section>

        <!-- 🔎 2. PAGE: SEARCH -->
        <section id="page-search" class="hidden space-y-4">
            <h2 class="text-2xl font-bold">🔎 ค้นหาบทเรียน</h2>
            <div class="relative">
                <input type="text" id="search-input" oninput="runSearch(this.value)" placeholder="ค้นจากชื่อ, คำอธิบาย เช่น if, วนซ้ำ, input..." 
                       class="w-full pl-10 pr-4 py-3 rounded-2xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-brand-500 shadow-sm">
                <i class="fas fa-search absolute left-3 top-4 text-gray-400"></i>
            </div>
            <div id="search-results" class="grid gap-3 pt-2">
                <div class="text-gray-400 text-center py-8">พิมพ์คำค้นหาเพื่อเริ่มค้นหาบทเรียน...</div>
            </div>
        </section>

        <!-- 📚 3. PAGE: LESSONS LIST -->
        <section id="page-lessons" class="hidden space-y-6">
            <h2 class="text-2xl font-bold">📚 หมวดหมู่บทเรียน</h2>
            <div class="grid gap-4" id="lessons-category-list"></div>
        </section>

        <!-- 💻 4. PAGE: LESSON DETAIL -->
        <section id="page-detail" class="hidden space-y-6">
            <button onclick="nav('lessons')" class="text-sm text-gray-500 hover:text-brand-600 flex items-center gap-1">
                <i class="fas fa-arrow-left"></i> ย้อนกลับไปหน้าบทเรียน
            </button>
            <div id="detail-content" class="bg-white dark:bg-gray-800 p-6 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 space-y-6"></div>
        </section>

        <!-- 📖 8. PAGE: CHEAT SHEET -->
        <section id="page-cheatsheet" class="hidden space-y-4">
            <h2 class="text-2xl font-bold">📖 Python Cheat Sheet</h2>
            <p class="text-sm text-gray-500">สรุปคำสั่งที่ใช้งานบ่อย เปิดดูรวดเร็ว</p>
            <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
                            <th class="p-3 font-semibold">คำสั่ง</th>
                            <th class="p-3 font-semibold">การใช้งาน</th>
                        </tr>
                    </thead>
                    <tbody id="cheatsheet-body" class="divide-y divide-gray-100 dark:divide-gray-700 text-sm"></tbody>
                </table>
            </div>
        </section>

        <!-- 🐛 9. PAGE: DEBUGGER -->
        <section id="page-debugger" class="hidden space-y-4">
            <h2 class="text-2xl font-bold">🐛 Code Debugger ช่วยวิเคราะห์ Error</h2>
            <p class="text-sm text-gray-500">วางโค้ดที่รันไม่ผ่านเพื่อวิเคราะห์สาเหตุของข้อผิดพลาดเบื้องต้น</p>
            <div class="space-y-3">
                <textarea id="debug-code" rows="5" class="w-full p-3 font-mono text-sm rounded-xl border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 focus:ring-2 focus:ring-brand-500 focus:outline-none" placeholder="เช่น age = int(input(&quot;อายุ: &quot;)"></textarea>
                <button onclick="analyzeError()" class="w-full bg-red-500 hover:bg-red-600 text-white font-bold py-2.5 rounded-xl transition">🔍 ตรวจสอบ Error</button>
            </div>
            <div id="debug-result" class="hidden p-4 rounded-2xl border border-red-200 bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 space-y-2">
                <div class="font-bold text-lg" id="debug-type">🚨 SyntaxError</div>
                <div class="text-sm" id="debug-desc">น่าจะลืมปิดวงเล็บ ) ตอนท้ายคำสั่ง</div>
            </div>
        </section>

        <!-- ⭐ 10. PAGE: BOOKMARKS -->
        <section id="page-bookmarks" class="hidden space-y-4">
            <h2 class="text-2xl font-bold">⭐ บทเรียนที่บันทึกไว้</h2>
            <div id="bookmark-list" class="grid gap-3"></div>
        </section>

        <!-- 🗺️ 13. PAGE: LEARNING PATH -->
        <section id="page-path" class="hidden space-y-4">
            <h2 class="text-2xl font-bold">🗺️ เส้นทางการเรียนรู้ Python</h2>
            <div class="space-y-3 relative pl-4 border-l-2 border-brand-500 ml-2" id="path-list"></div>
        </section>

        <!-- 🏆 14. PAGE: ACHIEVEMENTS -->
        <section id="page-achievements" class="hidden space-y-4">
            <h2 class="text-2xl font-bold">🏆 ความสำเร็จของคุณ (Achievements)</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3" id="achievement-list"></div>
        </section>

    </main>

    <!-- 📱 Mobile Navigation -->
    <nav class="fixed bottom-0 left-0 right-0 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 z-50">
        <div class="max-w-md mx-auto flex justify-around py-2">
            <button onclick="nav('home')" class="nav-btn flex flex-col items-center text-gray-500 dark:text-gray-400 hover:text-brand-600 text-xs">
                <i class="fas fa-home text-lg mb-0.5"></i>
                <span>หน้าแรก</span>
            </button>
            <b
