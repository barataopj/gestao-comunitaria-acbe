from django import forms
from .models import Solicitacao


class SolicitacaoForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ["descricao", "categoria"]
        widgets = {
            "descricao": forms.Textarea(attrs={"rows": 3, "maxlength": 500}),
            "categoria": forms.Select(),
        }

    def clean_descricao(self):
        descricao = self.cleaned_data["descricao"].strip()
        if len(descricao) < 10:
            raise forms.ValidationError("Informe uma descrição com pelo menos 10 caracteres.")
        return descricao


class AtualizarStatusForm(forms.ModelForm):
    class Meta:
        model = Solicitacao
        fields = ["status"]
