from app import db

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa' #Must be defined the table name

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)
    nim = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    def __init__(self, nim, name):
        self.nim = nim
        self.name = name

    def __repr__(self):
        return "<Name: {}, Nim: {}>".format(self.name, self.nim)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def getAll():
        students = Mahasiswa.query.all()
        result = []
        for student in students:
            obj = {
                'id': student.id,
                'nim': student.nim,
                'name': student.name
            }
            result.append(obj)
        return result

    def delete(self):
        db.session.delete(self)
        db.session.commit()
