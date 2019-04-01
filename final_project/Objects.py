from abc import ABC, abstractmethod
import pygame
import random
import yaml


# Комменты чтобы не запутаться)
# Создание изображения объекта
def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


# базовый абстрактный класс с с инициализатором и абстрактным методом draw
class AbstractObject(ABC):
    def __init__(self):
        pass

    def draw(self, display):
        pass


# базовый абстрактный класс для организации взаимодействия между героем и объектами(сейчас это
# враги(Enemy) и союзники(Ally))
class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


# класс союзника
class Ally(AbstractObject, Interactive):
    # Получаем данные из ямл файла
    yaml_tag = u'!ally'

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


# Базовый класс
class Creature(AbstractObject):
    # кстати для отрисовки других обьектов навроде сундука, нужно же наверное создавать отдельный класс?
    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2

    # Реализуем взаимодействие героя и врага, а также союзника

    # Удар
    def hit(self, other):
        """
        Определяем, кто бьет первым,ха а тут встает проблема, каждый раз перед ударом будет производится
        расчет или нет.Ведь герой может получить какой то эффект который повлияет на его удачу. А так как
        у нас вроде бы пошаговый бой,то возможна ситуация когда противник просто не сможет ударить.
        Значит если не углублятся в подробности нужно определять первого бьющего, вне метода hit()
        Тогда нужно создать метод определяющий кто бьет первым
        :param other:
        :return:изменение количества едениц здоровья
        """

    # def who_is_first(self, other):
    #     """
    #     Название конечно так себе .Предположим что первым по умолчанию является тот кто вызывает метод
    #     who_is_first и только в случае если у other параметр Удача больше то первым бьет other
    #     Вообще я думаю что можно сделать его staticmethod
    #     :param other:
    #     :return: кортеж где нулевым элементом будет первый бьющий а первым элементом, второй
    #     """
    #     first = self
    #     if self.stats['luck'] < other.stats['luck']:
    #         return (other, self)
    #     return (first, other)
    #


class Enemy(Creature, Interactive):
    yaml_tag = u'!enemies'

    def __init__(self, icon, stats, hp, position):
        self.icon = icon
        self.stats = stats
        self.hp = hp
        self.position = position

    def interact(self, engine, hero):
        """

        :param engine:движок
        :param hero: объект героя
        :return: результат сражения. Удаление объекта героя либо объекта врага
        Бой будет идти пока у кого то не закончатся хп
        Первый нападает тот  у кого больше Удача
        Урон будем высчитывать складывая показатели Силы и Интеллекта, дабы соблюсти баланс между
        воинами и магами и добавлять какой то рандомный коэфициент в зависимости от удачи.
        Кстати герой может же сбежать от боя, но думаю это потребует серьезной модификации движка
        Хотя по идее, нужно будет поменять позицию героя здоровье врага и героя,
         ввести параметр регерации, какой то эффект,
         ну например маг впадает в уныние а воин хочет отомстить.Ладно не будем плодить сущностей
         Для боя нужно реализовать метод hit в базовом классе, так как союзник же ведь тоже гипотетически может сражаться
        Хотя можно предположить что герой взаимодействует с объектами только одним способом т.е
        врагов только бьет, союзники только накладывают эффекты.Но в будущем же возможно введение
        возможности переманивать врагов, говорить с ними и прочее. Поэтому исходя из пройденного материала
        и того что каждая функция должна делать что то одно, введу пока метод hit
        Сделаем упрощенно
        если враг побеждает то удаляем героя
        если герой побеждает, то он получает опыт и удаляем врага
        Чет помойму это костыль, лучше убрать этот метод
        и просто внутри интеракта сравнивать удачу через условный оператор
        """

        while True:
            if self.stats['luck'] > hero.stats['luck']:
                self.hit(hero)
                hero.hit(self)
            else:
                # Будем считать что если удача равна то герой бьет первый
                hero.hit(self)
                self.hit(hero)
            if self.hp > 0 and hero.hp <= 0:
                print(f'Герой повержен !!!')
                del hero
                break
            elif self.hp <= 0 and hero.hp > 0:
                print('Герой одержал победу над исчадием мрака!!!')
                hero.exp += self.stats['experience']
                del self
                break
            else:
                continue


class Hero(Creature, Interactive):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.stats['strength'] += 10
        self.stats['endurance'] += 10
        self.stats['intelligence'] -= 5


class Blessing(Effect):
    def apply_effect(self):
        self.stats['strength'] += 5
        self.stats['endurance'] += 5
        self.stats['intelligence'] += 5
        self.stats['luck'] += 5


class Weakness(Effect):
    def apply_effect(self):
        self.stats['strength'] -= 3
        self.stats['endurance'] -= 3
        self.stats['intelligence'] -= 3
        self.stats['luck'] -= 3
