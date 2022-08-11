import os
import matplotlib.pyplot as plt
import numpy as np
import random
import math
import calendar
import matplotlib as mpl
from matplotlib import style

import matplotlib.dates

from datetime import datetime
from datetime import date

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import time

from astral.sun import sun
from astral import Observer

def getECHAIMParams(lat,lon,year,month,day,hour,minute,second):
    import subprocess as subp
    import numpy as np
    #turn off storm and precip and see difference DONE
    #solar miximum years
    #sunset and sunrise on the plot
    #bin by kp index
    #grid plot with # of data points
    #thursday ask about membership with AGU
    #thusday ask about using using madrigal data , PHIL
    storm = 0
    precip = 0
    dregion = 0
    command = ["./echaimpy_ionosonde",str(lat),str(lon),str(year),str(month),str(day),str(hour),str(minute),str(second),str(storm),str(precip),str(dregion)]
    #print(command)
    process = subp.Popen(command, shell=False, stdout=subp.PIPE, stderr=subp.STDOUT)
    output = process.communicate()[0]
    exitCode = process.returncode
    # file1 = open("echaimpyerrors.txt", "r")
    # s = file1.read()
    # #print(s)
    # file1.close()
    #print(output)
    arr = list(map(float,output.split()))

    return np.array(arr)

def getIRI2016Params(lat,lon,yyyy,mmdd,hour):
    import subprocess as subp
    import numpy as np
    #,str(lat),str(lon),str(yyyy),str(mmdd),str(hour)
    fname = 'iripyinputs'
    # with open(fname, 'w') as f:
    #     f.write( "{:8.2f}  Transmitter latitude (degrees N)\n".format( lat ) )
    #     f.write( "{:8.2f}  Transmitter Longitude (degrees E)\n".format( lon ) )
    #     f.write( "{:8d}  Year (yyyy)\n".format( yyyy ) )
    #     f.write( "{:8d}  Month and day (mmdd)\n".format( mmdd ) )
    #     f.write( "{:8.2f}  hour (add 25 for UT) (begin)\n".format( hour + 25 ) )
    #     f.write( "None"+"\n" ) # DaViTpy install path

    command = ["./IRIpyIonosonde",str(lat),str(lon),str(yyyy),str(mmdd),str(hour + 25)]
    #print(command)
    process = subp.Popen(command, shell=False, stdout=subp.PIPE, stderr=subp.STDOUT)
    output = process.communicate()[0]
    exitCode = process.returncode
    arr = list(map(float,output.split()))
    #print(arr)
    return np.array(arr)

def main():
    ec_wins = 0
    ir_wins = 0
    ec_wins_nm = 0
    ir_wins_nm = 0
    with open("/home/texasred/sondrestrom_ionosonde/data") as f:
        for _ in range(23):
            next(f)
        for line in f:
            data = line.split()
            timestamp = data[0]
            cs = float(data[1])
            foF2 = data[2]
            QD_1 = data[3]
            foF1 = data[4]
            QD_2 = data[5]
            hmF2 = data[6]
            QD_3 = data[7]
            hmF1 = data[8]
            QD_4 = data[9]
            year = timestamp[0:4]
            month = timestamp[5:7]
            day = timestamp[8:10]
            hour = timestamp[11:13]
            minute = timestamp[14:16]
            second = timestamp[17:23]
            #print(timestamp)
            #print(year + ' ' + month + ' ' + day + ' ' + hour + ' ' + minute + ' ' + second)
            if (cs >= 80 and foF2 != '---' and foF1 != '---' and hmF2 != '---' and hmF1 != '---' ):
                print(timestamp + ' ' + foF2 + ' ' + foF1 + ' ' + hmF2 + ' ' + hmF1)
                #hmf1_out[0],hmf2_out[0],nmf2_out[0],nmf2storm_out[0]
                pr = getECHAIMParams(66.98,309.06,int(year),int(month),int(day),float(hour),float(minute),float(second))
                #OARR(1) = NMF2/M-3           #OARR(2) = HMF2/KM
                #OARR(3) = NMF1/M-3           #OARR(4) = HMF1/KM
                pr2 = getIRI2016Params(66.98,309.06,int(year),int(month)*100 + int(day),float(hour) + float(minute)/60.0)
                print("E-CHAIM: " + str(pr[1]) + ' ' + str(pr[2]))
                print("IRI: " + str(pr2[1]) + ' ' + str(pr2[0]))
                nmF2 = float(foF2)*float(foF2)*1.24*(10**10)
                print("DATA: " + hmF2 + ' ' + str(nmF2 ) + ' ' + str(cs))
                if (math.fabs(float(hmF2) - pr[1]) > math.fabs(float(hmF2) - pr2[1])):
                    ir_wins = ir_wins + 1
                else:
                    ec_wins = ec_wins + 1

                if (math.fabs(nmF2 - pr[2]) > math.fabs(nmF2 - pr2[0])):
                    ir_wins_nm = ir_wins_nm + 1
                else:
                    ec_wins_nm = ec_wins_nm + 1

    print('ECHAIM: ' + str(ec_wins  ) + ' ' + str(ec_wins_nm))
    print('IRI-2016: ' + str(ir_wins  ) + ' ' + str(ir_wins_nm))


if __name__ == '__main__':
   main()
