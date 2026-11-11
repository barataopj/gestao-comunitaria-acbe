from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AtualizarStatusForm, SolicitacaoForm
from .models import HistoricoStatus, Solicitacao


@login_required
def listar(request):
    itens = Solicitacao.objects.select_related("criada_por").all()
    status = request.GET.get("status", "")
    categoria = request.GET.get("categoria", "")
    if status in Solicitacao.Status.values:
        itens = itens.filter(status=status)
    if categoria in Solicitacao.Categoria.values:
        itens = itens.filter(categoria=categoria)
    return render(request, "solicitacoes/lista.html", {
        "solicitacoes": itens,
        "status_selecionado": status,
        "categoria_selecionada": categoria,
        "status_choices": Solicitacao.Status.choices,
        "categoria_choices": Solicitacao.Categoria.choices,
    })


@login_required
def criar(request):
    if request.method == "POST":
        form = SolicitacaoForm(request.POST)
        if form.is_valid():
            solicitacao = form.save(commit=False)
            solicitacao.criada_por = request.user
            with transaction.atomic():
                solicitacao.save()
                HistoricoStatus.objects.create(
                    solicitacao=solicitacao,
                    status=solicitacao.status,
                    alterado_por=request.user,
                )
            messages.success(request, f"Solicitação {solicitacao.protocolo} cadastrada.")
            return redirect("solicitacoes:listar")
    else:
        form = SolicitacaoForm()
    return render(request, "solicitacoes/formulario.html", {"form": form})


@login_required
def atualizar_status(request, pk):
    solicitacao = get_object_or_404(Solicitacao, pk=pk)
    if request.method == "POST":
        form = AtualizarStatusForm(request.POST, instance=solicitacao)
        if form.is_valid():
            novo_status = form.cleaned_data["status"]
            if novo_status != solicitacao.status:
                with transaction.atomic():
                    solicitacao.status = novo_status
                    solicitacao.save(update_fields=["status"])
                    HistoricoStatus.objects.create(
                        solicitacao=solicitacao,
                        status=novo_status,
                        alterado_por=request.user,
                    )
                messages.success(request, "Status atualizado com sucesso.")
            return redirect("solicitacoes:listar")
    else:
        form = AtualizarStatusForm(instance=solicitacao)
    return render(request, "solicitacoes/status.html", {"form": form, "solicitacao": solicitacao})
