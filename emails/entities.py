from collections import namedtuple


EmailEntity = namedtuple(
    'Email', ['to', 'to_name', 'from_email', 'from_name', 'subject', 'body']
)
