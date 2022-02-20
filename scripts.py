import random
import sys

from datacenter.models import (Schoolkid, Mark, Lesson,
                               Chastisement, Commendation)
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

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
    except ObjectDoesNotExist:
        sys.exit("Нет ученика с таким именем!")
    except MultipleObjectsReturned:
        sys.exit("Учеников с таким именем несколько!")
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

    while True:
        lessons = Lesson.objects.filter(
            year_of_study=6,
            group_letter='А',
            subject__title=lesson_subject
        )
        random_lesson = random.choice(lessons)
        if Commendation.objects.filter(
                created=random_lesson.date,
                schoolkid=schoolkid,
                subject=random_lesson.subject,
                teacher=random_lesson.teacher
        ):
            continue
        Commendation.objects.create(
            text=random.choice(commendations),
            created=random_lesson.date,
            schoolkid=schoolkid,
            subject=random_lesson.subject,
            teacher=random_lesson.teacher
        )
        break
