from django.utils.translation import gettext_lazy as _

import api.guardianApi
import api.newsApi

LANGUAGE_CHOICES = [
    ('ar', _('Arabic')),
    ('de', _('German')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('he', _('Hebrew')),
    ('it', _('Italian')),
    ('nl', _('Dutch')),
    ('no', f"{_('Norwegian Bokmål')} / {_('Norwegian Nynorsk')}"),
    ('pt', _('Portuguese')),
    ('ru', _('Russian')),
    ('sv', _('Swedish')),
    ('zh', f"{_('Simplified Chinese')} / {_('Traditional Chinese')}"),
]

COUNTRIES_CHOICES_NEWS = [('us', _('United States'))]

TITLE = 'title'
DESCRIPTION = 'description'
CONTENT = 'content'

SEARCH_IN_CHOICES = (
    (TITLE, _('Title')),
    (DESCRIPTION, _('Description')),
    (CONTENT, _('Content')),
)

sources_response = api.newsApi.NewsApi().get_sources_list()
SOURCES_CHOICES = [(s['id'], s['name']) for s in sources_response['sources']]

sections = api.guardianApi.GuardianApi().get_sections_list()
SECTIONS_CHOICES = [(s['id'], s['webTitle']) for s in sections['sections']]

BUSINESS = 'business'
ENTERTAINMENT = 'entertainment'
GENERAL = 'general'
HEALTH = 'health'
SPORTS = 'sports'
SCIENCE = 'science'
TECHNOLOGY = 'technology'
CATEGORIES_CHOICES = [
    (BUSINESS, _('Business')),
    (ENTERTAINMENT, _('Entertainment')),
    (GENERAL, _('General')),
    (HEALTH, _('Health')),
    (SPORTS, _('Sports')),
    (SCIENCE, _('Science')),
    (TECHNOLOGY, _('Technology')),
]

RELEVANCY = 'relevancy'
POPULARITY = 'popularity'
PUBLISHED_AT = 'publishedAt'
SORT_BY_CHOICES = [
    (RELEVANCY, _('Relevancy')),
    (POPULARITY, _('Popularity')),
    (PUBLISHED_AT, _('Published_at')),
]

NEWEST = 'newest'
OLDEST = 'oldest'
RELEVANCE = 'relevance'
ORDER_BY_CHOICES = [
    (NEWEST, _('Newest')),
    (OLDEST, _('Oldest')),
    (RELEVANCE, _('Relevance')),
]

COUNTRIES_CHOICES_SOURCES = [
    ('ae', _('United Arab Emirates')),
    ('ar', _('Argentina')),
    ('at', _('Austria')),
    ('au', _('Australia')),
    ('be', _('Belgium')),
    ('bg', _('Bulgaria')),
    ('br', _('Brazil')),
    ('ca', _('Canada')),
    ('ch', _('Switzerland')),
    ('cn', _('China')),
    ('co', _('Colombia')),
    ('cu', _('Cuba')),
    ('cz', _('Czech Republic')),
    ('de', _('Germany')),
    ('eg', _('Egypt')),
    ('fr', _('France')),
    ('gb', _('United Kingdom')),
    ('gr', _('Greece')),
    ('hk', _('Hong Kong')),
    ('hu', _('Hungary')),
    ('id', _('Indonesia')),
    ('ie', _('Ireland')),
    ('il', _('Israel')),
    ('in', _('India')),
    ('it', _('Italy')),
    ('jp', _('Japan')),
    ('kr', _('South Korea')),
    ('lt', _('Lithuania')),
    ('lv', _('Latvia')),
    ('ma', _('Morocco')),
    ('mx', _('Mexico')),
    ('my', _('Malaysia')),
    ('ng', _('Nigeria')),
    ('nl', _('Netherlands')),
    ('no', _('Norway')),
    ('nz', _('New Zealand')),
    ('ph', _('Philippines')),
    ('pl', _('Poland')),
    ('pt', _('Portugal')),
    ('ro', _('Romania')),
    ('rs', _('Serbia')),
    ('ru', _('Russia')),
    ('sa', _('Saudi Arabia')),
    ('se', _('Sweden')),
    ('sg', _('Singapore')),
    ('si', _('Slovenia')),
    ('sk', _('Slovakia')),
    ('th', _('Thailand')),
    ('tr', _('Turkey')),
    ('tw', _('Taiwan')),
    ('ua', _('Ukraine')),
    ('us', _('United States')),
    ('ve', _('Venezuela')),
    ('za', _('South Africa')),
]

NONE_RATING = None
ONE = '1'
TWO = '2'
THREE = '3'
FOUR = '4'
FIVE = '5'

RATING_CHOICES = (
    (NONE_RATING, _('None')),
    (ONE, '1'),
    (TWO, '2'),
    (THREE, '3'),
    (FOUR, '4'),
    (FIVE, '5'),
)
