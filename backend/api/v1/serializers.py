from typing import Dict, List

from rest_framework.fields import IntegerField
from rest_framework.serializers import (ModelSerializer, CharField,
                                        ValidationError)

from shared_info.models import (Schedule, EducationLevel, Course,
                                Specialization, Location)
from students.models import Student, Skill
from users.serializers import CustomUserSerializer
from vacancies.models import (Vacancy, VacancySkills, VacancyEducationLevel,
                              VacancySchedule, VacancySpecialization)


# ----------------------------------------------------------------------------
                    # Students serializers
# ----------------------------------------------------------------------------


class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class EducationLevelSerializer(ModelSerializer):
    class Meta:
        model = EducationLevel
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class SpecializationSerializer(ModelSerializer):
    class Meta:
        model = Specialization
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class LocationSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name')
        extra_kwargs = {
            'name': {'required': False},
        }


class StudentSerializer(ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    schedule = ScheduleSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)

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
            'skills'
        )


class StudentDetailSerializer(ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    sex = CharField(source='get_sex_display')
    schedule = ScheduleSerializer(many=True, read_only=True)
    specialization = SpecializationSerializer(read_only=True)
    education_level = EducationLevelSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    location = LocationSerializer(read_only=True)

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
            'skills'
        )


# ----------------------------------------------------------------------------
                    # Vacancies serializers
# ----------------------------------------------------------------------------


class VacancyReadSerializer(ModelSerializer):
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
            'specialization',
            'schedule',
            'required_education_level',
            'required_skills',
        )


class VacancySkillsSerializer(ModelSerializer):
    """
    Сериализатор для связи между моделями Vacancy и Skill.

    Attributes:
        id (int, write-only): Идентификатор скилла.
    """
    id = IntegerField(write_only=True)

    class Meta:
        model = VacancySkills
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
    author = CustomUserSerializer(read_only=True)
    id = IntegerField(read_only=True)
    required_skills = VacancySkillsSerializer(many=True)
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
            'specialization',
            'schedule',
            'required_education_level',
            'required_skills',
        )

    def to_representation(self, instance: Vacancy) -> Dict:
        """Преобразует ингредиенты в словарь с данными из списка словарей."""
        request = self.context.get('request')
        context = {'request': request}
        return VacancyReadSerializer(instance, context=context).data

    @staticmethod
    def create_vacancy_essentials(vacancy: Vacancy,
                                  skills: List[Dict],
                                  levels,
                                  schedules,
                                  specializations) -> None:
        """Создает связи между вакансией и прочим."""

        # Создание связи между вакансией и грейдами.

        required_skills = []
        for skill in skills:
            try:
                skill_obj = Skill.objects.get(id=skill['id'])
            except Skill.DoesNotExist:
                raise ValidationError(
                    {"skills": f'Скилла с ID {skill["id"]}'
                               f' не существует.'})

            composition = VacancySkills(
                vacancy=vacancy,
                skill=skill_obj,
            )
            required_skills.append(composition)
        VacancySkills.objects.bulk_create(required_skills)

        # Создание связи между вакансией и грейдами.

        education_levels = []
        for level in levels:
            try:
                level_obj = EducationLevel.objects.get(id=level['id'])
            except EducationLevel.DoesNotExist:
                raise ValidationError(
                    {"education_level": f'Грейда с ID {level["id"]}'
                                        f' не существует.'})

            composition = VacancyEducationLevel(
                vacancy=vacancy,
                education_level=level_obj,
            )
            education_levels.append(composition)
        VacancyEducationLevel.objects.bulk_create(education_levels)

        # Создание связи между вакансией и графиками.

        vacancy_schedules = []
        for schedule in schedules:
            try:
                schedule_obj = Schedule.objects.get(id=schedule['id'])
            except Schedule.DoesNotExist:
                raise ValidationError(
                    {"schedule": f'Графика работы с ID {schedule["id"]}'
                                 f' не существует.'})

            composition = VacancySchedule(
                vacancy=vacancy,
                schedule=schedule_obj,
            )
            vacancy_schedules.append(composition)
        VacancySchedule.objects.bulk_create(vacancy_schedules)

        # Создание связи между вакансией и специализациями.

        vacancy_specializations = []
        for specialization in specializations:
            try:
                specialization_obj = Specialization.objects.get(
                    id=specialization['id']
                )
            except Specialization.DoesNotExist:
                raise ValidationError(
                    {"schedule": f'Специализации с ID {specialization["id"]}'
                                 f' не существует.'})

            composition = VacancySpecialization(
                vacancy=vacancy,
                specialization=specialization_obj,
            )
            vacancy_specializations.append(composition)
        VacancySpecialization.objects.bulk_create(vacancy_specializations)

    def create(self, validated_data: Dict) -> Vacancy:
        """Создает новую вакансию в базе данных."""
        print(validated_data)
        required_skills = validated_data.pop('required_skills', [])
        required_education_level = validated_data.pop(
            'required_education_level'
        )
        schedules = validated_data.pop('schedule')
        specializations = validated_data.pop('specialization')

        for skill in required_skills:

            skill = skill['id']
            try:
                Skill.objects.get(id=skill)
            except Skill.DoesNotExist:
                raise ValidationError(
                    {"required_skills": f"Скила с ID {skill} "
                                        f"не существует."})

        for level in required_education_level:
            level = level['id']
            try:
                EducationLevel.objects.get(id=level)
            except EducationLevel.DoesNotExist:
                raise ValidationError(
                    {"required_skills": f"Грейда с ID {level} "
                                        f"не существует."})

        for schedule in schedules:
            schedule = schedule['id']
            try:
                Schedule.objects.get(id=schedule)
            except Schedule.DoesNotExist:
                raise ValidationError(
                    {"required_skills": f"Графика с ID {schedule} "
                                        f"не существует."})

        for specialization in specializations:
            specialization = specialization['id']
            try:
                Specialization.objects.get(id=specialization)
            except Specialization.DoesNotExist:
                raise ValidationError(
                    {"required_skills": f"Специлазиации с ID {specialization} "
                                        f"не существует."})

        vacancy = Vacancy.objects.create(**validated_data)
        self.create_vacancy_essentials(vacancy=vacancy,
                                       skills=required_skills,
                                       levels=required_education_level,
                                       schedules=schedules,
                                       specializations=specializations
                                       )
        return vacancy
