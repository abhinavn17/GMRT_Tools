import argparse
import subprocess   
import sys
import glob
import os


def run_container(gtool, args):

    module_dir = os.path.dirname(os.path.realpath(__file__))

    module_dir = module_dir + '/../singularity'

    run_dir = os.getcwd()

    command = ['singularity', 'run', '--bind', run_dir + ':' + run_dir, module_dir + '/gtools.sif', gtool] + args

    try:

        # Run the command
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:

        # Exit
        sys.exit(1)

def main():

    # Create the parser

    module_dir = os.path.dirname(os.path.realpath(__file__))

    gtools_list = glob.glob(module_dir + '/../src/*')

    parser = argparse.ArgumentParser(description='Gtools container working with Singularity')
    parser.add_argument('gtool', type=str, help='The gtool to run', choices=[gtool.split('/')[-1] for gtool in gtools_list])
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Arguments to pass to the gtool')

    # Parse the arguments

    args = parser.parse_args()

    run_container(args.gtool, args.args)

    