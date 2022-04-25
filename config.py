DB_URI = 'mysql+pymysql://root:tanyuan0107@localhost:3306/test' 
# DB_URI = 'mysql+pymysql://root:root@localhost:3306/graduation' #windows

# 确保数据库存在
# 指定数据库连接
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'abcdefghijklmm'