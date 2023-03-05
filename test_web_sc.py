from bs4 import BeautifulSoup
from web_sc_functions import extraer_atributos_casa, \
    obtener_bloques_informacion
from unittest import mock


@mock.patch('web_sc_functions.descargar_pagina')
def test_descargar_pagina(mock_descargar_pagina):
    url = "https://www.google.com"
    page = mock_descargar_pagina(url)
    mock_descargar_pagina.assert_called_once_with(url)
    assert page is not None


def test_obtener_bloques_informacion():
    html = """
    <html>
        <body>
            <div class="MuiCardContent-root">Bloque 1</div>
            <div class="MuiCardContent-root">Bloque 2</div>
            <div class="OtroClase-root">No es un bloque</div>
        </body>
    </html>
    """
    page = BeautifulSoup(html, "html.parser")

    # Obtenemos los bloques de información
    bloques = obtener_bloques_informacion(page)

    # Verificamos que se hayan obtenido los bloques correctos
    assert len(bloques) == 2
    assert bloques[0].text.strip() == "Bloque 1"
    assert bloques[1].text.strip() == "Bloque 2"


def test_extraer_atributos_casa():
    bloques = [
        BeautifulSoup(
            '<div class="MuiCardContent-root"><span>4 Habitaciones</span>\
                <span>3 Baños</span></div>', "html.parser"),
        BeautifulSoup(
            '<div class="MuiCardContent-root"><span>3 Habitaciones</span>\
                <span>2 Baños</span></div>', "html.parser"),
        BeautifulSoup(
            '<div class="MuiCardContent-root"><span>2 Habitaciones</span>\
                <span>1 Baño</span></div>', "html.parser")
    ]
    casas = extraer_atributos_casa(bloques)
    assert len(casas) == 3
    assert casas[0] == ['4 Habitaciones', '3 Baños']
    assert casas[1] == ['3 Habitaciones', '2 Baños']
    assert casas[2] == ['2 Habitaciones', '1 Baño']
