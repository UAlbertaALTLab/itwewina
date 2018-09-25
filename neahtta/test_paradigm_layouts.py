# -*- coding: UTF-8 -*-

# Neahttadigisánit — online, inflectional dictionary
# Copyright (C) 2013–2017 University of Tromsø
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from paradigm_layouts import *

def read_layout_file(fname):
    import yaml

    with open(fname, 'r') as F:
        data = F.read()

    opts, _, data = data.partition('--')

    options = yaml.load(opts)

    return (options, data)

def get_layout(lang, lemma):
    """ A test function for developing this, return (parsed_layout, generated_paradigm)
    """
    from neahtta import app

    ps = []
    with app.app_context():

        parads = app.morpholexicon.paradigms
        morph = app.config.morphologies.get(lang, False)

        lookups = app.morpholexicon.lookup(lemma, source_lang=lang, target_lang='nob')

        for node, analyses in lookups:
            if (node is not None) and analyses:
                pp, pt = parads.get_paradigm(lang, node, analyses, return_template=True)
                lp, lt = parads.get_paradigm_layout(lang, node, analyses, debug=True, return_template=True)

                form_tags = [_t.split('+')[1::] for _t in pp.splitlines()]
                _generated, _, _ = morph.generate_to_objs(lemma, form_tags, node, return_raw_data=True)

                ps.append((lp, _generated))

    return ps

def main():

    # fname = sys.argv[1]

    # opts, data = read_layout_file(fname)

    generated_paradigms = get_layout('sme', 'arvit')
    # print generated_paradigms

    for layout, paradigm in generated_paradigms:
        if layout:
            rows = layout.for_paradigm(paradigm).fill_generation()
            for r in rows:
                for value in r:
                    if value.cell.header:
                        print '**' + value.value + '**'
                    else:
                        print ', '.join(value.value)

        else:
            print "no layout found"

    # print generated_paradigms

    # t = parse_table(data, options=opts)

    # filled_table = t.fill_generation(generated_paradigms[0])



if __name__ == "__main__":
    sys.exit(main())

