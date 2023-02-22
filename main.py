import subprocess
from concurrent.futures import ThreadPoolExecutor
import PySimpleGUI as sg


def ping(i):
    result = subprocess.run(['ping', '-w', '2', i], capture_output=True)
    return result.returncode == 0


def main():
    # Coloque a lista de IP's abaixo:
    stations = ['IP1', 'IP2', 'IP3']

    with ThreadPoolExecutor(max_workers=len(stations)) as executor:
        futures = [executor.submit(ping, i) for i in stations]

    result = [[i, f.result()] for i, f in zip(stations, futures)]

    print([l for l in result if l[1] == False])
    # Cria a janela e a tabela
    layout = [
        [sg.Table(values=result, headings=["Station", "Status"], background_color="black", key="-TABLE-",
                  auto_size_columns=True, num_rows=len(stations))]
    ]
    window = sg.Window("Ping Test", layout)
    '''
    try:
        # Atualiza a cor de fundo da linha da tabela de acordo com o resultado do teste
        for row_num, row in enumerate(result):
            if row[1]:
                for col_num in range(len(row)):
                    cell_widget = window["-TABLE-"].Widget.cell(row_num, col_num)
                    cell_widget.TKCanvas.itemconfig(cell_widget.TKText, bg="green")
            else:
                for col_num in range(len(row)):
                    cell_widget = window["-TABLE-"].Widget.cell(row_num, col_num)
                    cell_widget.TKCanvas.itemconfig(cell_widget.TKText, bg="red")
    except:
        pass
    '''
    # Aguarda o usuário fechar a janela
    event, values = window.read()
    window.close()


if __name__ == '__main__':
    main()
