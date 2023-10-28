from typing import Dict, List

from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import (ModelSerializer, CharField,
                                        ValidationError)

from shared_info.models import (Schedule, EducationLevel, Course,
                                Specialization, Location)
from students.models import Student, Skill
from users.serializers import CustomUserSerializer
from vacancies.models import (Vacancy, VacancySkills, VacancyEducationLevel,
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


class StudentSerializer(ModelSerializer):
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
    """
    Сериализатор для модели Vacancy.

    Attributes:
        - author (CustomUserSerializer, read-only): Сериализатор для
        автора вакансии.
        - id (IntegerField, read-only): Идентификатор вакансии.
        - required_skills (VacancySkillsSerializer, write-only): Сериализатор
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

        # Создание связи между вакансией и скилами.

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
        for field, value in validated_data.items():
            # Если поле — список, то осуществляем обновление связанных объектов
            if field in ['required_skills', 'schedule',
                         'specialization', 'required_education_level']:

                if field == 'required_skills':
                    new_skills = []
                    for skill in value:
                        skill_id = skill.get('id')
                        try:
                            skill = Skill.objects.get(id=skill_id)
                            new_skills.append(
                                VacancySkills(vacancy=instance,
                                              skill=skill))
                        except Skill.DoesNotExist:
                            raise ValidationError(
                                {"required_skills": f"Скила с ID {skill_id} "
                                                    f"не существует."})
                    instance.required_skills.clear()
                    VacancySkills.objects.bulk_create(new_skills)

                elif field == 'schedule':
                    new_schedules = []
                    for schedule in value:
                        schedule_id = schedule.get('id')
                        try:
                            schedule = Schedule.objects.get(id=schedule_id)
                            new_schedules.append(
                                VacancySchedule(vacancy=instance,
                                                schedule=schedule))
                        except Schedule.DoesNotExist:
                            raise ValidationError(
                                {"schedule": f"Графика с ID {schedule_id} "
                                             f"не существует."})
                    instance.schedule.clear()
                    VacancySchedule.objects.bulk_create(new_schedules)

                elif field == 'specialization':
                    new_specializations = []
                    for specialization in value:
                        specialization_id = specialization.get('id')
                        try:
                            specialization = Specialization.objects.get(
                                id=specialization_id
                            )
                            new_specializations.append(
                                VacancySpecialization(
                                    vacancy=instance,
                                    specialization=specialization
                                )
                            )
                        except Specialization.DoesNotExist:
                            raise ValidationError(
                                {"specialization": f"Специализации с ID "
                                                   f"{specialization_id} "
                                                   f"не существует."})
                    instance.specialization.clear()
                    VacancySpecialization.objects.bulk_create(
                        new_specializations
                    )

                elif field == 'required_education_level':
                    new_education_levels = []
                    for level in value:
                        level_id = level.get('id')
                        try:
                            level = EducationLevel.objects.get(id=level_id)
                            new_education_levels.append(
                                VacancyEducationLevel(
                                    vacancy=instance,
                                    education_level=level
                                )
                            )
                        except EducationLevel.DoesNotExist:
                            raise ValidationError(
                                {"required_education_level": f"Грейда "
                                                             f"с ID "
                                                             f"{level_id} не "
                                                             f"существует."})
                    instance.required_education_level.clear()
                    VacancyEducationLevel.objects.bulk_create(
                        new_education_levels
                    )
            else:
                # Для обычных полей просто обновляем их
                setattr(instance, field, value)

        instance.save()
        return instance


# ----------------------------------------------------------------------------
#                       Students serializers
# ----------------------------------------------------------------------------


class MatchingStudentSerializer(StudentSerializer):
    matching_percentage = SerializerMethodField()

    def get_matching_percentage(self, student):
        # Здесь идёт рассчёт процентного соотношения скиллов
        # из вакансии со скиллами студента и возврат его значения.
        vacancy_id = self.context['vacancy_id']
        vacancy = Vacancy.objects.get(id=vacancy_id)
        required_skills = vacancy.required_skills.all()

        student_skills = student.skills.all()
        common_skills_count = len(set(required_skills) & set(student_skills))
        total_required_skills = len(required_skills)

        if total_required_skills == 0:
            return 0  # Избегаем деления на ноль

        matching_percentage = (
                (common_skills_count / total_required_skills)* 100
        )
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