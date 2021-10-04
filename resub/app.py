#
# REsub ds ChRIS plugin app
#
# (c) 2021 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

from chrisapp.base import ChrisApp
import os
import sys
import re
from os import path
from pathlib import Path
from tqdm import tqdm
from glob import iglob

Gstr_title = r"""
______ _____       _____       _     
| ___ \  ___|     /  ___|     | |    
| |_/ / |__ ______\ `--. _   _| |__  
|    /|  __|______|`--. \ | | | '_ \ 
| |\ \| |___      /\__/ / |_| | |_) |
\_| \_\____/      \____/ \__,_|_.__/ 
                            
"""


class Resub(ChrisApp):
    """
    A ChRIS ds plugin for using regular expressions to perform find-and-replace.
    """
    PACKAGE                 = __package__
    TITLE                   = 'Regex Substitution'
    CATEGORY                = 'Format'
    TYPE                    = 'ds'
    ICON                    = ''   # url of an icon image
    MIN_NUMBER_OF_WORKERS   = 1    # Override with the minimum number of workers as int
    MAX_NUMBER_OF_WORKERS   = 1    # Override with the maximum number of workers as int
    MIN_CPU_LIMIT           = 1000 # Override with millicore value as int (1000 millicores == 1 CPU core)
    MIN_MEMORY_LIMIT        = 200  # Override with memory MegaByte (MB) limit as int
    MIN_GPU_LIMIT           = 0    # Override with the minimum number of GPUs as int
    MAX_GPU_LIMIT           = 0    # Override with the maximum number of GPUs as int

    # Use this dictionary structure to provide key-value output descriptive information
    # that may be useful for the next downstream plugin. For example:
    #
    # {
    #   "finalOutputFile":  "final/file.out",
    #   "viewer":           "genericTextViewer",
    # }
    #
    # The above dictionary is saved when plugin is called with a ``--saveoutputmeta``
    # flag. Note also that all file paths are relative to the system specified
    # output directory.
    OUTPUT_META_DICT = {}

    def define_parameters(self):
        # this is a future spec
        # https://github.com/FNNDSC/chrisapp/issues/6
        self.add_argument(
            '-p', '--inputPathFilter',
            dest='inputPathFilter',
            help='selection (glob) for which files to evaluate.',
            default='*',
            type=str,
            optional=True
        )

        self.add_argument(
            '-e', '--expression',
            dest='expr',
            help='regular expression to match, uses Python `re` syntax',
            optional=False,
            type=str
        )

        self.add_argument(
            '-r', '--replacement',
            dest='repl',
            help='what to replace the matches with',
            optional=False,
            type=str
        )

        self.add_argument(
            '-s', '--ifs',
            dest='ifs',
            help='delimiter between chained regexes',
            optional=True,
            default='',
            type=str
        )

    def run(self, options):
        """
        Define the code to be run by this plugin app.
        """
        print(Gstr_title)
        print(f'Version: {self.get_version()}')

        if options.ifs:
            regexs = [re.compile(e) for e in options.expr.split(options.ifs)]
            repls = options.repl.split(options.ifs)
            if len(regexs) != len(repls):
                print(f'Expression count mismatch using --ifs={options.ifs}')
                print(f'Found {len(regexs)} matching expressions in `--expression={options.expr}`')
                print(f'Found {len(repls)} replacement expressions in `--replacement={options.repl}`')
                sys.exit(1)
        else:
            regexs = [re.compile(options.expr)]
            repls = [options.repl]

        # stay in the inputdir as working directory,
        # write to outputdir by absolute paths
        outputdir = Path(options.outputdir).resolve()
        os.chdir(options.inputdir)

        # not the perfect solution for collecting list of files
        # to process, but it's simple and resolves immediately
        # so tqdm can provide a progress bar.

        input_files = [
            fname for fname in iglob(options.inputPathFilter, recursive=True)
            if path.isfile(fname)
        ]

        for fname in tqdm(input_files):
            output_fname = outputdir / fname

            # if files were in subdirectories, we must recreate
            # those subdirectories in the output folder
            parentdir = path.dirname(fname)
            if parentdir:
                os.makedirs(outputdir / parentdir, exist_ok=True)

            # execute regular expression substitution line-by-line
            with open(fname, 'r') as r:
                with output_fname.open('w') as w:
                    for line in r:
                        for regex, repl in zip(regexs, repls):
                            line = regex.sub(repl, line)
                        w.write(line)

    def show_man_page(self):
        self.print_help()
