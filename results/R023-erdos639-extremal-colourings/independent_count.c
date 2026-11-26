#include <stdio.h>
#include <stdint.h>
int main(){for(int n=4;n<=8;n++){int id[8][8],m=0;for(int i=0;i<n;i++)for(int j=i+1;j<n;j++){id[i][j]=id[j][i]=m++;}
 uint32_t T[64];int nt=0;for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++)T[nt++]=(1u<<id[a][b])|(1u<<id[a][c])|(1u<<id[b][c]);
 int best=-1;long long cnt=0,k44=0;uint64_t N=1ull<<m;
 for(uint64_t r=0;r<N;r++){uint32_t cov=0;for(int t=0;t<nt;t++){uint32_t x=r&T[t];if(x==T[t]||x==0)cov|=T[t];}
  int u=m-__builtin_popcount(cov);if(u>best){best=u;cnt=0;k44=0;}
  if(u==best){cnt++;if(n==8&&u==16){uint32_t U=~cov&((1u<<m)-1);int tf=1;for(int t=0;t<nt;t++)if((U&T[t])==T[t]){tf=0;break;}k44+=tf;}}}
 printf("n=%d max_uncovered=%d count=%lld",n,best,cnt);if(n==8)printf(" triangle_free_16edge(=K44 by Mantel)=%lld",k44);printf("\n");}}
