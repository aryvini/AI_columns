from numpy import zeros


def numero_ganchos(base, altura, nx, ny, c, fi_t, fi_l):
    n_barras = 2 * (nx + ny) - 4
    posicoes = zeros([n_barras, 4])  # x - y - dy - dx

    d_linha = c + (fi_t + fi_l / 2) / 10
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

    protecao_flam = {'x-n': -base / 2 + c + (fi_t / 10) * 20,
                     'x-p': base / 2 - c - (fi_t / 10) * 20,
                     'y-n': -altura / 2 + c + (fi_t / 10) * 20,
                     'y-p': altura / 2 - c - (fi_t / 10) * 20}

    ng_x = ng_y = 0

    for i in range(0, n_barras):

        if posicoes[i, 1] == altura / 2 - d_linha:
            if protecao_flam['x-n'] < posicoes[i, 0] < protecao_flam['x-p']:
                ng_y += 1

        if posicoes[i, 0] == base/2 - d_linha:
            if protecao_flam['y-n'] < posicoes[i, 1] < protecao_flam['y-p']:
                ng_x += 1

    return ng_x, ng_y
