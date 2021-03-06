"""
Example of how to import and use the brewblox service
"""

from brewblox_history import influx, query_api, relays, sse
from brewblox_service import brewblox_logger, events, scheduler, service

LOGGER = brewblox_logger(__name__)
OLD_EXCHANGE = 'brewcast'


def create_parser(default_name='history'):
    parser = service.create_parser(default_name=default_name)
    parser.add_argument('--broadcast-exchange',
                        help='Eventbus exchange to which device services broadcast their state. [%(default)s]',
                        default='brewcast.history')
    parser.add_argument('--write-interval',
                        help='Interval (sec) between writing batches of received data to Influx. [%(default)s]',
                        default=5,
                        type=float)
    parser.add_argument('--poll-interval',
                        help='Interval (sec) between queries in live SSE requests. [%(default)s]',
                        default=5,
                        type=float)
    return parser


def main():
    app = service.create_app(parser=create_parser())

    scheduler.setup(app)
    events.setup(app)
    influx.setup(app)
    query_api.setup(app)
    sse.setup(app)
    relays.setup(app)

    relays.subscribe(app,
                     exchange_name=OLD_EXCHANGE,
                     routing='#')
    relays.subscribe(app,
                     exchange_name=app['config']['broadcast_exchange'],
                     routing='#')

    service.furnish(app)
    service.run(app)


if __name__ == '__main__':
    main()
