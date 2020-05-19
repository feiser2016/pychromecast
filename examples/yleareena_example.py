"""
Example on how to use the Yle Areena Controller

"""

import pychromecast
import argparse
from pychromecast.controllers.yleareena import YleAreenaController
from time import sleep

import logging
logger = logging.getLogger(__name__)


# Change to the name of your Chromecast
CAST_NAME = "My Chromecast"

parser = argparse.ArgumentParser(
    description="Example on how to use the Yle Areena Controller.")
parser.add_argument('--show-debug', help='Enable debug log',
                    action='store_true')
parser.add_argument('--cast',
                    help='Name of cast device (default: "%(default)s")',
                    default=CAST_NAME)
parser.add_argument('--program', help='Areena Program ID',
                    default="1-50097921")
parser.add_argument('--audio_language', help='audio_language',
                    default="")
parser.add_argument('--text_language', help='text_language',
                    default="off")
args = parser.parse_args()

if args.show_debug:
    logging.basicConfig(level=logging.DEBUG)


def get_kaltura_id(program_id):
    """
    Dive into the yledl internals and fetch the kaltura player id.
    This can be used with Chromecast
    """
    from yledl.streamfilters import StreamFilters
    from yledl.http import HttpClient
    from yledl.localization import TranslationChooser
    from yledl.extractors import extractor_factory
    from yledl.titleformatter import TitleFormatter

    title_formatter = TitleFormatter()
    language_chooser = TranslationChooser('fin')
    httpclient = HttpClient(None)
    stream_filters = StreamFilters()

    url = 'https://areena.yle.fi/{}'.format(program_id)

    extractor = extractor_factory(url, stream_filters, language_chooser, httpclient)
    pid = extractor.program_id_from_url(url)

    info = extractor.program_info_for_pid(pid, url, title_formatter, None)

    return info.media_id.split('-')[-1]


chromecasts = pychromecast.get_chromecasts()
cast = next(cc for cc in chromecasts if cc.device.friendly_name == args.cast)
print(cast)
cast.wait()
yt = YleAreenaController()
cast.register_handler(yt)
yt.play_areena_media(entry_id=get_kaltura_id(args.program), audio_language=args.audio_language, text_language=args.text_language)
sleep(10)