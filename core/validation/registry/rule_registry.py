# rule_registry.py

from __future__ import annotations

from modules.connections.rules.name_rule import NameRule
from modules.connections.rules.database_type_rule import DatabaseTypeRule
from modules.connections.rules.host_rule import HostRule
from modules.connections.rules.port_rule import PortRule
from modules.connections.rules.database_rule import DatabaseRule
from modules.connections.rules.user_rule import UserRule


class RuleRegistry:

    @staticmethod
    def connection_rules():
        return [
            NameRule(),
            DatabaseTypeRule(),
            HostRule(),
            PortRule(),
            DatabaseRule(),
            UserRule(),
        ]