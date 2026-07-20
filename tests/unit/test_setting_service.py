# test_setting_service.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.database import Base
from modules.settings.setting import Setting
from modules.settings.setting_dto import SettingDTO
from modules.settings.setting_service import SettingService
from modules.settings.setting_repository import SettingRepository
from modules.settings.setting_validator import SettingValidator

@pytest.fixture
def db_session():
    # Usar banco SQLite em memória para isolamento de testes
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_setting(db_session):
    repo = SettingRepository(db_session)
    service = SettingService(repo)
    
    dto = SettingDTO(
        nm_setting="Config Teste",
        id_conexao=None,
        high_quality=True,
        low_quality=False,
        output_dir="/out"
    )
    
    # Validar DTO
    validator = SettingValidator()
    report = validator.validate(dto)
    assert report.valid
    
    # Criar configuração
    created = service.create_setting(dto)
    assert created.id_setting is not None
    assert created.nm_setting == "Config Teste"
    assert created.output_dir == "/out"
    assert created.high_quality is True
    
    # Buscar no banco
    fetched = service.get_setting_by_id(created.id_setting)
    assert fetched is not None
    assert fetched.nm_setting == "Config Teste"

def test_update_setting(db_session):
    repo = SettingRepository(db_session)
    service = SettingService(repo)
    
    # Criar registro inicial
    dto = SettingDTO(nm_setting="Original", id_conexao=None)
    created = service.create_setting(dto)
    
    # Atualizar registro
    dto_update = SettingDTO(
        id_setting=created.id_setting,
        nm_setting="Modificado",
        id_conexao=None,
        output_dir="/new_out"
    )
    service.update_setting(dto_update)
    
    # Validar alteração
    fetched = service.get_setting_by_id(created.id_setting)
    assert fetched.nm_setting == "Modificado"
    assert fetched.output_dir == "/new_out"

def test_delete_setting(db_session):
    repo = SettingRepository(db_session)
    service = SettingService(repo)
    
    dto = SettingDTO(nm_setting="Para Deletar", id_conexao=None)
    created = service.create_setting(dto)
    
    # Excluir
    service.delete_setting(created.id_setting)
    
    # Validar exclusão
    assert service.get_setting_by_id(created.id_setting) is None

def test_validator_missing_name():
    validator = SettingValidator()
    
    # Sem nome (vazio)
    dto1 = SettingDTO(nm_setting="", id_conexao=None)
    report1 = validator.validate(dto1)
    assert not report1.valid
    assert any(e.field == "nm_setting" for e in report1.errors)
    
    # Apenas espaços
    dto2 = SettingDTO(nm_setting="   ", id_conexao=None)
    report2 = validator.validate(dto2)
    assert not report2.valid
