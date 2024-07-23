from append import append
from append_excel import append_excel_data

import var
from add_data import add_data


if __name__ == "__main__":
    #### Caso precise recriar a tabela bruta#####
    # append(var.PATH_VW_ARCGIS, var.PATH_DADOS_BRUTOS)
    # append_excel_data(var.PATH_VW_ARCGIS, var.PATH_DADOS_BRUTOS)
    #### Caso precise recriar a tabela bruta#####

    add_data(var.PATH_VW_ARCGIS, var.PATH_DADOS_BRUTOS)
