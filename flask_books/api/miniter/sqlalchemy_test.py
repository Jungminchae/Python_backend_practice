from sqlalchemy import create_engine, text 

db = {
    'user' : 'root',
    'password' : 'minchae1234',
    'host' : 'localhost' ,
    'port' : 3306,
    'database' : 'miniter'
}

db_url = f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}?charset=utf8'
db = create_engine(db_url, encoding='utf-8', max_overflow =0)

params = {'name' :'정민채'}
rows = db.execute(text("select * from users where name = :name"), params).fetchall()

for row in rows:
    print(f"name : {row['name']}")
    print(f"email : {row['email']}")