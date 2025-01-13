import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def calculadora(consumo: list, classe: str, bandeira: str) -> tuple:
    """
    retorna uma tupla de floats contendo economia anual, economia mensal, desconto aplicado e cobertura.
    """
    economia_anual = 0
    economia_mensal = 0
    desconto_aplicado = 0
    cobertura = 0

    # Desenvolva seu código aqui #
    tarifa = 0

    service = Service()
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://www.cemig.com.br/atendimento/valores-de-tarifas-e-servicos/")
    
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()

   #tarifas = driver.find_element(By.CLASS_NAME, "table").parent.find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")[0].find_elements(By.TAG_NAME, "td")

    tabelas = driver.find_elements(By.TAG_NAME, "table")
    linhas = str()
    if classe == "Residencial":
        linhas = tabelas[0].find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    else:
        linhas = tabelas[6].find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
    colunas = linhas[0].find_elements(By.TAG_NAME, "td")


    tarifas = [coluna.text for coluna in colunas]
    tarifas.pop(0)

    tarifas = [float(tarifa.replace(",", ".")) for tarifa in tarifas]

    if bandeira == "BANDEIRA VERDE":
        tarifa = tarifas[0]
    elif bandeira == "BANDEIRA AMARELA":
        tarifa = tarifas[1]
    elif bandeira == "BANDEIRA VERMELHA 1":
        tarifa = tarifas[2]
    else:
        tarifa = tarifas[3]
    
    driver.quit()
    
    media_consumo = sum(consumo) / len(consumo)
    
    tabela = [[10000, 0.18, 0.16, 0.12],
             [20000,0.22, 0.18, 0.15],
             [20000, 0.25,0.22,0.18]]
    
    classificar = {"Residencial": 1,"Comercial": 2, "Industrial": 3}

    if media_consumo < 10000:
        cobertura = 0.9
        desconto_aplicado = tabela[0][classificar[classe]]
    elif media_consumo >= 10000 and media_consumo <=20000:
        cobertura = 0.95
        desconto_aplicado = tabela[1][classificar[classe]]
    else:
        cobertura = 0.99
        desconto_aplicado = tabela[2][classificar[classe]]    
    
    economia_mensal = media_consumo*tarifa* desconto_aplicado*cobertura
    economia_anual = economia_mensal * 12
    
    print(round(economia_anual, 2),
        round(economia_mensal, 2),
        round(desconto_aplicado, 2),
        round(cobertura, 2),
        tarifa,
    )

    return (
        round(economia_anual, 2),
        round(economia_mensal, 2),
        round(desconto_aplicado, 2),
        round(cobertura, 2),
    )


if __name__ == "__main__":
    print("Testando...")

    assert calculadora([1518, 1071, 968], "Industrial", "BANDEIRA VERMELHA 2") == (
        1349.86,
        112.49,
        0.12,
        0.90,
    ) 

    assert calculadora([1000, 1054, 1100], "Residencial", "BANDEIRA VERMELHA 1") == (
        1725.61,
        143.8,
        0.18,
        0.90
    )

    assert calculadora([973, 629, 726], "Comercial", "BANDEIRA AMARELA") == (
        1097.6,
        91.47,
        0.16,
        0.90
    )

    assert calculadora([15000, 14000, 16000], "Industrial", "BANDEIRA VERMELHA 1") == (
        21656.81,
        1804.73,
        0.15,
        0.95
    )

    assert calculadora([12000, 11000, 11400], "Residencial", "BANDEIRA VERDE") == (
        22997.8,
        1916.48,
        0.22,
        0.95
    )

    assert calculadora([17500, 16000, 16400], "Comercial", "BANDEIRA AMARELA") == (
        27938.08,
        2328.17,
        0.18,
        0.95
    )

    assert calculadora([30000, 29000, 29500], "Industrial", "BANDEIRA VERMELHA 1") == (
        53262.07,
        4438.51,
        0.18,
        0.99
    )

    assert calculadora([22000, 21000, 21400], "Residencial", "BANDEIRA AMARELA") == (
        52186.84,
        4348.9,
        0.25,
        0.99
    )

    assert calculadora([25500, 23000, 21400], "Comercial", "BANDEIRA VERDE") == (
        48697.35,
        4058.11,
        0.22,
        0.99
    )

    print("Todos os testes passaram!")
    