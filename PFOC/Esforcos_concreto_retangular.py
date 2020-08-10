# noinspection PyUnresolvedReferences
from numpy import array, cos, sin, tan, pi, concatenate, sign, zeros, arccos, sqrt, asarray


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


def intercepto(base1, altura1, a_reta1, b_reta1, alfa1):
    cont1 = 0
    intercepto1 = []

    if abs(alfa1) != pi / 2:
        if altura1 / 2 >= a_reta1 * (-base1 / 2) + b_reta1 >= -altura1 / 2:  # x = B/2
            xx = round(-base1 / 2, 4)
            yy = round(a_reta1 * (-base1 / 2) + b_reta1, 4)
            intercepto1.append([xx, yy])
            cont1 += 1

        if alfa1 != 0 and base1 / 2 >= (altura1 / 2 - b_reta1) / a_reta1 >= -base1 / 2:  # y = H/2
            xx = round((altura1 / 2 - b_reta1) / a_reta1, 4)
            yy = round(altura1 / 2, 4)
            intercepto1.append([xx, yy])
            cont1 += 1

        if (altura1 / 2 >= a_reta1 * base1 / 2 + b_reta1 >= -altura1 / 2) and cont1 != 2:  # x = -B/2
            xx = round(base1 / 2, 4)
            yy = round(a_reta1 * (base1 / 2) + b_reta1, 4)
            intercepto1.append([xx, yy])
            cont1 += 1

        if alfa1 != 0 and (base1 / 2 >= (-altura1 / 2 - b_reta1) / a_reta1 >= -base1 / 2) and cont1 != 2:  # y = -H/2
            xx = round((-altura1 / 2 - b_reta1) / a_reta1, 4)
            yy = round(-altura1 / 2, 4)
            intercepto1.append([xx, yy])
            cont1 += 1
    else:
        if base1 / 2 >= b_reta1 >= -base1 / 2:  # y = H/2
            xx = round(b_reta1, 4)
            yy = round(altura1 / 2, 4)
            intercepto1.append([xx, yy])

        if base1 / 2 >= b_reta1 >= -base1 / 2:  # y = -H/2
            xx = round(b_reta1, 4)
            yy = round(-altura1 / 2, 4)
            intercepto1.append([xx, yy])

    if len(intercepto1) == 0:
        intercepto2 = []
    else:
        intercepto2 = [intercepto1[0]]
        if intercepto1[0] != intercepto1[1]:
            intercepto2.append(intercepto1[1])

    return intercepto2


# Integrais
def fr_c_sit1(n1, t, a1, b1, fcd1, k2, k3):
    if abs(round(-a1 * t - b1 + k2, 4)) < 10 ** (-3):
        return -0.85 * fcd1 * (0.5 * a1 * t ** 2 + b1 * t)
    else:
        return -0.85 * fcd1 * (
                    (0.5 * a1 * t ** 2 + b1 * t) - k3 * (-a1 * t - b1 + k2) ** (n1 + 2) / (a1 * (n1 + 1) * (n1 + 2)))


def fr_c_sit3(n1, t, c1, fcd1, k2, k3):
    if abs(round(k2 - c1, 4)) < 10 ** (-3):
        return -0.85 * fcd1 * t * c1
    else:
        return -0.85 * fcd1 * t * (c1 + (k3 * (k2 - c1) ** (n1 + 1)) / (n1 + 1))


def mry_sit1(n1, v, a1, fcd1, k2, k3):
    if abs(round(k2 - v, 4)) < 10 ** (-3):
        return (-0.85 * fcd1 / a1) * (v ** 3 / 6)
    else:
        return (-0.85 * fcd1 / a1) * (
                    v ** 3 / 6 - (k3 * (k2 - v) ** (n1 + 2) * (v * (n1 + 1) + 2 * k2)) / ((n1 + 1) * (n1 + 2) *
                                                                                          (n1 + 3)))


def mry_sit3(n1, t, c1, fcd1, k2, k3):
    if abs(round(k2 - c1, 4)) < 10 ** (-3):
        return -0.85 * fcd1 * t * (0.5 * c1 ** 2)
    else:
        return -0.85 * fcd1 * t * (
                    0.5 * c1 ** 2 + (k3 * (k2 - c1) ** (n1 + 1) * (n1 * c1 + k2 + c1)) / (n1 ** 2 + 3 * n1 + 2))


def mrx_sit1(n1, t, a1, b1, fcd1, k2, k3):
    if abs(round(-a1 * t - b1 + k2, 4)) < 10 ** (-3):
        return -0.85 * fcd1 * (a1 * t ** 3 / 3 + 0.5 * b1 * t ** 2)
    else:
        return -0.85 * fcd1 * ((a1 * t ** 3 / 3 + 0.5 * b1 * t ** 2) - k3 * (-a1 * t - b1 + k2) ** (n1 + 2) *
                               (a1 * t * (n1 + 2) - b1 + k2) / (a1 ** 2 * (n1 + 1) * (n1 ** 2 + 5 * n1 + 6)))


def mrx_sit3(n1, t, c1, fcd1, k2, k3):
    if abs(round(k2 - c1, 4)) < 10 ** (-3):
        return -0.425 * fcd1 * t ** 2 * c1
    else:
        return -0.425 * fcd1 * t ** 2 * (c1 + k3 * (k2 - c1) ** (n1 + 1) / (n1 + 1))


def parabola(pontos1, fcd1, y_max, x_0, x_ec2, n1, esforco):
    total = 0
    k1 = 1 + (y_max - x_0) / x_ec2
    k2 = k1 * x_ec2
    k3 = 1 / (x_ec2 ** n1)
    n_pontos = len(pontos1) - 1

    for i11 in range(0, n_pontos):
        delta_x = round(pontos1[i11 + 1, 0] - pontos1[i11, 0], 6)
        delta_y = round(pontos1[i11 + 1, 1] - pontos1[i11, 1], 6)

        if abs(delta_x) > 1 / 100 and abs(delta_y) > 1 / 100:
            m = delta_y / delta_x
            a1 = m
            b1 = pontos1[i11, 1] - pontos1[i11, 0] * m

            if esforco == 'forca':
                parcial_aa = fr_c_sit1(n1, pontos1[i11, 0], a1, b1, fcd1, k2, k3)
                parcial_bb = fr_c_sit1(n1, pontos1[i11 + 1, 0], a1, b1, fcd1, k2, k3)

            elif esforco == 'mrx':
                parcial_aa = mrx_sit1(n1, pontos1[i11, 0], a1, b1, fcd1, k2, k3)
                parcial_bb = mrx_sit1(n1, pontos1[i11 + 1, 0], a1, b1, fcd1, k2, k3)
            else:
                parcial_aa = mry_sit1(n1, pontos1[i11, 1], a1, fcd1, k2, k3)
                parcial_bb = mry_sit1(n1, pontos1[i11 + 1, 1], a1, fcd1, k2, k3)

        elif abs(delta_x) < 1 / 100:
            parcial_aa = parcial_bb = 0

        else:
            c1 = pontos1[i11][1]

            if esforco == 'forca':
                parcial_aa = fr_c_sit3(n1, pontos1[i11, 0], c1, fcd1, k2, k3)
                parcial_bb = fr_c_sit3(n1, pontos1[i11 + 1, 0], c1, fcd1, k2, k3)

            elif esforco == 'mrx':
                parcial_aa = mrx_sit3(n1, pontos1[i11, 0], c1, fcd1, k2, k3)
                parcial_bb = mrx_sit3(n1, pontos1[i11 + 1, 0], c1, fcd1, k2, k3)
            else:
                parcial_aa = mry_sit3(n1, pontos1[i11, 0], c1, fcd1, k2, k3)
                parcial_bb = mry_sit3(n1, pontos1[i11 + 1, 0], c1, fcd1, k2, k3)

        total += parcial_bb - parcial_aa

    return total


def area_ou_momentos(pp, tipo='area'):
    area = 0
    me_y = 0
    me_x = 0

    for i12 in range(0, len(pp) - 1):
        area += pp[i12][0] * pp[i12 + 1][1] - pp[i12][1] * pp[i12 + 1][0]
        me_y += (pp[i12][1] + pp[i12 + 1][1]) * (pp[i12][0] * pp[i12 + 1][1] - pp[i12][1] * pp[i12 + 1][0])
        me_x += (pp[i12][0] + pp[i12 + 1][0]) * (pp[i12][0] * pp[i12 + 1][1] - pp[i12][1] * pp[i12 + 1][0])

    area *= 1 / 2
    me_y *= 1 / 6
    me_x *= 1 / 6

    if tipo == 'area':
        return area
    elif tipo == 'mry':
        return me_y
    else:
        return me_x


def esforcos_resistentes(fck1, base1, altura1, alfa1, x_o, d_1, h_inc, y_max):
    # PARCELA DO CONCRETO
    # Cálculo dos parâmetros: n, ec2, ecu, fcd
    if fck1 * 10 <= 50:
        n = 2
        ec2 = 2 / 1000
        ecu = 3.5 / 1000

    else:
        n = 1.4 + 23.4 * ((90 - fck1 * 10) / 100) ** 4
        ec2 = (2 + 0.085 * (fck1 * 10 - 50) ** 0.53) / 1000
        ecu = (2.6 + 35 * ((90 - fck1 * 10) / 100) ** 4) / 1000

    fcd1 = fck1 / 1.4

    # cálculo dos parâmetros: e1, e2, xec2
    if x_o == 0:
        forca_total = mrx_total = mry_total = 0

    else:
        if 0 < x_o <= ecu * d_1 / (ecu + 10 / 1000):
            e1 = (10 / 1000) * x_o / (d_1 - x_o)
            e2 = -10 / 1000

        elif ecu * d_1 / (ecu + 10 / 1000) < x_o <= h_inc:
            e1 = ecu
            e2 = ecu * (x_o - d_1) / x_o

        else:
            e1 = (ecu * ec2) * x_o / (ecu * x_o - (ecu - ec2) * h_inc)
            e2 = (ecu * ec2) * (x_o - d_1) / (ecu * x_o - (ecu - ec2) * h_inc)

        if round(abs(e1 - e2), 6) != 0:

            xec2 = round(d_1 * ec2 / (e1 - e2), 6)

            if abs(x_o - xec2) < 0.05:
                xec2 = x_o

            # Descrição da retas y1 = ymax - xo e y1 = ymax - xo + xec2
            beta = round(y_max - x_o, 6)
            beta_xec2 = beta + xec2

            if abs(alfa1) != pi / 2:

                a_reta = tan(alfa1)
                b_reta_xo = tan(alfa1) * beta * sin(alfa1) + beta * cos(alfa1)
                b_reta_xec2 = tan(alfa1) * beta_xec2 * sin(alfa1) + beta_xec2 * cos(alfa1)
            else:
                b_reta_xo = beta
                a_reta = 0
                b_reta_xec2 = beta_xec2

            intercepto_xo = intercepto(base1, altura1, a_reta, b_reta_xo, alfa1)
            intercepto_xec2 = intercepto(base1, altura1, a_reta, b_reta_xec2, alfa1)

            # Pontos da poligonal (parábola) e ordenação no sentido anti-horário
            poligonal_parabola = []
            poligonal_retangulo = []

            if abs(alfa1) != pi / 2:  # alfa não é igual a -90
                if len(intercepto_xo) == 0 or len(intercepto_xo) == 1:  # Ponto (-b/2, -h/2) - LN
                    poligonal_parabola.append([-base1 / 2, -altura1 / 2])
                else:
                    if intercepto_xo[0][0] < intercepto_xo[1][0]:
                        poligonal_parabola.append(intercepto_xo[0])
                        poligonal_parabola.append(intercepto_xo[1])

                    else:
                        poligonal_parabola.append(intercepto_xo[1])
                        poligonal_parabola.append(intercepto_xo[0])

                if a_reta * (base1 / 2) + b_reta_xo < -altura1 / 2 < a_reta * (base1 / 2) + b_reta_xec2:
                    # Ponto (b/2, -h/2) - LN e Xec2
                    poligonal_parabola.append([base1 / 2, -altura1 / 2])

                if abs((ec2 - e2)) * 1000 > 1 / 1000 or (abs((ec2 - e2)) * 1000 < 1 / 1000 and fck1 * 10 == 90):
                    if len(intercepto_xec2) == 2:  # LN + Xec2
                        if intercepto_xec2[0][0] > intercepto_xec2[0][1]:
                            poligonal_parabola.append(intercepto_xec2[0])
                            poligonal_parabola.append(intercepto_xec2[1])
                        else:
                            poligonal_parabola.append(intercepto_xec2[1])
                            poligonal_parabola.append(intercepto_xec2[0])

                    elif (len(intercepto_xec2) == 1 and intercepto_xec2[0][1] == altura1 / 2) or \
                            len(intercepto_xec2) == 0:
                        # (b/2, h/2)
                        poligonal_parabola.append([base1 / 2, altura1 / 2])

                    if a_reta * (-base1 / 2) + b_reta_xo < altura1 / 2 < a_reta * (-base1 / 2) + b_reta_xec2:
                        # Ponto (-b/2, h/2)
                        poligonal_parabola.append([-base1 / 2, altura1 / 2])
                else:
                    poligonal_parabola = []

            else:  # alfa é igual a -90
                if len(intercepto_xo) == 0:  # Ponto (-b/2, -h/2) - LN
                    poligonal_parabola.append([-base1 / 2, altura1 / 2])
                    poligonal_parabola.append([-base1 / 2, -altura1 / 2])
                else:
                    if intercepto_xo[0][1] > intercepto_xo[1][1]:
                        poligonal_parabola.append(intercepto_xo[0])
                        poligonal_parabola.append(intercepto_xo[1])

                    else:
                        poligonal_parabola.append(intercepto_xo[1])
                        poligonal_parabola.append(intercepto_xo[0])

                if abs(ec2 - e2) * 1000 > 1 / 1000 or (abs((ec2 - e2)) * 1000 < 1 / 1000 and fck1 * 10 == 90):
                    if len(intercepto_xec2) == 2:  # LN + Xec2
                        if intercepto_xec2[0][1] < intercepto_xec2[1][1]:
                            poligonal_parabola.append(intercepto_xec2[0])
                            poligonal_parabola.append(intercepto_xec2[1])
                        else:
                            poligonal_parabola.append(intercepto_xec2[1])
                            poligonal_parabola.append(intercepto_xec2[0])
                    else:
                        poligonal_parabola.append([base1 / 2, -altura1 / 2])
                        poligonal_parabola.append([base1 / 2, altura1 / 2])
                else:
                    poligonal_parabola = []

            # Pontos da poligonal (retangulo) e ordenação no sentido anti-horário
            if len(intercepto_xec2) == 0 or abs(xec2 - x_o) < 1 / 1000:
                poligonal_retangulo = []
            elif abs((ec2 - e2)) < 0.05 / 1000:  # Caso em que a LN é muito grande e assim e2 tende a ec2
                poligonal_retangulo = [[base1 / 2, altura1 / 2], [-base1 / 2, altura1 / 2],
                                       [-base1 / 2, -altura1 / 2], [base1 / 2, -altura1 / 2]]

            elif abs(alfa1) != pi / 2:
                if intercepto_xec2[0][0] < intercepto_xec2[1][0]:
                    poligonal_retangulo.append(intercepto_xec2[0])
                    poligonal_retangulo.append(intercepto_xec2[1])
                else:
                    poligonal_retangulo.append(intercepto_xec2[1])
                    poligonal_retangulo.append(intercepto_xec2[0])

                if - altura1 / 2 > a_reta * (base1 / 2) + b_reta_xec2:
                    poligonal_retangulo.append([base1 / 2, -altura1 / 2])  # (b/2, -h/2)
                if altura1 / 2 > a_reta * (base1 / 2) + b_reta_xec2:
                    poligonal_retangulo.append([base1 / 2, altura1 / 2])
                if altura1 / 2 > a_reta * (-base1 / 2) + b_reta_xec2:
                    poligonal_retangulo.append([-base1 / 2, altura1 / 2])  # (-b/2, h/2)
            else:
                if intercepto_xec2[0][1] > intercepto_xec2[1][1]:
                    poligonal_retangulo.append(intercepto_xec2[0])
                    poligonal_retangulo.append(intercepto_xec2[1])
                else:
                    poligonal_retangulo.append(intercepto_xec2[1])
                    poligonal_retangulo.append(intercepto_xec2[0])

                poligonal_retangulo.append([base1 / 2, -altura1 / 2])
                poligonal_retangulo.append([base1 / 2, altura1 / 2])

            # Cálculo da forca e dos momentos resultantes
            if len(poligonal_parabola) == 0:
                forca_parabola = 0
                mrx_parabola = 0
                mry_parabola = 0
            else:
                poligonal_parabola.append(poligonal_parabola[0])
                # deve-se fechar o polígono ao aplicar o teorema de Green!
                poligonal_parabola = asarray(poligonal_parabola)
                poligonal_parabola1 = zeros([len(poligonal_parabola), 2])
                poligonal_parabola1[:, 0], poligonal_parabola1[:, 1] = rotacao(alfa1, poligonal_parabola[:, 0],
                                                                               poligonal_parabola[:, 1])

                forca_parabola = parabola(poligonal_parabola1, fcd1, y_max, x_o, xec2, n, esforco='forca')  # F em kN
                mrx_parabola = parabola(poligonal_parabola1, fcd1, y_max, x_o, xec2, n, esforco='mrx')
                mry_parabola = parabola(poligonal_parabola1, fcd1, y_max, x_o, xec2, n, esforco='mry')
            if len(poligonal_retangulo) == 0:
                forca_retangulo = 0
                mrx_retangulo = 0
                mry_retangulo = 0
            else:
                poligonal_retangulo.append(poligonal_retangulo[0])
                forca_retangulo = area_ou_momentos(poligonal_retangulo, tipo='area') * 0.85 * fcd1  # F em kN
                # print(f"forca = {forca_retangulo:.2f} kN")
                mrx_retangulo = area_ou_momentos(poligonal_retangulo, tipo='mrx') * 0.85 * fcd1
                mry_retangulo = area_ou_momentos(poligonal_retangulo, tipo='mry') * 0.85 * fcd1

            forca_total = forca_parabola + forca_retangulo
            mrx_parabola1, mry_parabola1 = rotacao(abs(alfa1), mrx_parabola, mry_parabola)

            # if __name__ == '__main__':
            # print(f"\nFp = {forca_parabola:.2f} kN")
            # print(f"Mp,x' = {mrx_parabola:.2f} kNcm")
            # print(f"Mp,y' = {mry_parabola:.2f} kNcm\n")

            mrx_total = mrx_parabola1 + mrx_retangulo
            mry_total = mry_parabola1 + mry_retangulo

            # print(poligonal_parabola)
            # print()

        else:

            mrx_total = mry_total = 0

            forca_total = base1 * altura1 * fcd1 * 0.85
    # print(f"{forca_total:.2f}")
    return forca_total, mrx_total, mry_total


if __name__ == '__main__':
    f, mx, my = esforcos_resistentes(9, 30, 30, 0, 20, 37.84, 43.48, 21.74)
    # f, mx, my = esforcos_resistentes(9, 30, 30, 0, 20, 37.84, 43.48, 21.74)
    print(f"f = {f:.2f} kN\nMx = {mx:.2f} kNcm\nMy = {my:.2f} kNcm")

# fck1, base1, altura1, alfa1, x_o, d_1, h_inc, y_max
