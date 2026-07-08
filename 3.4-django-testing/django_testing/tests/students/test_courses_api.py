import pytest
from django.urls import reverse

from students.models import Course

pytestmark = pytest.mark.django_db  # все тесты будут использовать БД


def test_retrieve_course(api_client, course_factory):
    course = course_factory('Course', name='Math')

    url = reverse('courses-detail', kwargs={'pk': course.id})
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data['id'] == course.id
    assert response.data['name'] == course.name


def test_list_courses(api_client, course_factory):
    course1 = course_factory('Course', name='Math')
    course2 = course_factory('Course', name='Physics')

    url = reverse('courses-list')
    response = api_client.get(url)

    assert response.status_code == 200
    assert len(response.data) == 2
    assert {c['id'] for c in response.data} == {course1.id, course2.id}


def test_filter_courses_by_id(api_client, course_factory):
    course1 = course_factory('Course', name='Math')
    course2 = course_factory('Course', name='Physics')

    url = reverse('courses-list')
    response = api_client.get(url, data={'id': course1.id})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == course1.id


def test_filter_courses_by_name(api_client, course_factory):
    course1 = course_factory('Course', name='Math')
    course2 = course_factory('Course', name='Physics')

    url = reverse('courses-list')
    response = api_client.get(url, data={'name': 'Math'})

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Math'


def test_create_course(api_client):
    data = {'name': 'Chemistry'}
    url = reverse('courses-list')
    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data['name'] == 'Chemistry'
    assert response.data['students'] == []  # пустой список по умолчанию


def test_update_course(api_client, course_factory):
    course = course_factory('Course', name='Math')
    data = {'name': 'Advanced Math'}
    url = reverse('courses-detail', kwargs={'pk': course.id})

    response = api_client.put(url, data)

    assert response.status_code == 200
    assert response.data['name'] == 'Advanced Math'

    # Проверка, что обновилось в БД
    course.refresh_from_db()
    assert course.name == 'Advanced Math'


def test_delete_course(api_client, course_factory):
    course = course_factory('Course', name='Math')
    url = reverse('courses-detail', kwargs={'pk': course.id})

    response = api_client.delete(url)

    assert response.status_code == 204
    assert not Course.objects.filter(id=course.id).exists()


@pytest.mark.parametrize("student_count, expect_error", [
    (20, False),   # допустимо
    (21, True),    # слишком много
])
def test_course_max_students_limit(
    api_client, student_factory, settings, student_count, expect_error
):
    # Переопределяем settings (только для этого теста)
    settings.MAX_STUDENTS_PER_COURSE = 20

    students = student_factory('Student', _quantity=student_count)
    student_ids = [s.id for s in students]

    data = {'name': 'Big Course', 'students': student_ids}
    url = reverse('courses-list')
    response = api_client.post(url, data)

    if expect_error:
        assert response.status_code == 400
        assert 'Максимум 20 студентов' in str(response.data['students'])
    else:
        assert response.status_code == 201
        assert len(response.data['students']) == 20