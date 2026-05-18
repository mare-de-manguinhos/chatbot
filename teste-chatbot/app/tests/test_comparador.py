import pytest
from app.models.campo_esperado import CampoEsperado
from app.services.comparador import comparar


def _campo(chave: str, valor: str) -> CampoEsperado:
    c = CampoEsperado()
    c.id = "teste"
    c.caso_de_teste_id = "teste"
    c.chave = chave
    c.valor = valor
    return c


class TestComparar:
    def test_todos_campos_corretos_retorna_aprovado(self):
        campos = [_campo("pescador", "João"), _campo("peixe", "corvina")]
        json_obtido = {"pescador": "João", "peixe": "corvina"}
        resultado = comparar(campos, json_obtido)
        assert resultado.passou is True
        assert resultado.total_verificado == 2
        assert len(resultado.falhas) == 0

    def test_campo_errado_retorna_reprovado(self):
        campos = [_campo("peixe", "corvina")]
        json_obtido = {"peixe": "tilapia"}
        resultado = comparar(campos, json_obtido)
        assert resultado.passou is False
        assert len(resultado.falhas) == 1
        assert resultado.falhas[0].chave == "peixe"
        assert resultado.falhas[0].esperado == "corvina"
        assert resultado.falhas[0].obtido == "tilapia"

    def test_campo_ausente_no_json_retorna_reprovado(self):
        campos = [_campo("pescador", "Maria")]
        resultado = comparar(campos, {})
        assert resultado.passou is False
        assert resultado.falhas[0].obtido is None

    def test_comparacao_case_insensitive(self):
        campos = [_campo("peixe", "CORVINA")]
        resultado = comparar(campos, {"peixe": "corvina"})
        assert resultado.passou is True

    def test_comparacao_ignora_espacos_extras(self):
        campos = [_campo("pescador", "  João Silva  ")]
        resultado = comparar(campos, {"pescador": "João Silva"})
        assert resultado.passou is True

    def test_lista_vazia_de_campos_sempre_passa(self):
        resultado = comparar([], {"pescador": "qualquer"})
        assert resultado.passou is True
        assert resultado.total_verificado == 0
