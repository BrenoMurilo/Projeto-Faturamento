from Drivers.DataBase_Drivers.SqlAlchemy import SqlAlchemy
from models import Escritorios, Arquivos, Emails
from config import config, config_param, config_email
import os
from sqlalchemy import text  



config_param.gerar_planilha('Parâmetros')