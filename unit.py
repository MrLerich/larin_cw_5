from __future__ import annotations

from abc import ABC, abstractmethod
from random import randint

from classes import UnitClass
from equipment import Weapon, Armor


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """

    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        return round(self.hp, 1)  # TODO возвращаем аттрибут hp в красивом виде

    @property
    def stamina_points(self):
        return round(self.stamina, 1)  # TODO возвращаем аттрибут hp в красивом виде

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon  # TODO присваиваем нашему герою новое оружие
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        self.armor = armor  # TODO одеваем новую броню
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """подсчет урона при круге"""
        self.stamina -= self.weapon.stamina_per_hit
        #  логику расчета урона игрока
        damage = self.weapon.damage * self.unit_class.attack
        # уменьшение выносливости атакующего при ударе
        #  и уменьшение выносливости защищающегося при использовании брони
        target_stamina = target.armor.stamina_per_turn * target.unit_class.stamina
        if target.stamina > target_stamina:
            damage -= target.armor.defence * target.unit_class.armor
            target.stamina -= target_stamina

        #  после всех расчетов цель получает урон - target.get_damage(damage)
        damage = round(damage, 1)
        target.get_damage(damage=damage)
        return damage

    def get_damage(self, damage: int) -> None:
        """получение урона целью присваиваем новое значение для аттрибута self.hp"""
        if damage > 0:
            self.hp -= damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return "Навык уже использован"

        self._is_skill_used = True
        return self.unit_class.skill.use(self, target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.\n" \
                   f"{self.name}, ты слишком слаб для этого!!! ХаХаХа!!!"

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его блокирует.\n" \
               f"Звезда в шоке!!!"


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости.\n" \
                   f"Шалабон!"

        damage = self._count_damage(target)
        if damage > 0:
            return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."

        return f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает.\n" \
               f"Стопэээ!!!"
