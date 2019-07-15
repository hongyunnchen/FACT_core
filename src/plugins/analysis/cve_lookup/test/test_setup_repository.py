from collections import namedtuple
from os import remove
from pathlib import Path

import pytest

from ..internal import data_prep as dp
from ..internal import setup_repository as sr
from ..internal.meta import DB, get_meta

QUERIES = get_meta()
PATH_TO_TEST = str(Path(__file__).parent.parent) + '/test/'
YEARTUPLE = namedtuple('years', 'start_year end_year')
YEARS = YEARTUPLE(2016, 2019)

DATABASE_YEARS_INPUT = [2015, 2016, 2017]
OVERLAP_OUTPUT = [2018, 2019]

EXISTS_INPUT = [[''], []]
EXISTS_OUTPUT = [True, False]

EXPECTED_CPE_OUTPUT = [('cpe:2.3:a:\\$0.99_kindle_books_project:\\$0.99_kindle_books:6:*:*:*:*:android:*:*', 'a',
                        '\\$0\\.99_kindle_books_project', '\\$0\\.99_kindle_books', '6', 'ANY', 'ANY', 'ANY', 'ANY', 'android', 'ANY', 'ANY'),
                       ('cpe:2.3:a:1000guess:1000_guess:-:*:*:*:*:*:*:*', 'a', '1000guess', '1000_guess', 'NA',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('cpe:2.3:a:1024cms:1024_cms:0.7:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms', '0\\.7', 'ANY',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('cpe:2.3:a:1024cms:1024_cms:1.2.5:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms', '1\\.2\\.5',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('cpe:2.3:a:1024cms:1024_cms:1.3.1:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms', '1\\.3\\.1',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY')]

EXPECTED_CVE_OUTPUT = [('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_7:-:*:*:*:*:*:*:*', 'o', 'microsoft',
                        'windows_7', 'NA', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_7:-:sp1:x64:*:*:*:*:*', 'o', 'microsoft',
                        'windows_7', 'NA', 'sp1', 'x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_7:-:sp1:x86:*:*:*:*:*', 'o', 'microsoft',
                        'windows_7', 'NA', 'sp1', 'x86', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2003:*:sp2:*:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2003', 'ANY', 'sp2', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:*:sp2:x32:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'ANY', 'sp2', 'x32', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:*:sp2:x64:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'ANY', 'sp2', 'x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:-:sp2:itanium:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'NA', 'sp2', 'itanium', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:r2:*:itanium:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'r2', 'ANY', 'itanium', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:r2:*:x64:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'r2', 'ANY', 'x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:itanium:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'r2', 'sp1', 'itanium', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:x64:*:*:*:*:*', 'o',
                        'microsoft', 'windows_server_2008', 'r2', 'sp1', 'x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_vista:*:sp2:*:*:*:*:*:*', 'o',
                        'microsoft', 'windows_vista', 'ANY', 'sp2', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_vista:*:sp2:x64:*:*:*:*:*', 'o',
                        'microsoft', 'windows_vista', 'ANY', 'sp2', 'x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2012-0001', 2012, 'cpe:2.3:o:microsoft:windows_xp:*:sp2:professional_x64:*:*:*:*:*', 'o',
                        'microsoft', 'windows_xp', 'ANY', 'sp2', 'professional_x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:6:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie', '6',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:7:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie', '7',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:8:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie', '8',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                       ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:9:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie', '9',
                        'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY')]

EXTRACT_CPE_OUTPUT = ['cpe:2.3:a:\\$0.99_kindle_books_project:\\$0.99_kindle_books:6:*:*:*:*:android:*:*',
                      'cpe:2.3:a:1000guess:1000_guess:-:*:*:*:*:*:*:*',
                      'cpe:2.3:a:1024cms:1024_cms:0.7:*:*:*:*:*:*:*', 'cpe:2.3:a:1024cms:1024_cms:1.2.5:*:*:*:*:*:*:*',
                      'cpe:2.3:a:1024cms:1024_cms:1.3.1:*:*:*:*:*:*:*']

EXPECTED_SUM_OUTPUT = [('CVE-2018-20229', 2018, 'GitLab Community and Enterprise Edition before 11.3.14, 11.4.x before '
                                                '11.4.12, and 11.5.x before 11.5.5 allows Directory Traversal.'),
                       ('CVE-2018-8825', 2018, 'Google TensorFlow 1.7 and below is affected by: Buffer Overflow. '
                                               'The impact is: execute arbitrary code (local).')]

EXPECTED_UPDATED_CPE_TABLE = [('cpe:2.3:a:\\$0.99_kindle_books_project:\\$0.99_kindle_books:6:*:*:*:*:android:*:*',
                               'a', '\\$0\\.99_kindle_books_project', '\\$0\\.99_kindle_books', '6', 'ANY', 'ANY',
                               'ANY', 'ANY', 'android', 'ANY', 'ANY'),
                              ('cpe:2.3:a:1000guess:1000_guess:-:*:*:*:*:*:*:*', 'a', '1000guess', '1000_guess', 'NA',
                               'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('cpe:2.3:a:1024cms:1024_cms:0.7:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms', '0\\.7',
                               'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('cpe:2.3:a:1024cms:1024_cms:1.2.5:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms',
                               '1\\.2\\.5', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('cpe:2.3:a:1024cms:1024_cms:1.3.1:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms',
                               '1\\.3\\.1', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('cpe:2.3:a:1024cms:1024_cms:1.4.1:*:*:*:*:*:*:*', 'a', '1024cms', '1024_cms',
                               '1\\.4\\.1', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY')]

EXPECTED_UPDATED_CVE_TABLE = [('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:7:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie',
                               '7', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:9:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie',
                               '9', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:6:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie',
                               '6', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('CVE-2018-0010', 2018, 'cpe:2.3:a:microsoft:ie:8:*:*:*:*:*:*:*', 'a', 'microsoft', 'ie',
                               '8', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('CVE-2018-20229', 2018, 'cpe:2.3:o:microsoft:windows_xp:*:sp3:*:*:*:*:*:*', 'o',
                               'microsoft', 'windows_xp', 'ANY', 'sp3', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('CVE-2018-20229', 2018, 'cpe:2.3:o:microsoft:windows_xp:-:sp2:x64:*:*:*:*:*', 'o',
                               'microsoft', 'windows_xp', 'NA', 'sp2', 'x64', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY'),
                              ('CVE-2018-1136', 2018, 'cpe:2.3:a:moodle:moodle:*:*:*:*:*:*:*:*', 'a', 'moodle',
                               'moodle', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY', 'ANY')]
EXPECTED_UPDATED_SUMMARY_TABLE = [('CVE-2012-0001', 2012, 'The kernel in Microsoft Windows XP SP2, Windows Server '
                                   '2003 SP2, Windows Vista SP2, Windows Server 2008 SP2, R2, and R2 SP1, and Windows 7'
                                   ' Gold and SP1 does not properly load structured exception handling tables, which '
                                   'allows context-dependent attackers to bypass the SafeSEH security feature by '
                                   'leveraging a Visual C++ .NET 2003 application, aka \"Windows Kernel SafeSEH Bypass '
                                   'Vulnerability.\"'),
                                  ('CVE-2018-7576', 2018, 'Google TensorFlow 1.6.x and earlier is affected by: Null '
                                   'Pointer Dereference. The type of exploitation is: context-dependent.'),
                                  ('CVE-2018-8825', 2018, 'Google TensorFlow 1.7 and below is affected by: Buffer '
                                   'Overflow. The impact is: execute arbitrary code (local).')]

EXPECTED_GET_CVE_FEEDS_UPDATE_CONTENT = ['CVE-2012-0001', 'cpe:2.3:o:microsoft:windows_server_2003:*:sp2:*:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:*:sp2:x32:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:r2:*:x64:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_7:-:*:*:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:-:sp2:itanium:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_vista:*:sp2:*:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_7:-:sp1:x86:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_7:-:sp1:x64:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:itanium:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:r2:sp1:x64:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:r2:*:itanium:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_xp:*:sp2:professional_x64:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_server_2008:*:sp2:x64:*:*:*:*:*',
                                         'cpe:2.3:o:microsoft:windows_vista:*:sp2:x64:*:*:*:*:*', 'CVE-2018-0010',
                                         'cpe:2.3:a:microsoft:ie:8:*:*:*:*:*:*:*', 'cpe:2.3:a:microsoft:ie:6:*:*:*:*:*:*:*',
                                         'cpe:2.3:a:microsoft:ie:9:*:*:*:*:*:*:*', 'cpe:2.3:a:microsoft:ie:7:*:*:*:*:*:*:*']


EXPECTED_GET_CVE_SUMMARY_UPDATE_CONTENT = ['CVE-2018-20229', 'CVE-2018-8825',
                                           'GitLab Community and Enterprise Edition before 11.3.14, 11.4.x before '
                                           '11.4.12, and 11.5.x before 11.5.5 allows Directory Traversal.',
                                           'Google TensorFlow 1.7 and below is affected by: Buffer Overflow. '
                                           'The impact is: execute arbitrary code (local).']


@pytest.fixture(scope='session', autouse=True)
def setup() -> None:
    try:
        remove('cve_cpe.db')
    except OSError:
        pass
    cpe_base = dp.setup_cpe_table(dp.extract_cpe(PATH_TO_TEST + 'test_resources/test_cpe_extract.xml'))
    cve_base, summary_base = dp.extract_cve(PATH_TO_TEST + 'test_resources/test_cve_extract.json')
    cve_base, summary_base = dp.setup_cve_feeds_table(cve_list=cve_base), dp.setup_cve_summary_table(summary_list=summary_base)

    with DB(PATH_TO_TEST + 'test_update.db') as db:
        db.table_manager(query=QUERIES['sqlite_queries']['create_cpe_table'].format('cpe_table'))
        db.insert_rows(query=QUERIES['sqlite_queries']['insert_cpe'].format('cpe_table'), input_t=cpe_base)
        db.table_manager(query=QUERIES['sqlite_queries']['create_cve_table'].format('cve_table'))
        db.table_manager(query=QUERIES['sqlite_queries']['create_summary_table'].format('summary_table'))
        db.insert_rows(query=QUERIES['sqlite_queries']['insert_cve'].format('cve_table'), input_t=cve_base)
        db.insert_rows(query=QUERIES['sqlite_queries']['insert_summary'].format('summary_table'), input_t=summary_base)

        db.table_manager(query=QUERIES['sqlite_queries']['test_create_update'].format('outdated'))
        db.table_manager(query=QUERIES['sqlite_queries']['test_create_update'].format('new'))
        db.insert_rows(query=QUERIES['sqlite_queries']['test_insert_cve_id'].format('outdated'), input_t=[('CVE-2018-0001', 2018), ('CVE-2018-0002', 2018)])
        db.insert_rows(query=QUERIES['sqlite_queries']['test_insert_cve_id'].format('new'), input_t=[('CVE-2018-0002', 2018), ('CVE-2018-0003', 2018)])

    yield None
    try:
        remove(PATH_TO_TEST + 'test_update.db')
        remove(PATH_TO_TEST + 'test_import.db')
    except OSError:
        pass


@pytest.fixture(scope='function', autouse=True)
def patch_download(monkeypatch):

    class MockRequests:
        content = b''

    monkeypatch.setattr(dp.ZipFile, '_RealGetContents', lambda *_, **__: None)
    monkeypatch.setattr(dp.requests, 'get', lambda *_, **__: MockRequests)


def test_overlap():
    assert OVERLAP_OUTPUT == sr.overlap(requested_years=YEARS, years_in_cve_database=DATABASE_YEARS_INPUT)


def test_exists(monkeypatch):
    with monkeypatch.context() as monkey:
        monkey.setattr(sr.DATABASE, 'select_query', lambda *_, **__: EXISTS_INPUT[0])
        assert EXISTS_OUTPUT[0] == sr.exists(table_name='')
        monkey.setattr(sr.DATABASE, 'select_query', lambda *_, **__: EXISTS_INPUT[1])
        assert EXISTS_OUTPUT[1] == sr.exists(table_name='')


def test_extract_relevant_feeds():
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
    assert [('CVE-2018-0002', 2018), ('CVE-2018-0003', 2018)] == sr.extract_relevant_feeds(from_table='new', where_table='outdated')


def test_delete_outdated_feeds():
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
    sr.delete_outdated_feeds(delete_outdated_from='outdated', use_for_selection='new')
    assert sr.DATABASE.select_single(query=QUERIES['sqlite_queries']['select_all'].format('outdated'))[0] == 'CVE-2018-0001'


def test_create():
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_import.db')
    sr.create(query='test_create', table_name='test')
    assert sr.DATABASE.select_single(query=QUERIES['sqlite_queries']['exist'].format('test'))[0] == 'test'


def test_insert_into():
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_import.db')
    sr.insert_into(query='test_insert', table_name='test', input_data=[(1, ), (2, )])
    assert [(1, ), (2, )] == list(sr.DATABASE.select_query(query=QUERIES['sqlite_queries']['select_all'].format('test')))


def test_drop_table():
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_import.db')
    sr.drop_table('test')
    assert [] == list(sr.DATABASE.select_query(query=QUERIES['sqlite_queries']['exist'].format('test')))


def test_update_cpe(monkeypatch):
    with monkeypatch.context() as monkey:
        sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/test_cpe_update.xml'])
        sr.update_cpe('')
        EXPECTED_UPDATED_CPE_TABLE.sort()
        actual_cpe_update = list(sr.DATABASE.select_query(query=QUERIES['sqlite_queries']['select_all'].format('cpe_table')))
        actual_cpe_update.sort()
        assert EXPECTED_UPDATED_CPE_TABLE == actual_cpe_update


def test_import_cpe(monkeypatch):
    with monkeypatch.context() as monkey:
        sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_import.db')
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/test_cpe_extract.xml'])
        sr.import_cpe('')
        EXPECTED_CPE_OUTPUT.sort()
        actual_cpe_output = list(sr.DATABASE.select_query(QUERIES['sqlite_queries']['select_all'].format('cpe_table')))
        actual_cpe_output.sort()
        assert EXPECTED_CPE_OUTPUT == actual_cpe_output


def test_get_cpe_content(monkeypatch):
    with monkeypatch.context() as monkey:
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/test_cpe_extract.xml'])
        EXTRACT_CPE_OUTPUT.sort()
        actual_output = sr.get_cpe_content(path=PATH_TO_TEST + 'test_resources/test_cpe_extract.xml')
        actual_output.sort()
        assert EXTRACT_CPE_OUTPUT == actual_output


def test_init_cve_feeds_table():
    pass


def test_init_summaries_table():
    pass


def test_get_cve_import_content(monkeypatch):
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
    with monkeypatch.context() as monkey:
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/test_cve_extract.json'])
        feeds, summary = sr.get_cve_update_content('')
        EXPECTED_GET_CVE_FEEDS_UPDATE_CONTENT.sort()
        feeds.sort()
        EXPECTED_GET_CVE_SUMMARY_UPDATE_CONTENT.sort()
        summary.sort()
        assert EXPECTED_GET_CVE_FEEDS_UPDATE_CONTENT == feeds
        assert EXPECTED_GET_CVE_SUMMARY_UPDATE_CONTENT == summary


def test_get_cve_update_content(monkeypatch):
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
    with monkeypatch.context() as monkey:
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/test_cve_extract.json'])
        feeds, summary = sr.get_cve_update_content('')
        EXPECTED_GET_CVE_FEEDS_UPDATE_CONTENT.sort()
        feeds.sort()
        EXPECTED_GET_CVE_SUMMARY_UPDATE_CONTENT.sort()
        summary.sort()
        assert EXPECTED_GET_CVE_FEEDS_UPDATE_CONTENT == feeds
        assert EXPECTED_GET_CVE_SUMMARY_UPDATE_CONTENT == summary


def test_cve_summaries_can_be_imported():
    assert sr.cve_summaries_can_be_imported(['']) is True
    assert sr.cve_summaries_can_be_imported([]) is False


def test_update_cve_repository(monkeypatch):
    with monkeypatch.context() as monkey:
        sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/nvdcve_test_cve_update.json'])
        sr.update_cve_repository(cve_extract_path='')
        EXPECTED_UPDATED_CVE_TABLE.sort()
        actual_cve_update = list(sr.DATABASE.select_query(QUERIES['sqlite_queries']['select_all'].format('cve_table')))
        actual_cve_update.sort()
        EXPECTED_UPDATED_SUMMARY_TABLE.sort()
        actual_summary_update = list(sr.DATABASE.select_query(QUERIES['sqlite_queries']['select_all'].format('summary_table')))
        actual_summary_update.sort()
        assert EXPECTED_UPDATED_CVE_TABLE == actual_cve_update
        assert EXPECTED_UPDATED_SUMMARY_TABLE == actual_summary_update


def test_update_cve_feeds():
    pass


def test_update_cve_summaries():
    pass


def test_get_years_from_database():
    sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_update.db')
    assert sr.get_years_from_database()[0] == 2018


def test_import_cve(monkeypatch):
    with monkeypatch.context() as monkey:
        sr.DATABASE = sr.DB(PATH_TO_TEST + 'test_import.db')
        monkey.setattr(sr, 'glob', lambda *_, **__: [PATH_TO_TEST + 'test_resources/test_cve_extract.json'])
        sr.import_cve(cve_extract_path='', years=YEARS)
        EXPECTED_CVE_OUTPUT.sort()
        EXPECTED_SUM_OUTPUT.sort()
        actual_cve_output = list(sr.DATABASE.select_query(QUERIES['sqlite_queries']['select_all'].format('cve_table')))
        actual_summary_output = list(sr.DATABASE.select_query(QUERIES['sqlite_queries']['select_all'].format('summary_table')))
        actual_cve_output.sort()
        actual_summary_output.sort()
        assert EXPECTED_CVE_OUTPUT == actual_cve_output
        assert EXPECTED_SUM_OUTPUT == actual_summary_output


def test_set_repository():
    pass


def test_update_repository():
    pass


def test_setup_argparser():
    pass


@pytest.mark.parametrize('specify, years, raising', [(-1, YEARTUPLE(2002, 2019), ValueError), (0, YEARTUPLE(2002, 2019), None),
                                                     (3, YEARS, ValueError), (0, YEARTUPLE(2001, 2019), ValueError),
                                                     (0, YEARTUPLE(2018, 2017), ValueError)])
def test_check_validity_of_arguments(specify, years, raising):
    if raising:
        with pytest.raises(ValueError):
            sr.check_validity_of_arguments(specify=specify, years=years)
    else:
        sr.check_validity_of_arguments(specify=specify, years=years)