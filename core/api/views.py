from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from core.api.serializers import ProductSerializer
from core.models import Product

# SCRAPERS
from core.scrapers.Maximum import MaximumStoreScraper
from core.scrapers.badr_group import BadrGroupScraper
from core.scrapers.egypt_laptop import EgyptLaptopScraper
from core.scrapers.high_end import HighEndScraper
from core.scrapers.sigma_computer import SigmaComputerScraper
from core.scrapers.scraper import ScraperThread
from core.scrapers.utils import get_store_config
from core.scrapers.scraper import ScraperThread

from core.mixins import TSearchByGETMixin

from core.tasks import run_scraper
from django.conf import settings


@method_decorator(cache_page(7200), name='get')  # 15 * 60
class ScrapersAPIView(APIView):
    def get(self, request, store_name, *args, **kwargs):
        search_text = self.request.query_params['search_text']

        cf = get_store_config('bg')
        # run_scraper.delay(cf, search_text)
        for store_conf in settings.STORES_CONF.get('configs'):
            scraper_thread = ScraperThread(store_conf, search_text)

        # scraper_thread = ScraperThread(cf, search_text)
        # scraper_thread.start()  # noqa
        # scraper_thread.join()  # noqa

        queryset = Product.objects.filter(name__icontains=search_text, store='{store_name}'.format(
            store_name=store_name.upper()
        ))

        return Response(ProductSerializer(queryset, many=True).data)
#
# @method_decorator(cache_page(7200), name='get')  # 15 * 60
# class BadrGroupAPI(TSearchByGETMixin, APIView):
#     scraper_thread_class = BadrGroupScraper

#
# # @method_decorator(cache_page(7200), name='get') # 15 *60
# class EgyptLaptopAPI(TSearchByGETMixin, APIView):
#     scraper_thread_class = EgyptLaptopScraper
#
#
# # @method_decorator(cache_page(7200), name='get') # 15 *60
# class HighEndAPI(TSearchByGETMixin, APIView):
#     scraper_thread_class = HighEndScraper
#
#
# # @method_decorator(cache_page(7200), name='get')  # 15 *60
# class MaximumStoreAPI(TSearchByGETMixin, APIView):
#     scraper_thread_class = MaximumStoreScraper
#
#
# # @method_decorator(cache_page(7200), name='get') # 15 *60
# class SigmaComputerAPI(TSearchByGETMixin, APIView):
#     scraper_thread_class = SigmaComputerScraper
#
#
# stores_map = {
#     'bg': BadrGroupAPI,
#     'el': EgyptLaptopAPI,
#     'he': HighEndAPI,
#     'mx': MaximumStoreAPI,
#     'spc': SigmaComputerAPI,
# }
#
#
# class StoresHandler(View):
#     """
#     Redirect to the right APIView according to stores/<store_name>/
#     """
#
#     def get(self, request, store_name, *args, **kwargs):
#         return stores_map[store_name.lower()].as_view()(request, store_name.lower(), *args, **kwargs)
