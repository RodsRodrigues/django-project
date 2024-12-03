from django import forms

class ApiCotacaoForms(forms.Form):
    choices = (("", "Selecione a moeda"), ("USD", "USD"), ("EUR", "EUR"), ("BRL", "BRL"))
    converter = forms.ChoiceField(
        label="Converter de",
        required=True,
        choices=choices,
        widget=forms.Select(
            attrs={
                "class": "form_control"
            }
        )
    )

    converter_para= forms.ChoiceField(
        label="Converter Para",
        required=True,
        choices=choices,
        widget=forms.Select(
            attrs={
                "class": "form_control"
            }
        )
    )

    valor_venda= forms.CharField(
        label="Valor de Venda",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form_control"
            }
        )        
    )
    
    valor_compra= forms.CharField(
        label="Valor de Compra",
        required=False,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form_control"
            }
        )        
    )

    def __init__(self, *args, **kwargs):
        # Pass optional visibility control
        mostrar_campos = kwargs.pop('mostrar_campos', False)
        super().__init__(*args, **kwargs)

        if not mostrar_campos:
            self.fields['valor_venda'].widget.attrs['hidden'] = 'hidden'
            self.fields['valor_compra'].widget.attrs['hidden'] = 'hidden'