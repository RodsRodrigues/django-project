import os
import django
import datetime as dt
from request import ApiRequest

# Passar import do django após o setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup_django.settings')
django.setup()
from api_cotacao.models import CotacaoHistorico
from django.utils.timezone import make_aware


class PipelineRequestToSqlite:
    def __init__(self, code: str, codein: str):
        self.code = code
        self.codein = codein

    def save_to_sqlite(self):
        full_code = self.code + self.codein

        res = ApiRequest.request(entry_currency=self.code, to_currency=self.codein)

        create_date_naive = res[full_code]["create_date"]
        create_date_aware = make_aware(dt.datetime.strptime(create_date_naive, '%Y-%m-%d %H:%M:%S'))

        data = CotacaoHistorico(
            code=res[full_code]["code"],
            codein=res[full_code]["codein"],
            name=res[full_code]["name"],
            high=res[full_code]["high"],
            low=res[full_code]["low"],
            varBid=res[full_code]["varBid"],
            pctChange=res[full_code]["pctChange"],
            bid=res[full_code]["bid"],
            ask=res[full_code]["ask"],
            create_date=create_date_aware,
        )

        data.save()

        return CotacaoHistorico.objects.all()

if __name__ == "__main__":
    pipeline = PipelineRequestToSqlite('USD', 'BRL')
    resultados = pipeline.save_to_sqlite()
