//ECHAIM python wrapper
#include <stdio.h>
#include <stdlib.h>
#include "ECHAIM/ECHAIM.h"
#include "ECHAIM/errorCodes.h"

double* makeAltProfile(double start,double end,int steps)
{
  double* alloc = malloc(sizeof(double)*steps);
  for (size_t i = 0; i < steps; i++) {
    alloc[i] = start + i*((end - start)/500.0);
  }
  return alloc;
}


int main(int argc, char const *argv[]) {
  // float** testvar_re = alloc_2d_array_float(2,2);
  // fortranArrayToC_2D(testvar_re,testvar,2,2);
  // printf("Test %f %f %f %f\n",testvar_re[0][0],testvar_re[0][1],testvar_re[1][0],testvar_re[1][1] );
  // double* lat_d = fortranRealToDouble(lat,1);
  // double* lon_d = fortranRealToDouble(lon,1);
  // double* year_d = fortranRealToDouble(year,1);
  // double* month_d = fortranRealToDouble(month,1);
  // double* day_d = fortranRealToDouble(day,1);
  // double* hour_d = fortranRealToDouble(hour,1);
  // double* min_d = fortranRealToDouble(min,1);
  // double* sec_d = fortranRealToDouble(sec,1);
  //double* alt_d = fortranRealToDouble(alt,*l1);
  int storm,precip,dregion;

  double lat_d,lon_d,year_d,month_d,day_d,hour_d,min_d,sec_d;
  sscanf(argv[1], "%lf", &lat_d);
  sscanf(argv[2], "%lf", &lon_d);
  sscanf(argv[3], "%lf", &year_d);
  sscanf(argv[4], "%lf", &month_d);
  sscanf(argv[5], "%lf", &day_d);
  sscanf(argv[6], "%lf", &hour_d);
  sscanf(argv[7], "%lf", &min_d);
  sscanf(argv[8], "%lf", &sec_d);
  sscanf(argv[9], "%i", &storm);
  sscanf(argv[10], "%i", &precip);
  sscanf(argv[11], "%i", &dregion);

  logErrors(1);

  double * nmf2_out = NmF2(&lat_d, &lon_d, &year_d, &month_d, &day_d, &hour_d, &min_d, &sec_d, 1, 0);

double * nmf2storm_out = NmF2Storm(&lat_d, &lon_d, &year_d, &month_d, &day_d, &hour_d, &min_d, &sec_d, 1, 0);

double * hmf2_out = HmF2(&lat_d, &lon_d, &year_d, &month_d, &day_d, &hour_d, &min_d, &sec_d, 1, 0);

double * hmf1_out = HmF1(&lat_d, &lon_d, &year_d, &month_d, &day_d, &hour_d, &min_d, &sec_d, 1, 0);


  printf("%lf %lf %lf %lf",hmf1_out[0],hmf2_out[0],nmf2_out[0],nmf2storm_out[0] );


  return 0;
}
