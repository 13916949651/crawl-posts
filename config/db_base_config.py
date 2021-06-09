# from manage import db
#
#
# class duty(db.Model):
#     __tablename__ = 'duty'
#
#     duty_id = db.Column(db.Integer, primary_key=True)
#     duty_name = db.Column(db.String(100), unique=True)
#     duty_addtime = db.Column(db.DateTime, index=True)
#     duty_is_true = db.Column(db.Integer)
#
#
# class User(db.Model):
#     __tablename__ = 'user'
#
#     user_id = db.Column(db.Integer, primary_key=True)
#     user_count = db.Column(db.String(100), unique=True)
#     user_name = db.Column(db.String(100), unique=True)
#     user_sex = db.Column(db.String(100))
#     user_pwd = db.Column(db.String(100))
#     user_mail = db.Column(db.String(100))
#     user_phone = db.Column(db.String(100))
#     user_addtime = db.Column(db.DateTime, index=True)
#     user_photo = db.Column(db.String(100))
#     user_ispass = db.Column(db.Integer)
#     user_section = db.Column(db.ForeignKey('section.section_name'), index=True)
#     user_duty = db.Column(db.ForeignKey('duty.duty_name'), index=True)
#     user_power = db.Column(db.ForeignKey('power.power_name'), index=True)
#     user_salary = db.Column(db.ForeignKey('salary.salary_id'), index=True)
#
#     duty = db.relationship('duty', primaryjoin='User.user_duty == duty.duty_name', backref='users')
#     power = db.relationship('power', primaryjoin='User.user_power == power.power_name', backref='users')
#     salary = db.relationship('Salary', primaryjoin='User.user_salary == Salary.salary_id', backref='users')
#     section = db.relationship('section', primaryjoin='User.user_section == section.section_name', backref='users')
#
#     def check_pwd(self, pwd):
#         from werkzeug.security import check_password_hash
#         return check_password_hash(self.user_pwd, pwd)
