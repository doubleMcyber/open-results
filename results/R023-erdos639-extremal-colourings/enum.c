#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(int argc,char**argv){
  int n=atoi(argv[1]); int E=n*(n-1)/2; int id[10][10]; int k=0;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){id[i][j]=id[j][i]=k++;}
  uint32_t tm[200]; int T=0;
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)
    tm[T++]=(1u<<id[a][b])|(1u<<id[a][c])|(1u<<id[b][c]);
  int best=-1; long cnt=0;
  FILE*f=fopen(argv[2],"w");
  // colour swap symmetry: fix edge 0 colour 0
  for(uint64_t c=0;c<(1ull<<(E-1));c++){
    uint32_t cov=0; uint32_t cc=(uint32_t)c;
    for(int t=0;t<T;t++){uint32_t x=cc&tm[t]; if(x==0||x==tm[t])cov|=tm[t];}
    int unc=E-__builtin_popcount(cov);
    if(unc>best){best=unc;cnt=0; fclose(f); f=fopen(argv[2],"w");}
    if(unc==best){cnt++; fprintf(f,"%u\n",cc);}
  }
  fclose(f);
  printf("n=%d max_uncovered=%d count_with_edge0_fixed=%ld\n",n,best,cnt);
}
