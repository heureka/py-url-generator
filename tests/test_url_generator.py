import pytest
from pathlib import Path

from url_generator import UrlGenerator, UrlGeneratorException


@pytest.fixture()
def url_generator():
    return UrlGenerator(Path(__file__).parent / 'test.json')


@pytest.mark.parametrize('path,params,expected', [
    ('only_host', {}, 'http://www.example.com'),

    ('very', {}, 'http://www.example.com/very'),
    ('very.deep', {}, 'http://www.example.com/very/deep'),
    ('very.deep.structure', {}, 'http://www.example.com/very/deep/structure'),
    ('very.deep.structure.with', {}, 'http://www.example.com/very/deep/structure/with'),
    ('very.deep.structure.with.advance', {}, 'http://www.example.com/very/deep/structure/with/advance'),
    ('very.deep.structure.with.advance.heredity', {}, 'http://www.example.com/very/deep/structure/with/advance#heredity'),

    ('path_test', {'some_param': 'bla'}, 'http://www.example.com?sp=bla'),
    ('path_test.with_leading_slash', {'some_param': 'bla'}, 'http://www.example.com/alohamora?sp=bla'),
    ('path_test.with_trailing_slash', {'some_param': 'bla'}, 'http://www.example.com/alohamora/?sp=bla'),
    ('path_test.with_trailing_slash', {}, 'http://www.example.com/alohamora/'),
    ('path_test.with_both_slashes', {'some_param': 'bla'}, 'http://www.example.com/alohamora/?sp=bla'),
    ('path_test.with_both_slashes', {}, 'http://www.example.com/alohamora/'),
    ('path_test.slash_only', {'some_param': 'bla'}, 'http://www.example.com/?sp=bla'),
    ('path_test.slash_only', {}, 'http://www.example.com/'),

    ('query_params_test', {}, 'http://www.example.com'),
    ('query_params_test', {'some_query_param': 'v'}, 'http://www.example.com?sqp=v'),
    ('query_params_test', {'some_query_param': 'v', 'some_other_query_param': 10}, 'http://www.example.com?sqp=v&soqp=10'),
    ('query_params_test.without_params', {}, 'http://www.example.com'),
    ('query_params_test.with_overloaded_params', {'another_param': 'omnia'}, 'http://www.example.com?ap=omnia'),

    ('fully_parametric_site', {'host': 'yomama.com', 'port': '666', 'path': 'so/fat'}, 'http://yomama.com:666/so/fat'),
    ('fully_parametric_site.with_param', {'host': 'yomama.com', 'port': '666', 'path': 'so/fat', 'some_query_param': 5}, 'http://yomama.com:666/so/fat?q=5'),
    ('fully_parametric_site.with_param.and_fragment', {'host': 'yomama.com', 'port': '666', 'path': 'so/fat', 'some_query_param': 5, 'fragment': 'hot'}, 'http://yomama.com:666/so/fat?q=5#hot'),

    ('comparative_condition', {'env': 'production', 'lang': 'cz'}, 'http://www.example.com/hledani'),
    ('comparative_condition', {'env': 'production', 'lang': 'cz', 'another': 10}, 'http://www.example.com/another'),
    ('comparative_condition', {'env': 'production', 'lang': 'cz', 'another': 666}, 'http://www.example.com/hledani'),
    ('comparative_condition', {'env': 'production', 'lang': 'pl'}, 'http://www.example.com/sukanie'),
    ('comparative_condition', {'env': 'production'}, 'http://www.example.com'),

    ('comparative_condition', {'env': 'dev', 'lang': 'cz'}, 'http://www.example.dev.czech/hledani'),
    ('comparative_condition', {'env': 'dev', 'lang': 'cz', 'another': 10}, 'http://www.example.dev.czech/another'),
    ('comparative_condition', {'env': 'dev', 'lang': 'cz', 'another': "10"}, 'http://www.example.dev.czech/another'),
    ('comparative_condition', {'env': 'dev', 'lang': 'pl'}, 'http://www.example.dev.czech/sukanie'),
    ('comparative_condition', {'env': 'dev'}, 'http://www.example.dev.czech'),

    ('comparative_condition', {'env': 'local', 'lang': 'cz'}, 'http://localhost/hledani'),
    ('comparative_condition', {'env': 'local', 'lang': 'cz', 'another': 10}, 'http://localhost/another'),
    ('comparative_condition', {'env': 'local', 'lang': 'cz', 'another': "bad"}, 'http://localhost/hledani'),
    ('comparative_condition', {'env': 'local', 'lang': 'pl'}, 'http://localhost/sukanie'),
    ('comparative_condition', {'env': 'local'}, 'http://localhost'),

    ('comparative_condition', {'lang': 'cz'}, 'http://www.noenv.com/hledani'),
    ('comparative_condition', {'lang': 'cz', 'another': 10}, 'http://www.noenv.com/another'),
    ('comparative_condition', {'lang': 'cz', 'another': "1"}, 'http://www.noenv.com/hledani'),
    ('comparative_condition', {'lang': 'pl'}, 'http://www.noenv.com/sukanie'),
    ('comparative_condition', {}, 'http://www.noenv.com'),

    ('comparative_condition.conflictive', {}, 'http://www.noenv.com/outer'),
    ('comparative_condition.conflictive', {'lang': 'pl'}, 'http://www.noenv.com/sukanie'),
    ('comparative_condition.conflictive', {'lang': 'cz'}, 'http://www.noenv.com/inner'),

    ('comparative_condition.conflictive', {'env': 'production'}, 'http://www.example.com/outer'),
    ('comparative_condition.conflictive', {'env': 'production', 'lang': 'pl'}, 'http://www.example.com/sukanie'),
    ('comparative_condition.conflictive', {'env': 'production', 'lang': 'cz'}, 'http://www.example.com/inner'),

    ('comparative_condition.conflictive', {'env': 'dev'}, 'http://www.example.dev.czech/outer'),
    ('comparative_condition.conflictive', {'env': 'dev', 'lang': 'pl'}, 'http://www.example.dev.czech/sukanie'),
    ('comparative_condition.conflictive', {'env': 'dev', 'lang': 'cz'}, 'http://www.example.dev.czech/inner'),
])
def test_get_url(url_generator, path, params, expected):
    actual = url_generator.get_url(path, **params)
    assert expected == actual


def test_constructor_params():
    url_generator = UrlGenerator(Path(__file__).parent / 'test.json', host='example.com', port='666')

    assert 'http://example.com:666/under-construction' == url_generator.get_url('fully_parametric_site', path='under-construction')
    assert 'http://cool.com:666/baby' == url_generator.get_url('fully_parametric_site', host='cool.com', path='baby')

    try:
        url_generator.get_url('fully_parametric_site')
        assert False
    except UrlGeneratorException:
        assert True


def test_invalid_path(url_generator):
    try:
        url_generator.get_url('some.non_existing.path')
        assert False
    except UrlGeneratorException:
        assert True


def test_invalid_scheme(url_generator):
    try:
        url_generator.get_url('invalid_scheme')
        assert False
    except UrlGeneratorException:
        assert True


def test_missing_configuration():
    try:
        UrlGenerator('non/existing/file')
        assert False
    except UrlGeneratorException:
        assert True

