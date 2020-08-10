# DIMENSIONAMENTO DE PILARES RETANGULARES SUBMETIDOS À FCO
# Desenvolvido por: Daniel D. Grossmann
# noinspection PyUnresolvedReferences

# MÓDULOS IMPORTADOS
from numpy import zeros, array, pi, arccos, sqrt, sign, set_printoptions
from scipy import optimize
from Esforcos_concreto_retangular import *
from operator import itemgetter
from functools import partial


# FUNÇÕES UTILIZADAS
# Deformação das barras (Domínio 2 - Domínio 3, 4 e 4a - Domínio 5, respectivamente)
def deformacao(x, di, h, d11, ecu, ec2):
    if 0 <= x <= ecu / (ecu + 10) * d11:
        return (10 / 1000) * (x - di) / (d11 - x)

    elif ecu / (ecu + 10) * d11 < x <= h:
        return (ecu / 1000) * (x - di) / x

    else:
        return (ecu * ec2) * (x - di) / (ecu * x - (ecu - ec2) * h) / 1000


# Tensão das barras, segue a figura 8.4 da NBR 6118:2014
def tensao(e):
    if round(abs(e)*1000, 3) <= 2.0704:
        return e * 21000
    elif 2.0704 < round(abs(e)*1000, 3) <= 10:
        return 50 / 1.15 * sign(e)


# Nsd - Nrd
def normal(x,  fck, base, altura, Aso, alfa1, posicoes_inc, h_inc, d1, ymax_inc, n_barras, Nd, ecu, ec2):
    tensoes = zeros(n_barras)

    acc, sxc, syc = esforcos_resistentes(fck, base, altura, alfa1, x, d1, h_inc, ymax_inc)
    for ii in range(n_barras):
        tensoes[ii] = tensao(deformacao(x, posicoes_inc[ii, 4], h_inc, d1, ecu, ec2))
        # print(f"{deformacao(x, posicoes_inc[ii, 4], h_inc, d1)*1000:.5f} ***", end='')
    soma_sigma = sum(tensoes)

    return Nd - (Aso * soma_sigma / n_barras + acc)


# Momento resistente em y
def myd(fck, base, altura, Aso, x, alfa1, posicoes_inc, h_inc, d1, ymax_inc, n_barras, ecu, ec2):
    tensoes = zeros(n_barras)

    acc, sxc, syc = esforcos_resistentes(fck, base, altura, alfa1, x, d1, h_inc, ymax_inc)
    for ii in range(n_barras):
        tensoes[ii] = tensao(deformacao(x, posicoes_inc[ii, 4], h_inc, d1, ecu, ec2))
    soma_sigma_y = sum(tensoes * posicoes_inc[:, 1])
    return abs(syc + Aso / n_barras * soma_sigma_y)


# Momento resistente em x
def mxd(fck, base, altura, Aso, x, alfa1, posicoes_inc, h_inc, d1, ymax_inc, n_barras, ecu, ec2):
    tensoes = zeros(n_barras)

    acc, sxc, syc = esforcos_resistentes(fck, base, altura, alfa1, x, d1, h_inc, ymax_inc)

    for ii in range(n_barras):
        tensoes[ii] = tensao(deformacao(x, posicoes_inc[ii, 4], h_inc, d1, ecu, ec2))

    soma_sigma_x = sum(tensoes * posicoes_inc[:, 0])

    return abs(sxc + Aso / n_barras * soma_sigma_x)


# Encontrar inclinação da linha neutra (alfa)
def angulo(alfa, fck, base, altura, Aso, Nd, n_barras, ecu, ec2, theta_d, pontos, posicoes, resultado='inc'):

    posicoes_inc = zeros([n_barras, 5])  # x - y - x' - y' - d'
    posicoes_inc[:, 0] = posicoes[:, 0]
    posicoes_inc[:, 1] = posicoes[:, 1]
    posicoes_inc[:, 2], posicoes_inc[:, 3] = rotacao(alfa, posicoes[:, 0], posicoes[:, 1])

    ymax_inc = max(rotacao(alfa, pontos[:, 0], pontos[:, 1], num=1))
    ymin_inc = min(rotacao(alfa, pontos[:, 0], pontos[:, 1], num=1))
    posicoes_inc[:, 4] = ymax_inc - posicoes_inc[:, 3]

    posicoes_inc = sorted(posicoes_inc.tolist(), key=itemgetter(4), reverse=True)
    posicoes_inc = array(posicoes_inc)
    h_inc = ymax_inc - ymin_inc
    d1 = posicoes_inc[0, 4]
    # print(d1)
    normal_parcial = partial(normal, fck=fck, base=base, altura=altura, Aso=Aso, alfa1=alfa, posicoes_inc=posicoes_inc,
                             h_inc=h_inc, d1=d1, ymax_inc=ymax_inc, n_barras=n_barras, Nd=Nd, ecu=ecu, ec2=ec2)
    # x, fck, base, altura, Aso, alfa1, posicoes_inc, h_inc, d1, ymax_inc, n_barras, Nd, ecu, ec2

    if normal_parcial(0) * normal_parcial(ecu / (ecu + 10) * d1) < 0:

        x1 = optimize.brentq(normal_parcial, 0, ecu / (ecu + 10) * d1, xtol=1e-6, rtol=1e-8)

    elif normal_parcial(ecu / (ecu + 10) * d1) * normal_parcial(h_inc) < 0:

        x1 = optimize.brentq(normal_parcial, ecu / (ecu + 10) * d1, h_inc, xtol=1e-6, rtol=1e-8)

    elif normal_parcial(h_inc) * normal_parcial(10 ** 8) < 0:

        x1 = optimize.brentq(normal_parcial, h_inc, 10 ** 8, xtol=1e-6, rtol=1e-8)
    else:
        x1 = -100

    if x1 != -100:
        mxd_p = mxd(fck, base, altura, Aso, x1, alfa, posicoes_inc, h_inc, d1, ymax_inc, n_barras, ecu, ec2)
        # fck, base, altura, Aso, x, alfa1, posicoes_inc, h_inc, d1, ymax_inc, n_barras, ecu, ec2
        myd_p = myd(fck, base, altura, Aso, x1, alfa, posicoes_inc, h_inc, d1, ymax_inc, n_barras, ecu, ec2)
        theta_r = arccos(mxd_p / sqrt(mxd_p ** 2 + myd_p ** 2))
    else:
        theta_r = -100
        mxd_p = myd_p = 0

    if resultado == 'inc':
        return theta_r - theta_d
    elif resultado == 'momentos':
        return mxd_p, myd_p
    else:
        return x1, d1, h_inc, ymax_inc


def verificacao(fck, base, altura, c, nx, ny, fi_t, fi_l, Nd, Mdx, Mdy, Aso, relatorio=False):
    n_barras = 2 * (nx + ny) - 4
    d_linha = c + (fi_t + fi_l / 2) / 10

    # d_linha = 4

    if fck * 10 <= 50:
        ec2 = 2
        ecu = 3.5

    else:
        ec2 = round((2 + 0.085 * (fck * 10 - 50) ** 0.53), 3)
        ecu = (2.6 + 35 * ((90 - fck * 10) / 100) ** 4)

    posicoes = zeros([n_barras, 4])  # x - y - dy - dx

    pontos = array([[base / 2, altura / 2], [-base / 2, altura / 2], [base / 2, -altura / 2], [-base / 2, -altura / 2]])

    # Descrição das posições das barras (x - y e d)
    n_linha_x = []

    for i in range(0, ny):
        if i == 0 or i == ny - 1:
            n_linha_x.append(nx)
        else:
            n_linha_x.append(2)

    k = i = 0
    while k < ny:
        cont = 0
        while True:
            posicoes[i, 3] = d_linha + (ny - k - 1) * (altura - 2 * d_linha) / (ny - 1)
            posicoes[i, 1] = altura / 2 - posicoes[i, 3]

            posicoes[i, 2] = d_linha + (n_linha_x[k] - cont - 1) * (base - 2 * d_linha) / (n_linha_x[k] - 1)
            posicoes[i, 0] = base / 2 - posicoes[i, 2]
            cont += 1
            i += 1

            if cont == n_linha_x[k]:
                k += 1
                break

    # Dimensionamento em si
    theta_d = arccos(Mdx / sqrt(Mdx**2 + Mdy**2))

    # alfa, fck, base, altura, Aso, Nd, n_barras, ecu, ec2, theta_d, pontos, posicoes, resultado = 'inc'
    angulo_parcial = partial(angulo, fck=fck, base=base, altura=altura, Aso=Aso, Nd=Nd, n_barras=n_barras, ecu=ecu,
                             ec2=ec2, theta_d=theta_d, pontos=pontos, posicoes=posicoes, resultado='inc')

    if angulo_parcial(0) * angulo_parcial(-pi/2) <= 0:
        resp = optimize.brentq(angulo_parcial, 0, -pi/2, xtol=1e-6, rtol=1e-8)

        mrx, mry = angulo(resp, fck, base, altura, Aso, Nd, n_barras, ecu, ec2, theta_d, pontos, posicoes,
                          resultado='momentos')

        mr = sqrt(mrx**2 + mry**2)
        ms = sqrt(Mdx**2 + Mdy**2)
        razao = mr/ms

        if relatorio:

            x0, d_1, hinc, ymax = angulo(resp, fck, base, altura, Aso, Nd, n_barras, ecu, ec2, theta_d, pontos,
                                         posicoes, resultado='variáveis')

            print(f"• Parâmetros principais:")
            print(f"alfa = {resp*180/pi:.2f}°\nx = {x0:.2f} cm\nd1 = {d_1:.2f} cm\nHa = {hinc:.2f} cm\n"
                  f"ymax = {ymax:.2f} cm\nAso = {Aso:.2f} cm²\n")

            print("• Verificação em si:")
            if razao >= 0.99:
                print(f"ER/ES = {razao:.4f}. Verifica!")
            else:
                print(f"ER/ES = {razao:.4f}. Não verifica!")

    else:
        razao = -1

        if relatorio:
            print(razao)

    return razao


if __name__ == '__main__':
    fck1 = 2  # kN/cm²
    E = 21000  # kN/cm²
    altura1 = 71.5  # cm
    base1 = 40.3  # cm
    c11 = 2.5  # cm

    nx1 = 3
    ny1 = 3

    fi_t1 = 5  # mm
    fi_l1 = 10  # mm

    Nd1 = 1150  # kN
    Mdx1 = Nd1 * 7.5  # kNcm
    Mdy1 = Nd1 * 20  # kNcm

    # Aso1 = (2*(nx1 + ny1) - 4) * (fi_l1/20) ** 2 * pi  # cm²
    Aso1 = 11.5
    razao1 = verificacao(fck1, base1, altura1, c11, nx1,
                         ny1, fi_t1, fi_l1, Nd1, Mdx1,
                         Mdy1, Aso1, relatorio=True)

# fck, base, altura, c, nx, ny, fi_t, fi_l, Nd, Mdx, Mdy

