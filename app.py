import os
from flask import Flask, request, redirect, send_from_directory
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')

# 邮箱配置（用环境变量保护敏感信息）
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '735433470@qq.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'sfndnqpaifpxbeff')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', '735433470@qq.com')

mail = Mail(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        message = request.form.get('message')

        if name and phone and email and address and message:
            email_body = f"""
            姓名: {name}
            电话: {phone}
            邮箱: {email}
            地址: {address}
            需求描述: {message}
            """
            msg = Message(subject="网站表单新提交",
                          recipients=[os.environ.get('MAIL_RECEIVER', '735433470@qq.com')],
                          body=email_body)
            try:
                mail.send(msg)
                print("邮件发送成功")
            except Exception as e:
                print(f"邮件发送失败: {e}")
        else:
            print("表单数据不完整")
        
        return redirect('/')
    
    # 直接返回 index.html 文件
    return send_from_directory('.', 'index.html')

# 静态文件路由 - 只处理特定文件类型
@app.route('/style.css')
def css_file():
    return send_from_directory('.', 'style.css')

@app.route('/<filename>')
def static_files(filename):
    """处理其他静态文件请求，只允许 GET 方法"""
    # 检查文件是否存在
    if os.path.exists(filename):
        return send_from_directory('.', filename)
    else:
        return "文件不存在", 404

if __name__ == '__main__':
    app.run(debug=False) 