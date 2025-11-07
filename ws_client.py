from zeep import Client, xsd
from zeep.transports import Transport
import requests
from config import USUARIO, SENHA

WSDL_URL = "https://www.folhasinergyrh.com.br/Sinergy.WebServices.Dados/DadosFuncionarios.asmx?WSDL"

def get_authenticated_client():
    session = requests.Session()
    transport = Transport(session=session)
    client = Client(wsdl=WSDL_URL, transport=transport)

    auth_header_type = xsd.Element(
        '{http://tempuri.org/}AuthSoapHd',
        xsd.ComplexType([
            xsd.Element('{http://tempuri.org/}Usuario', xsd.String()),
            xsd.Element('{http://tempuri.org/}Senha', xsd.String()),
        ])
    )
    auth_header = auth_header_type(Usuario=USUARIO, Senha=SENHA)
    client.set_default_soapheaders([auth_header])

    return client
