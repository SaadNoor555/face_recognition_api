from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    return 'media/{0}'.format(filename)


class User(models.Model):
    id              = models.IntegerField(primary_key=True, default=1)
    username        = models.CharField(max_length=50)
    img             = models.ImageField(upload_to=user_directory_path)
    face_encoding   = models.TextField()

    def __str__(self) -> str:
        return str( 'id: ' +self.id+
                    '\nname: '+self.name+
                    '\nImage: '+self.img)