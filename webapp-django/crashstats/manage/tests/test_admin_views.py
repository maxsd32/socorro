import json
import os

import mock
import pytest
import requests_mock

from django.core.urlresolvers import reverse

from crashstats.crashstats.models import GraphicsDevice
from crashstats.crashstats.tests.test_views import BaseTestViews
from crashstats.supersearch.models import (
    SuperSearchFields,
    SuperSearchMissingFields,
)


class SiteAdminTestViews(BaseTestViews):
    def _login(self, is_superuser=True):
        user = super(SiteAdminTestViews, self)._login(
            username='lonnen',
            email='lonnen@example.com',
        )
        user.is_superuser = is_superuser
        user.is_staff = is_superuser
        user.save()
        return user


class TestCrashMeNow(SiteAdminTestViews):
    def test_view(self):
        url = reverse('siteadmin:crash_me_now')
        response = self.client.get(url)
        assert response.status_code == 302

        self._login()
        with pytest.raises(ZeroDivisionError):
            self.client.get(url)


class TestSiteStatus(SiteAdminTestViews):
    @requests_mock.Mocker()
    def test_page_load(self, req_mock):
        """Basic test to make sure the page loads at all"""
        req_mock.get(
            'http://localhost:8000/__version__',
            json={'foo': 'bar'}
        )

        url = reverse('siteadmin:site_status')
        response = self.client.get(url)
        assert response.status_code == 302

        self._login()
        response = self.client.get(url)
        assert response.status_code == 200


class TestAnalyzeModelFetches(SiteAdminTestViews):
    def test_analyze_model_fetches(self):
        """Basic test to make sure the page loads at all"""
        url = reverse('siteadmin:analyze_model_fetches')
        response = self.client.get(url)
        assert response.status_code == 302

        self._login()
        response = self.client.get(url)
        assert response.status_code == 200


class TestSuperSearchFieldsMissing(SiteAdminTestViews):
    def test_supersearch_fields_missing(self):
        url = reverse('siteadmin:supersearch_fields_missing')
        response = self.client.get(url)
        assert response.status_code == 302

        self._login()

        def mocked_supersearchfields(**params):
            return {
                'product': {
                    'name': 'product',
                    'namespace': 'processed_crash',
                    'in_database_name': 'product',
                    'query_type': 'enum',
                    'form_field_choices': None,
                    'permissions_needed': [],
                    'default_value': None,
                    'is_exposed': True,
                    'is_returned': True,
                    'is_mandatory': False,
                }
            }

        def mocked_supersearchfields_get_missing_fields(**params):
            return {
                'hits': [
                    'field_a',
                    'namespace1.field_b',
                    'namespace2.subspace1.field_c',
                ],
                'total': 3
            }

        supersearchfields_mock_get = mock.Mock()
        supersearchfields_mock_get.side_effect = mocked_supersearchfields
        SuperSearchFields.get = supersearchfields_mock_get

        SuperSearchMissingFields.implementation().get.side_effect = (
            mocked_supersearchfields_get_missing_fields
        )

        response = self.client.get(url)
        assert response.status_code == 200
        assert 'field_a' in response.content
        assert 'namespace1.field_b' in response.content
        assert 'namespace2.subspace1.field_c' in response.content


class TestGraphicsDevices(SiteAdminTestViews):
    def test_render_graphics_devices_page(self):
        url = reverse('siteadmin:graphics_devices')
        response = self.client.get(url)
        assert response.status_code == 302
        self._login()
        response = self.client.get(url)
        assert response.status_code == 200

    def test_graphics_devices_lookup(self):
        self._login()
        url = reverse('siteadmin:graphics_devices_lookup')

        GraphicsDevice.objects.create(
            vendor_hex='abc123',
            adapter_hex='xyz123',
            vendor_name='Logictech',
            adapter_name='Webcamera'
        )

        response = self.client.get(url)
        assert response.status_code == 400

        response = self.client.get(url, {
            'vendor_hex': 'abc123',
            'adapter_hex': 'xyz123',
        })
        assert response.status_code == 200
        content = json.loads(response.content)
        assert content['total'] == 1
        expected = {
            'vendor_hex': 'abc123',
            'adapter_hex': 'xyz123',
            'vendor_name': 'Logictech',
            'adapter_name': 'Webcamera'
        }
        assert content['hits'][0] == expected

    def devices_to_list(self, devices):
        """Convert devices to sorted list"""
        devices_list = [
            {
                'vendor_hex': device.vendor_hex,
                'adapter_hex': device.adapter_hex,
                'vendor_name': device.vendor_name,
                'adapter_name': device.adapter_name
            }
            for device in devices
        ]
        devices_list.sort(key=lambda d: (d['vendor_hex'], d['adapter_hex']))
        return devices_list

    def test_graphics_devices_edit(self):
        self._login()
        url = reverse('siteadmin:graphics_devices')

        data = {
            'vendor_hex': 'abc123',
            'adapter_hex': 'xyz123',
            'vendor_name': 'Logictech',
            'adapter_name': 'Webcamera'
        }
        response = self.client.post(url, data)
        assert response.status_code == 302
        assert url in response['location']

        devices = self.devices_to_list(GraphicsDevice.objects.all())
        assert devices == [
            {
                'vendor_hex': 'abc123',
                'adapter_hex': 'xyz123',
                'vendor_name': 'Logictech',
                'adapter_name': 'Webcamera'
            }
        ]

    def test_graphics_devices_csv_upload_pcidatabase_com(self):
        self._login()
        url = reverse('siteadmin:graphics_devices')

        sample_file = os.path.join(os.path.dirname(__file__), 'sample-graphics.csv')
        with open(sample_file) as fp:
            response = self.client.post(url, {
                'file': fp,
                'database': 'pcidatabase.com',
            })
            assert response.status_code == 302
            assert url in response['location']

        devices = self.devices_to_list(GraphicsDevice.objects.all())
        assert devices == [
            {
                'adapter_hex': '0x002f',
                'adapter_name': '.43 ieee 1394 controller',
                'vendor_hex': '0x0033',
                'vendor_name': 'Paradyne Corp.'
            },
            {
                'adapter_hex': '0x0333',
                'adapter_name': (
                    '1ACPI\\GenuineIntel_-_x86_Family_6_Model_23\\_0 '
                    '1ACPI\\GenuineIntel_-_x86_Family_6_Model_23\\_0'
                ),
                'vendor_hex': '0x0033',
                'vendor_name': 'Paradyne Corp.'
            },
            {
                'adapter_hex': '0x08b2',
                'adapter_name': u'123abc logitech QuickCam\ufffd Pro 4000',
                'vendor_hex': '0x0033',
                'vendor_name': 'Paradyne Corp.'
            },
            {
                'adapter_hex': '0x0221',
                'adapter_name': 'LavaPort Quad-650 PCI C/D',
                'vendor_hex': '0x0407',
                'vendor_name': 'Lava Computer MFG Inc.'
            },
            {
                'adapter_hex': '0x0200',
                'adapter_name': 'DS38xx Oregon Scientific',
                'vendor_hex': '0x0553',
                'vendor_name': 'Aiptek USA'
            },
            {
                'adapter_hex': '0x0201',
                'adapter_name': 'DS38xx Oregon Scientific',
                'vendor_hex': '0x0553',
                'vendor_name': 'Aiptek USA'
            },
            {
                'adapter_hex': '0x6128',
                'adapter_name': 'USB\\VID_0C45&PID_6148&REV_0101 USB PC Camera Plus',
                'vendor_hex': '0x0553',
                'vendor_name': 'Aiptek USA'
            }
        ]

    def test_graphics_devices_csv_upload_pci_ids(self):
        self._login()
        url = reverse('siteadmin:graphics_devices')

        sample_file = os.path.join(os.path.dirname(__file__), 'sample-pci.ids')
        with open(sample_file) as fp:
            response = self.client.post(url, {
                'file': fp,
                'database': 'pci.ids',
            })
            assert response.status_code == 302
            assert url in response['location']

        devices = self.devices_to_list(GraphicsDevice.objects.all())
        assert devices == [
            {
                'adapter_hex': '0x8139',
                'adapter_name': 'AT-2500TX V3 Ethernet',
                'vendor_hex': '0x0010',
                'vendor_name': 'Allied Telesis, Inc'
            },
            {
                'adapter_hex': '0x0001',
                'adapter_name': 'PCAN-PCI CAN-Bus controller',
                'vendor_hex': '0x001c',
                'vendor_name': 'PEAK-System Technik GmbH'
            },
            {
                'adapter_hex': '0x001c',
                'adapter_name': '0005  2 Channel CAN Bus SJC1000 (Optically Isolated)',
                'vendor_hex': '0x001c',
                'vendor_name': 'PEAK-System Technik GmbH'
            },
            {
                'adapter_hex': '0x7801',
                'adapter_name': 'WinTV HVR-1800 MCE',
                'vendor_hex': '0x0070',
                'vendor_name': 'Hauppauge computer works Inc.'
            },
            {
                'adapter_hex': '0x0680',
                'adapter_name': 'Ultra ATA/133 IDE RAID CONTROLLER CARD',
                'vendor_hex': '0x0095',
                'vendor_name': 'Silicon Image, Inc. (Wrong ID)'
            }
        ]


class TestDebugView(SiteAdminTestViews):
    def test_view_loads(self):
        """Tests that the page loads--doesn't verify any information"""
        url = reverse('siteadmin:debug_view')
        response = self.client.get(url)
        assert response.status_code == 302

        self._login()
        self.client.get(url)
