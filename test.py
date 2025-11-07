from zeep import Client
from zeep import xsd
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


USUARIO = 'user.guesshrg.service'
SENHA = '8LwDlczLOHgA'

def main():
 
    wsdl_url = 'https://www.folhasinergyrh.com.br/Sinergy.WebServices.Dados/DadosFuncionarios.asmx?WSDL'


    client = Client(wsdl=wsdl_url)

  
    auth_header_type = xsd.Element(
        '{http://tempuri.org/}AuthSoapHd',
        xsd.ComplexType([
            xsd.Element('{http://tempuri.org/}Usuario', xsd.String()),
            xsd.Element('{http://tempuri.org/}Senha', xsd.String()),
        ])
    )
    auth_header_value = auth_header_type(Usuario=USUARIO, Senha=SENHA)

   
    client.set_default_soapheaders([auth_header_value])
    REFERENCIA = "102025"
    CPF_TESTE = "438.809.518-45" 

    resultado = client.service.GetDadosFuncionariosFichaFinanceira(CPF_TESTE, REFERENCIA)


 
    print(resultado)

if __name__ == "__main__":
    main()
