# setting_repository.py
from sqlalchemy.orm import Session
from .setting import Setting

class SettingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return (
            self.session
            .query(Setting)
            .order_by(Setting.nm_setting)
            .all()
        )

    def get_by_id(self, id_setting: int):
        return (
            self.session
            .query(Setting)
            .filter(Setting.id_setting == id_setting)
            .first()
        )

    def create(self, setting: Setting):
        self.session.add(setting)
        self.session.commit()
        self.session.refresh(setting)
        return setting

    def update(self):
        self.session.commit()

    def delete(self, setting: Setting):
        self.session.delete(setting)
        self.session.commit()

    def get_by_name(self, nm_setting: str):
        return (
            self.session
            .query(Setting)
            .filter(Setting.nm_setting == nm_setting)
            .first()
        )

    def exists_by_name(self, nm_setting: str) -> bool:
        return self.get_by_name(nm_setting) is not None

    def count(self) -> int:
        return (
            self.session
            .query(Setting)
            .count()
        )

    def search(self, text: str):
        return (
            self.session
            .query(Setting)
            .filter(Setting.nm_setting.ilike(f"%{text}%"))
            .order_by(Setting.nm_setting)
            .all()
        )
