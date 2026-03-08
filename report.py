from database import buscar_eventos_hoje
from datetime import date

def gerar_relatorio_html():
    eventos = buscar_eventos_hoje()
    hoje = date.today().strftime("%d/%m/%Y")

    linhas = ""
    for e in eventos:
        funcionario, inicio, fim, duracao, ear = e
        linhas += f"""
        <tr>
            <td>{funcionario}</td>
            <td>{inicio.strftime('%H:%M:%S')}</td>
            <td>{fim.strftime('%H:%M:%S')}</td>
            <td>{duracao:.1f}s</td>
            <td>{ear:.3f}</td>
        </tr>"""

    html = f"""
    <html><body>
    <h2>Relatório de Sonolência — {hoje}</h2>
    <p>Total de eventos: <strong>{len(eventos)}</strong></p>
    <table border="1" cellpadding="5">
        <tr>
            <th>Funcionário</th><th>Início</th><th>Fim</th>
            <th>Duração</th><th>EAR Médio</th>
        </tr>
        {linhas}
    </table>
    </body></html>
    """
    with open("relatorio.html", "w", encoding="utf-8") as f:
        f.write(html)
    return "relatorio.html"