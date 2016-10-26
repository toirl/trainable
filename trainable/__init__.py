from pyramid.config import Configurator
from pyramid.i18n import TranslationStringFactory

from ringo.lib.sql.db import setup_db_session, setup_db_engine
from ringo.model import Base
from ringo.config import setup_modules
from ringo.lib.i18n import translators
from trainable.model import extensions

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = setup_db_engine(settings)
    setup_db_session(engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    # Include basic ringo configuration.
    config.include('ringo')
    config.include('trainable')
    for extension in extensions:
        config.include(extension)
    config.scan()
    return config.make_wsgi_app()

def includeme(config):
    # Now configure the application and optionally overwrite previously
    translators.append(TranslationStringFactory('trainable'))
    config.add_translation_dirs('trainable:locale/')
    config.add_static_view('trainable-static', path='trainable:static',
                           cache_max_age=3600)
    config.add_route("syncstrava", "/strava/sync")
    config.add_route("authstrava", "/strava/authorisation")
