from sqlalchemy import create_engine
import pandas as pd


engine = create_engine('postgresql+psycopg2://root:root@localhost/test_db')

sql = '''
select * from public."Billboard" limit 10;
'''

df3 = pd.read_sql_query(sql, engine)


sql = '''
select t1."date"
    ,t1."rank"
    ,t1.artist
    ,t1.song 
    from public."Billboard" as t1
    where t1.artist like 'Elvis%%'
    order by t1.artist, t1.song, t1."date";
'''

engine.execute(sql)
