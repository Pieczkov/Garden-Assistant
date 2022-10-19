from datetime import date

import pytest
from django.test import Client
from django.urls import reverse

from garden_app.forms import AddPlantForm, AddTaskForm, AddPlanOfWorkForm
from garden_app.models import Unit, PlantType, Plant, Task, PlanOfWork
from garden_app.tests.conftest import create_fake_unit, create_fake_plant_type


@pytest.mark.django_db
def test_index():
    client = Client()
    url = "/"
    response = client.get(url)
    assert response.status_code == 200
    assert "Assistant Gardeners" in str(response.content)


@pytest.mark.django_db
def test_home():
    client = Client()
    url = reverse("base_view")
    response = client.get(url)
    assert response.status_code == 200
    assert "Login" in str(response.content)


@pytest.mark.django_db
def test_add_unit_get():
    client = Client()
    url = reverse("add_unit")
    response = client.get(url)
    assert response.status_code == 200
    assert "Add unit" in str(response.content)


@pytest.mark.django_db
def test_add_unit_post():
    client = Client()
    url = reverse("add_unit")
    data = {"name": "test"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith("/plant_list")
    assert Unit.objects.get(name="test")


@pytest.mark.django_db
def test_add_plant_type_get():
    client = Client()
    url = reverse("add_type")
    response = client.get(url)
    assert response.status_code == 200
    assert "Add plant type" in str(response.content)


@pytest.mark.django_db
def test_add_plant_type_post():
    client = Client()
    url = reverse("add_type")
    data = {"name": "test"}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith("/plant_list")
    assert PlantType.objects.get(name="test")


@pytest.mark.django_db
def test_add_plant_get():
    client = Client()
    url = reverse("add_plant")
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context["form"]
    assert isinstance(form_in_view, AddPlantForm)


# na razie jeden jak znajde czas to dodamy wszytkie mozliwosci
@pytest.mark.django_db
@pytest.mark.parametrize(
    ("data", "should_fail"),
    (
        (
            {
                "name": "haha",
                "species": "tree",
                "description": "kk",
                "amount": 3,
            },
            False,
        ),
        (
            {
                "name": "haha",
                "species": "tree",
                "description": "kk",
                "amount": "gfg",
            },
            True,
        ),
    ),
)
def test_add_plant_post(fake_plant_type, fake_unit, data, should_fail):
    client = Client()
    data = data.update({"unit": fake_unit.id, "type": fake_plant_type.id})
    response = client.post("/add_plant", data=data, follow=True)

    if should_fail:
        assert response.status_code == 404
        assert len(Plant.objects.all()) == 0
        return

    assert response.status_code == 302
    assert response.url.startswith("/add_task")
    assert Plant.objects.get(name="haha")


@pytest.mark.django_db
def test_plant_list_get(plants):
    client = Client()
    url = reverse("plant_list")
    response = client.get(url)
    assert response.status_code == 200
    plant_from_view = response.context["plants"]
    assert plant_from_view.count() == len(plants)


@pytest.mark.django_db
def test_plant_delete_get(fake_plant):
    client = Client()
    url = reverse("delete_plant", args=(fake_plant.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith("/plant_list")
    assert Plant.objects.count() == 0


@pytest.mark.django_db
def test_add_task_get():
    client = Client()
    url = reverse("add_task")
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context["form"]
    assert isinstance(form_in_view, AddTaskForm)


# na razie jeden jak znajde czas to dodamy wszytkie mozliwosci
@pytest.mark.django_db
def test_add_task_post(fake_plant, fake_plan):
    client = Client()
    url = reverse("add_task")
    data = {"name": "apple", "description": "", "plant": fake_plant.id, "plan": fake_plan.id}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith("/plan_list")
    assert Task.objects.get(name="apple")


@pytest.mark.django_db
def test_task_list_get(tasks):
    client = Client()
    url = reverse("task_list")
    response = client.get(url)
    assert response.status_code == 200
    task_from_view = response.context["tasks"]
    assert task_from_view.count() == len(tasks)


#
#
@pytest.mark.django_db
def test_task_delete_get(fake_task):
    client = Client()
    url = reverse("delete_task", args=(fake_task.id,))
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith("/task_list")
    assert Task.objects.count() == 0


@pytest.mark.django_db
def test_plan_add_get():
    client = Client()
    url = reverse("add_plan")
    response = client.get(url)
    assert response.status_code == 200
    form_in_view = response.context["form"]
    assert isinstance(form_in_view, AddPlanOfWorkForm)


@pytest.mark.django_db
def test_plan_add_post():
    client = Client()
    url = reverse("add_plan")
    data = {
        "name": "grusza",
        "description": "",
        "date": date.today(),
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith("/plan_list")
    assert PlanOfWork.objects.get(name="grusza")


@pytest.mark.django_db
def test_plan_view_get(fake_plan):
    client = Client()
    url = reverse("plan_view", args=(fake_plan.id,))
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_plan_list_get(plans):
    client = Client()
    url = reverse("plan_list")
    response = client.get(url)
    assert response.status_code == 200
    assert PlanOfWork.objects.count() == len(plans)
