from flask import Flask, render_template, request, url_for, redirect

from equipment import Equipment
from classes import unit_classes
from base import Arena
from unit import BaseUnit, PlayerUnit, EnemyUnit


app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena() #   инициализируем класс арены


@app.route("/")
def menu_page():
    """Стартовая страница"""
    #   рендерим главное меню (шаблон index.html)
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """Арена"""
    #  выполняем функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    #  рендерим экран боя (шаблон fight.html)
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)

@app.route("/fight/hit")
def hit():
    """Бой"""
    #  кнопка нанесения удара
    #  обновляем экран боя (нанесение удара) (шаблон fight.html)
    #  если игра идет - вызываем метод player.hit() экземпляра класса арены
    #  если игра не идет - пропускаем срабатывание метода (просто рендерим шаблон с текущими данными)
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """Применение умений"""
    #  кнопка использования скилла
    #  логика пркатикчески идентична предыдущему эндпоинту
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """Пропуск Хода"""
    #  кнопка пропуска хода
    # логика пркатикчески идентична предыдущему эндпоинту
    # однако вызываем здесь функцию следующий ход (arena.next_turn())
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """Окончание схватки"""
    # кнопка завершить игру - переход в главное меню
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """Выбор героя"""
    # кнопка выбор героя. 2 метода GET и POST
    # на GET отрисовываем форму.
    # на POST отправляем форму и делаем редирект на эндпоинт choose enemy
    if request.method == 'GET':

        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        result = {
            'header': 'Выберите героя',
            'classes': classes,
            'weapon': weapons,
            'armors': armors,
            }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']
        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        player.equip_armor(equipment.get_armor(armor_name))
        player.equip_weapon(equipment.get_weapon(weapon_name))
        heroes['player'] = player
        return redirect(url_for("choose_hero"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    # TODO кнопка выбор соперников. 2 метода GET и POST
    # TODO также на GET отрисовываем форму.
    # TODO а на POST отправляем форму и делаем редирект на начало битвы
    if request.method == 'GET':

        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes
        result = {
            'header': 'Выберите противника',
            'classes': classes,
            'weapon': weapons,
            'armors': armors,
        }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        armor_name = request.form['armor']
        weapon_name = request.form['weapon']
        unit_class = request.form['unit_class']
        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        enemy.equip_armor(equipment.get_armor(armor_name))
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        heroes['enemy'] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run()
