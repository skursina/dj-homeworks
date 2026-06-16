from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Scope(models.Model):
    article = models.ForeignKey(
        'Article', 
        on_delete=models.CASCADE, 
        related_name='scopes',
        verbose_name='Статья',
    )

    tag = models.ForeignKey(
        'Tag', 
        on_delete=models.CASCADE, 
        related_name='scopes',
        verbose_name='Тэг',
    )

    is_main = models.BooleanField(
        verbose_name='Основной',
        default=False,
    )

    class Meta:
        verbose_name = 'Тэг статьи'
        verbose_name_plural = 'Тэги статьи'
        ordering = ['-is_main', 'tag__name']
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'tag'], 
                name='unique_article_tag'
                ),
            models.UniqueConstraint(
                fields=['article'],
                condition=models.Q(is_main=True),
                name='unique_main_scope_per_article'),
            ]
    def __str__(self):
        return f'{self.article}: {self.tag}'
        


class Article(models.Model):

    title = models.CharField(max_length=256, verbose_name='Название')
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)

    tags = models.ManyToManyField(
        'Tag', 
        through='Scope', 
        related_name='articles',
        verbose_name='Тэги',
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title
