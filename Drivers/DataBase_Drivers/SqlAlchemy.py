from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, Numeric, Date, Time, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from sqlalchemy.inspection import inspect
import logger 

Base = declarative_base()

class SqlAlchemy:

    def __init__(self,connection_string):
        self.engine=create_engine(connection_string,echo=True)
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

    def iniciar_sessao(self):
        if self.session is None:
            self.session = self.Session()

    def Fechar_sessao(self):
        if not self.session is None:
            self.session.close()

    def CriarRecriarTabelas(self):
        Base.metadata.create_all(self.engine)
        self.SalvarAlteracoes()


    def AdicionarRegistro(self, novo_registro):
        self.session.add(novo_registro)
        self.SalvarAlteracoes()

    def AdicionarListaRegistros(self, tabela, lista_registros, salvar_cada_registro=False):
        colunas = [column.key for column in inspect(tabela).columns]
        for dados in lista_registros:
            dados_dict = dict(zip(colunas, dados))
            novo_registro = tabela(**dados_dict)
            try:
                self.session.add(novo_registro)
                if salvar_cada_registro:
                    self.session.commit() 
            except IntegrityError:
                print(f"Erro ao adicionar registro: {dados}. Esse registro pode já existir.")  
            except Exception as e:
                print(f"Erro ao adicionar registro: {dados}. Erro: {str(e)}")
        self.SalvarAlteracoes()


    def ExcluirRegistro(self, tabela,nome_coluna_id, id):
        consulta = self.session.query(tabela).filter(getattr(tabela, nome_coluna_id) == id).first()
        self.session.delete(consulta)
        self.SalvarAlteracoes()

    def ExluirFiltroRegistros(self, tabela, nome_coluna_filtro, filtro):
        consulta = self.session.query(tabela).filter(getattr(tabela, nome_coluna_filtro) == filtro)
        consulta.delete()
        self.SalvarAlteracoes()

    
    def ObterTodosRegistros(self,tabela, incluir_id=True, tipo_retorno = 'list_of_dict'):
        consulta = self.session.query(tabela).all()
        dados =[]
        colunas = list(tabela.__table__.columns)
        if tipo_retorno == 'list_of_dict':
            dados = self.converter_consulta_list_of_dict(consulta, colunas, incluir_id)
        elif tipo_retorno == 'list_of_list':
            dados = self.converter_consulta_list_of_list(consulta, colunas, incluir_id)
        return dados
    
    def ObterFiltroRegistros(self, tabela, nome_coluna_filtro, filtro, incluir_id=True, tipo_retorno = 'list_of_dict'):
        consulta = self.session.query(tabela).filter(getattr(tabela, nome_coluna_filtro) == filtro)
        dados =[]
        colunas = list(tabela.__table__.columns)
        if tipo_retorno == 'list_of_dict':
            dados = self.converter_consulta_list_of_dict(consulta, colunas, incluir_id)
        elif tipo_retorno == 'list_of_list':
            dados = self.converter_consulta_list_of_list(consulta, incluir_id)
        return dados

    def ObterRegistro(self, tabela, nome_coluna_id, id):
        consulta = self.session.query(tabela).filter(getattr(tabela, nome_coluna_id) == id).first()
        dados=[]
        if consulta is None: return []
        linha = {}
        for column in tabela.__table__.columns:
            linha[column.name] = getattr(consulta, column.name)
        dados.append(linha)
        return dados[0]
    
    def ObterCampo(self, tabela, nome_coluna_id, id, nome_campo):
        consulta = self.session.query(tabela).filter(getattr(tabela, nome_coluna_id) == id).first()
        if consulta is None: return None
        if not hasattr(consulta, nome_campo):
            raise AttributeError(f"O campo '{nome_campo}' não existe na tabela.")
        return getattr(consulta, nome_campo)
    
    def AlterarCampo(self, tabela, nome_coluna_id, id, nome_campo, novo_dado):
        consulta = self.session.query(tabela).filter(getattr(tabela, nome_coluna_id) == id).first()
        if consulta is None: return None
        if not hasattr(consulta, nome_campo):
            raise AttributeError(f"O campo '{nome_campo}' não existe na tabela.")
        setattr(consulta, nome_campo, novo_dado)
        self.SalvarAlteracoes()

    def CriarTabela(self, tabela):
        tabela.__table__.create(self.engine)
        self.SalvarAlteracoes()

    def LimparDadosTabela(self, tabela):
        if self.session.query(tabela).count() > 0:
            self.session.query(tabela).delete()
            self.SalvarAlteracoes()

    def ExcluirTabela(self, tabela):
        tabela.__table__.drop(self.engine)
        self.SalvarAlteracoes()

    def ExcutarConsultaSQL (self, consulta: str):
        consulta_text = text(consulta)
        consulta = self.engine.connect().execute(consulta_text).fetchall()
        return consulta
    
    def atualizar_tabela(self, tabela, data):
        self.LimparDadosTabela(tabela)
        self.AdicionarListaRegistros(tabela, data)
        self.SalvarAlteracoes()

    def atualizar_registro(self, tabela, id_registro, novos_dados):
        registro = self.session.query(tabela).get(id_registro)
        if registro:
            for campo in novos_dados.__dict__:
                if campo != '_sa_instance_state':  
                    setattr(registro, campo, getattr(novos_dados, campo))
        self.SalvarAlteracoes()
        


    def SalvarAlteracoes(self):
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()  
            print("Erro ao salvar alterações:", e)

    
    def converter_consulta_list_of_dict(self, consulta, colunas, incluir_primeira_coluna=True):
        dados=[]
        if consulta is None:
            return []
        for row in consulta:
            linha = {}
            for i, column in enumerate(colunas):
                if incluir_primeira_coluna or i > 0:  
                    linha[column.name] = getattr(row, column.name)
            dados.append(linha)
        return dados
    

    def converter_consulta_list_of_list(self, consulta, colunas= False, incluir_primeira_coluna=True):
        dados = []
        if consulta is None:
            return []
        if hasattr(consulta, 'column_descriptions'):
            cabecalhos = [col['name'] for col in consulta.column_descriptions]
        else:
            cabecalhos = [col.name for col in consulta[0].__table__.columns]
        dados.append(cabecalhos)
        for row in consulta:
            if colunas:
                linha = []
                for i, column in enumerate(colunas):
                    if incluir_primeira_coluna or i > 0:  
                        linha.append(getattr(row, column.name))
                dados.append(linha)
            else:
                linha = []
                for col, col_value in enumerate(row):
                    if incluir_primeira_coluna or col > 0:
                        linha.append(col_value)
                dados.append(linha)
        return dados
    



        
