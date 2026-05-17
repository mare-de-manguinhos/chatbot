from app.models.campo_esperado import CampoEsperado
from app.schemas.execucao import DiferencaCampo, ResultadoComparacao


def _normalizar(valor: str) -> str:
    return valor.strip().lower()


def _valores_iguais(esperado: str, obtido: str) -> bool:
    return _normalizar(esperado) == _normalizar(obtido)


def comparar(campos_esperados: list[CampoEsperado], json_obtido: dict) -> ResultadoComparacao:
    falhas: list[DiferencaCampo] = []

    for campo in campos_esperados:
        valor_obtido = json_obtido.get(campo.chave)
        passou = valor_obtido is not None and _valores_iguais(campo.valor, str(valor_obtido))

        if not passou:
            falhas.append(DiferencaCampo(
                chave=campo.chave,
                esperado=campo.valor,
                obtido=str(valor_obtido) if valor_obtido is not None else None,
                passou=False,
            ))

    return ResultadoComparacao(
        passou=len(falhas) == 0,
        total_verificado=len(campos_esperados),
        falhas=falhas,
    )
