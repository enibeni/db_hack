import random
import sys

from datacenter.models import (Schoolkid, Mark, Lesson,
                               Chastisement, Commendation)

commendations = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
]


def find_kid_by_fullname(full_name: str) -> Schoolkid:
    try:
        schoolkid = Schoolkid.objects.filter(full_name__contains=full_name).get()
    except Schoolkid.ObjectDoesNotExist:
        print("Нет ученика с таким именем!")
        return None
    except Schoolkid.MultipleObjectsReturned:
        print("Учеников с таким именем несколько!")
        return None
    return schoolkid


def fix_marks(full_name: str) -> None:
    schoolkid = find_kid_by_fullname(full_name)
    if not schoolkid:
        return None
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__lt=4)
    for mark in bad_marks:
        mark.points = 5
        mark.save()


def remove_chastisements(full_name: str) -> None:
    schoolkid = find_kid_by_fullname(full_name)
    if not schoolkid:
        return None
    kid_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
    for chastisement in kid_chastisements:
        chastisement.delete()


def create_commendation(full_name: str, lesson_subject: str) -> None:
    schoolkid = find_kid_by_fullname(full_name)
    if not schoolkid:
        return None
    lesson = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=lesson_subject
    ).order_by('date').reverse()[0]
    if not lesson:
        print("Такого предмета нет")
        return None
    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
