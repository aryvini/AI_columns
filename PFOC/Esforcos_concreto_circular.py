from scipy.integrate import quad
from numpy import sqrt, sin, arcsin, pi, cos


def rotacao(alfa1, x, y, volta=False, num=2):
    """
    Rotaciona os pontos em relação a um dado ângulo (de x e y para x' e y').
    :param alfa1: ângulo de rotação do plano cartesiano.
    :param x: coordenadas em x (vetor, deve ser usado o módulo numpy)
    :param y: coordenadas em y (vetor, deve ser usado o módulo numpy)
    :param volta: se verdadeiro este considera que os pontos dados já foram rotacionados (x' e y') e deseja-se
    obter estes em relação ao plano x e y padrão (opcional).
    :param num: se 1 retorna apenas a posição de y se 2 retorna de ambos (opcional)
    :return: os pontos rotacionados
    """

    if num == 2:
        if not volta:
            x_linha1 = x * cos(alfa1) + y * sin(alfa1)
            y_linha1 = -x * sin(alfa1) + y * cos(alfa1)
            return x_linha1, y_linha1
        else:
            x_linha1 = x * cos(alfa1) - y * sin(alfa1)
            y_linha1 = x * sin(alfa1) + y * cos(alfa1)
            return x_linha1, y_linha1
    elif num == 3:
        if not volta:
            x_linha1 = x * cos(alfa1) + y * sin(alfa1)
            return x_linha1
        else:
            x_linha1 = x * cos(alfa1) - y * sin(alfa1)
            return x_linha1
    else:
        if not volta:
            y_linha1 = -x * sin(alfa1) + y * cos(alfa1)
            return y_linha1
        else:
            y_linha1 = x * sin(alfa1) + y * cos(alfa1)
            return y_linha1


def fr_sit3(n1, t, c, fcd1, k2, k3):
    if abs(round(k2 - c, 4)) < 10 ** (-3):
        return -0.85 * fcd1 * t * c
    else:
        return -0.85 * fcd1 * t * (c + (k3 * (k2 - c) ** (n1 + 1)) / (n1 + 1))


def mry_sit3(n1, t, c1, fcd1, k2, k3):
    if abs(round(k2 - c1, 4)) < 10 ** (-3):
        return -0.85 * fcd1 * t * (0.5 * c1 ** 2)
    else:
        return -0.85 * fcd1 * t * (
                    0.5 * c1 ** 2 + (k3 * (k2 - c1) ** (n1 + 1) * (n1 * c1 + k2 + c1)) / (n1 ** 2 + 3 * n1 + 2))


# PARCELA RETANGULAR
def retangular(xec2, R1, x_o):
    c1 = (R1 - x_o + xec2) / R1

    teta = arcsin(c1)
    A = R1 ** 2 * (pi / 2 - teta) - (R1 - x_o + xec2) * R1 * cos(teta)
    Sy = (2/3) * R1 * cos(teta) * (R1 ** 2 - (R1 - x_o + xec2) ** 2)
    return A, Sy


# PARCELA PARABÓLICA
def f_rp(R, fck1, xo, d_1):
    # Cálculo dos parâmetros: n, ec2, ecu, fcd
    if fck1 * 10 <= 50:
        n = 2
        ec2 = 2 / 1000
        ecu = 3.5 / 1000

    else:
        n = 1.4 + 23.4 * ((90 - fck1 * 10) / 100) ** 4
        ec2 = (2 + 0.085 * (fck1 * 10 - 50) ** 0.53) / 1000
        ecu = (2.6 + 35 * ((90 - fck1 * 10) / 100) ** 4) / 1000

    fcd = fck1 / 1.4

    # cálculo dos parâmetros: e1, e2, xec2
    if xo == 0:
        forca = 0

    else:
        if 0 < xo <= ecu * d_1 / (ecu + 10 / 1000):
            e1 = (10 / 1000) * xo / (d_1 - xo)
            e2 = -10 / 1000

        elif ecu * d_1 / (ecu + 10 / 1000) < xo <= R:
            e1 = ecu
            e2 = ecu * (xo - d_1) / xo

        else:
            e1 = (ecu * ec2) * xo / (ecu * xo - (ecu - ec2) * 2 * R)
            e2 = (ecu * ec2) * (xo - d_1) / (ecu * xo - (ecu - ec2) * 2 * R)

        if round(abs(e1 - e2), 6) != 0:
            xec2 = round(d_1 * ec2 / (e1 - e2), 6)

            if abs(xec2 - xo) < 0.05:
                xec2 = xo

            k1 = 1 + (R - xo) / xec2
            k2 = k1 * xec2
            k3 = 1 / xec2 ** n
            y1 = round(R - xo, 6)
            y2 = round(y1 + xec2, 6)

            if (-R < y1 < R) and (-R < y2 < R):  # Situação 1

                # print('Situação 1')

                # PARCELA PARABÓLICA
                # Reta y1
                p1 = round(- sqrt(R ** 2 - y1 ** 2), 3)
                p2 = - p1

                forca = fr_sit3(n, p2, y1, fcd, k2, k3) - fr_sit3(n, p1, y1, fcd, k2, k3)

                # Trecho circular - y1 para y2
                p1 = round(arcsin(y1/R), 3)
                p2 = round(arcsin(y2/R), 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1), p1, p2)
                forca += 0.85 * fcd * (R ** 2 * (0.5*(p2 - p1) + 0.25 * (sin(2*p1) - sin(2*p2))) + resp[0] *
                                       (k3*R) / (n + 1))

                # Reta y2
                p1 = round(sqrt(R ** 2 - y2 ** 2), 3)
                p2 = -p1

                forca += (fr_sit3(n, p2, y2, fcd, k2, k3) - fr_sit3(n, p1, y2, fcd, k2, k3))

                # Trecho circular - y2 para y1
                p1 = round(pi - arcsin(y2/R), 3)
                p2 = round(pi - arcsin(y1/R), 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1), p1, p2)
                forca += 0.85 * fcd * (
                            R ** 2 * (0.5 * (p2 - p1) + 0.25 * (sin(2 * p1) - sin(2 * p2))) + resp[0] *
                            (k3 * R) / (n + 1))

                # PARCELA RETANGULAR
                area, momento = retangular(xec2, R, xo)
                forca += 0.85 * fcd * area

            elif (-R < y1 < R) and y2 >= R:  # Situação 2

                # print('Situação 2')

                # PARCELA PARABÓLICA
                # Reta y1
                p1 = round(- sqrt(R ** 2 - y1 ** 2), 3)
                p2 = - p1

                forca = fr_sit3(n, p2, y1, fcd, k2, k3) - fr_sit3(n, p1, y1, fcd, k2, k3)

                # Trecho circular - y1 para y1
                p1 = round(arcsin(y1/R), 3)
                p2 = round(pi - p1, 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1), p1, p2)

                forca += 0.85 * fcd * (
                        R ** 2 * (0.5 * (p2 - p1) + 0.25 * (sin(2 * p1) - sin(2 * p2))) + resp[0] * (k3 * R) / (n + 1))

                # PARCELA RETANGULAR
                # Não há parcela retangular apenas a parabólica

            elif fck1 * 10 != 90:  # Situação 3

                # print('Situação 3')

                # PARCELA PARABÓLICA
                # Trecho circular - y2 para y2
                p1 = -(pi + arcsin(y2 / R))
                p2 = arcsin(y2 / R)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1), p1, p2)
                forca = 0.85 * fcd * (
                        R ** 2 * (0.5 * (p2 - p1) + 0.25 * (sin(2 * p1) - sin(2 * p2))) + resp[0] * (k3 * R) / (n + 1))

                # Reta y2
                p1 = sqrt(R ** 2 - y2 ** 2)
                p2 = -p1

                forca += (fr_sit3(n, p2, y2, fcd, k2, k3) - fr_sit3(n, p1, y2, fcd, k2, k3))

                # PARCELA RETANGULAR
                area, momento = retangular(xec2, R, xo)
                forca += 0.85 * fcd * area

            else:
                # print('Situação especial')
                p1 = 0
                p2 = round(2*pi, 2)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1), p1, p2)
                forca = 0.85 * fcd * (
                        R ** 2 * (0.5 * (p2 - p1) + 0.25 * (sin(2 * p1) - sin(2 * p2))) + resp[0] * (k3 * R) / (n + 1))

        else:
            forca = fcd * (R ** 2 * pi) * 0.85
    return forca


def m_ry(alfa, R, fck1, xo, d_1):
    # Cálculo dos parâmetros: n, ec2, ecu, fcd
    if fck1 * 10 <= 50:
        n = 2
        ec2 = 2 / 1000
        ecu = 3.5 / 1000

    else:
        n = 1.4 + 23.4 * ((90 - fck1 * 10) / 100) ** 4
        ec2 = (2 + 0.085 * (fck1 * 10 - 50) ** 0.53) / 1000
        ecu = (2.6 + 35 * ((90 - fck1 * 10) / 100) ** 4) / 1000

    fcd = fck1 / 1.4

    # cálculo dos parâmetros: e1, e2, xec2
    if xo == 0:
        Mx = My = 0

    else:
        if 0 < xo <= ecu * d_1 / (ecu + 10 / 1000):
            e1 = (10 / 1000) * xo / (d_1 - xo)
            e2 = -10 / 1000

        elif ecu * d_1 / (ecu + 10 / 1000) < xo <= R:
            e1 = ecu
            e2 = ecu * (xo - d_1) / xo

        else:
            e1 = (ecu * ec2) * xo / (ecu * xo - (ecu - ec2) * 2 * R)
            e2 = (ecu * ec2) * (xo - d_1) / (ecu * xo - (ecu - ec2) * 2 * R)

        if round(abs(e1 - e2), 6) != 0:
            xec2 = round(d_1 * ec2 / (e1 - e2), 6)

            if abs(xec2 - xo) < 0.05:
                xec2 = xo

            k1 = 1 + (R - xo) / xec2
            k2 = k1 * xec2
            k3 = 1 / xec2 ** n
            y1 = round(R - xo, 6)
            y2 = round(y1 + xec2, 6)

            if (-R < y1 < R) and (-R < y2 < R) and fck1*10 != 90:  # Situação 1
                # PARCELA PARABÓLICA
                # Reta y1
                p1 = round(- sqrt(R ** 2 - y1 ** 2), 3)
                p2 = - p1

                mry = mry_sit3(n, p2, y1, fcd, k2, k3) - mry_sit3(n, p1, y1, fcd, k2, k3)

                # Trecho circular - y1 para y2
                p1 = round(arcsin(y1/R), 3)
                p2 = round(arcsin(y2/R), 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1) * (k2 + (n + 1) * R * sin(x)), p1, p2)
                mry += 0.85 * fcd * ((R ** 3 / 2) * (3/4*(cos(p1) - cos(p2)) + 1/12 * (cos(3*p2) - cos(3*p1))) +
                                     resp[0] * (k3*R) / (n ** 2 + 3 * n + 2))

                # Reta y2
                p1 = sqrt(R ** 2 - y2 ** 2)
                p2 = -p1

                mry += (mry_sit3(n, p2, y2, fcd, k2, k3) - mry_sit3(n, p1, y2, fcd, k2, k3))

                # Trecho circular - y2 para y1
                p1 = round(pi - arcsin(y2/R), 3)
                p2 = round(pi - arcsin(y1/R), 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1) * (k2 + (n + 1) * R * sin(x)), p1, p2)
                mry += 0.85 * fcd * ((R ** 3 / 2) * (3 / 4 * (cos(p1) - cos(p2)) + 1 / 12 * (cos(3 * p2) - cos(3 * p1)))
                                     + resp[0] * (k3 * R) / (n ** 2 + 3 * n + 2))

                # PARCELA RETANGULAR
                area, momento = retangular(xec2, R, xo)
                mry += 0.85 * fcd * momento

            elif (-R < y1 < R) and y2 >= R:  # Situação 2
                # PARCELA PARABÓLICA
                # Reta y1
                p1 = round(- sqrt(R ** 2 - y1 ** 2), 3)
                p2 = - p1

                mry = mry_sit3(n, p2, y1, fcd, k2, k3) - mry_sit3(n, p1, y1, fcd, k2, k3)

                # Trecho circular - y1 para y1
                p1 = round(arcsin(y1/R), 3)
                p2 = round(pi - p1, 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1) * (k2 + (n + 1) * R * sin(x)), p1, p2)
                mry += 0.85 * fcd * ((R ** 3 / 2) * (3 / 4 * (cos(p1) - cos(p2)) + 1 / 12 * (cos(3 * p2) - cos(3 * p1)))
                                     + resp[0] * (k3 * R) / (n ** 2 + 3 * n + 2))

                # PARCELA RETANGULAR
                # Não há parcela retangular apenas a parabólica

            elif fck1 * 10 != 90:  # Situação 3
                # PARCELA PARABÓLICA
                # Trecho circular - y2 para y2
                p1 = round(-(pi + arcsin(y2 / R)), 3)
                p2 = round(arcsin(y2 / R), 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1) * (k2 + (n + 1) * R * sin(x)), p1, p2)
                mry = 0.85 * fcd * ((R ** 3 / 2) * (3 / 4 * (cos(p1) - cos(p2)) + 1 / 12 * (cos(3 * p2) - cos(3 * p1)))
                                    + resp[0] * (k3 * R) / (n ** 2 + 3 * n + 2))

                # Reta y2
                p1 = sqrt(R ** 2 - y2 ** 2)
                p2 = -p1

                mry += (mry_sit3(n, p2, y2, fcd, k2, k3) - mry_sit3(n, p1, y2, fcd, k2, k3))

                # PARCELA RETANGULAR
                area, momento = retangular(xec2, R, xo)
                mry += 0.85 * fcd * momento

            else:
                p1 = 0
                p2 = round(2*pi, 3)

                resp = quad(lambda x: sin(x) * (k2 - R * sin(x)) ** (n + 1) * (k2 + (n + 1) * R * sin(x)), p1, p2)
                mry = 0.85 * fcd * ((R ** 3 / 2) * (3 / 4 * (cos(p1) - cos(p2)) + 1 / 12 * (cos(3 * p2) - cos(3 * p1)))
                                     + resp[0] * (k3 * R) / (n ** 2 + 3 * n + 2))

            mrx = 0
            Mx, My = rotacao(abs(alfa), mrx, mry)
        else:
            Mx = My = 0

    return Mx, My


if __name__ == '__main__':
    f = f_rp(15, 9, 40, 26)
    # my = m_ry(15, 2, 15, 26)  # R, fck1, xo, d_1
    # print(f"F = {f:.4f} kN\nMy = {my:.4f} kNcm")
