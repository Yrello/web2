from predict import pred


def convert_chol(a):  # converting chol value to ds standart
    return a * 38.665


def convert_glucose(a):  # converting glucose value to ds standart
    return a * 18.016


class Stat:
    def __init__(self, version, age, sex, cigs, chol, bp, glucose):
        self.version = version
        self.age = age
        self.sex = sex
        self.cigs = cigs
        self.chol = chol
        self.bp = bp
        self.glucose = glucose
        self.data = dict()

    def get_age(self, age):
        self.age = age

    def get_sex(self, sex):
        self.sex = sex

    def get_cigs(self, cigsPerDay):
        self.cigs = cigsPerDay

    def get_chol(self, totChol):
        self.chol = int(convert_chol(totChol))

    def get_bp(self, sysBP):
        self.bp = sysBP

    def get_glucose(self, glucose):
        self.glucose = int(convert_glucose(glucose))

    def pack_data(self):
        self.data['age'] = self.age
        self.data['sex'] = self.sex
        self.data['cigs'] = self.cigs
        self.data['chol'] = self.chol
        self.data['bp'] = self.bp
        self.data['glucose'] = self.glucose

    def get_data(self):
        return self.data

    def predict_result(self):
        return pred(([self.age, self.sex, self.cigs, self.chol, self.bp, self.glucose]), 'true_seasup.pkl')
