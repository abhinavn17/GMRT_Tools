from casatasks import importgmrt
import argparse
import os
from .main import run_container

def main():
    
    # Create the parser
    parser = argparse.ArgumentParser(description='LTA/FITS to CASA MS conversion')
    parser.add_argument('input', nargs='+', type=str, help='The input LTA/FITS file(s)')
    parser.add_argument('--output', default=None, type=str, help='Name of output MS file (optional)')

    # Parse the arguments

    args = parser.parse_args()

    if len(args.input) == 2:

        print('Running ltamerge on lta and ltb files...')

        lta_name = [name for name in args.input if name.split('.')[-1] == 'lta' or name.split('.')[-2] == 'lta' or name.split('.')[-1] == 'LTA' or name.split('.')[-2] == 'LTA'][0]
        ltb_name = [name for name in args.input if name.split('.')[-1] == 'ltb' or name.split('.')[-2] == 'ltb' or name.split('.')[-1] == 'LTB' or name.split('.')[-2] == 'LTB'][0]

        run_container('ltamerge', ['-i', ltb_name, '-I', lta_name])

        print('ltamerge done!')

        print('Converting to FITS...')

        run_container('listscan', ['ltamerge_out.lta'])

        run_container('gvfits', ['ltamerge_out.log'])

        print('FITS conversion done!')

        print('Converting to MS...')

        if args.output is None:

            output = lta_name.split('.')[0] + '.ms'

        else:

            output = args.output

        if os.path.exists(output):

            os.system('rm -rf ' + output + '*')

        importgmrt(vis=output, fitsfile='TEST.FITS')

        print('MS conversion done!')

        print('Deleting temporary files...')

        os.remove('ltamerge_out.lta')
        os.remove('TEST.FITS')

    elif len(args.input) == 1:

        file = args.input[0]

        if file.split('.')[-1] == 'lta' or file.split('.')[-2] == 'lta' or file.split('.')[-1] == 'LTA' or file.split('.')[-2] == 'LTA':
            
            filename = file.split('.')[0]

            print('Converting to FITS...')

            run_container('listscan', [file])

            run_container('gvfits', [filename + '.log'])    

            print('FITS conversion done!')

            print('Converting to MS...')

            if args.output is None:

                output = filename + '.ms'

            else:

                output = args.output

            if os.path.exists(output):

                os.system('rm -rf ' + output + '*')

            importgmrt(vis=output, fitsfile='TEST.FITS')

            print('MS conversion done!')

            print('Deleting temporary files...')

            os.remove('TEST.FITS')

        elif file.split('.')[-1] == 'fits' or file.split('.')[-2] == 'fits' or file.split('.')[-1] == 'FITS' or file.split('.')[-2] == 'FITS':

            filename = file.split('.')[0]

            print('Converting to MS...')

            if args.output is None:

                output = filename + '.ms'

            else:

                output = args.output

            if os.path.exists(output):

                os.system('rm -rf ' + output + '*')

            importgmrt(vis=output, fitsfile=file)

            print('MS conversion done!')
    
    else:

        print('Invalid number of input files!')
        
    print('Job done!')

if __name__ == '__main__':

    main()