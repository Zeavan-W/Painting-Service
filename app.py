from flask import Flask, render_template_string, request, redirect, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于闪现消息

# 邮箱配置（以QQ邮箱为例，其他邮箱请修改对应参数）
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = '735433470@qq.com'
app.config['MAIL_PASSWORD'] = 'sfndnqpaifpxbeff'
app.config['MAIL_DEFAULT_SENDER'] = '735433470@qq.com'

mail = Mail(app)

# 直接用字符串渲染表单页面，方便初学者测试
HTML = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>PSD Painting - 获取免费报价</title>
</head>
<body>
  <h3>获取免费报价</h3>
  {% with messages = get_flashed_messages() %}
    {% if messages %}
      <ul>
      {% for message in messages %}
        <li>{{ message }}</li>
      {% endfor %}
      </ul>
    {% endif %}
  {% endwith %}
  <form action="/" method="POST">
    <input type="text" name="name" placeholder="您的姓名" required><br>
    <input type="tel" name="phone" placeholder="联系电话" required><br>
    <input type="text" name="address" placeholder="服务地址" required><br>
    <textarea name="message" placeholder="需求描述" required></textarea><br>
    <button type="submit">提交</button>
  </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        message = request.form.get('message')

        # 构建邮件内容
        email_body = f"""
        姓名: {name}
        电话: {phone}
        地址: {address}
        需求描述: {message}
        """

        # 发送邮件
        msg = Message(subject="网站表单新提交",
                      recipients=['735433470@qq.com'],
                      body=email_body)
        try:
            mail.send(msg)
            flash('提交成功，感谢您的反馈！')
        except Exception as e:
            flash('邮件发送失败，请稍后再试。')
        return redirect('/')
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(debug=True) 