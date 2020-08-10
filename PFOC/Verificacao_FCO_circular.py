# DIMENSIONAMENTO DE PILARES CIRCULARES SUBMETIDOS À FCO
# Desenvolvido por: Daniel D. Grossmann
# noinspection PyUnresolvedReferences

# 1 - MÓDULOS UTILIZADOS
from numpy import pi, sin, cos, zeros, array, sign, arcsin, arccos, set_printoptions
from Esforcos_concreto_circular import *
from scipy import optimize
from operator import itemgetter
from functools import partial
set_printoptions(suppress=True)
import pandas as pd


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
def normal(x, fck, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, Nd, ecu, ec2):
    tensoes = zeros(n_barras)

    acc = f_rp(fi_pilar/2, fck, x, d1)
    for ii in range(n_barras):
        tensoes[ii] = tensao(deformacao(x, posicoes_inc[ii, 4], h_inc, d1, ecu, ec2))
        # print(f"{deformacao(x, posicoes_inc[ii, 4], h_inc, d1)*1000:.5f} ***", end='')
    soma_sigma = sum(tensoes)
    # print(tensoes)
    return Nd - (Aso * soma_sigma / n_barras + acc)


# Momento resistente em y
def myd(x, fck, alfa1, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, ecu, ec2):
    tensoes = zeros(n_barras)
    sxc, syc = m_ry(alfa1, fi_pilar/2, fck, x, d1)

    for ii in range(n_barras):
        tensoes[ii] = tensao(deformacao(x, posicoes_inc[ii, 4], h_inc, d1, ecu, ec2))
    soma_sigma_y = sum(tensoes * posicoes_inc[:, 1])

    return abs(syc + Aso / n_barras * soma_sigma_y)


def mxd(x, fck, alfa1, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, ecu, ec2):
    tensoes = zeros(n_barras)
    sxc, syc = m_ry(alfa1, fi_pilar/2, fck, x, d1)

    for ii in range(n_barras):
        tensoes[ii] = tensao(deformacao(x, posicoes_inc[ii, 4], h_inc, d1, ecu, ec2))

    soma_sigma_x = sum(tensoes * posicoes_inc[:, 0])

    return abs(sxc + Aso / n_barras * soma_sigma_x)


# Encontrar inclinação da linha neutra (alfa)
def angulo(alfa, fck, Nc, posicoes, fi_pilar, ecu, ec2, theta_d, Aso, Nd, resultado='inc'):

    n_barras = Nc
    posicoes_inc = zeros([n_barras, 5])  # x - y - x' - y' - d'
    posicoes_inc[:, 0] = posicoes[:, 0]
    posicoes_inc[:, 1] = posicoes[:, 1]
    posicoes_inc[:, 2], posicoes_inc[:, 3] = rotacao(alfa, posicoes[:, 0], posicoes[:, 1])

    ymax_inc = fi_pilar / 2
    posicoes_inc[:, 4] = ymax_inc - posicoes_inc[:, 3]

    posicoes_inc = sorted(posicoes_inc.tolist(), key=itemgetter(4), reverse=True)
    posicoes_inc = array(posicoes_inc)
    h_inc = fi_pilar
    d1 = posicoes_inc[0, 4]

    normal_parcial = partial(normal, fck=fck, posicoes_inc=posicoes_inc, h_inc=h_inc, d1=d1, fi_pilar=fi_pilar,
                             n_barras=n_barras, Aso=Aso, Nd=Nd, ecu=ecu, ec2=ec2)
    # x, fck, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, Nd, ecu, ec2

    if normal_parcial(0) * normal_parcial(ecu / (ecu + 10) * d1) < 0:

        x1 = optimize.brentq(normal_parcial, 0, ecu / (ecu + 10) * d1)

    elif normal_parcial(ecu / (ecu + 10) * d1) * normal_parcial(h_inc) < 0:

        x1 = optimize.brentq(normal_parcial, ecu / (ecu + 10) * d1, h_inc)

    elif normal_parcial(h_inc) * normal_parcial(10 ** 7) < 0:

        x1 = optimize.brentq(normal_parcial, h_inc, 10 ** 7)
    else:
        x1 = -100

    if x1 != -100:
        mxd_p = mxd(x1, fck, alfa, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, ecu, ec2)
        myd_p = myd(x1, fck, alfa, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, ecu, ec2)
        # x, fck, alfa1, posicoes_inc, h_inc, d1, fi_pilar, n_barras, Aso, ecu, ec2

        theta_r = arccos(mxd_p / sqrt(mxd_p ** 2 + myd_p ** 2))
    else:
        theta_r = - 100
        mxd_p = myd_p = 0

    if resultado == 'inc':
        return theta_r - theta_d
    elif resultado == 'momentos':
        return mxd_p, myd_p
    else:
        return x1, d1, h_inc, ymax_inc


def verificacao(fck, fi_pilar, c, Nc, fi_t, fi_l, Nd, Mdx, Mdy, Aso, relatorio=False, tabela=False):
    # CÁLCULOS

    if fck * 10 <= 50:
        ec2 = 2
        ecu = 3.5

    else:
        ec2 = (2 + 0.085 * (fck * 10 - 50) ** 0.53)
        ecu = (2.6 + 35 * ((90 - fck * 10) / 100) ** 4)

    n_barras = Nc
    posicoes = zeros([n_barras, 4])  # x - y - dy - dx

    # Descrição das posições das barras (x - y e d)
    R = (fi_pilar - 2 * c - 2 * fi_t / 10 - fi_l / 10) / 2

    for i in range(0, Nc):
        angulo_total = (2 * pi / Nc) * i
        posicoes[i, 0] = R * cos(angulo_total)
        posicoes[i, 1] = R * sin(angulo_total)
        posicoes[i, 2] = R - posicoes[i, 1] + (c + fi_l / 20 + fi_t / 10)
        posicoes[i, 3] = R - posicoes[i, 0] + (c + fi_l / 20 + fi_t / 10)

    if tabela:
        tabela_posicoes = pd.DataFrame(posicoes, columns=['x', 'y', "dx", "dy"])
        tabela_posicoes.to_excel(f"{fi_pilar}.xlsx")

    # Dimensionamento em si
    theta_d = arccos(Mdx / sqrt(Mdx**2 + Mdy**2))
    # print(angulo(0))

    angulo_parcial = partial(angulo, fck=fck, Nc=Nc, posicoes=posicoes, fi_pilar=fi_pilar, ecu=ecu, ec2=ec2,
                             theta_d=theta_d, Aso=Aso, Nd=Nd, resultado='inc')
    # alfa, fck, Nc, posicoes, fi_pilar, ecu, ec2, theta_d, Aso, Nd, resultado = 'inc'

    if angulo_parcial(0) * angulo_parcial(-pi/2) <= 0:
        resp = optimize.brentq(angulo_parcial, 0, -pi/2)

        mrx, mry = angulo(resp, fck, Nc, posicoes, fi_pilar, ecu, ec2, theta_d, Aso, Nd, resultado='momentos')
        x0, d_1, hinc, ymax = angulo(resp, fck, Nc, posicoes, fi_pilar, ecu, ec2, theta_d, Aso, Nd,
                                     resultado='variáveis')

        mr = sqrt(mrx**2 + mry**2)
        ms = sqrt(Mdx**2 + Mdy**2)
        razao = mr/ms

        if relatorio:
            print(f"1 - Parâmetros principais:")
            x0, d_1, hinc, ymax = angulo(resp, fck, Nc, posicoes, fi_pilar, ecu, ec2, theta_d, Aso, Nd,
                                         resultado='variáveis')

            print(f"\nVariáveis:\nalfa = {resp*180/pi:.2f}°\nx = {x0:.4f} cm\nd1 = {d_1:.4f} cm\nHa = {hinc:.2f} cm\n"
                  f"ymax = {ymax:.2f} cm")
            print(f'Aso = {Aso:.2f} cm²\n')
            print("2 - Verificação em si:")
            if razao >= 0.99:
                print(f"MR/MS = {razao:.4f}. Verifica!\n")
            else:
                print(f"MR/MS = {razao:.4f}. Não verifica!\n")

    else:
        razao = - 1
        if relatorio:
             print(razao)

    return razao


if __name__ == '__main__':
    fck1 = 2.0  # kN/cm²
    fi_pilar1 = 25  # cm
    c11 = 2.5  # cm

    Nc1 = 6
    fi_t1 = 5  # mm
    fi_l1 = 12.5  # mm

    Nd1 = 600 * 1.4  # kN
    Mdx1 = 0  # kNcm
    Mdy1 = 15000 * 1.4   # kNcm

    Aso1 = (fi_l1/20) ** 2 * pi * Nc1  # kNcm

    razao1 = verificacao(fck1, fi_pilar1, c11, Nc1, fi_t1,
                         fi_l1, Nd1, Mdx1, Mdy1, Aso1, relatorio=True)
