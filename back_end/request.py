import requests

class ApiRequest:
    def request(entry_currency: str, to_currency: str):
        url = f'https://economia.awesomeapi.com.br/last/{entry_currency}-{to_currency}'

        response = requests.get(url)

        # Verifica se a requisição foi bem-sucedida
        if response.status_code == 200:
            print(response.json())
            return response.json()
        else:
            print(f"Erro na requisição: {response.status_code}")
            return None
        
if __name__ == "__main__":
    ApiRequest.request('USD', 'BRL')