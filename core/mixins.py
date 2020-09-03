from core.models import Product
from rest_framework.response import Response
from core.api.serializers import ProductSerializer


class JsonConfigurable:
    config_file = None

    def get_config_file(self):
        return self.config_file


# T prefix -> Threaded
class TSearchByGETMixin:
    scraper_thread_class = None

    def get(self, request, store_name, *args, **kwargs):
        search_text = self.request.query_params['search_text']  # noqa
        scraper_thread_class = self.get_scraper_thread_class()  # noqa

        scraper_thread = scraper_thread_class(search_text)
        scraper_thread.start()  # noqa
        scraper_thread.join()  # noqa

        queryset = Product.objects.filter(name__icontains=search_text, store='{store_name}'.format(
            store_name=store_name.upper()
        ))

        return Response(ProductSerializer(queryset, many=True).data)

    @classmethod
    def get_scraper_thread_class(cls):
        return cls.scraper_thread_class
