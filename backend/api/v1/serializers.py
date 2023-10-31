from typing import Dict, List

from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import (ModelSerializer, CharField,
                                        ValidationError)

from shared_info.models import (Schedule, EducationLevel, Course,
                                Specialization, Location)
from students.models import Student, Skill, FavoriteStudent, CompareStudent
from users.serializers import CustomUserSerializer
from vacancies.models import (Vacancy, VacancySkill, VacancyEducationLevel,
                              VacancySchedule, VacancySpecialization)


# ----------------------------------------------------------------------------
#                       Shared_info serializers
# ----------------------------------------------------------------------------


class SkillSerializer(ModelSerializer):
    """
    Сериализатор для модели Skill.

    Attributes:
        id (int): Идентификатор навыка.
        name (str): Название навыка.
    """

    class Meta:
        model = Skill
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class EducationLevelSerializer(ModelSerializer):
    """
    Сериализатор для модели EducationLevel.

    Attributes:
        id (int): Идентификатор грейда.
        name (str): Название грейда.
    """

    class Meta:
        model = EducationLevel
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class CourseSerializer(ModelSerializer):
    """
    Сериализатор для модели Course.

    Attributes:
        id (int): Идентификатор курса.
        name (str): Название курса.
    """

    class Meta:
        model = Course
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class SpecializationSerializer(ModelSerializer):
    """
    Сериализатор для модели Specialization.

    Attributes:
        id (int): Идентификатор специализации.
        name (str): Название специализации.
    """

    class Meta:
        model = Specialization
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class ScheduleSerializer(ModelSerializer):
    """
    Сериализатор для модели Schedule.

    Attributes:
        id (int): Идентификатор графика.
        name (str): Название графика.
    """

    class Meta:
        model = Schedule
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class LocationSerializer(ModelSerializer):
    """
    Сериализатор для модели Location.

    Attributes:
        id (int): Идентификатор локации.
        name (str): Название локации.
    """

    class Meta:
        model = Location
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


# ----------------------------------------------------------------------------
#                       Students serializers
# ----------------------------------------------------------------------------


class StudentDetailSerializer(ModelSerializer):
    """
    Сериализатор для модели Student с детальной информацией.

    Attributes:
        - skills (SkillSerializer, read-only): Сериализатор для списка
        навыков студента.
        - sex (CharField, read-only): Пол студента в текстовом виде.
        - schedule (ScheduleSerializer, read-only): Сериализатор для списка
        графиков занятости студента.
        - specialization (SpecializationSerializer, read-only): Сериализатор
        для специализации студента.
        - education_level (EducationLevelSerializer, read-only): Сериализатор
        для грейда студента.
        - course (CourseSerializer, read-only): Сериализатор для
        курса студента.
        - location (LocationSerializer, read-only): Сериализатор для
        местоположения студента.
    """
    skills = SkillSerializer(many=True, read_only=True)
    sex = CharField(source='get_sex_display')
    schedule = ScheduleSerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    education_level = EducationLevelSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_compare_list = SerializerMethodField()

    class Meta:
        model = Student
        fields = (
            'id',
            'avatar',
            'last_name',
            'first_name',
            'location',
            'email',
            'sex',
            'age',
            'telegram',
            'phone_number',
            'experience',
            'specialization',
            'course',
            'education_level',
            'schedule',
            'skills',
            'is_favorited',
            'is_in_compare_list'
        )

    def get_is_favorited(self, student: Student) -> bool:
        """Указывает, добавлен ли студент в избранные текущим пользователем."""
        return ((user := self.context.get('request').user)
                and user.is_authenticated
                and FavoriteStudent.objects.filter(user=user,
                                                   student=student).exists())

    def get_is_in_compare_list(self, student: Student) -> bool:
        """Указывает, добавлен ли студент в сравнение текущим пользователем."""
        return ((user := self.context.get('request').user)
                and user.is_authenticated
                and CompareStudent.objects.filter(user=user,
                                                  student=student).exists())


class StudentSerializer(StudentDetailSerializer):
    """
    Сериализатор для модели Student.

    Attributes:
        - skills (SkillSerializer, read-only): Сериализатор для списка
        навыков студента.
        - schedule (ScheduleSerializer, read-only): Сериализатор для списка
        графиков занятости студента.
        - location (LocationSerializer, read-only): Сериализатор для
        местоположения студента.
    """

    class Meta:
        model = Student
        fields = (
            'id',
            'avatar',
            'last_name',
            'first_name',
            'email',
            'location',
            'telegram',
            'schedule',
            'skills',
            'is_favorited'
        )


# ----------------------------------------------------------------------------
#                       Vacancies serializers
# ----------------------------------------------------------------------------


class VacancyReadSerializer(ModelSerializer):
    """
    Сериализатор для модели Vacancy с основной информацией.

    Attributes:
        - required_skills (SkillSerializer, read-only): Сериализатор для
        списка требуемых навыков.
        - schedule (ScheduleSerializer, read-only): Сериализатор для списка
        графиков работы.
        - specialization (SpecializationSerializer, read-only): Сериализатор
        для специализаций.
        - required_education_level (EducationLevelSerializer, read-only):
        Сериализатор для грейдов.
        - location (LocationSerializer, read-only): Сериализатор для
        местоположения вакансии.
    """
    required_skills = SkillSerializer(many=True)
    schedule = ScheduleSerializer(many=True)
    specialization = SpecializationSerializer(many=True)
    required_education_level = EducationLevelSerializer(many=True)
    location = LocationSerializer()

    class Meta:
        model = Vacancy
        fields = (
            'id',
            'name',
            'author',
            'location',
            'text',
            'pub_date',
            'salary',
            'specialization',
            'schedule',
            'required_education_level',
            'required_skills',
        )


class VacancySmallReadSerializer(VacancyReadSerializer):
    """
    Сериализатор для модели Vacancy с краткой информацией для
    карточного представления.

    Полностью наследуется от VacancyReadSerializer.
    """

    class Meta:
        model = Vacancy
        fields = (
            'id',
            'name',
            'author',
            'location',
            'pub_date',
            'salary',
            'schedule',
            'required_education_level',
            'required_skills',
        )


class VacancySkillSerializer(ModelSerializer):
    """
    Сериализатор для связи между моделями Vacancy и Skill.

    Attributes:
        id (int, write-only): Идентификатор скилла.
    """
    id = IntegerField(write_only=True)

    class Meta:
        model = VacancySkill
        fields = (
            'id',
        )


class VacancyEducationLevelSerializer(ModelSerializer):
    """
    Сериализатор для связи между моделями Vacancy и EducationLevel.

    Attributes:
        id (int, write-only): Идентификатор грейда.
    """
    id = IntegerField(write_only=True)

    class Meta:
        model = VacancyEducationLevel
        fields = (
            'id',
        )


class VacancyScheduleSerializer(ModelSerializer):
    """
    Сериализатор для связи между моделями Vacancy и Schedule.

    Attributes:
        id (int, write-only): Идентификатор графика.
    """
    id = IntegerField(write_only=True)

    class Meta:
        model = VacancySchedule
        fields = (
            'id',
        )


class VacancySpecializationSerializer(ModelSerializer):
    """
    Сериализатор для связи между моделями Vacancy и Specialization.

    Attributes:
        id (int, write-only): Идентификатор спецализации.
    """
    id = IntegerField(write_only=True)

    class Meta:
        model = VacancySpecialization
        fields = (
            'id',
        )


class VacancySerializer(ModelSerializer):
    """
    Сериализатор для модели Vacancy.

    Attributes:
        - author (CustomUserSerializer, read-only): Сериализатор для
        автора вакансии.
        - id (IntegerField, read-only): Идентификатор вакансии.
        - required_skills (VacancySkillSerializer, write-only): Сериализатор
        для связи с требуемыми навыками.
        - schedule (VacancyScheduleSerializer, write-only): Сериализатор для
        связи с графиками работы.
        - specialization (VacancySpecializationSerializer, write-only):
        Сериализатор для связи со специализациями.
        - required_education_level (VacancyEducationLevelSerializer,
        write-only): Сериализатор для связи с уровнями образования.
    """
    author = CustomUserSerializer(read_only=True)
    id = IntegerField(read_only=True)
    required_skills = VacancySkillSerializer(many=True)
    schedule = VacancyScheduleSerializer(many=True)
    specialization = VacancySpecializationSerializer(many=True)
    required_education_level = VacancyEducationLevelSerializer(many=True)

    class Meta:
        model = Vacancy
        fields = (
            'id',
            'name',
            'author',
            'location',
            'text',
            'pub_date',
            'salary',
            'specialization',
            'schedule',
            'required_education_level',
            'required_skills',
        )

    def to_representation(self, instance: Vacancy) -> Dict:
        """
        Преобразует вакансию в словарь с данными из списка словарей.

        Args:
            instance (Vacancy): Экземпляр вакансии.

        Returns:
            Dict: Словарь с данными вакансии из VacancyReadSerializer.
        """
        request = self.context.get('request')
        context = {'request': request}
        return VacancyReadSerializer(instance, context=context).data

    @staticmethod
    def create_vacancy_essentials(vacancy: Vacancy,
                                  skills: List[Dict],
                                  levels,
                                  schedules,
                                  specializations) -> None:
        """
        Создает связи между вакансией и другими сущностями
        (навыками, грейдом, графиками работы, специализациями).

        Args:
            vacancy (Vacancy): Вакансия, с которой устанавливаются связи.
            skills (List[Dict]): Список словарей с информацией о навыках.
            levels (List): Список уровней образования.
            schedules (List): Список графиков работы.
            specializations (List): Список специализаций.

        Raises:
            ValidationError: Если указанные навыки, грейды, графики работы
            или специализации не существуют.
        """
        essentials = [
            (skills, Skill, 'skill'),
            (levels, EducationLevel, 'education_level'),
            (schedules, Schedule, 'schedule'),
            (specializations, Specialization, 'specialization')
        ]

        for items, model, field in essentials:
            compositions = []
            for item in items:
                item_id = item['id']
                try:
                    item_obj = model.objects.get(id=item_id)
                except model.DoesNotExist:
                    raise ValidationError(
                        {f'{model.__name__} с ID {item_id} не существует.'})

                composition = (f'Vacancy{model.__name__}(vacancy=vacancy, '
                               f'{field}=item_obj)')
                compositions.append(eval(composition))

            composition_model = eval(f'Vacancy{model.__name__}')
            composition_model.objects.bulk_create(compositions)

    def create(self, validated_data: Dict) -> Vacancy:
        """
        Создает новую вакансию в базе данных.

        Args:
            validated_data (Dict): Валидированные данные для создания вакансии.

        Returns:
            Vacancy: Созданный экземпляр вакансии.

        Raises:
            ValidationError: Если указанные навыки, грейды, графики работы
            или специализации не существуют.
        """
        required_skills = validated_data.pop('required_skills', [])
        required_education_level = validated_data.pop(
            'required_education_level'
        )
        schedules = validated_data.pop('schedule')
        specializations = validated_data.pop('specialization')

        for field, model in [
            ('required_skills', Skill),
            ('required_education_level', EducationLevel),
            ('schedule', Schedule),
            ('specialization', Specialization)
        ]:
            for item in validated_data.get(field, []):
                if not model.objects.filter(id=item['id']).exists():
                    raise ValidationError(
                        {field: f"{model.__name__} с ID {item['id']} "
                                f"не существует."})

        vacancy = Vacancy.objects.create(**validated_data)
        self.create_vacancy_essentials(vacancy=vacancy,
                                       skills=required_skills,
                                       levels=required_education_level,
                                       schedules=schedules,
                                       specializations=specializations)

        return vacancy

    def update(self, instance, validated_data):
        """
        Обновляет экземпляр вакансии с учетом валидированных данных.

        Args:
            instance: Экземпляр вакансии, который нужно обновить.
            validated_data: Валидированные данные для обновления экземпляра.

        Returns:
            instance: Обновленный экземпляр вакансии.

        Raises:
            ValidationError: Если указанные навыки, грейды, графики работы
            или специализации не существуют.
        """
        # Перебираем поля валидированных данных и применяем их к экземпляру

        related_fields = {'required_skills': Skill,
                          'schedule': Schedule,
                          'specialization': Specialization,
                          'required_education_level': EducationLevel}

        for field, values in validated_data.items():
            if field in related_fields:
                new_field = []
                for value in values:
                    model = related_fields[field]
                    value_id = value.get('id')
                    try:
                        value_obj = model.objects.get(id=value_id)
                        new_field.append(value_obj)
                    except model.DoesNotExist:
                        raise ValidationError(
                            {field: f"{model.__name__} с ID {value_id} "
                                    f"не существует."})

                # Очищаем поле и устанавливаем новые значения
                getattr(instance, field).clear()
                getattr(instance, field).set(new_field)

            else:
                # Для обычных полей просто обновляем их
                setattr(instance, field, values)

        instance.save()
        return instance


# ----------------------------------------------------------------------------
#                       Matching serializers
# ----------------------------------------------------------------------------


class MatchingStudentSerializer(StudentSerializer):
    """
    Сериализатор для студентов, с дополнительным полем matching_percentage,
    представляющим процентное соотношение скиллов студента
    к скиллам из вакансии.

    Attributes:
        matching_percentage (int): Поле, представляющее процентное соотношение
            скиллов студента к скиллам из вакансии.
    """
    matching_percentage = SerializerMethodField()

    def get_matching_percentage(self, student):
        """
        Рассчитывает процентное соотношение скиллов студента к
        скиллам из вакансии и возвращает его значение.

        Args:
            student (Student): Объект студента, для которого рассчитывается
                процентное соотношение.

        Returns:
            int: Процентное соотношение скиллов студента к скиллам из вакансии.
        """
        vacancy_id = self.context['vacancy_id']
        vacancy = Vacancy.objects.get(id=vacancy_id)
        required_skills = vacancy.required_skills.all()

        student_skills = student.skills.all()
        common_skills_count = len(set(required_skills) & set(student_skills))
        total_required_skills = len(required_skills)

        if total_required_skills == 0:
            return 0  # Избегаем деления на ноль

        matching_percentage = ((common_skills_count / total_required_skills)
                               * 100)
        return int(matching_percentage)

    class Meta:
        model = Student
        fields = (
            'id',
            'avatar',
            'last_name',
            'first_name',
            'email',
            'location',
            'telegram',
            'schedule',
            'skills',
            'matching_percentage'
        )
