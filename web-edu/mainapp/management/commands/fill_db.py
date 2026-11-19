import random
import uuid
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from mainapp.models import Question, Answer, Tag, Profile, QuestionLike, AnswerLike

fake = Faker('ru_RU')


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        num_users = ratio
        num_questions = ratio * 10
        num_answers = ratio * 100
        num_tags = ratio
        num_likes = ratio * 200

        batch_size = 50000
        users_to_create = []

        for i in range(num_users):
            username = f"{fake.user_name()}_{uuid.uuid4().hex[:4]}"
            users_to_create.append(User(username=username))

            if i != 0 and i % batch_size == 0:
                User.objects.bulk_create(users_to_create, batch_size=1000)
                users_to_create.clear()
        if users_to_create:
            User.objects.bulk_create(users_to_create, batch_size=1000)

        db_users = list(User.objects.all())

        profiles_to_create = []
        for i, user in enumerate(db_users):
            profiles_to_create.append(Profile(
                user=user,
                bio=fake.text(max_nb_chars=200),
            ))
            if i != 0 and i % batch_size == 0:
                Profile.objects.bulk_create(profiles_to_create, batch_size=1000)
                profiles_to_create.clear()
        if profiles_to_create:
            Profile.objects.bulk_create(profiles_to_create, batch_size=1000)

        tags_to_create = []
        for i in range(num_tags):
            tag_name = fake.word()
            tags_to_create.append(Tag(name=f"{tag_name}_{i}"))

            if i != 0 and i % batch_size == 0:
                Tag.objects.bulk_create(tags_to_create, batch_size=1000)
                tags_to_create.clear()
        if tags_to_create:
            Tag.objects.bulk_create(tags_to_create, batch_size=1000)

        db_tags = list(Tag.objects.all())

        questions_to_create = []
        for i in range(num_questions):
            questions_to_create.append(Question(
                title=fake.sentence(nb_words=10),
                content=fake.paragraph(nb_sentences=random.randint(4, 15)),
                author=random.choice(db_users)
            ))
            if i != 0 and i % batch_size == 0:
                Question.objects.bulk_create(questions_to_create, batch_size=1000)
                questions_to_create.clear()
        if questions_to_create:
            Question.objects.bulk_create(questions_to_create, batch_size=1000)

        db_questions_ids = list(Question.objects.values_list('id', flat=True))

        for question in Question.objects.all().prefetch_related('tags'):
            random_tags = random.sample(db_tags, k=random.randint(1, min(3, len(db_tags))))
            question.tags.set(random_tags)

        answers_to_create = []
        for i in range(num_answers):
            answers_to_create.append(Answer(
                question_id=random.choice(db_questions_ids),
                author=random.choice(db_users),
                content=fake.paragraph(nb_sentences=random.randint(1, 7)),
                is_correct=random.choice([True, False, False, False])
            ))
            if i != 0 and i % batch_size == 0:
                Answer.objects.bulk_create(answers_to_create, batch_size=1000)
                answers_to_create.clear()
        if answers_to_create:
            Answer.objects.bulk_create(answers_to_create, batch_size=1000)

        db_answers_ids = list(Answer.objects.values_list('id', flat=True))

        target_q_likes = num_likes // 2
        target_a_likes = num_likes - target_q_likes

        q_likes_set = set()
        max_q = num_users * len(db_questions_ids)
        target_q_likes = min(target_q_likes, max_q)

        while len(q_likes_set) < target_q_likes:
            q_likes_set.add((random.choice(db_users).id, random.choice(db_questions_ids)))

        QuestionLike.objects.bulk_create(
            [QuestionLike(user_id=u, question_id=q) for u, q in q_likes_set],
            batch_size=1000
        )

        a_likes_set = set()
        max_a = num_users * len(db_answers_ids)
        target_a_likes = min(target_a_likes, max_a)

        while len(a_likes_set) < target_a_likes:
            a_likes_set.add((random.choice(db_users).id, random.choice(db_answers_ids)))

        AnswerLike.objects.bulk_create(
            [AnswerLike(user_id=u, answer_id=a) for u, a in a_likes_set],
            batch_size=1000
        )