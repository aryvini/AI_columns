"""
Esforcos_de_calculo - Neste arquivo realiza-se a verificação dos esforços de cálculo
"""

from numpy import sqrt, asarray
import pandas as pd


def esforcos_de_calculo(base, altura, PDE, h_viga_x, h_viga_y, fck, nk, mk_y_topo1, mk_y_base1, mk_x_topo1,
                        mk_x_base1, relatorio=False):

    # Manipulação dos dados (evitar possíveis erros devido aos sinais inseridos para os esforços)
    if mk_x_base1 == mk_x_topo1:
        mk_x_base = abs(mk_x_base1)
        mk_x_topo = abs(mk_x_topo1)

    else:
        mk_x_topo = max(abs(mk_x_topo1), abs(mk_x_base1))
        mk_x_base = - min(abs(mk_x_topo1), abs(mk_x_base1))

    if mk_y_base1 == mk_y_topo1:
        mk_y_base = abs(mk_y_base1)
        mk_y_topo = abs(mk_y_topo1)

    else:
        mk_y_topo = max(abs(mk_y_topo1), abs(mk_y_base1))
        mk_y_base = - min(abs(mk_y_topo1), abs(mk_y_base1))

    # Classificação
    if mk_x_topo == mk_y_topo == 0:
        tipo = 'Interno'
    elif mk_y_topo != 0 and mk_x_topo != 0:
        tipo = 'Canto'
    else:
        tipo = 'Extremidade'

    # Esforço normal de cálculo
    if min(base, altura) >= 19:
        gama_n = 1
    else:
        gama_n = 1.95 - 0.05*min(base, altura)

    gama_f = 1.4
    nd = nk * gama_n * gama_f

    # Valores de cálculo (conversão dos valores característicos)
    mk_y_topo *= gama_f * gama_n
    mk_y_base *= gama_f * gama_n
    mk_x_topo *= gama_f * gama_n
    mk_x_base *= gama_f * gama_n

    # Excentricidades iniciais
    e1x = mk_x_topo / nd
    e1y = mk_y_topo / nd

    # Comprimentos de flambagem
    lex = min(PDE, PDE - h_viga_x + base)
    ley = min(PDE, PDE - h_viga_y + altura)

    # Esbeltez
    lx = sqrt(12)*lex/base
    ly = sqrt(12)*ley/altura

    # Momentos mínimos mínimos
    m1dx_min = (1.5 + 0.03*base)*nd
    m1dy_min = (1.5 + 0.03*altura)*nd

    # Esbeltez limite
    if m1dx_min > mk_x_topo:
        alfa_bx = 1.0
    else:
        alfa_bx = 0.6 + 0.4 * mk_x_base / mk_x_topo
        alfa_bx = max(min(1.0, alfa_bx), 0.4)

    if m1dy_min > mk_y_topo:
        alfa_by = 1.0
    else:
        alfa_by = 0.6 + 0.4 * mk_y_base / mk_y_topo
        alfa_by = max(min(1.0, alfa_by), 0.4)

    l1x = max((25 + 12.5*e1x/base) / alfa_bx, 35)
    l1y = max((25 + 12.5*e1y/altura) / alfa_by, 35)
    # print(f'a,bx = {alfa_bx:.2f} - a,by = {alfa_by:.2f}')

    # Efeitos de 2a ordem (eixo x)
    m1dc_x = max(0.6 * mk_x_topo + 0.4 * mk_x_base, 0.4 * mk_x_topo,
                 m1dx_min)

    if l1x >= lx:
        efeitos_2ordem_x = 'Desprezados'
        mdx_total = 0

    else:
        efeitos_2ordem_x = 'Devem ser considerados'

        v = nd / (base * altura * fck / gama_f)
        mdx_total = min(0.005 / (base * (v + 0.5)), 0.005 / base) * lex ** 2 / 10 * nd + alfa_bx * m1dc_x

    # Efeitos de 2a ordem (eixo y)
    m1dc_y = max(0.6 * mk_y_topo + 0.4 * mk_y_base, 0.4 * mk_y_topo,
                 m1dy_min)

    if l1y >= ly:
        efeitos_2ordem_y = 'Desprezados'
        mdy_total = 0

    else:
        efeitos_2ordem_y = 'Devem ser considerados'

        v = nd / (base * altura * fck / gama_f)
        mdy_total = min(0.005 / (altura * (v + 0.5)), 0.005 / altura) * ley ** 2 / 10 * nd + alfa_by * m1dc_y

    # Esforços finais e análise
    if tipo != 'Canto':

        mdx = round(max(mdx_total, mk_x_topo, m1dx_min), 2)
        mdy = round(max(mdy_total, mk_y_topo, m1dy_min), 2)

        # Análise
        situacoes_de_calculo = [[mdx, 0], [0, mdy]]

    else:

        md_topo = [round(max(mk_x_topo, m1dx_min), 2), round(max(mk_y_topo, m1dy_min), 2)]
        md_base = [round(max(mk_x_base, m1dx_min), 2), round(max(mk_y_base, m1dy_min), 2)]
        mdc_2ordem_x = [round(max(m1dc_x, mdx_total), 2), round(m1dc_y, 2)]
        mdc_2ordem_y = [round(m1dc_x, 2), round(max(m1dc_y, mdy_total), 2)]

        # Análise
        b = ['', '', '', '']
        situacoes_de_calculo = []
        canto = [md_topo, md_base, mdc_2ordem_x, mdc_2ordem_y]

        for i in range(4):

            for k in range(4):

                if i != k:
                    if (canto[i][0] <= canto[k][0] and canto[i][1] < canto[k][1]) \
                            or (canto[i][0] < canto[k][0] and canto[i][1] <= canto[k][1]):
                        b[i] += 'n'
                    elif canto[i][0] == canto[k][0] and canto[i][1] == canto[k][1]:
                        b[i] += 'r'

        for i in range(4):
            if ('n' not in b[i]) and ('r' not in b[i]):
                situacoes_de_calculo.append(canto[i])

            cont = 0

            if 'r' in b[i] and 'n' not in b[i]:
                for k in range(len(situacoes_de_calculo)):
                    if canto[i] != situacoes_de_calculo[k]:
                        cont += 1
                if cont == len(situacoes_de_calculo):
                    situacoes_de_calculo.append(canto[i])

        # print('\n10 - Situações de cálculo: ')
        # for i in range(len(situacoes_de_calculo)):
        #     print(f'• x = {situacoes_de_calculo[i][0]:.2f} kNcm - y = {situacoes_de_calculo[i][1]:.2f} kNcm ')

    situacoes_de_calculo = asarray(situacoes_de_calculo)
    tabela_situacoes_de_calculo = pd.DataFrame(situacoes_de_calculo, columns=["Mdx (kNcm)", "Mdy (kNcm)"])

    if relatorio:
        print(f'\n\033[1;34m{"2.4 Esforços de cálculo":}\033[m')
        print(f'1 - Classificação do pilar: {tipo};')
        print(f'2 - Esforços de cálculo:\n'
              f'  • Msk,x-topo = {mk_x_topo:.2f} kNcm - Msk,x-base = {mk_x_base:.2f} kNcm;\n'
              f'  • Msk,y-topo = {mk_y_topo:.2f} kNcm - Msk,y-base = {mk_y_base:.2f} kNcm;')
        print(f'3 - Esforço normal de cálculo: {nd:.2f} kN;')
        print(f'4 - Excentricidades de projeto (características): \n'
              f'  • e1x = {e1x:.2f} cm - e1y = {e1y:.2f} cm;')
        print(f'5 - Comprimentos de flambagem: lex = {lex:.2f} cm - ley = {ley:.2f} cm;')
        print(f'6 - Esbeltez: λx = {lx:.2f} - λy = {ly:.2f};')
        print(f'7 - Momentos mínimos: {m1dx_min:.2f} kNcm - {m1dy_min:.2f} kNcm;')
        print(f'8 - Esbeltez limite: λ1x = {l1x:.2f} - λ1y = {l1y:.2f};')

        if efeitos_2ordem_x == 'Devem ser considerados':
            print(f'8 - Efeitos de segunda ordem no eixo x: {efeitos_2ordem_x} - Mdx,tot = {mdx_total:.2f}  kNcm;')
        else:
            print(f'8 - Efeitos de segunda ordem no eixo x: {efeitos_2ordem_x};')

        if efeitos_2ordem_y == 'Devem ser considerados':
            print(f'9 - Efeitos de segunda ordem no eixo y: {efeitos_2ordem_y} - Mdy,tot = {mdy_total:.2f}  kNcm;')
        else:
            print(f'9 - Efeitos de segunda ordem no eixo y: {efeitos_2ordem_y};')

        print(f'\n10 - Tabela com situações de cálculo:\n')
        print(tabela_situacoes_de_calculo)

    return tabela_situacoes_de_calculo


if __name__ == '__main__':

    SC = esforcos_de_calculo(14, 70, 300, 20, 20, 3, 857.14, 0, 0, 0, 0, relatorio=True)
    # base [cm], altura [cm], PDE [cm], h_viga_x [cm], h_viga_y [cm], fck [kN/cm²],
    # nk [kN], mk_y_topo1 [kNcm], mk_y_base1 [kNcm], mk_x_topo1 [kNcm], mk_x_base1 [kNcm]
