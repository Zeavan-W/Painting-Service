import os
from flask import Flask, render_template_string, request, redirect, flash
from flask_mail import Mail, Message
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')
csrf = CSRFProtect(app)

# 邮箱配置（用环境变量保护敏感信息）
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.qq.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'True') == 'True'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '735433470@qq.com')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'sfndnqpaifpxbeff')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', '735433470@qq.com')

mail = Mail(app)

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(max=20)])
    address = StringField('Address', validators=[DataRequired(), Length(max=100)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])

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
    {{ form.hidden_tag() }}
    <input type="text" name="name" placeholder="您的姓名" value="{{ form.name.data or '' }}" maxlength="30" required><br>
    <input type="tel" name="phone" placeholder="联系电话" value="{{ form.phone.data or '' }}" maxlength="20" required><br>
    <input type="text" name="address" placeholder="服务地址" value="{{ form.address.data or '' }}" maxlength="100" required><br>
    <textarea name="message" placeholder="需求描述" maxlength="500" required>{{ form.message.data or '' }}</textarea><br>
    <button type="submit">提交</button>
  </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        message = form.message.data

        email_body = f"""
        姓名: {name}
        电话: {phone}
        地址: {address}
        需求描述: {message}
        """
        msg = Message(subject="网站表单新提交",
                      recipients=[os.environ.get('MAIL_RECEIVER', '735433470@qq.com')],
                      body=email_body)
        try:
            mail.send(msg)
            flash('提交成功，感谢您的反馈！')
        except Exception:
            flash('邮件发送失败，请稍后再试。')
        return redirect('/')
    elif request.method == 'POST':
        flash('表单填写有误，请检查后再提交。')
    return render_template_string(HTML, form=form)

if __name__ == '__main__':
    app.run(debug=False) 