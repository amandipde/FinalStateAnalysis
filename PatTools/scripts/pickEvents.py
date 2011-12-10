#!/usr/bin/env python

'''

Pick events from different datasets using a special json specifier file.

The json file should have the following format:

{
    "DATASET_ALIAS" : [ [run1, lumi1, evt1], [run2, lumi2, evt] ],
    "ANOTHER_DATASET_ALIAS" : [ [run1, lumi1, evt1], [run2, lumi2, evt] ]
}

The actual dataset corresponding to a dataset alias is mapped in
PatTools.python.datadefs

The resulting edmPickEvents.py calles

Author: Evan K. Friis, UW Madison

'''

import sys
import os
import json
from subprocess import Popen, PIPE, STDOUT
from FinalStateAnalysis.PatTools.datadefs import datadefs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s [json_file]\n")
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        sys.stderr.write("Input file %s does not exist!\n" % filename)
        sys.exit(2)

    file = open(filename, 'r')
    events = json.load(file)

    for dataset, runevts in events.iteritems():
        real_dataset = datadefs[dataset]['datasetpath']
        command = ['edmPickEvents.py']
        command.append('--output=%s' % dataset)
        command.append(real_dataset)
        sys.stderr.write('Picking events for dataset: %s = %s '
                         % (dataset, real_dataset))
        if not runevts:
            sys.stderr.write('==> no events, skipping!\n')
            continue
        else:
            sys.stderr.write('==> picking %i events\n' % len(runevts))
        for item in runevts:
            command.append(':'.join('%i' % x for x in item))
        sys.stderr.write('Running: ' + ' '.join(command) + '\n')
        p = Popen(command, stdout=PIPE, stderr=PIPE)
        stdoutdata, stderrdata = p.communicate()
        sys.stderr.write(stderrdata)
        sys.stdout.write(stdoutdata)