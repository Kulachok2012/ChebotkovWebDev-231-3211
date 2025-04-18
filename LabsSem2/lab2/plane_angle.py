import math

class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __sub__(self, other):
        # Вычитание векторов
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def dot(self, other):
        # Скалярное произведение
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        # Векторное произведение
        return Point(self.y * other.z - self.z * other.y,
                     self.z * other.x - self.x * other.z,
                     self.x * other.y - self.y * other.x)

    def absolute(self):
        # Модуль вектора
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

def plane_angle(a, b, c, d):
    # Векторы AB, BC, CD
    ab = b - a
    bc = c - b
    cd = d - c

    # Векторные произведения AB × BC и BC × CD
    x = ab.cross(bc)
    y = bc.cross(cd)

    # Скалярное произведение X · Y
    dot_product = x.dot(y)

    # Модули векторов X и Y
    x_magnitude = x.absolute()
    y_magnitude = y.absolute()

    # Косинус угла между X и Y
    cos_phi = dot_product / (x_magnitude * y_magnitude)

    # Угол в радианах -> градусы
    angle = 180 - math.degrees(math.acos(cos_phi))
    return angle


if __name__ == '__main__':
    a = Point(*map(float, input().split()))
    b = Point(*map(float, input().split()))
    c = Point(*map(float, input().split()))
    d = Point(*map(float, input().split()))

    result = plane_angle(a, b, c, d)
    print(f"{result:.2f}")
