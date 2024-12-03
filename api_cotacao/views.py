from django.shortcuts import render, redirect
from api_cotacao.forms import ApiCotacaoForms
from back_end.save_currency_to_sqlite import PipelineRequestToSqlite
from .models import CotacaoHistorico

def cotacao(request):
    # Controle para decidir se os campos adicionais devem ser exibidos
    mostrar_campos = bool(request.GET.get('mostrar_campos'))  # Pode vir como parâmetro de URL

    # Passe a flag 'mostrar_campos' ao formulário
    form = ApiCotacaoForms(request.POST or None, mostrar_campos=mostrar_campos)

    if request.method == 'POST' and form.is_valid():
        # Obtém os valores limpos usando cleaned_data
        converter = form.cleaned_data["converter"]
        converter_para = form.cleaned_data["converter_para"]

        # Processa a pipeline para salvar no SQLite
        pipeline = PipelineRequestToSqlite(converter, converter_para)
        pipeline.save_to_sqlite()

        # Obtém o último registro do modelo CotacaoHistorico
        ultima_cotacao = CotacaoHistorico.objects.latest('id')  # Obtém o último registro pelo campo ID

        # Redireciona para a página específica com o ID
        return redirect(f'/cotacao/{ultima_cotacao.code}{ultima_cotacao.codein}/')

    return render(request, 'api_cotacao/cotacao.html', {"form": form})


def cotacao_detalhe(request, code_codein):
    # Divide o código para obter code e codein
    code = code_codein[:3]
    codein = code_codein[3:]

    # Obtém o registro mais recente com base em code e codein
    cotacao = CotacaoHistorico.objects.filter(code=code, codein=codein).order_by('-create_date').first()

    if not cotacao:
        return render(request, '404.html', {"message": "Cotação não encontrada"})
    # Inicializa o formulário com os valores de ask e bid
    form = ApiCotacaoForms(
        initial={
            'valor_venda': cotacao.ask,
            'valor_compra': cotacao.bid,
        },
        mostrar_campos=True,  # Força mostrar os campos
    )

    if request.method == 'POST' and form.is_valid():
        # Obtém os valores limpos do formulário
        converter = form.cleaned_data["converter"]
        converter_para = form.cleaned_data["converter_para"]

        # Processa a pipeline para atualizar os dados
        pipeline = PipelineRequestToSqlite(converter, converter_para)
        pipeline.save_to_sqlite()

        # Após atualizar, redireciona para a mesma página com os novos dados
        return redirect(f'/cotacao/{code_codein}/')


    return render(request, 'api_cotacao/cotacao_detalhe.html', {"form": form, "cotacao": cotacao})