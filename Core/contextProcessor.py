from Core.models import FavPicture


def contextFav(request):
    result = FavPicture.objects.all().first()
    return {
        'favicon_32': result
    }
