# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import cgi
import json

from flask import url_for

from udata.core.dataset.factories import (
    DatasetFactory, LicenseFactory, VisibleDatasetFactory
)
from udata.core.reuse.factories import ReuseFactory, VisibleReuseFactory
from udata.core.organization.factories import OrganizationFactory
from udata.core.spatial.factories import GeoZoneFactory, SpatialCoverageFactory
from udata.frontend.markdown import md
from udata.models import Badge, PUBLIC_SERVICE
from udata.settings import Testing
from udata.tests import TestCase, DBTestMixin
from udata.tests.api import APITestCase
from udata.tests.frontend import FrontTestCase
from udata.tests.test_sitemap import SitemapTestCase
from udata.tests.features.territories.test_territories_process import (
    create_geozones_fixtures
)

from .models import (
    DATACONNEXIONS_5_CANDIDATE, DATACONNEXIONS_6_CANDIDATE,
    TERRITORY_DATASETS
)
from .views import DATACONNEXIONS_5_CATEGORIES, DATACONNEXIONS_6_CATEGORIES
from .metrics import PublicServicesMetric


class GouvFrSettings(Testing):
    TEST_WITH_THEME = True
    TEST_WITH_PLUGINS = True
    PLUGINS = ['gouvfr']
    THEME = 'gouvfr'


class GouvFrThemeTest(FrontTestCase):
    '''Ensure themed views render'''
    settings = GouvFrSettings

    def test_render_home(self):
        '''It should render the home page'''
        with self.autoindex():
            for i in range(3):
                org = OrganizationFactory()
                DatasetFactory(organization=org)
                ReuseFactory(organization=org)

        response = self.get(url_for('site.home'))
        self.assert200(response)

    def test_render_home_no_data(self):
        '''It should render the home page without data'''
        response = self.get(url_for('site.home'))
        self.assert200(response)

    def test_render_search(self):
        '''It should render the search page'''
        with self.autoindex():
            for i in range(3):
                org = OrganizationFactory()
                DatasetFactory(organization=org)
                ReuseFactory(organization=org)

        response = self.get(url_for('front.search'))
        self.assert200(response)

    def test_render_search_no_data(self):
        '''It should render the search page without data'''
        response = self.get(url_for('front.search'))
        self.assert200(response)

    def test_render_metrics(self):
        '''It should render the search page'''
        for i in range(3):
            org = OrganizationFactory()
            DatasetFactory(organization=org)
            ReuseFactory(organization=org)
        response = self.get(url_for('site.dashboard'))
        self.assert200(response)

    def test_render_metrics_no_data(self):
        '''It should render the search page without data'''
        response = self.get(url_for('site.dashboard'))
        self.assert200(response)

    def test_render_dataset_page(self):
        '''It should render the dataset page'''
        org = OrganizationFactory()
        dataset = DatasetFactory(organization=org)
        ReuseFactory(organization=org, datasets=[dataset])

        response = self.get(url_for('datasets.show', dataset=dataset))
        self.assert200(response)

    def test_render_organization_page(self):
        '''It should render the organization page'''
        org = OrganizationFactory()
        datasets = [DatasetFactory(organization=org) for _ in range(3)]
        for dataset in datasets:
            ReuseFactory(organization=org, datasets=[dataset])

        response = self.get(url_for('organizations.show', org=org))
        self.assert200(response)

    def test_render_reuse_page(self):
        '''It should render the reuse page'''
        org = OrganizationFactory()
        dataset = DatasetFactory(organization=org)
        reuse = ReuseFactory(organization=org, datasets=[dataset])

        response = self.get(url_for('reuses.show', reuse=reuse))
        self.assert200(response)


class GouvFrMetricsTest(DBTestMixin, TestCase):
    '''Check metrics'''
    settings = GouvFrSettings

    def test_public_services(self):
        ps_badge = Badge(kind=PUBLIC_SERVICE)
        public_services = [
            OrganizationFactory(badges=[ps_badge]) for _ in range(2)
        ]
        for _ in range(3):
            OrganizationFactory()

        self.assertEqual(PublicServicesMetric().get_value(),
                         len(public_services))


class LegacyUrlsTest(FrontTestCase):
    settings = GouvFrSettings

    def create_app(self):
        app = super(LegacyUrlsTest, self).create_app()
        app.config['DEFAULT_LANGUAGE'] = 'en'
        return app

    def test_redirect_datasets(self):
        dataset = DatasetFactory()
        response = self.client.get('/en/dataset/%s/' % dataset.slug)
        self.assertRedirects(
            response, url_for('datasets.show', dataset=dataset))

    def test_redirect_datasets_not_found(self):
        response = self.client.get('/en/DataSet/wtf')
        self.assert404(response)

    def test_redirect_organizations(self):
        org = OrganizationFactory()
        response = self.client.get('/en/organization/%s/' % org.slug)
        self.assertRedirects(response, url_for('organizations.show', org=org))

    def test_redirect_organization_list(self):
        response = self.client.get('/en/organization/')
        self.assertRedirects(response, url_for('organizations.list'))

    def test_redirect_topics(self):
        response = self.client.get('/en/group/societe/')
        self.assertRedirects(
            response, url_for('topics.display', topic='societe'))


class SpecificUrlsTest(FrontTestCase):
    settings = GouvFrSettings

    def test_redevances(self):
        response = self.client.get(url_for('gouvfr.redevances'))
        self.assert200(response)

    def test_faq_home(self):
        response = self.client.get(url_for('gouvfr.faq'))
        self.assert200(response)
        self.assert_template_used('faq/home.html')

    def test_citizen_faq(self):
        response = self.client.get(url_for('gouvfr.faq', section='citizen'))
        self.assert200(response)
        self.assert_template_used('faq/citizen.html')

    def test_producer_faq(self):
        response = self.client.get(url_for('gouvfr.faq', section='producer'))
        self.assert200(response)
        self.assert_template_used('faq/producer.html')

    def test_reuser_faq(self):
        response = self.client.get(url_for('gouvfr.faq', section='reuser'))
        self.assert200(response)
        self.assert_template_used('faq/reuser.html')

    def test_developer_faq(self):
        response = self.client.get(url_for('gouvfr.faq', section='developer'))
        self.assert200(response)
        self.assert_template_used('faq/developer.html')

    def test_credits(self):
        response = self.client.get(url_for('gouvfr.credits'))
        self.assert200(response)


class DataconnexionsTest(FrontTestCase):
    settings = GouvFrSettings

    def test_redirect_to_last_dataconnexions(self):
        response = self.client.get(url_for('gouvfr.dataconnexions'))
        self.assertRedirects(response, url_for('gouvfr.dataconnexions6'))

    def test_render_dataconnexions_5_without_data(self):
        response = self.client.get(url_for('gouvfr.dataconnexions5'))
        self.assert200(response)

    def test_render_dataconnexions_5_with_data(self):
        for tag, label, description in DATACONNEXIONS_5_CATEGORIES:
            badge = Badge(kind=DATACONNEXIONS_5_CANDIDATE)
            VisibleReuseFactory(tags=[tag], badges=[badge])
        response = self.client.get(url_for('gouvfr.dataconnexions5'))
        self.assert200(response)

    def test_render_dataconnexions_6_without_data(self):
        response = self.client.get(url_for('gouvfr.dataconnexions6'))
        self.assert200(response)

    def test_render_dataconnexions_6_with_data(self):
        # Use tags until we are sure all reuse are correctly labeled
        for tag, label, description in DATACONNEXIONS_6_CATEGORIES:
            badge = Badge(kind=DATACONNEXIONS_6_CANDIDATE)
            VisibleReuseFactory(tags=['dataconnexions-6', tag], badges=[badge])
        response = self.client.get(url_for('gouvfr.dataconnexions6'))
        self.assert200(response)


class C3Test(FrontTestCase):
    settings = GouvFrSettings

    def test_redirect_c3(self):
        response = self.client.get(url_for('gouvfr.c3'))
        self.assertRedirects(response, '/en/climate-change-challenge')

    def test_render_c3_without_data(self):
        response = self.client.get(url_for('gouvfr.climate_change_challenge'))
        self.assert200(response)


class TerritoriesSettings(GouvFrSettings):
    ACTIVATE_TERRITORIES = True


class TerritoriesTest(FrontTestCase):
    settings = TerritoriesSettings

    def test_with_gouvfr_town_territory_datasets(self):
        bdr = GeoZoneFactory(
            id='fr/county/13', level='fr/county', name='Bouches-du-Rhône')
        arles = GeoZoneFactory(
            id='fr/town/13004', level='fr/town', parents=[bdr.id],
            name='Arles', code='13004', population=52439)
        response = self.client.get(
            url_for('territories.territory', territory=arles))
        self.assert200(response)
        data = response.data.decode('utf-8')
        self.assertIn(arles.name, data)
        base_datasets = self.get_context_variable('base_datasets')
        self.assertEqual(len(base_datasets), 10)
        for dataset in base_datasets:
            self.assertIn(
                '<div data-udata-territory-id="{dataset.slug}"'.format(
                    dataset=dataset),
                data)
        self.assertIn(bdr.name, data)

    def test_with_gouvfr_county_territory_datasets(self):
        bdr = GeoZoneFactory(
            id='fr/county/13', level='fr/county', name='Bouches-du-Rhône')
        response = self.client.get(
            url_for('territories.territory', territory=bdr))
        self.assert200(response)
        data = response.data.decode('utf-8')
        self.assertIn(bdr.name, data)
        base_datasets = self.get_context_variable('base_datasets')
        self.assertEqual(len(base_datasets), 11)
        for dataset in base_datasets:
            self.assertIn(
                '<div data-udata-territory-id="{dataset.slug}"'.format(
                    dataset=dataset),
                data)

    def test_with_gouvfr_region_territory_datasets(self):
        paca = GeoZoneFactory(
            id='fr/region/93', level='fr/region',
            name='Provence Alpes Côtes dAzur')
        response = self.client.get(
            url_for('territories.territory', territory=paca))
        self.assert200(response)
        data = response.data.decode('utf-8')
        self.assertIn(paca.name, data)
        base_datasets = self.get_context_variable('base_datasets')
        self.assertEqual(len(base_datasets), 8)
        for dataset in base_datasets:
            self.assertIn(
                '<div data-udata-territory-id="{dataset.slug}"'.format(
                    dataset=dataset),
                data)


class OEmbedsTerritoryAPITest(APITestCase):
    settings = TerritoriesSettings

    def test_oembed_town_territory_api_get(self):
        '''It should fetch a town territory in the oembed format.'''
        arles = GeoZoneFactory(
            id='fr/town/13004', level='fr/town',
            name='Arles', code='13004', population=52439)
        licence_ouverte = LicenseFactory(id='fr-lo', title='Licence Ouverte')
        LicenseFactory(id='notspecified', title='Not Specified')
        for territory_dataset_class in TERRITORY_DATASETS['town'].values():
            organization = OrganizationFactory(
                id=territory_dataset_class.organization_id)
            territory = territory_dataset_class(arles)
            reference = 'territory-{id}'.format(id=territory.slug)
            response = self.get(url_for('api.oembeds', references=reference))
            self.assert200(response)
            data = json.loads(response.data)[0]
            self.assertIn('html', data)
            self.assertIn('width', data)
            self.assertIn('maxwidth', data)
            self.assertIn('height', data)
            self.assertIn('maxheight', data)
            self.assertTrue(data['type'], 'rich')
            self.assertTrue(data['version'], '1.0')
            self.assertIn(territory.title, data['html'])
            self.assertIn(cgi.escape(territory.url), data['html'])
            self.assertIn(
                'alt="{name}"'.format(name=organization.name), data['html'])
            self.assertIn(
                md(territory.description, source_tooltip=True), data['html'])
            self.assertIn('Download from localhost', data['html'])
            self.assertIn('Add to your own website', data['html'])
            if territory_dataset_class not in (
                    TERRITORY_DATASETS['town']['comptes_t'],):
                self.assertIn(
                    'License: {title}'.format(title=licence_ouverte.title),
                    data['html'])
                self.assertIn(
                    '© {license_id}'.format(license_id=licence_ouverte.id),
                    data['html'])
                self.assertIn(
                    '<a data-tooltip="Source" href="http://localhost/datasets',
                    data['html'])

    def test_oembed_county_territory_api_get(self):
        '''It should fetch a county territory in the oembed format.'''
        midi_pyrenees = GeoZoneFactory(
            id='fr/region/73', level='fr/region', name='Midi-Pyrénées',
            code='73')
        aveyron = GeoZoneFactory(
            id='fr/county/12', level='fr/county', name='Aveyron', code='12',
            parents=[midi_pyrenees.id])
        licence_ouverte = LicenseFactory(id='fr-lo', title='Licence Ouverte')
        LicenseFactory(id='notspecified', title='Not Specified')
        for territory_dataset_class in TERRITORY_DATASETS['county'].values():
            organization = OrganizationFactory(
                id=territory_dataset_class.organization_id)
            territory = territory_dataset_class(aveyron)
            reference = 'territory-{id}'.format(id=territory.slug)
            response = self.get(url_for('api.oembeds', references=reference))
            self.assert200(response)
            data = json.loads(response.data)[0]
            self.assertIn('html', data)
            self.assertIn('width', data)
            self.assertIn('maxwidth', data)
            self.assertIn('height', data)
            self.assertIn('maxheight', data)
            self.assertTrue(data['type'], 'rich')
            self.assertTrue(data['version'], '1.0')
            self.assertIn(territory.title, data['html'])
            self.assertIn(cgi.escape(territory.url), data['html'])
            self.assertIn(
                'alt="{name}"'.format(name=organization.name), data['html'])
            self.assertIn(
                md(territory.description, source_tooltip=True), data['html'])
            self.assertIn('Download from localhost', data['html'])
            self.assertIn('Add to your own website', data['html'])
            if territory_dataset_class not in (
                    TERRITORY_DATASETS['county']['comptes_c'],
                    TERRITORY_DATASETS['county']['zonages_c']):
                self.assertIn(
                    'License: {title}'.format(title=licence_ouverte.title),
                    data['html'])
                self.assertIn(
                    '© {license_id}'.format(license_id=licence_ouverte.id),
                    data['html'])
                self.assertIn(
                    '<a data-tooltip="Source" href="http://localhost/datasets',
                    data['html'])

    def test_oembed_region_territory_api_get(self):
        '''It should fetch a region territory in the oembed format.'''
        midi_pyrenees = GeoZoneFactory(
            id='fr/region/73', level='fr/region', name='Midi-Pyrénées',
            code='73')
        licence_ouverte = LicenseFactory(id='fr-lo', title='Licence Ouverte')
        LicenseFactory(id='notspecified', title='Not Specified')
        for territory_dataset_class in TERRITORY_DATASETS['region'].values():
            organization = OrganizationFactory(
                id=territory_dataset_class.organization_id)
            territory = territory_dataset_class(midi_pyrenees)
            reference = 'territory-{id}'.format(id=territory.slug)
            response = self.get(url_for('api.oembeds', references=reference))
            self.assert200(response)
            data = json.loads(response.data)[0]
            self.assertIn('html', data)
            self.assertIn('width', data)
            self.assertIn('maxwidth', data)
            self.assertIn('height', data)
            self.assertIn('maxheight', data)
            self.assertTrue(data['type'], 'rich')
            self.assertTrue(data['version'], '1.0')
            self.assertIn(territory.title, data['html'])
            self.assertIn(cgi.escape(territory.url), data['html'])
            self.assertIn(
                'alt="{name}"'.format(name=organization.name), data['html'])
            self.assertIn(
                md(territory.description, source_tooltip=True), data['html'])
            self.assertIn('Download from localhost', data['html'])
            self.assertIn('Add to your own website', data['html'])
            if territory_dataset_class not in (
                    TERRITORY_DATASETS['region']['comptes_r'],
                    TERRITORY_DATASETS['region']['zonages_r']):
                self.assertIn(
                    'License: {title}'.format(title=licence_ouverte.title),
                    data['html'])
                self.assertIn(
                    '© {license_id}'.format(license_id=licence_ouverte.id),
                    data['html'])
                self.assertIn(
                    '<a data-tooltip="Source" href="http://localhost/datasets',
                    data['html'])


class SpatialTerritoriesApiTest(APITestCase):
    settings = TerritoriesSettings

    def test_zone_datasets_with_dynamic_region(self):
        paca, bdr, arles = create_geozones_fixtures()
        with self.autoindex():
            organization = OrganizationFactory()
            for _ in range(3):
                VisibleDatasetFactory(
                    organization=organization,
                    spatial=SpatialCoverageFactory(zones=[paca.id]))

        response = self.get(
            url_for('api.zone_datasets', id=paca.id), qs={'with_dynamic': 1})
        self.assert200(response)
        self.assertEqual(len(response.json), 11)

    def test_zone_datasets_with_dynamic_region_and_size(self):
        paca, bdr, arles = create_geozones_fixtures()
        with self.autoindex():
            organization = OrganizationFactory()
            for _ in range(3):
                VisibleDatasetFactory(
                    organization=organization,
                    spatial=SpatialCoverageFactory(zones=[paca.id]))

        response = self.get(
            url_for('api.zone_datasets', id=paca.id),
            qs={'with_dynamic': 1, 'size': 2})
        self.assert200(response)
        self.assertEqual(len(response.json), 10)

    def test_zone_datasets_without_dynamic_region(self):
        paca, bdr, arles = create_geozones_fixtures()
        with self.autoindex():
            organization = OrganizationFactory()
            for _ in range(3):
                VisibleDatasetFactory(
                    organization=organization,
                    spatial=SpatialCoverageFactory(zones=[paca.id]))

        response = self.get(
            url_for('api.zone_datasets', id=paca.id))
        self.assert200(response)
        self.assertEqual(len(response.json), 3)

    def test_zone_datasets_with_dynamic_county(self):
        paca, bdr, arles = create_geozones_fixtures()
        with self.autoindex():
            organization = OrganizationFactory()
            for _ in range(3):
                VisibleDatasetFactory(
                    organization=organization,
                    spatial=SpatialCoverageFactory(zones=[bdr.id]))

        response = self.get(
            url_for('api.zone_datasets', id=bdr.id), qs={'with_dynamic': 1})
        self.assert200(response)
        self.assertEqual(len(response.json), 14)

    def test_zone_datasets_with_dynamic_town(self):
        paca, bdr, arles = create_geozones_fixtures()
        with self.autoindex():
            organization = OrganizationFactory()
            for _ in range(3):
                VisibleDatasetFactory(
                    organization=organization,
                    spatial=SpatialCoverageFactory(zones=[arles.id]))

        response = self.get(
            url_for('api.zone_datasets', id=arles.id), qs={'with_dynamic': 1})
        self.assert200(response)
        self.assertEqual(len(response.json), 13)


class SitemapTest(FrontTestCase):
    settings = GouvFrSettings

    def test_urls_within_sitemap(self):
        '''It should add gouvfr pages to sitemap.'''
        response = self.get('sitemap.xml')
        self.assert200(response)

        urls = [
            url_for('gouvfr.credits_redirect', _external=True),
            url_for('gouvfr.redevances_redirect', _external=True),
            url_for('gouvfr.faq_redirect', _external=True),
        ]
        for section in ('citizen', 'producer', 'reuser', 'developer'):
            urls.append(url_for('gouvfr.faq_redirect',
                                section='citizen', _external=True))

        for url in urls:
            self.assertIn('<loc>{url}</loc>'.format(url=url), response.data)


class SitemapTerritoriesTest(SitemapTestCase):
    settings = TerritoriesSettings

    def test_towns_within_sitemap(self):
        '''It should return the town from the sitemap.'''
        territory = GeoZoneFactory(
            id='fr/town/13004', name='Arles', code='13004', level='fr/town')

        self.get_sitemap_tree()

        url = self.get_by_url('territories.territory', territory=territory)
        self.assertIsNotNone(url)
        self.assert_url(url, 0.5, 'weekly')

    def test_counties_within_sitemap(self):
        '''It should return the county from the sitemap.'''
        territory = GeoZoneFactory(
            id='fr/county/12', level='fr/county', name='Aveyron', code='12')

        self.get_sitemap_tree()

        url = self.get_by_url('territories.territory', territory=territory)
        self.assertIsNotNone(url)
        self.assert_url(url, 0.5, 'weekly')

    def test_regions_within_sitemap(self):
        '''It should return the county from the sitemap.'''
        territory = GeoZoneFactory(
            id='fr/region/93', level='fr/region',
            name='Provence Alpes Côtes dAzur')

        self.get_sitemap_tree()

        url = self.get_by_url('territories.territory', territory=territory)
        self.assertIsNotNone(url)
        self.assert_url(url, 0.5, 'weekly')
