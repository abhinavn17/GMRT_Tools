from casatasks import importgmrt, concat, mstransform
from casatools import table
import argparse
import os
from .main import run_container

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def make_output_name(input_name):
    parts = input_name.split('.')
    parts = [p for p in parts if p != 'lta' and p != 'fits' and p != 'LTA' and p != 'FITS' and p != 'ltb' and p != 'LTB']
    filename = '_'.join(parts)
    output_name = filename + '.ms'
    return output_name

def main():
    
    # Create the parser
    parser = argparse.ArgumentParser(description='LTA/FITS to CASA MS conversion')
    parser.add_argument('input', nargs='+', type=str, help='The input LTA/FITS file(s)')
    parser.add_argument('--output', '-o', default=None, type=str, help='Name of output MS file (optional)')
    parser.add_argument('--max-pol', default=2, type=int, help='Maximum number of polarizations to retain in the output MS (default: 2, i.e., RR and LL)')
    parser.add_argument('--max-chan', default=2**15, type=int, help='Maximum number of channels to retain in the output MS (default: 32768)')
    parser.epilog = 'Example usage: make_ms.py input.lta --output output.ms'

    # Parse the arguments

    args = parser.parse_args()

    if len(args.input) == 2:

        print(f"{bcolors.OKBLUE}Running ltamerge on lta and ltb files...{bcolors.ENDC}")

        lta_name = [name for name in args.input if name.split('.')[-1] == 'lta' or name.split('.')[-2] == 'lta' or name.split('.')[-1] == 'LTA' or name.split('.')[-2] == 'LTA'][0]
        ltb_name = [name for name in args.input if name.split('.')[-1] == 'ltb' or name.split('.')[-2] == 'ltb' or name.split('.')[-1] == 'LTB' or name.split('.')[-2] == 'LTB'][0]

        try:

            run_container('ltamerge', ['-i', ltb_name, '-I', lta_name])
        
        except Exception as e:

            print(f'{bcolors.FAIL}ltamerge failed!{bcolors.ENDC}')

        lta_merge_size = os.path.getsize('ltamerge_out.lta')

        if lta_merge_size < 1000:

            os.remove('ltamerge_out.lta')

            print(f'{bcolors.WARNING}Will run gvfits seperately on lta and ltb files...{bcolors.ENDC}')

            run_container('listscan', [lta_name])

            run_container('gvfits', [lta_name.split('.')[0] + '.log'])

            os.system('mv TEST.FITS TEST1.FITS')

            run_container('listscan', [ltb_name])

            run_container('gvfits', [ltb_name.split('.')[0] + '.log'])

            os.system('mv TEST.FITS TEST2.FITS')

            print(f'{bcolors.OKGREEN}FITS conversion done!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Converting to MS...{bcolors.ENDC}')

            if args.output is None:

                output = make_output_name(lta_name)
            
            else:

                output = args.output

            if os.path.exists(output):

                os.system('rm -rf ' + output + '*')

            output1 = output + '.1'
            output2 = output + '.2'

            importgmrt(vis=output1, fitsfile='TEST1.FITS')
            importgmrt(vis=output2, fitsfile='TEST2.FITS')

            print(f'{bcolors.OKGREEN}MS conversion done!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Combining MS files...{bcolors.ENDC}')

            output_combined = output + '.combined'

            concat(vis=[output1, output2], concatvis=output_combined, timesort=True)

            mstransform(vis=output_combined, outputvis=output, datacolumn='DATA', combinespws=True)

            print(f'{bcolors.OKGREEN}MS files combined!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Deleting temporary files...{bcolors.ENDC}')

            os.remove('TEST1.FITS')
            os.remove('TEST2.FITS')

            os.system('rm -rf ' + output1 + '*')
            os.system('rm -rf ' + output2 + '*')

            os.system('rm -rf ' + output_combined + '*')
            os.system('rm -rf ' + output1 + '*')
            os.system('rm -rf ' + output2 + '*')

        else:

            print(f'{bcolors.OKGREEN}ltamerge successful!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Converting to FITS...{bcolors.ENDC}')

            run_container('listscan', ['ltamerge_out.lta'])

            run_container('gvfits', ['ltamerge_out.log'])

            print(f'{bcolors.OKGREEN}FITS conversion done!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Converting to MS...{bcolors.ENDC}')

            if args.output is None:

                output = make_output_name(lta_name)

            else:

                output = args.output

            if os.path.exists(output):

                os.system('rm -rf ' + output + '*')

            importgmrt(vis=output, fitsfile='TEST.FITS')

            print(f'{bcolors.OKGREEN}MS conversion done!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Deleting temporary files...{bcolors.ENDC}')

            os.remove('ltamerge_out.lta')
            os.remove('TEST.FITS')

    elif len(args.input) == 1:

        file = args.input[0]

        if file.split('.')[-1] == 'lta' or file.split('.')[-2] == 'lta' or file.split('.')[-1] == 'LTA' or file.split('.')[-2] == 'LTA' or file.split('.')[-1] == 'ltb' or file.split('.')[-2] == 'ltb' or file.split('.')[-1] == 'LTB' or file.split('.')[-2] == 'LTB':

            print(f'{bcolors.OKBLUE}Running gvfits on LTA file...{bcolors.ENDC}')

            run_container('listscan', [file])

            run_container('gvfits', [file.split('.')[0] + '.log'])    

            print(f'{bcolors.OKGREEN}FITS conversion done!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Converting to MS...{bcolors.ENDC}')

            if args.output is None:

                output = make_output_name(file)

            else:

                output = args.output

            if os.path.exists(output):

                os.system('rm -rf ' + output + '*')

            importgmrt(vis=output, fitsfile='TEST.FITS')

            print(f'{bcolors.OKGREEN}MS conversion done!{bcolors.ENDC}')

            print(f'{bcolors.OKBLUE}Deleting temporary files...{bcolors.ENDC}')

            os.remove('TEST.FITS')

        elif file.split('.')[-1] == 'fits' or file.split('.')[-2] == 'fits' or file.split('.')[-1] == 'FITS' or file.split('.')[-2] == 'FITS':
        
            print(f'{bcolors.OKBLUE}Converting to MS...{bcolors.ENDC}')

            if args.output is None:

                output = make_output_name(file)

            else:

                output = args.output

            if os.path.exists(output):

                os.system('rm -rf ' + output + '*')

            importgmrt(vis=output, fitsfile=file)

            print(f'{bcolors.OKGREEN}MS conversion done!{bcolors.ENDC}')
    
    else:

        print(f'{bcolors.FAIL}Invalid number of input files!{bcolors.ENDC}')
        
    msfile = output

    spectral_table = table(msfile + '/SPECTRAL_WINDOW', readonly=True)

    nchan = spectral_table.getcol('NUM_CHAN')[0]

    spectral_table.close()

    polarization_table = table(msfile + '/POLARIZATION', readonly=True)

    npol = polarization_table.getcol('NUM_CORR')[0]

    print(f'{bcolors.OKBLUE}Found {nchan} channels and {npol} polarizations in the data...{bcolors.ENDC}')
    
    if npol > args.max_pol and nchan > args.max_chan:

        output_ms = msfile.split('.ms')[0] + '_shrunk.ms'

        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Found {npol} polarizations in the data, averaging data to 4 polarizations...{bcolors.ENDC}')

        mstransform(vis = msfile, outputvis = output_ms, correlation= 'RR,LL', chanaverage=True, chanbin=int(nchan/2048), datacolumn='data')

        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Deleting redundant MS file...{bcolors.ENDC}')

        os.system('rm -rf ' + msfile + '*')

        os.system('mv ' + output_ms + ' ' + msfile)

    elif nchan > args.max_chan:

        output_ms = msfile.split('.ms')[0] + '_shrunk.ms'

        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Found {nchan} channels in the data, averaging data to 2048 channels...{bcolors.ENDC}')

        mstransform(vis = msfile, outputvis = output_ms, chanaverage=True, chanbin=int(nchan/2048), datacolumn='data')

        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Deleting redundant MS file...{bcolors.ENDC}')

        os.system('rm -rf ' + msfile + '*')
    
        os.system('mv ' + output_ms + ' ' + msfile)

    elif npol > args.max_pol:

        output_ms = msfile.split('.ms')[0] + '_polI.ms'

        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Found {npol} polarizations in the data, averaging data to 4 polarizations...{bcolors.ENDC}')

        mstransform(vis = msfile, outputvis = output_ms, correlation= 'RR,LL', datacolumn='data')

        print(f'{bcolors.OKBLUE}{bcolors.BOLD}Deleting redundant MS file...{bcolors.ENDC}')

        os.system('rm -rf ' + msfile + '*')

        os.system('mv ' + output_ms + ' ' + msfile)

    print(f'{bcolors.OKBLUE}Final MS file: {msfile}{bcolors.ENDC}')

    print(f'{bcolors.OKGREEN}{bcolors.BOLD}All done!{bcolors.ENDC}')
    
if __name__ == '__main__':

    main()