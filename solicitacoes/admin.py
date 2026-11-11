from django.contrib import admin
from .models import HistoricoStatus, Solicitacao


class HistoricoStatusInline(admin.TabularInline):
    model = HistoricoStatus
    extra = 0
    readonly_fields = ("status", "alterado_em", "alterado_por")


@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ("protocolo", "categoria", "status", "criada_em", "criada_por")
    list_filter = ("categoria", "status")
    search_fields = ("descricao",)
    readonly_fields = ("criada_em",)
    inlines = [HistoricoStatusInline]
