import argparse
from itertools import product

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to generate a stage file for metamoreph. Be careful, this script also generate z-distance, so it will damage \
        the objective if set too high. The generated pattern will be a AxB grid in CxD wells in 24 well plate, start from coodinate (0,0)")
        
    parser.add_argument("A", type=int, help="Number positions in the x-axis for each well")
    parser.add_argument("B", type=int, help="Number positions in the y-axis for each well")
    parser.add_argument("C", type=int, help="Number wells (24 well plate format) in the x-axis")
    parser.add_argument("D", type=int, help="Number wells (24 well plate format) in the y-axis")

    parser.add_argument("offset", type=float, help='auto-focusing offset in microns')

    parser.add_argument("-z", type=int, default=-400, help="z-distance of the objective in microns")
    parser.add_argument("-i", type=int, default=650., help="Intervals between different positions ")

    parser.add_argument("-n", "--PosName", default='POS', help='Prefix of the position names')

    parser.add_argument("-o", "--Output", type=str, default='./', help="Directory for the output file")

    args = parser.parse_args()

    # Distance between wells in a 24 well plate
    wellDist = 18000

    fileHeader = '\"Stage Memory List\", Version 6.0\n0, 0, 0, 0, 0, 0, 0, \"microns\", \"microns\"\n0\n'
    
    posInterv = args.i
    posNamePref = args.PosName
    zDist = args.z
    offset = args.offset

    with open('{0}GeneratedStage.stg'.format(args.Output), 'w+') as f:
        f.write(fileHeader)
        f.write(str(args.C * args.D * args.A * args.B) + '\n')
        for idx, wellPos in enumerate(product(range(args.C), range(args.D), range(args.A), range(args.B))):
            wellX, wellY, posX, posY = wellPos
            posName = posNamePref + "_well{0:02d}_pos{1:02d}".format(wellX * args.D + wellY, posX * args.B + posY)
            absX = - posX * posInterv - wellX * wellDist
            absY = posY * posInterv + wellY * wellDist

            restString = "FALSE, -9999, TRUE, TRUE, 0, -1, \"\"\n"

            f.write(', '.join([posName, str(absX), str(absY), str(zDist), str(offset), str(zDist), restString]))