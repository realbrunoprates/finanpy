from django.test import SimpleTestCase, override_settings
from django.urls import include, path


def trigger_error(_request):
    raise RuntimeError('Forced error for testing')


urlpatterns = [
    path('force-error/', trigger_error),
    path('', include('core.urls')),
]


@override_settings(
    ROOT_URLCONF='core.tests.test_error_pages',
    DEBUG=False,
)
class TestErrorPages(SimpleTestCase):
    """Verifica se as páginas 404 e 500 customizadas são exibidas."""

    def test_404_template_is_used(self):
        response = self.client.get('/missing-url/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, 'Página não encontrada', status_code=404)

    def test_500_template_is_used(self):
        self.client.raise_request_exception = False
        response = self.client.get('/force-error/')
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')
        self.assertContains(response, 'Erro interno do servidor', status_code=500)
