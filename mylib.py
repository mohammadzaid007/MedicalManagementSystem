import pymysql
def make_connection():
    conn=pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="",
        db="zaid",
        autocommit=True
    )
    cur=conn.cursor()
    return cur

def check_medicine_photo(mid):
    cur=make_connection()
    cur.execute("SELECT * FROM medicine_photo where med_id=" +str(mid) )
    n=cur.rowcount
    photo="no"
    if n>0:
        row=cur.fetchone()
        photo=row[1] #fetch name of photo

    return photo
