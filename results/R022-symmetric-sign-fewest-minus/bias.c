#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int sing(int n,int64_t a[8][8]){
  int64_t m[8][8];for(int i=0;i<n;i++)for(int j=0;j<n;j++)m[i][j]=a[i][j];
  int64_t prev=1;
  for(int k=0;k<n-1;k++){
    if(m[k][k]==0){int r=-1;for(int i=k+1;i<n;i++)if(m[i][k]){r=i;break;}
      if(r<0)return 1; for(int j=0;j<n;j++){int64_t t=m[k][j];m[k][j]=m[r][j];m[r][j]=t;}}
    for(int i=k+1;i<n;i++)for(int j=k+1;j<n;j++) m[i][j]=(m[i][j]*m[k][k]-m[i][k]*m[k][j])/prev;
    prev=m[k][k];
  }
  return m[n-1][n-1]==0;
}
int main(int c,char**v){int n=atoi(v[1]);int f=0;int pos[40][2];
  for(int i=0;i<n;i++)for(int j=i;j<n;j++){pos[f][0]=i;pos[f][1]=j;f++;}
  uint64_t tot=1ULL<<f;static uint64_t h[40];int64_t a[8][8];
  for(uint64_t b=0;b<tot;b++){
    for(int t=0;t<f;t++){int64_t x=((b>>t)&1)?-1:1;a[pos[t][0]][pos[t][1]]=x;a[pos[t][1]][pos[t][0]]=x;}
    if(sing(n,a))h[__builtin_popcountll(b)]++;}
  printf("n=%d k(minus count in upper triangle incl diag): singular count\n",n);
  for(int k=0;k<=f;k++)printf("%d %llu\n",k,(unsigned long long)h[k]);
}
