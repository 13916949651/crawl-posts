# coding=utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from controller.tiktok_download_controller import tiktok as tiktok_blueprint
from controller.facebook_download_controller import facebook as facebook_blueprint

app = Flask(__name__)
# 数据库配置
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Ltb518818lfan@127.0.0.1:3306/flask?charset=utf8"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# 密钥配置，在生产环境中使用系统自动生成
# app.config['SECRET_KEY'] = 'd890fbe7e26c4c3eb557b6009e3f4d3d'

# 调试开关，生产环境是关闭的
app.debug = True

# 注册数据模型
# db = SQLAlchemy(app)
# redis配置
# app.config['REDIS_HOST'] = "127.0.0.1"  # redis数据库地址
# app.config['REDIS_PORT'] = 6379  # redis 端口号
# app.config['REDIS_DB'] = 0  # 数据库名
# app.config['REDIS_EXPIRE'] = 60  # redis 过期时间60秒

# 注册蓝图
# app.register_blueprint(admin_blueprint, url_prefix='/admin/')
# app.register_blueprint(tiktok_blueprint, url_prefix='/')
app.register_blueprint(tiktok_blueprint)
app.register_blueprint(facebook_blueprint)

if __name__ == "__main__":
    # server = pywsgi.WSGIServer(('127.0.0.1', 8989), app)
    # server.serve_forever()
    app.run(debug=True, port=8989)
