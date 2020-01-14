#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Parses crkeng.xml and produces the same XML, only with sources="MD" elements
taken out.
"""

import sys
import xml.etree.ElementTree as ET
from collections import Counter


def get_sources(t):
    raw_sources = t.get("sources")
    if raw_sources is None:
        return

    for t in raw_sources.upper().split():
        yield t


MD = frozenset(["MD"])

if __name__ == "__main__":
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    source_labels = Counter()
    nodes_removed = 0
    nodes_before = len(root)
    str_before = ET.tostring(root)

    for e in root.findall("e"):
        ts = e.findall(".//*[@sources]")
        if len(ts) == 0:
            print >>sys.stderr, "Warning: entry has no <t> elements: " + ET.tostring(e)
            continue

        sources = frozenset(source for t in ts for source in get_sources(t))
        source_labels[sources] += 1

        if sources == MD:
            root.remove(e)
            nodes_removed += 1

    nodes_after = len(root)

    assert nodes_removed > 0
    assert nodes_before > nodes_after
    assert nodes_removed == source_labels[MD]
    assert nodes_after == nodes_before - nodes_removed

    str_after = ET.tostring(root)
    assert len(str_before) > len(str_after)

    assert 'sources="CW"' in str_after
    assert 'sources="MD CW"' in str_after
    print(source_labels)
    print("removed %d nodes" % nodes_removed)

    tree.write("crkeng.modified.xml")
