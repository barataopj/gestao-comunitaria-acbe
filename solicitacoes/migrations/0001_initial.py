from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="Solicitacao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("descricao", models.CharField(max_length=500, verbose_name="descrição")),
                ("categoria", models.CharField(choices=[("infraestrutura", "Infraestrutura"), ("limpeza", "Limpeza"), ("seguranca", "Segurança"), ("eventos", "Eventos"), ("outros", "Outros")], max_length=20, verbose_name="categoria")),
                ("status", models.CharField(choices=[("recebida", "Recebida"), ("em_analise", "Em análise"), ("encaminhada", "Encaminhada"), ("concluida", "Concluída")], default="recebida", max_length=20, verbose_name="status")),
                ("criada_em", models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name="data de registro")),
                ("criada_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="solicitacoes_criadas", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "solicitação", "verbose_name_plural": "solicitações", "ordering": ["-criada_em"]},
        ),
        migrations.CreateModel(
            name="HistoricoStatus",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("recebida", "Recebida"), ("em_analise", "Em análise"), ("encaminhada", "Encaminhada"), ("concluida", "Concluída")], max_length=20, verbose_name="status")),
                ("alterado_em", models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name="data da alteração")),
                ("alterado_por", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ("solicitacao", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="historico", to="solicitacoes.solicitacao")),
            ],
            options={"verbose_name": "movimentação", "verbose_name_plural": "histórico de movimentações", "ordering": ["alterado_em", "pk"]},
        ),
    ]
