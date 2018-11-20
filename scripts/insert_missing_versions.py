# flake8: noqa

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This inserts version/build data that's missing from archive.mozilla.org into
# the crashstats_productversion table. This data was in Socorro's
# product_versions/product_version_builds data, extracted, adjusted manually,
# and then put into this fine script.
#
# Generated: November 19th, 2018
# Generator: Will
#
# To use this, run:
#
#     scripts/insert_missing_versions.py
#

import os
import sys

import psycopg2


MISSING_DATA = [
    {'build_id': '20150702113555', 'version_string': '40.0b1rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150702173756', 'version_string': '40.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150706172413', 'version_string': '40.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150709163524', 'version_string': '40.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150713153304', 'version_string': '40.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150720220238', 'version_string': '40.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150723165742', 'version_string': '40.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150727174134', 'version_string': '40.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150730171029', 'version_string': '40.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150803103853', 'version_string': '40.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150804131237', 'version_string': '40.0rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150806104315', 'version_string': '40.0rc3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150806153638', 'version_string': '40.0rc4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150807085045', 'version_string': '40.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0', 'product_name': 'Firefox'},
    {'build_id': '20150811223153', 'version_string': '40.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0.1', 'product_name': 'Firefox'},
    {'build_id': '20150812163655', 'version_string': '40.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0.2', 'product_name': 'Firefox'},
    {'build_id': '20150826023504', 'version_string': '40.0.3', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 40, 'release_version': '40.0.3', 'product_name': 'Firefox'},

    {'build_id': '20150811185633', 'version_string': '41.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150817163452', 'version_string': '41.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150820142145', 'version_string': '41.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150824144923', 'version_string': '41.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150827142634', 'version_string': '41.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150831172306', 'version_string': '41.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150903133607', 'version_string': '41.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150907144446', 'version_string': '41.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150910171927', 'version_string': '41.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150914185908', 'version_string': '41.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150916203902', 'version_string': '41.0rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150917150946', 'version_string': '41.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0', 'product_name': 'Firefox'},
    {'build_id': '20150928151607', 'version_string': '41.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0.1', 'product_name': 'Firefox'},
    {'build_id': '20150929144111', 'version_string': '41.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0.1', 'product_name': 'Firefox'},
    {'build_id': '20151013193107', 'version_string': '41.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0.2', 'product_name': 'Firefox'},
    {'build_id': '20151014143721', 'version_string': '41.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 41, 'release_version': '41.0.2', 'product_name': 'Firefox'},

    {'build_id': '20150921151815', 'version_string': '42.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20150928102225', 'version_string': '42.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151001142456', 'version_string': '42.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151005144425', 'version_string': '42.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151008162217', 'version_string': '42.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151012151721', 'version_string': '42.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151015151621', 'version_string': '42.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151019161651', 'version_string': '42.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151022152545', 'version_string': '42.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151026170526', 'version_string': '42.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},
    {'build_id': '20151029151421', 'version_string': '42.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 42, 'release_version': '42.0', 'product_name': 'Firefox'},

    {'build_id': '20151102024757', 'version_string': '43.0b1rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151103023037', 'version_string': '43.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151109145326', 'version_string': '43.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151112144305', 'version_string': '43.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151116155110', 'version_string': '43.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151119130424', 'version_string': '43.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151123113812', 'version_string': '43.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151126120800', 'version_string': '43.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151201152349', 'version_string': '43.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151203163240', 'version_string': '43.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151208100201', 'version_string': '43.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151208200940', 'version_string': '43.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0', 'product_name': 'Firefox'},
    {'build_id': '20151216175450', 'version_string': '43.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0.1', 'product_name': 'Firefox'},
    {'build_id': '20151221130713', 'version_string': '43.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0.2', 'product_name': 'Firefox'},
    {'build_id': '20151223140742', 'version_string': '43.0.3', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0.3', 'product_name': 'Firefox'},
    {'build_id': '20160104150030', 'version_string': '43.0.4', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0.4', 'product_name': 'Firefox'},
    {'build_id': '20160105164030', 'version_string': '43.0.4', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 43, 'release_version': '43.0.4', 'product_name': 'Firefox'},

    {'build_id': '20151216164151', 'version_string': '44.0b1rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20151217102820', 'version_string': '44.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20151221151411', 'version_string': '44.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20151228134903', 'version_string': '44.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160104162232', 'version_string': '44.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160107144911', 'version_string': '44.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160111185352', 'version_string': '44.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160114165817', 'version_string': '44.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160118143821', 'version_string': '44.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160120154102', 'version_string': '44.0rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160123151951', 'version_string': '44.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0', 'product_name': 'Firefox'},
    {'build_id': '20160204162354', 'version_string': '44.0.1rc1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0.1', 'product_name': 'Firefox'},
    {'build_id': '20160205155049', 'version_string': '44.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0.1', 'product_name': 'Firefox'},
    {'build_id': '20160209150140', 'version_string': '44.0.2rc2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0.2', 'product_name': 'Firefox'},
    {'build_id': '20160210153822', 'version_string': '44.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 44, 'release_version': '44.0.2', 'product_name': 'Firefox'},

    {'build_id': '20160127070712', 'version_string': '45.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160201143558', 'version_string': '45.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160204142810', 'version_string': '45.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160208194709', 'version_string': '45.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160211221018', 'version_string': '45.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160215141016', 'version_string': '45.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160218171844', 'version_string': '45.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160221141421', 'version_string': '45.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160222143322', 'version_string': '45.0b9rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160223142613', 'version_string': '45.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160225145837', 'version_string': '45.0b10', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160301003640', 'version_string': '45.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160303134406', 'version_string': '45.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0', 'product_name': 'Firefox'},
    {'build_id': '20160315153207', 'version_string': '45.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0.1', 'product_name': 'Firefox'},
    {'build_id': '20160407164938', 'version_string': '45.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 45, 'release_version': '45.0.2', 'product_name': 'Firefox'},

    {'build_id': '20160307101827', 'version_string': '46.0b1rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160307215824', 'version_string': '46.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160314144540', 'version_string': '46.0b2rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160316065941', 'version_string': '46.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160321115535', 'version_string': '46.0b4rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160322075646', 'version_string': '46.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160324011246', 'version_string': '46.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160328182534', 'version_string': '46.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160401021843', 'version_string': '46.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160404120533', 'version_string': '46.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160407053945', 'version_string': '46.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160411042519', 'version_string': '46.0b10', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160414152344', 'version_string': '46.0b11', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160418114253', 'version_string': '46.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160420024437', 'version_string': '46.0rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160421124000', 'version_string': '46.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0', 'product_name': 'Firefox'},
    {'build_id': '20160502172042', 'version_string': '46.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 46, 'release_version': '46.0.1', 'product_name': 'Firefox'},

    {'build_id': '20160425095909', 'version_string': '47.0b1rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160425205003', 'version_string': '47.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160502152141', 'version_string': '47.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160505125249', 'version_string': '47.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160509171155', 'version_string': '47.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160512003946', 'version_string': '47.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160516123243', 'version_string': '47.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160518173344', 'version_string': '47.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160523113146', 'version_string': '47.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160526140250', 'version_string': '47.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160531183335', 'version_string': '47.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160602131235', 'version_string': '47.0rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160604131506', 'version_string': '47.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0', 'product_name': 'Firefox'},
    {'build_id': '20160623154057', 'version_string': '47.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0.1', 'product_name': 'Firefox'},
    {'build_id': '20161027172622', 'version_string': '47.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 47, 'release_version': '47.0.2', 'product_name': 'Firefox'},

    {'build_id': '20160606200529', 'version_string': '48.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160620091522', 'version_string': '48.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160623122823', 'version_string': '48.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160627144420', 'version_string': '48.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160630123429', 'version_string': '48.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160706215822', 'version_string': '48.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160711002726', 'version_string': '48.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160714050942', 'version_string': '48.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160718142219', 'version_string': '48.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160721144529', 'version_string': '48.0b10', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160725093659', 'version_string': '48.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160726073904', 'version_string': '48.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0', 'product_name': 'Firefox'},
    {'build_id': '20160816033124', 'version_string': '48.0.1rc1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0.1', 'product_name': 'Firefox'},
    {'build_id': '20160817112116', 'version_string': '48.0.1', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0.1', 'product_name': 'Firefox'},
    {'build_id': '20160823121617', 'version_string': '48.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 48, 'release_version': '48.0.2', 'product_name': 'Firefox'},

    {'build_id': '20160802125802', 'version_string': '49.0b1rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160802125805', 'version_string': '49.0b1rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160802125813', 'version_string': '49.0b1rc3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160802125837', 'version_string': '49.0b1rc4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160802125918', 'version_string': '49.0b1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160808002253', 'version_string': '49.0b2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160811031722', 'version_string': '49.0b3', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160814184416', 'version_string': '49.0b4', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160818050015', 'version_string': '49.0b5', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160822111414', 'version_string': '49.0b6', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160825132718', 'version_string': '49.0b7', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160829102229', 'version_string': '49.0b8', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160901141622', 'version_string': '49.0b9', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160902105049', 'version_string': '49.0b10', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160905130425', 'version_string': '49.0rc1', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160907153016', 'version_string': '49.0rc2', 'release_channel': 'beta', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20160912134115', 'version_string': '49.0', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0', 'product_name': 'Firefox'},
    {'build_id': '20161018030522', 'version_string': '49.0.2', 'release_channel': 'release', 'archive_url': 'manual', 'major_version': 49, 'release_version': '49.0.2', 'product_name': 'Firefox'},
]


def main():
    postgres_dsn = os.environ['DATABASE_URL']
    conn = psycopg2.connect(postgres_dsn)

    sql = """
    INSERT INTO crashstats_productversion
    (product_name, release_channel, major_version, release_version, version_string, build_id, archive_url)
    VALUES
    (%(product_name)s, %(release_channel)s, %(major_version)s, %(release_version)s, %(version_string)s, %(build_id)s, %(archive_url)s)
    """

    total = len(MISSING_DATA)
    inserted = 0

    for item in MISSING_DATA:
        try:
            cursor = conn.cursor()
            cursor.execute(sql, item)
            conn.commit()
            print('inserted: %s' % item)
            inserted += 1
        except psycopg2.IntegrityError:
            conn.rollback()
            print('exists: %s' % item)

    print('Inserted %s out of %s items' % (inserted, total))


if __name__ == '__main__':
    sys.exit(main())
