from django.db import models
from django.utils import timezone


class BotUser(models.Model):
    chat_id = models.IntegerField()
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    bot_state = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self) -> str:
        return str(self.chat_id)


class CashLink(models.Model):
    class Type(models.IntegerChoices):
        LESS_30 = 1, 'Если выбрано <неважно> или <до 30>'
        GREAT_30 = 2, 'Если выбрано <более 30>'
        LOANS_NOT_RECEIVED = 3, 'Если не получилось взять займы'

    type = models.IntegerField(choices=Type.choices, verbose_name='Тип')
    title = models.CharField(max_length=255, verbose_name='Название')
    url = models.URLField(verbose_name='Ссылка')

    class Meta:
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    user = models.ForeignKey(
        BotUser,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь',
    )
    text = models.CharField(max_length=255, verbose_name='Текст отзыва')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self) -> str:
        return str(self.user)


class UnfulfilledManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            date__lt=timezone.now(),
            done=False,
        )


class TaskManager(models.Model):
    class Type(models.IntegerChoices):
        ASK_FOR_LOANS_1 = 1
        ASK_FOR_LOANS_2 = 2

    tasks = models.Manager()
    unfulfilled = UnfulfilledManager()
    type = models.IntegerField(choices=Type.choices)
    user = models.ForeignKey(to=BotUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f'{self.id}. {self.type}'


class KeyManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Key')


class MessageManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Message')


class SmileManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type='Smile')


class Template(models.Model):
    class Type(models.TextChoices):
        KEY = 'Key', 'Кнопка'
        MESSAGE = 'Message', 'Сообщение'
        SMILE = 'Smile', 'Смайл'

    templates = models.Manager()
    keys = KeyManager()
    messages = MessageManager()
    smiles = SmileManager()

    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10, choices=Type.choices)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)

        keys = Template.keys.all()
        messages = Template.messages.all()
        smiles = Template.smiles.all()
        with open('backend/templates.py', 'w') as file:
            file.write('from .models import Template\n\n')
            file.write('\n')
            file.write('keys = Template.keys.all()\n')
            file.write('messages = Template.messages.all()\n\n')
            file.write('smiles = Template.smiles.all()\n\n')
            file.write('\n')
            file.write('class Keys():\n')
            for index, key in enumerate(keys):
                file.write(f'    {key.title} = keys[{index}].body\n')

            file.write('\n\n')
            file.write('class Messages():\n')
            for index, message in enumerate(messages):
                file.write(f'    {message.title} = messages[{index}].body\n')

            file.write('\n\n')
            file.write('class Smiles():\n')
            for index, smile in enumerate(smiles):
                file.write(f'    {smile.title} = smiles[{index}].body\n')

        return result

    class Meta:
        verbose_name = 'Шаблон'
        verbose_name_plural = 'Шаблоны'

    def format(self, **kwargs):
        return self.body.format(**kwargs)

    def __format__(self, format_spec):
        return format(self.body, format_spec)

    def __str__(self):
        return self.title
