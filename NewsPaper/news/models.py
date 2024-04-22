from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        rating_post_obj = self.post_set.all().aggregate(sum_rating_post=Sum('rating_post'))
        rating_post = rating_post_obj.get('sum_rating_post')

        rating_comment_obj = self.user.comment_set.all().aggregate(sum_rating_comment=Sum('rating_comment'))
        rating_comment = rating_comment_obj.get('sum_rating_comment')

        rating_comment_post_obj = self.post_set.all()
        rsum_comment_post = 0
        for post in rating_comment_post_obj:
            rsum = post.comment_set.all().aggregate(sum_rating_comment=Sum('rating_comment'))
            rsum_comment_post += rsum.get('sum_rating_comment')

        self.rating_author = rating_post * 3 + rating_comment + rsum_comment_post
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)


class Post(models.Model):

    new = 'NE'
    article = 'AR'

    TYPE_POST = [
        (new, 'новость'),
        (article, 'статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type_post = models.CharField(max_length=2,
                                 choices=TYPE_POST,
                                 default='new')
    time_add = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    article_post = models.CharField(max_length=255)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def like(self):
        self.rating_post = self.rating_post + 1
        self.save()

    def dislike(self):
        self.rating_post = self.rating_post - 1
        self.save()

    def preview(self):
        return self.text_post[:125] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    time_add = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment = self.rating_comment + 1
        self.save()

    def dislike(self):
        self.rating_comment = self.rating_comment - 1
        self.save()
