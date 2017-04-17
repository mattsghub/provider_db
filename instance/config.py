SECRET_KEY = 'p9Bv<3Eid9a_(@*JSD(jdjd9sOadxxxsdsd2)(*&^21213$i01'

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="mattspython",
    password="password123",
    hostname="mattspython.mysql.pythonanywhere-services.com",
    databasename="mattspython$provider_db",
)
