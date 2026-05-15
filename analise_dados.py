import openpyxl as opx
import pandas as pd
from database import buscar_csv_sonolencia


def gerando_relatorio_excel():
    buscar_csv_sonolencia()

    csv_sonolencia = pd.read_csv('dados_sonolencia.csv',encoding='UTF-8',sep=',')
    dtf=pd.DataFrame(csv_sonolencia)

    with pd.ExcelWriter("relatorio_sonolencia.xlsx", engine='openpyxl',mode='w') as writer:
        dtf.to_excel(writer, index=False)

    