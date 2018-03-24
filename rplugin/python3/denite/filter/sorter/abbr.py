# ============================================================================
# FILE: sorter_abbr.py
# AUTHOR: JINNOUCHI Yasushi <delphinus@remora.cx>
# DESCRIPTION: Simple filter to sort candidates by ascii order of abbr
# License: MIT license
# ============================================================================
from operator import attrgetter
from ..base import Base


class Candidate():

    def __init__(self, orig):
        self.orig = orig

    def __lt__(self, other):
        left = self.orig
        right = other.orig
        if 'action__path' in left:
            return left['action__path'] < right['action__path'] or \
                int(left.get('action__line', 0)) < \
                int(right.get('action__line', 0)) or \
                int(left.get('action__col', 0)) < \
                int(right.get('action__col', 0)) or \
                left.get('action__text', '') < right.get('action__text', '')
        elif 'abbr' in left:
            return left['abbr'] < right['abbr']
        else:
            return left['word'] < right['word']


class Filter(Base):

    def __init__(self, vim):
        super().__init__(vim)

        self.name = 'sorter/abbr'
        self.description = 'sort candidates by ascii order of abbr'

    def filter(self, context):
        candidates = sorted([Candidate(x) for x in context['candidates']])
        return [x.orig for x in candidates]
