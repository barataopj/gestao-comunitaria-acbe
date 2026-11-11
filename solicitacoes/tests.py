from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .forms import SolicitacaoForm
from .models import HistoricoStatus, Solicitacao

User = get_user_model()


class SolicitacaoModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="operador", password="Senha-forte-123")

    def test_protocolo_e_status_inicial(self):
        item = Solicitacao.objects.create(
            descricao="Lâmpada queimada na praça do bairro",
            categoria=Solicitacao.Categoria.INFRAESTRUTURA,
            criada_por=self.user,
        )
        self.assertEqual(item.protocolo, f"SOL-{item.pk:05d}")
        self.assertEqual(item.status, Solicitacao.Status.RECEBIDA)

    def test_formulario_rejeita_descricao_curta(self):
        form = SolicitacaoForm(data={"descricao": "Curta", "categoria": "limpeza"})
        self.assertFalse(form.is_valid())
        self.assertIn("descricao", form.errors)


class SolicitacaoIntegrationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="operador", password="Senha-forte-123")

    def test_usuario_nao_autenticado_e_redirecionado(self):
        response = self.client.get(reverse("solicitacoes:listar"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_fluxo_cadastro_consulta_e_alteracao_de_status(self):
        self.client.login(username="operador", password="Senha-forte-123")
        response = self.client.post(reverse("solicitacoes:criar"), {
            "descricao": "Lâmpada queimada na praça do bairro",
            "categoria": "infraestrutura",
        })
        self.assertEqual(response.status_code, 302)
        item = Solicitacao.objects.get()
        self.assertEqual(item.criada_por, self.user)
        self.assertEqual(item.status, Solicitacao.Status.RECEBIDA)
        self.assertEqual(item.historico.count(), 1)

        response = self.client.get(reverse("solicitacoes:listar"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item.protocolo)
        self.assertContains(response, "Lâmpada queimada na praça do bairro")

        response = self.client.post(reverse("solicitacoes:atualizar_status", args=[item.pk]), {
            "status": Solicitacao.Status.EM_ANALISE,
        })
        self.assertEqual(response.status_code, 302)
        item.refresh_from_db()
        self.assertEqual(item.status, Solicitacao.Status.EM_ANALISE)
        self.assertEqual(item.historico.count(), 2)
        self.assertEqual(item.historico.order_by("-pk").first().status, Solicitacao.Status.EM_ANALISE)

    def test_cadastro_invalido_nao_persiste_registro(self):
        self.client.login(username="operador", password="Senha-forte-123")
        response = self.client.post(reverse("solicitacoes:criar"), {
            "descricao": "Ruim",
            "categoria": "infraestrutura",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Solicitacao.objects.count(), 0)
