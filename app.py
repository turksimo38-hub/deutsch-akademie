from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

app = Flask(__name__)

# إعداد الاتصال بـ Google Sheets
def connect_to_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # هنا الكود كايقرا الساروت من الملف محلياً، وإيلا ترفع أونلاين كايقراه من Render بأمان
    if os.path.exists("credentials.json"):
        creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    else:
        # هادي لزوم الشغل أونلاين ف Render من بعد
        import json
        creds_json = json.loads(os.environ.get("GOOGLE_CREDENTIALS"))
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
        
    client = gspread.authorize(creds)
 
    # التعديل هنا: رجعنا السمية الحقيقية د الـ Google Sheet ديالك بالظبط
    sheet = client.open("Deutschakademie_Anmeldungen").sheet1
    return sheet

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        print(f"Data received from Form: {data}")  # هادا غايطبع ليك الداتا ف الترمينال باش تشوفها
        
        # قراءة الاسم
        name = data.get('name') or data.get('username') or data.get('fullName', '')
        
        # قراءة الهاتف (بجميع التسميات الممكنة)
        telefon = data.get('telefon') or data.get('phone') or data.get('tel') or data.get('phone_number', '')
        
        # قراءة المستوى
        niveau = data.get('niveau') or data.get('level') or data.get('class', '')
        
        # قراءة السعر
        preis = data.get('preis') or data.get('price') or data.get('cost', '')
        
        # قراءة التوقيت د الكورس
        kurszeit = data.get('kurszeit') or data.get('time') or data.get('timing') or data.get('kurs_zeit', '')
        
        # الاتصال بالجدول وإضافة السطر الجديد
        sheet = connect_to_sheets()
        sheet.append_row([name, telefon, niveau, preis, kurszeit])
        
        return jsonify({"status": "success", "message": "تم تسجيلك بنجاح ف الـ Google Sheet!"})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "وقع مشكل ف التسجيل، عاود جرب."}), 500
        
        # الاتصال بالجدول وإضافة السطر الجديد
        sheet = connect_to_sheets()
        sheet.append_row([name, telefon, niveau, preis, kurszeit])
        
        return jsonify({"status": "success", "message": "تم تسجيلك بنجاح ف الـ Google Sheet!"})
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "وقع مشكل ف التسجيل، عاود جرب."}), 500

if __name__ == '__main__':
    app.run(debug=True)
    from flask import send_from_directory

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')