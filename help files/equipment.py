from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: int
    stamina_per_turn: int


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self):
        """рандомный урон от мин до макс"""
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name) -> Optional[Weapon]:
        """возвращает объект оружия по имени"""
        for weapon in self.equipment.weapons:
            if weapon.name == weapon_name:
                return weapon
        return None

    def get_armor(self, armor_name) -> Optional[Armor]:
        """возвращает объект брони по имени"""
        for armor in self.equipment.armors:
            if armor.name == armor_name:
                return armor
        return None

    def get_weapons_names(self) -> List:
        """возвращаем список с возможным оружием"""
        return [weapon.name for weapon in self.equipment.weapons]

    def get_armors_names(self) -> List:
        """возвращаем список с возможной броней"""
        return [armor.name for armor in self.equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """"загружает json в переменную EquipmentData"""
        with open("./data/equipment.json") as equipment_file:
            # equipment_file = open("./data/equipment.json")
            data = json.load(equipment_file)
            # equipment_file.close()
            equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
