import random, string
from django.db import models

# Create your models here.
class Member(models.Model):
    email = models.EmailField()
    qr_token = models.CharField(max_length=16)
    def save(self, *args, **kwargs):
        if self.qr_token is None:
            while True:
                x = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
                if not Member.objects.filter(qr_token=x).exists():
                    self.qr_token = x
                    super(Member, self).save(*args, **kwargs)
                    break
        else:
            super(Member, self).save(*args, **kwargs)