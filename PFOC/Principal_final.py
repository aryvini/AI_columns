# Módulos e bibliotecas necessários
from math import ceil, floor, pi, asin, sqrt
from numpy import asarray, concatenate
import pandas as pd
from numero_ganchos import *
from Esforcos_de_calculo import *
import Verificacao_FCO_retangular as retangular
import Verificacao_FCO_circular as circular
from time import time
import datetime

# 1) Etapa 1 - Dados de entrada
# 1.1) Escolha da geometria
print(f"\033[1;36m{'1 DADOS DE ENTRADA'}\033[m")
print(f"\n\033[1;36m{'1.1 Dados iniciais'}\033[m")
nome = input('Qual o nome do pilar? ').strip().upper()

secao = pd.read_excel("Dados de entrada.xlsx", sheet_name="Geometria")
geometria = str(secao["Geometria"][0]).lower()


# 1.2) Esforços atuantes de projeto
# Força em [kN] - Momentos em [kNcm]
print()
esforcos = pd.read_excel("Dados de entrada.xlsx", sheet_name="Esforços")
Nsk = esforcos["Nsk"][0]
Msk_y_topo = esforcos["Msk,y-topo"][0]
Msk_y_base = esforcos["Msk,y-base"][0]
Msk_x_topo = esforcos["Msk,x-topo"][0]
Msk_x_base = esforcos["Msk,x-base"][0]

print(f"\033[1;36m1.2 Esforços de projeto\033[m")
print(f"Nsk = {Nsk:.2f} kN\nMsk,x-topo = {Msk_x_topo:.2f} kNcm\nMsk,x-base = {Msk_x_base:.2f} kNcm")
print(f"Msk,y-topo = {Msk_y_topo:.2f} kNcm\nMsk,y-base = {Msk_y_base:.2f} kNcm")

# 1.3) Dados do projeto
# PDE e vigas em [cm] - delta_c em [mm], escolher 5 ou 10 - caa inteiros em [1, 5]
criterios = pd.read_excel("Dados de entrada.xlsx", sheet_name="criterios")

PDE = criterios["PDE"][0]
viga_x = criterios["Viga em x (ou laje)"][0]
viga_y = criterios["Viga em y (ou laje)"][0]
delta_c = criterios["Dc"][0]
caa = criterios["CAA"][0]

print(f"\n\033[1;36m1.3 Critérios de projeto\033[m")
print(f"PDE = {PDE} cm\nViga em x/Laje em x = {viga_x} cm\nViga em y/Laje em y  = {viga_y} cm\n"
      f"Δc = {delta_c} mm\nCAA = {caa}")

# 1.4) Faixas dos Materiais utilizados e custo destes (aço, concreto, e formas)
# Armadura transversal
at = pd.read_excel("Dados de entrada.xlsx", sheet_name="AT")
estribo = at.loc[:, ['Ø (mm)', 'R$/m']].values
estribo = estribo.tolist()

# Armadura longitudinal
al = pd.read_excel("Dados de entrada.xlsx", sheet_name="AL")
bitolas_iniciais = []

for i in range(0, len(al)):
    if al["Considerar?"][0] == 'Sim':
        bitolas_iniciais.append([al["Ø (mm)"][i], al["Custo (R$/m)"][i]])

# fck
fck_tabela = pd.read_excel("Dados de entrada.xlsx", sheet_name="fck")
fck_iniciais = []

for i in range(0, len(fck_tabela)):
    if fck_tabela["Considerar?"][i] == "Sim":
        fck_iniciais.append([fck_tabela["fck (MPa)"][i], fck_tabela["Custo (R$/m³)"][i]])

# Custo das formas
custo_forma = pd.read_excel("Dados de entrada.xlsx", sheet_name="fôrmas")
formas_retangular = custo_forma["Retangular"][0]
forma_circular = custo_forma["Circular"][0]


print(f"\n\033[1;36m1.4 Faixas de materiais\033[m")
Tabela_bitolas = pd.DataFrame(concatenate((asarray(estribo), asarray(bitolas_iniciais))), columns=['Ø (mm)', 'R$/m'])
Tabela_fck = pd.DataFrame(fck_iniciais, columns=['fck (MPa)', 'R$/m³'])

print(f"Aço\n{Tabela_bitolas}\n")
print(f"Concreto\n {Tabela_fck}\n")
print(f"Formas\nRetangular: {formas_retangular} R$/m²")
print(f"Circular: {forma_circular} R$/m²")

# 1.5) parâmetros da seção transversal
print(f"\n\033[1;36m1.5 Parâmetros da seção transversal\033[m")
print(f"Geometria escolhida: {geometria}\n")

# Circular
if geometria[0] == 'c':
    while True:
        g1 = input('Deseja fixar o diâmetro do pilar [S/N]? ').strip().lower()

        if g1 == 's':
            while True:
                secoes_iniciais = [int(input('Escolha um valor entre 22 cm e 30 cm, '
                                             'e de 30 a 50 cm (multiplo de 5): '))]

                if 22 <= secoes_iniciais[0] <= 30 or (secoes_iniciais[0] > 30 and secoes_iniciais[0] % 5 == 0):
                    break
            break
        elif g1 == 'n':
            secoes_iniciais = [22, 23, 24, 25, 26, 27, 28, 29, 30, 35, 40, 45, 50]
            break
        else:
            print(f'\033[1;31mErro! valor não válido.\033[m\n')

    inicio = time()

# Retangular
else:
    while True:
        b1 = input('Deseja fixar a base [S/N]? ').strip().lower()

        if b1 == 'n' or b1 == 's':
            break
        else:
            print(f'\033[1;31mErro! "{b1}" não é um valor válido.\033[m\n')

    while True:
        if b1 == 'n':
            b = 'livre'
            break

        elif b1 == 's':
            b = input('Digite o valor da base (14 cm a 25 cm, 30 cm): ').strip().lower()

            if b.isnumeric() and (14 <= int(b) <= 40):

                if (int(b) != 26 and int(b) != 27 and int(b) != 28 and int(b) != 29) or int(b) % 5 == 0:
                    break
                else:
                    print(f'\033[1;31mErro! "{b}" não é valor válido.\033[m\n')
            else:
                print(f'\033[1;31mErro! "{b}" não é valor válido.\033[m\n')

    print()

    while True:
        h1 = input('Deseja fixar a altura [S/N]? ').strip().lower()

        if h1 == 'n' or h1 == 's':
            break
        else:
            print(f'\033[1;31mErro! "{h1}" não é um valor válido.\033[m\n')

    while True:
        if h1 == 'n':
            h = 'livre'
            break
        elif h1 == 's':

            h = input('Digite o valor da altura (19 cm a 150 cm): ').strip().lower()

            if h.isnumeric() and (19 <= int(h) <= 150):
                v = True

                if b.isnumeric() and int(h) * int(b) <= 360:
                    v = False
                    print('\033[1;31mErro! B ∙ H ≥ 360 cm²\033[m\n')

                elif b.isnumeric():
                    if (int(b) != 19 and int(b) != 21 and int(b) != 22 and int(b) != 23 and int(b) != 24) \
                            and int(h) % 5 != 0:
                        v = False
                        print(f'\033[1;31mErro! "{b}" não é um valor válido.\033[m\n')

                if v:
                    break
            else:
                print(f'\033[1;31mErro! "{b}" não é um valor válido.\033[m\n')

    inicio = time()

    secoes_iniciais = [[14, [30, 35, 40, 45, 50, 55, 60, 65, 70]],
                       [15, [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75]],
                       [16, [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]],
                       [17, [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]],
                       [18, [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]],
                       [19, [19, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]],
                       [20, [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]],
                       [21, [21, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]],
                       [22, [22, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110]],
                       [23, [23, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115]],
                       [24, [24, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120]],
                       [25, [25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125]],
                       [30,
                        [30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135,
                         140, 145, 150]],
                       [35, [35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135,
                             140, 145, 150, 155, 160, 165, 170, 175]],
                       [40, [40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110, 115, 120, 125, 130, 135,
                             140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200]]]

    n_bases = len(secoes_iniciais[:])

    if b.isnumeric() and h.isnumeric():
        secoes_iniciais = [[int(b), [int(h)]]]

    elif b.isnumeric():
        secoes_iniciais1 = secoes_iniciais[:][:]

        for i in range(0, n_bases):
            if secoes_iniciais1[i][0] == int(b):
                secoes_iniciais = [[int(b), secoes_iniciais1[i][1]]]

        del secoes_iniciais1

    elif h.isnumeric():
        secoes_iniciais1 = secoes_iniciais[:][:]
        secoes_iniciais = []

        for i in range(0, n_bases):
            for k in range(0, len(secoes_iniciais1[i][1])):
                if secoes_iniciais1[i][1][k] == int(h):
                    secoes_iniciais.append([secoes_iniciais1[i][0], [secoes_iniciais1[i][1][k]]])
                    break

# 2) Etapa 2 - Obtenção dos AE possíveis

print(f'\n\033[1;34m{"2 RELATÓRIOS"}\033[m')
# 2.1) Definições iniciais
# Relação entre classe de agressividade ambiental (CAA), cobrimento e fck, baseado na tabela 7.2 da NBR 6118:2014
CAA = [{'fck': 20, 'c': 2.5}, {'fck': 25, 'c': 3}, {'fck': 30, 'c': 4}, {'fck': 40, 'c': 5}]
posicoes_AE = []
# Coeficientes e dados gerais
gama_f = 1.4
gama_s = 1.15
fyd = 50 / gama_s
Dmax_agreg = 1.9

# Verificação dos fcks possíveis (levando em conta o CAA) e do cobrimento
f_ck = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
fck_possiveis = []

for i in range(0, len(fck_iniciais)):

    for j in range(0, len(f_ck)):
        if f_ck[len(f_ck) - 1] >= fck_iniciais[i][0] >= CAA[caa - 1]['fck'] and fck_iniciais[i][0] == f_ck[j]:
            fck_possiveis.append([fck_iniciais[i][0], fck_iniciais[i][1]])
            break

if len(fck_possiveis) == 0:
    print('\033[1;31mErro. Sem fcks possíveis\033[m')
    exit()

Nsd = 0

# 2.2) Verificação dos AE possíveis
# Seção retangular
if geometria[0] == 'r':

    n_bases = len(secoes_iniciais[:])
    combinacoes_possiveis = []

    for i1 in range(0, n_bases):
        n_alturas = len(secoes_iniciais[i1][1])
        base = secoes_iniciais[i1][0]
        esbeltez_x = round(min(PDE, PDE - viga_x + base) * 3.46 / base, 2)

        if base <= 19:
            gama_n = 1.95 - 0.05 * base
        else:
            gama_n = 1

        Nsd = gama_f * gama_n * Nsk

        for i2 in range(0, n_alturas):
            altura = secoes_iniciais[i1][1][i2]
            esbeltez_y = round(min(PDE, PDE - viga_y + altura) * 3.46 / altura, 2)
            As_min = max(0.004 * base * altura, 0.15 * Nsd / fyd)
            As_max = 0.04 * base * altura

            # Avaliação dos critérios de esbeltez, elemento linear e área mínima e máxima
            if PDE / altura >= 3 and max(esbeltez_y, esbeltez_x) <= 90 and As_max > As_min:
                bitolas_possiveis = []
                fi_l_max = base * 10 / 8

                for i3 in range(0, len(bitolas_iniciais)):
                    if bitolas_iniciais[i3][0] <= fi_l_max:

                        fi_l = bitolas_iniciais[i3][0]
                        custo_fi_l = bitolas_iniciais[i3][1]

                        # Estribo
                        if 5 >= fi_l / 4:
                            fi_t = 5
                            custo_fi_t = estribo[0][1]
                        else:
                            fi_t = 6.3
                            custo_fi_t = estribo[1][1]

                        st = min(20, base, 12 * fi_l / 10)

                        if delta_c == 10:
                            c_inicial = CAA[caa - 1]['c']
                        else:
                            c_inicial = CAA[caa - 1]['c'] - 0.5

                        c_nom = max(c_inicial, 1.2 * Dmax_agreg, fi_l / 10)

                        emax_eixos = min(40, 2 * base)
                        emin_livre = max(1.2 * Dmax_agreg, fi_l / 10)

                        # Números mínimos e máximos. Considera-se as esperas no eixo y
                        Nx_min = ceil(max(2, (base - 2 * (c_nom + fi_t / 10) - fi_l / 10) / emax_eixos + 1))
                        Ny_min = ceil(max(2, (altura - 2 * (c_nom + fi_t / 10) - fi_l / 10) / emax_eixos + 1))

                        Nx_max = max(floor((base - 2 * (c_nom + fi_t / 10) + emin_livre + fi_l / 10) /
                                           (emin_livre + 2 * fi_l / 10)), 2)
                        Ny_max = floor((altura - 2 * (c_nom + fi_t / 10) + 2 * fi_l / 10 + emin_livre) /
                                       (emin_livre + 3 * fi_l / 10))

                        if Nx_min <= Nx_max and Ny_max >= Ny_min:
                            for i4 in range(Nx_min, Nx_max + 1):

                                for i5 in range(Ny_min, Ny_max + 1):

                                    AS = round((2 * (i4 + i5) - 4) * (fi_l / 20) ** 2 * pi, 2)

                                    if As_min <= AS <= As_max:

                                        # Cálculo do custo
                                        # Armadura
                                        N_barras = 2 * (i4 + i5) - 4
                                        C_st_r = 2 * (base + altura) - 8 * c_nom + 2 * max(5 * fi_t / 10,
                                                                                           5) + 3 * fi_t / 10
                                        Ng_x, Ng_y = numero_ganchos(base, altura, i4, i5, c_nom, fi_t, fi_l)

                                        if Ng_x > 0:
                                            C_st_sup_x = sqrt((base - 2 * c_nom - 2 * fi_t / 10 - fi_l / 10) ** 2 +
                                                              (fi_l / 10) ** 2) + pi * fi_l / 10 + 2 * max(
                                                5 * fi_t / 10, 5)

                                        else:
                                            C_st_sup_x = 0

                                        if Ng_y > 0:
                                            C_st_sup_y = sqrt((altura - 2 * c_nom - 2 * fi_t / 10 - fi_l / 10) ** 2 +
                                                              (fi_t / 10) ** 2) + pi * fi_l / 10 + 2 * max(
                                                5 * fi_t / 10, 5)
                                        else:
                                            C_st_sup_y = 0

                                        N_st = round(100 / st + 1, 0)
                                        C_armaduras = N_barras * custo_fi_l + N_st * C_st_r / 100 * custo_fi_t + N_st \
                                                      * (Ng_x * C_st_sup_x / 100 + Ng_y * C_st_sup_y / 100) * custo_fi_t

                                        # Formas
                                        # print(f"{N_barras * custo_fi_l :.2f} *** {N_barras} *** {}")
                                        C_formas = formas_retangular * 2 * (base / 100 + altura / 100)
                                        C_total = C_armaduras + C_formas

                                        combinacoes_possiveis.append([base, altura, fi_t, st, fi_l, i4,
                                                                      i5, Ng_x, Ng_y, c_nom, AS, C_st_sup_x,
                                                                      C_st_sup_y, C_total])

                    else:
                        break

    s = 0

    if len(combinacoes_possiveis) == 0:
        print('Erro. Sem AE possíveis.')
        exit()

    comp = len(combinacoes_possiveis[0])
    combinacoes_possiveis1 = combinacoes_possiveis[:][:]
    combinacoes_possiveis = []

    for i1 in range(0, len(fck_possiveis)):
        for i2 in range(0, len(combinacoes_possiveis1)):

            # Custo concreto
            base = combinacoes_possiveis1[i2][0]
            altura = combinacoes_possiveis1[i2][1]
            C_concreto = fck_possiveis[i1][1] * base / 100 * altura / 100

            aux = [fck_possiveis[i1][0]]
            for i3 in range(0, comp):
                if i3 < comp - 1:
                    aux.append(combinacoes_possiveis1[i2][i3])
                else:
                    C_total = round(combinacoes_possiveis1[i2][i3] + C_concreto, 2)
                    aux.append(C_total)
            combinacoes_possiveis.append(aux)

            s += 1

    combinacoes_possiveis = asarray(combinacoes_possiveis)
    tabela_solucoes_possiveis = pd.DataFrame(combinacoes_possiveis, columns=['fck', 'b', 'h', 'Øt', 'St', 'Øl', 'Nx',
                                                                              'Ny', 'Ngx', 'Ngy', 'Cnom', 'As',
                                                                             'C st sup x', 'C st sup y', 'R$/m'])

# Seção circular
else:
    combinacoes_possiveis = []
    s = 0

    for i1 in range(0, len(secoes_iniciais)):
        fi_pilar = secoes_iniciais[i1]
        area_pilar = pi * (fi_pilar / 2) ** 2

        esbeltez_x = round(min(PDE, PDE - viga_x + fi_pilar) * 4 / fi_pilar, 2)
        esbeltez_y = round(min(PDE, PDE - viga_y + fi_pilar) * 4 / fi_pilar, 2)

        gama_n = 1
        Nsd = gama_f * gama_n * Nsk

        As_min = max(0.004 * area_pilar, 0.15 * Nsd / fyd)
        As_max = 0.04 * area_pilar

        if PDE / fi_pilar >= 3 and max(esbeltez_y, esbeltez_x) <= 90 and As_max > As_min:
            bitolas_possiveis = []
            fi_l_max = fi_pilar * 10 / 8

            for i2 in range(0, len(bitolas_iniciais)):
                if bitolas_iniciais[i2][0] <= fi_l_max:
                    fi_l = bitolas_iniciais[i2][0]
                    custo_fi_l = bitolas_iniciais[i2][1]

                    # Estribo
                    if 5 >= fi_l / 4:
                        fi_t = 5
                        custo_fi_t = estribo[0][1]
                    else:
                        fi_t = 6.3
                        custo_fi_t = estribo[1][1]

                    st = min(20, fi_pilar, 12 * fi_l / 10)

                    if delta_c == 10:
                        c_inicial = CAA[caa - 1]['c']
                    else:
                        c_inicial = CAA[caa - 1]['c'] - 0.5

                    c_nom = max(c_inicial, 1.2 * Dmax_agreg, fi_l / 10)

                    emax_eixos = min(40, 2 * fi_pilar)
                    emin_livre = max(1.2 * Dmax_agreg, fi_l / 10)

                    fi_poligono = fi_pilar - 2 * (c_nom + fi_t / 10) - fi_l / 10
                    Nc_min = 6
                    Nc_max = floor(pi / asin((emin_livre + 3 * fi_l / 10) / fi_poligono))

                    if Nc_min <= Nc_max:

                        for i3 in range(Nc_min, Nc_max + 1):

                            AS = round(i3 * (fi_l / 20) ** 2 * pi, 4)

                            if i3 % 2 == 0:  # Armaduras simétricas

                                if As_min <= AS <= As_max:
                                    # Cálculo do custo
                                    # Armadura
                                    N_barras = i3
                                    C_st_c = 1.5 * pi * (fi_pilar - 2 * c_nom) + 2 * max(5 * fi_t / 10,
                                                                                         5) + 3 * pi * fi_t / 10
                                    C_armaduras = N_barras * custo_fi_l + round(100 / st + 1, 0) * C_st_c / 100 \
                                                  * custo_fi_t

                                    # Formas
                                    C_forma = fi_pilar * pi * forma_circular / 100

                                    C_total = C_forma + C_armaduras
                                    combinacoes_possiveis.append([fi_pilar, fi_t, st, fi_l, i3, c_nom, AS,
                                                                  esbeltez_x, esbeltez_y, C_total])
                else:
                    break

    s = 0

    if len(combinacoes_possiveis) == 0:
        print('Sem soluções possíveis para a seção transversal escolhida.')
        exit()

    comp = len(combinacoes_possiveis[0])

    combinacoes_possiveis1 = combinacoes_possiveis[:][:]
    combinacoes_possiveis = []
    for i1 in range(0, len(fck_possiveis)):

        for i2 in range(0, len(combinacoes_possiveis1)):
            fi_pilar = combinacoes_possiveis1[i2][0]
            C_concreto = (fck_possiveis[i1][1] * fi_pilar ** 2 * pi / 4) / 10 ** 4

            aux = [fck_possiveis[i1][0]]
            for i3 in range(0, comp):
                if i3 < comp - 1:
                    aux.append(combinacoes_possiveis1[i2][i3])
                else:
                    C_total = round(combinacoes_possiveis1[i2][i3] + C_concreto, 2)
                    aux.append(C_total)
            combinacoes_possiveis.append(aux)

            s += 1

    combinacoes_possiveis = asarray(combinacoes_possiveis)
    tabela_solucoes_possiveis = pd.DataFrame(combinacoes_possiveis, columns=['fck', 'Øpilar', 'Øt', 'St', 'Øl',
                                                                              'Nc', 'Cnom', 'As', 'λx', 'λy', 'R$/m'])

print(f'\n\033[1;34m{"2.1 AE possíveis "}\033[m')
print(f"Há {s} soluções possíveis (a serem verificadas).")
tabela_solucoes_possiveis.sort_values("R$/m", axis=0, ascending=True, inplace=True)

# if geometria[0] == 'r':
#     tabela_solucoes_possiveis.to_excel(f'{nome} (retangular) soluções possíveis.xlsx', sheet_name='soluções')
# else:
#     tabela_solucoes_possiveis.to_excel(f'{nome} (circular) soluções possíveis.xlsx', sheet_name='soluções')

# Etapa 4 - esforços de cálculo e Verificação dos arranjos
razao = 0
ha_respostas = False
n = 0

if geometria[0] == 'r':

    for i1 in range(0, len(tabela_solucoes_possiveis)):

        # fck', 'b', 'h', 'Øt', 'St', 'Øl', 'Nx', 'Ny', 'Ngx', 'Ngy', 'Cnom', 'As', 'C st sup x', 'C st sup y', 'R$/m
        fck = tabela_solucoes_possiveis.iloc[i1, 0] / 10
        b = tabela_solucoes_possiveis.iloc[i1, 1]
        h = tabela_solucoes_possiveis.iloc[i1, 2]
        fi_t = tabela_solucoes_possiveis.iloc[i1, 3]
        St = tabela_solucoes_possiveis.iloc[i1, 4]
        fi_l = tabela_solucoes_possiveis.iloc[i1, 5]
        Nx = tabela_solucoes_possiveis.iloc[i1, 6]
        Ny = tabela_solucoes_possiveis.iloc[i1, 7]
        Ng_x = tabela_solucoes_possiveis.iloc[i1, 8]
        Ng_y = tabela_solucoes_possiveis.iloc[i1, 9]
        cobrimento = tabela_solucoes_possiveis.iloc[i1, 10]
        Aso = tabela_solucoes_possiveis.iloc[i1, 11]
        C_st_sup_x = tabela_solucoes_possiveis.iloc[i1, 12]
        C_st_sup_y = tabela_solucoes_possiveis.iloc[i1, 13]
        custo = tabela_solucoes_possiveis.iloc[i1, 14]

        situacoes_de_calculo = esforcos_de_calculo(b, h, PDE, viga_x, viga_y, fck, Nsk, Msk_y_topo, Msk_y_base,
                                                   Msk_x_topo, Msk_x_base)

        numero_verificacoes = 0

        for i2 in range(0, len(situacoes_de_calculo)):

            Msd_x = situacoes_de_calculo.loc[i2, 'Mdx (kNcm)']
            Msd_y = situacoes_de_calculo.loc[i2, 'Mdy (kNcm)']

            razao = retangular.verificacao(fck, b, h, cobrimento, int(Nx), int(Ny), fi_t, fi_l, Nsd, Msd_x, Msd_y, Aso)
            # fck, base, altura, c, nx, ny, fi_t, fi_l, Nd, Mdx, Mdy, Aso, relatorio=False

            if razao >= 0.99:
                numero_verificacoes += 1

        # Impressão dos relatórios
        if numero_verificacoes == len(situacoes_de_calculo):
            ha_respostas = True
            print(f'\n\033[1;34m{"2.2 Número de soluções verificadas"}\033[m')
            print(i1)

            print(f'\n\033[1;34m{"2.3 Solução mais econômica"}\033[m')
            print(f'{"1 - Resistencia e dados da seção"}')
            print(f"  • fck = {fck*10} MPa\n  • base = {b} cm\n  • Altura = {h} cm\n  • C = {cobrimento} cm;")

            print(f'\n{"2 - Dados da armadura"}')
            print(f'{"2.1 - Armadura longitudinal"}')
            print(f"    • Øl = {fi_l} mm\n    • Nx = {int(Nx)}\n    • Ny = {int(Ny)}\n    • Aso = {Aso:.2f} cm²")
            print(f'\n{"2.2 - Transversal"}')
            C_st_r = 2 * (b + h) - 8 * cobrimento + 2 * max(5 * fi_t / 10, 5) + 3 * fi_t / 10
            print(f"    • St = {St:.2f} cm")
            print(f"    • Øt = {fi_t} mm\n    • Comp. estribo = {C_st_r:.2f} cm\n    • Ngx = {Ng_x:.0f}")

            if Ng_x > 0:
                print(f"    • Comp. gancho em x = {C_st_sup_x:.2f} cm")

            print(f"    • Ngy = {Ng_y:.0f}")

            if Ng_y > 0:
                print(f"    • Comp. gancho em x = {C_st_sup_y:.2f} cm")

            print(f'\n{"3 - Custo total (Concreto + Aço + fôrmas)"}')
            print(f"  • Custo = {custo:.2f} R$/m")

            esforcos_de_calculo(b, h, PDE, viga_x, viga_y, fck, Nsk, Msk_y_topo, Msk_y_base,
                                Msk_x_topo, Msk_x_base, relatorio=True)

            for i2 in range(0, len(situacoes_de_calculo)):
                Msd_x = situacoes_de_calculo.loc[i2, 'Mdx (kNcm)']
                Msd_y = situacoes_de_calculo.loc[i2, 'Mdy (kNcm)']

                texto = str(2.5 + i2/10) + ' Verificação da seção à FCO - S.C ' + str(i2)
                print(f'\n\033[1;34m{texto:}\033[m')
                retangular.verificacao(fck, b, h, cobrimento, int(Nx), int(Ny), fi_t, fi_l, Nsd,
                                       Msd_x, Msd_y, Aso, relatorio=True)
                print()
            break

        n += 1

    if not ha_respostas:
        print(f"\nSem soluções possíveis. \n")

else:

    for i1 in range(0, len(tabela_solucoes_possiveis)):

        # 'fck', 'Øpilar', 'Øt', 'St', 'Øl', 'Nc', 'Cnom', 'As', 'λx', 'λy', 'R$/m'
        fck = round(tabela_solucoes_possiveis.iloc[i1, 0] / 10, 1)
        fi_pilar = tabela_solucoes_possiveis.iloc[i1, 1]
        fi_t = tabela_solucoes_possiveis.iloc[i1, 2]
        St = tabela_solucoes_possiveis.iloc[i1, 3]
        fi_l = tabela_solucoes_possiveis.iloc[i1, 4]
        Nc = tabela_solucoes_possiveis.iloc[i1, 5]
        cobrimento = tabela_solucoes_possiveis.iloc[i1, 6]
        Aso = tabela_solucoes_possiveis.iloc[i1, 7]
        custo = tabela_solucoes_possiveis.iloc[i1, 10]

        # print(f"fck = {fck} *** Øp = {fi_pilar} *** Øl = {fi_l} *** Nc = {Nc} *** c = {cobrimento} *** As = {Aso:.2f}"
        #       f"*** custo = {custo}")

        situacoes_de_calculo = esforcos_de_calculo(fi_pilar, fi_pilar, PDE, viga_x, viga_y, fck, Nsk, Msk_y_topo,
                                                   Msk_y_base, Msk_x_topo, Msk_x_base)

        numero_verificacoes = 0

        for i2 in range(0, len(situacoes_de_calculo)):
            Msd_x = round(situacoes_de_calculo.loc[i2, 'Mdx (kNcm)'], 2)
            Msd_y = round(situacoes_de_calculo.loc[i2, 'Mdy (kNcm)'], 2)

            razao = circular.verificacao(fck, fi_pilar, cobrimento, int(Nc), fi_t, fi_l, Nsd, Msd_x, Msd_y, Aso)
            # fck1, fi_pilar1, c11, Nc1, fi_t1, fi_l1, Nd1, Mdx1, Mdy1, Aso1

            if razao >= 0.99:
                numero_verificacoes += 1

        # Impressão dos relatórios
        if numero_verificacoes == len(situacoes_de_calculo):
            ha_respostas = True

            C_st_c = 1.5 * pi * (fi_pilar - 2 * cobrimento) + 2 * max(5 * fi_t / 10, 5) + 3 * pi * fi_t / 10
            print(f'\n\033[1;34m{"2.2 Solução mais econômica"}\033[m')
            print(f'{"1 - Resistencia e dados da seção"}')
            print(f"  • fck = {fck * 10} MPa\n  • Øpilar = {fi_pilar} cm\n  • C = {cobrimento} cm;")
            print(f'\n{"2 - Dados da armadura"}')
            print(f"  • Øt = {fi_t} mm\n  • Øl = {fi_l} mm\n"
                  f"  • Nc = {Nc}\n"
                  f"  • Aso = {Aso:.2f} cm²\n"
                  f"  • St = {St:.2f} cm;\n"
                  f"  • Comp. estribo = {C_st_c:.2f} cm.")
            print(f'\n{"n3 - Custo total"}')
            print(f"  • Custo = {custo:.2f} R$/m")

            esforcos_de_calculo(fi_pilar, fi_pilar, PDE, viga_x, viga_y, fck, Nsk, Msk_y_topo,
                                Msk_y_base, Msk_x_topo, Msk_x_base, relatorio=True)

            for i2 in range(0, len(situacoes_de_calculo)):
                Msd_x = situacoes_de_calculo.loc[i2, 'Mdx (kNcm)']
                Msd_y = situacoes_de_calculo.loc[i2, 'Mdy (kNcm)']

                texto = str(2.4 + i2 / 10) + ' Verificação da seção à FCO - S.C ' + str(i2)
                print(f'\n\033[1;34m{texto:}\033[m')
                razao = circular.verificacao(fck, fi_pilar, cobrimento, int(Nc), fi_t, fi_l, Nsd, Msd_x, Msd_y, Aso,
                                             relatorio=True)
            break

        n += 1

    if not ha_respostas:
        print(f"\nSem soluções possíveis.\n")

fim = time()
tempo = fim - inicio

print(f'\033[1;34m{"2.6 Dados gerais"}\033[m')
print(f'\n\033[1;34m{"2.6.1 Tempo de execução"}\033[m')

if 60 * 60 >= tempo > 60:
    print(f"Tempo total de execução = {tempo/60:.2f} minutos.")
elif tempo <= 60:
    print(f"Tempo total de execução = {tempo :.2f} segundos.")
else:
    print(f"Tempo total de execução = {tempo / 3600:.2f} horas.")

now = datetime.datetime.now()

print(f'\n\033[1;34m{"2.6.2 Data de execução"}\033[m')
print(f"{now.day}/{now.month}/{now.year} - {now.hour}:{now.minute}")
