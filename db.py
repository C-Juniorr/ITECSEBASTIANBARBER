import sqlite3

conn=sqlite3.connect('pagamentos.db')
cor=conn.cursor()
#cor.execute('create table pagamentosbarbearia(uid varchar(13)primary key,txid varchar(60),status varchar(25),nome text(20))')
#conn.commit()
#cor.execute('insert into pagamentosbarbearia(uid,txid,status,nome)values(?,?,?,?)',('11','13','aprovado','gilson'))
conn.commit()
cor.execute('select * from pagamentosbarbearia')
j=cor.fetchall()
print(j)
#cor.execute('delete from pagamentosbarbearia')
conn.commit()