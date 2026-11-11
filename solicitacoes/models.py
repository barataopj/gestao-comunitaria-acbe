from django.conf import settings
from django.db import models
from django.utils import timezone


class Solicitacao(models.Model):
    class Categoria(models.TextChoices):
        INFRAESTRUTURA = "infraestrutura", "Infraestrutura"
        LIMPEZA = "limpeza", "Limpeza"
        SEGURANCA = "seguranca", "Segurança"
        EVENTOS = "eventos", "Eventos"
        OUTROS = "outros", "Outros"

    class Status(models.TextChoices):
        RECEBIDA = "recebida", "Recebida"
        EM_ANALISE = "em_analise", "Em análise"
        ENCAMINHADA = "encaminhada", "Encaminhada"
        CONCLUIDA = "concluida", "Concluída"

    descricao = models.CharField("descrição", max_length=500)
    categoria = models.CharField("categoria", max_length=20, choices=Categoria.choices)
    status = models.CharField("status", max_length=20, choices=Status.choices, default=Status.RECEBIDA)
    criada_em = models.DateTimeField("data de registro", default=timezone.now, editable=False)
    criada_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="solicitacoes_criadas")

    class Meta:
        ordering = ["-criada_em"]
        verbose_name = "solicitação"
        verbose_name_plural = "solicitações"

    def __str__(self):
        return f"SOL-{self.pk:05d} - {self.get_categoria_display()}"

    @property
    def protocolo(self):
        return f"SOL-{self.pk:05d}" if self.pk else "Novo"


class HistoricoStatus(models.Model):
    solicitacao = models.ForeignKey(Solicitacao, on_delete=models.CASCADE, related_name="historico")
    status = models.CharField("status", max_length=20, choices=Solicitacao.Status.choices)
    alterado_em = models.DateTimeField("data da alteração", default=timezone.now, editable=False)
    alterado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    class Meta:
        ordering = ["alterado_em", "pk"]
        verbose_name = "movimentação"
        verbose_name_plural = "histórico de movimentações"

    def __str__(self):
        return f"{self.solicitacao.protocolo}: {self.get_status_display()}"
