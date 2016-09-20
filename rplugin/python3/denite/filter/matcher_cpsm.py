# ============================================================================
# FILE: matcher_cpsm.py
# AUTHOR: Shougo Matsushita <Shougo.Matsu at gmail.com>
# License: MIT license
# ============================================================================

from .base import Base
from denite.util import globruntime
import sys
import os


class Filter(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'matcher_cpsm'
        self.description = 'cpsm matcher'

        self.__initialized = False

    def filter(self, context):
        if not context['candidates'] or not context['input']:
            return context['candidates']

        if not self.__initialized:
            # cpsm installation check
            if globruntime(self.vim, 'bin/cpsm_py.so'):
                # Add path
                sys.path.append(os.path.dirname(
                    globruntime(self.vim, 'bin/cpsm_py.so')[0]))
                self.__initialized = True
            else:
                return []

        import cpsm_py
        cpsm_result = cpsm_py.ctrlp_match(
            (d['word'] for d in context['candidates']),
            context['input'],
            ispath=('action__path' in context['candidates'][0]))[0][: 1000]
        return [x for x in context['candidates']
                if x['word'] in cpsm_result]