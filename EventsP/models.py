from django.db import models


class Person(models.Model):
    # Словарь для поля с выпадающим списком
    choice_status_list = (
        (0, 'Без статуса'),
        (1, 'Организатор'),
        (2, 'Участник'),
    )
    # id человека
    p_id = models.AutoField(primary_key=True)
    # Поле имени
    # max_length - максимальная длинна записи
    # verbose_name - отображаемое имя
    # unique - атрибут для каждой записи уникален
    # blank - возможность атрибута иметь неопределенное значение
    # null -  возможность записать в базу данных неопределенное значение
    # choices - выпадающий список
    middle_name = models.CharField(max_length=20, verbose_name='Фамилия')
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    family_name = models.CharField(max_length=20, verbose_name='Отчество')
    phone = models.CharField(unique=True, max_length=15, verbose_name='Телефон')
    group_name = models.CharField(max_length=10, blank=True, null=True, verbose_name='Номер группы')
    telegram_id = models.CharField(unique=True, max_length=50, verbose_name='Телеграм id')
    vk_url = models.CharField(max_length=50, verbose_name='VK')
    status = models.SmallIntegerField(default=0, verbose_name='Статус', choices=choice_status_list)

    # Вложенный класс определяет связь между моделью и сущностью внутри базы данных
    class Meta:
        managed = True  # изменения модели влекут за собой изменения сущности в базе данных
        db_table = 'ev_people'  # связанная таблица

    # Специальный метод для отображения ФИО целиком
    def i_name(self):
        return self.middle_name + ' ' + self.first_name + ' ' + self.family_name

    # Краткое название метода
    i_name.short_description = 'ФИО'


class Participant(Person):
    choice_status_list_1 = (
        (0, 'Не приехал'),
        (1, 'Приехал'),
        (2, 'Выехал'),
    )
    part_id = models.AutoField(primary_key=True)
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата Рождения')
    check_in = models.TimeField(blank=True, null=True, verbose_name='Время заезда')
    arrive_status = models.IntegerField(verbose_name='Статус прибытия',
                                        choices=choice_status_list_1, default=0)
    room = models.ForeignKey('Room', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Комната')
    team = models.ForeignKey('Team', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Команда')

    def save(self, *args, **kwargs):
        self.status = 2
        super(Participant, self).save(*args, **kwargs)

    def __str__(self):
        return self.family_name + ' ' + self.first_name + ' ' + self.middle_name

    class Meta:
        managed = True
        db_table = 'ev_part'
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Org(Person):
    org_id = models.AutoField(primary_key=True)

    def save(self, *args, **kwargs):
        self.status = 1
        super(Org, self).save(*args, **kwargs)

    def __str__(self):
        return self.middle_name + ' ' +  self.family_name + ' ' + self.first_name

    class Meta:
        managed = True
        db_table = 'ev_org'
        verbose_name = 'Организатор'
        verbose_name_plural = 'Организаторы'


class Room(models.Model):
    r_id = models.AutoField(primary_key=True)
    room_num = models.IntegerField(verbose_name='Номер комнаты')
    room_floor = models.IntegerField(blank=True, null=True, verbose_name='Этаж')
    room_building = models.CharField(max_length=5, blank=True, null=True, verbose_name='Корпус/Строение')
    bed_num = models.IntegerField(verbose_name='Всего кроватей')
    features = models.TextField(max_length=4000, blank=True, null=True)

    def __str__(self):
        return str(self.room_num)  # + ' кроватей: ' + str(self.bed_num)

    class Meta:
        managed = True
        db_table = 'ev_rooms'
        verbose_name = 'Комната'
        verbose_name_plural = 'Комнаты'


class Requisite(models.Model):
    req_id = models.AutoField(primary_key=True)
    req_name = models.CharField(max_length=20, verbose_name='Название')
    req_amount = models.DecimalField(max_digits=5, decimal_places=0, verbose_name='Количество')
    req_description = models.CharField(max_length=4000, blank=True, null=True, verbose_name='Описание')
    req_owner = models.ForeignKey(Org, on_delete=models.CASCADE, db_column='req_owner', verbose_name='Владелец')

    def __str__(self):
        return self.req_name

    class Meta:
        managed = True
        db_table = 'ev_requisite'
        verbose_name = 'Реквизит'
        verbose_name_plural = 'Реквизит'


class Team(models.Model):
    t_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=40, blank=True, null=True)

    def __str__(self):
        return self.team_name

    class Meta:
        managed = True
        db_table = 'ev_teams'
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Place(models.Model):
    place_id = models.AutoField(primary_key=True)
    place_name = models.CharField(max_length=50, verbose_name='Название')
    features = models.TextField(max_length=40000, blank=True, null=True, verbose_name='Особенности')

    def __str__(self):
        return self.place_name

    class Meta:
        managed = True
        db_table = 'ev_places'
        verbose_name = 'Место'
        verbose_name_plural = 'Места'


class Event(models.Model):
    ev_id = models.AutoField(primary_key=True)
    ev_name = models.CharField(max_length=50, verbose_name='Наименование')
    event_features = models.CharField(max_length=40000, blank=True, null=True, verbose_name='Особенности')

    def __str__(self):
        return self.ev_name

    class Meta:
        managed = True
        db_table = 'ev_events'
        verbose_name = 'Событие'
        verbose_name_plural = 'События'


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_name = models.CharField(unique=True, max_length=40, blank=True, null=True)

    def __str__(self):
        return self.post_name

    class Meta:
        managed = True
        db_table = 'ev_posts'
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'


class PersonWithPost(models.Model):
    id_person = models.ForeignKey(Org, on_delete=models.CASCADE, db_column='org_id',
                                  verbose_name='ФИО')
    id_post = models.ForeignKey('Post', on_delete=models.CASCADE, db_column='id_post',
                                verbose_name='Должность')

    def __str__(self):
        return str(self.id_person) + ' - ' + str(self.id_post)

    class Meta:
        managed = True
        db_table = 'ev_person_posts'
        verbose_name = 'Люди по должностям'
        verbose_name_plural = 'Люди по должностям'


class Timetable(models.Model):
    id_person_post = models.ForeignKey('PersonWithPost',
                                       on_delete=models.CASCADE,
                                       db_column='id_person_post',
                                       verbose_name='Человек + Должность')
    id_event = models.ForeignKey('Event',
                                 on_delete=models.CASCADE,
                                 db_column='id_event',
                                 verbose_name='Событие')
    team = models.ForeignKey('Team',
                             on_delete=models.CASCADE,
                             db_column='id_team',
                             blank=True, null=True,
                             verbose_name='Команда')
    place = models.ForeignKey('Place',
                              on_delete=models.CASCADE,
                              db_column='id_place',
                              blank=True, null=True,
                              verbose_name='Место')
    event_start_time = models.DateTimeField(blank=True, null=True, verbose_name='Начало')
    event_end_time = models.DateTimeField(blank=True, null=True, verbose_name='Окончание')

    def __str__(self):
        return str(self.id_person_post) + ' ' + str(self.id_event)

    def save(self, *args, **kwargs):
        tmp = Timetable.objects.filter(id_person_post=self.id_person_post)
        if tmp.exists():
            fl = True
            for timetable in tmp:
                print(timetable.event_end_time)
                if timetable.event_start_time < self.event_end_time and \
                        timetable.event_end_time > self.event_start_time:
                    fl = False
            if fl:
                super(Timetable, self).save(*args, **kwargs)
        else:
            super(Timetable, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'ev_timetable'
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписание'

    def b_time(self):
        return 'From  ' + str(self.event_start_time) + ' To  ' + str(self.event_end_time)
