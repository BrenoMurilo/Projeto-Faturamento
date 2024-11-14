from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException


class DriveSelenium:

    def __init__(self,stealth):
        chrome_options = Options()
        if stealth:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-notifications")  # Desabilitar notificações
            chrome_options.add_argument("--disable-extensions")  # Desabilitar extensões
            chrome_options.add_argument("--disable-infobars")  # Desabilitar infobars
            chrome_options.add_argument("--disable-gpu")  # Desabilitar aceleração de GPU
            chrome_options.add_argument("--disable-web-security")  # Desabilitar segurança web
            chrome_options.add_argument("--disable-features=EnableEphemeralFlashPermission")  # Desabilitar flash
            chrome_options.add_argument("--disable-features=site-per-process")  # Desabilitar site-per-process
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")  # Desabilitar VizDisplayCompositor
            chrome_options.add_argument("--disable-features=NetworkService")  # Desabilitar NetworkService
            chrome_options.add_argument("--disable-features=CrossSiteDocumentBlockingIfIsolating")  # Desabilitar CrossSiteDocumentBlockingIfIsolating
            chrome_options.add_argument("--disable-features=CrossSiteDocumentBlockingAlways")  # Desabilitar CrossSiteDocumentBlockingAlways
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Desabilitar controle de automação
            chrome_options.add_argument("--disable-blink-features=BlockCredentialedSubresources")  # Desabilitar subrecursos credenciados
                
        self.navegador = webdriver.Chrome(options=chrome_options)

    def RolarPaginaAteLimite(self,limite_rolagens):
        r=0
        rr=0
        altura_anterior = 0
        while True:
            try:
                altura_atual =  self.navegador.execute_script("return document.documentElement.scrollHeight")
                if altura_atual == altura_anterior  or rr == r and rr>0:
                    break
                self.navegador.execute_script('window.scrollTo(0,' + str(altura_atual) +')')
                r=r+1
                #print('Rolando página' + '('+ str(r) + ').....')
                if r == rr+limite_rolagens:
                    rr=r
                    time.sleep(2.5)
                    altura_anterior=altura_atual 
            except:
                print('ocorreu algum problema na hora de rolar a página. Vamos tentar novamente.')  
                time.sleep(20)
        if altura_atual == altura_anterior: 
            return True 
        else: 
            return False
        
    def coletarElementos(self, ID):
        localizadores = [
            (By.XPATH, ID),
            (By.CSS_SELECTOR, ID),
            (By.CLASS_NAME, ID),
            (By.ID, ID)
        ]
        dados = None
        for by, value in localizadores:
            try:
                dados = self.navegador.find_elements(by, value)
                if dados:
                    break
            except:
                pass
        if dados:
            return dados
        else:
            print(f"Elemento não encontrado usando = {value}")
        return []
    
    def coletarElemento(self, ID):
        localizadores = [
            (By.XPATH, ID),
            (By.CSS_SELECTOR, ID),
            (By.CLASS_NAME, ID),
            (By.ID, ID)
        ]
        dados = None
        for by, value in localizadores:
            try:
                dados = self.navegador.find_element(by, value)
                if dados:
                    break
            except:
                pass
        if dados:
            return dados
        else:
            print(f"Elemento não encontrado usando = {value}")
        return []
    
    def ListarDadosElemento(self, elements):
        dados={}
        for nome_element, id_element, coletar, atributo in elements:
            dados_element= self.coletarElementos(id_element)
            if coletar:
                for element in dados_element:
                    if not atributo or not element.get_attribute(atributo):
                        texto = element.text
                    else:
                        texto = element.get_attribute(atributo)
                    if nome_element in dados:
                        dados[nome_element].append(texto)
                    else:
                        dados[nome_element] = [texto]
        return dados
    
    def ContarDadosElemento(self,elements):
        for nome_element, id_element, coletar in elements:
            quantidade_dados= len(self.coletarElementos(id_element))
            break
        return quantidade_dados
    
    def excluirElementos(self, elements):
        for nome_element, id_element, coletar in elements:
            dados_element = self.coletarElementos(id_element)
            for element in dados_element:
                try:
                    self.navegador.execute_script("arguments[0].remove()", element)
                except:
                    #pass
                    print('Não foi possível excluir o elemento')
                             
    
    def CapturarDadosSite(self, url,elements):
        self.navegador.get(url)
        fim = False
        dados={}
        while not fim:
            fim = self.RolarPaginaAteLimite(10)
            if not fim or dados == {}:
                try:
                    novos_dados = self.ListarDadosElemento(elements)
                    for nome_element, dados_element in novos_dados.items():
                        if nome_element in dados:
                            dados[nome_element].extend(dados_element)
                        else:
                            dados[nome_element] = dados_element
                    self.excluirElementos(elements)
                except:
                    fim = True
        return dados
    
    def EsperarElementoColetar(self, id_element, timeout, rolar):
        start_time = time.time()
        elemento= None
        while not elemento:
            elemento = self.coletarElemento(id_element)
            if elemento:
                return elemento
            if time.time() - start_time > timeout:
                print(f"Tempo limite atingido ao esperar o elemento: {id_element}")
                return None
                break
            if rolar:
                self.RolarPaginaAteLimite(1)
            time.sleep(1)
        return elemento
    
    def EsperarElementoClicar(self, id_element, timeout, rolar):
        start_time = time.time()
        elemento= None
        while not elemento:
            elemento = self.coletarElemento(id_element)
            if elemento:
                elemento.click()
                break
            if time.time() - start_time > timeout:
                print(f"Tempo limite atingido ao esperar o elemento: {id_element}")
                break
            if rolar:
                self.RolarPaginaAteLimite(1)
            time.sleep(1)

        


    




            





        
    
