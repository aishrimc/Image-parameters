import numpy as np
from optparse import OptionParser

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC      = '\033[0m'

def Resolution(frequency,diameter):
    res = 1.22*3e8/(frequency*diameter)
    output = np.rad2deg(res)
    return output

def Sensitivity(frequency,num_baselines,source_time,bandwidth,num_polarisation):
    #print(f"{bcolors.UNDERLINE}\nCalculating Sensitivity{bcolors.ENDC}")
    if frequency<=155e6: T_sys = 615; G = 0.33; FF = 10
    elif frequency<=240e6: T_sys = 237; G = 0.33; FF = 5
    elif frequency<=330e6: T_sys = 106; G = 0.32; FF = 2
    elif frequency<=615e6: T_sys = 102; G = 0.32; FF = 2
    elif frequency<=1500e6: T_sys = 73; G = 0.22; FF = 2
    else: 
        print(f'{bcolors.FAIL}{bcolors.BOLD}Please specify frequency between 100MHz to 1.5GHz\n{bcolors.ENDC}')
        exit()
    #
    print(f"{bcolors.OKGREEN}\nNumber of Baslines: {num_baselines}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}BandWidth: {bandwidth:.4} Hz{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}On Source Time: {source_time} minutes{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Stokes: {num_polarisation}{bcolors.ENDC}")
    print(f"{bcolors.WARNING}\nSystem Temberature : {T_sys} K {bcolors.ENDC}")
    print(f"{bcolors.WARNING}Antenna Gain : {G} K Jy-1 Antenna-1{bcolors.ENDC}")
    #
    a = FF*T_sys/G
    b = num_baselines*num_polarisation*bandwidth*source_time*60
    output = a*1.e3/np.sqrt(b)
    return print(f"\nSensitivity : {output:.3f}mJy")

def main():
    parser = OptionParser("usage: %prog [options]")
    parser.add_option('--diameter', dest = 'dishDiameter', help = "Diameter of Single Disk; Default = 45m (GMRT)", default = 45)
    parser.add_option('--baseline', dest = 'maxBaseline', help = "Max basline distance; Default = 25000m (GMRT)", default = 25000)
    parser.add_option('--frequency', dest = 'frequency', help = "Observational/Central Frequency; Default = 150MHz", default='150MHz')
    parser.add_option('--nyquist', dest = 'nyquist', help = "Nyquist Limit; Default = 5", default = 5)
    parser.add_option('--ants', dest = 'numAntennas', help = "Number of Antennas; Default = 30 (GMRT)", default = 30)
    parser.add_option('--bandwidth', dest='bandwidth', help = "Total Bandwidth; Default = 16e6 or 32e6 (GMRT)", default = 16e6)
    parser.add_option('--time', dest='sourceTime', help='Total on-source Time; Default = 500 minutes', default = 500)
    parser.add_option('--stokes', dest='Stokes', help='Number of Polarisation; Default = 2 (GMRT)', default = 2)
    (options,args) = parser.parse_args()

    diameter = float(options.dishDiameter)
    baseline = float(options.maxBaseline)
    nyquist = int(options.nyquist)
    numbaselines = int(options.numAntennas*(options.numAntennas-1)/2)
    bandwidth = float(options.bandwidth)
    time = float(options.sourceTime)
    stokes = int(options.Stokes)

    try:
        frequency = int(options.frequency.rstrip('GHz'))*1.e9
    except:
        frequency = int(options.frequency.rstrip('MHz'))*1.e6

    fov = Resolution(frequency,diameter)
    resolution = Resolution(frequency,baseline)

    print("\n"+"#"*22+" START "+"#"*23)

    print(f"{bcolors.OKGREEN}\nDiameter of a Single Dish: {diameter:.2f}m{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Maximum baseline distance: {baseline:.2f}m{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}The Observation frequency: {frequency:.5} Hz{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Nyquist limit : {nyquist} pixels per beam {bcolors.ENDC}")
    print(f"{bcolors.WARNING}\nThe resolution : {resolution*3600:.2f}arcsec{bcolors.ENDC}")
    print(f"{bcolors.WARNING}The field-of-view : {fov*60:.2f}arcmin{bcolors.ENDC}")
    print(f"\nCell size : {resolution*3600./nyquist:.2f}arcsec")
    print(f"Image size : {fov*nyquist/resolution:4.0f}")

    Sensitivity(frequency,numbaselines,time,bandwidth,stokes)

    print("\n"+"#"*23+" DONE "+"#"*23+"\n")

if __name__ == '__main__':
    main()
