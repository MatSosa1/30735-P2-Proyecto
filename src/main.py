cursor = NotImplemented
user = 'hola'

cursor.execute('SELECT * FROM Users WHERE user = ?', [user])
