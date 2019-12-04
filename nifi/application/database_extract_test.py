from sshtunnel import SSHTunnelForwarder
import mysql.connector as mariadb



"""
install sshtunnel:
    pip install sshtunnel
    or 
    conda install -c conda-forge sshtunnel
"""
# server = SSHTunnelForwarder(
#     'b.autobiz.fr',
#     ssh_username='d.nguyen',
#     ssh_pkey= '/home/dnguyen/.ssh/id.rsa',
#     remote_bind_address=('172.16.2.6', 3306),
#     local_bind_address = ('',33306)
# )
# server.start()

connector = mariadb.connect(user='PANEL-RO', password='PNL-P@n3l', host='localhost', port=33306)
cursor=connector.cursor()
query_1= """
select table_name
from information_schema.TABLES
where table_name like "%%"
and TABLE_TYPE='BASE TABLE';
"""
query_2 = """
show databases;
"""
cursor.execute(query_2)
result = cursor.fetchall()
for line in result:
    print(line)
connector.commit()
connector.close()




