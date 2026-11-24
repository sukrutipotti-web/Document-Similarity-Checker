#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#define MAXW 500
#define WL 64
#define HASH 2053
#define K 3
typedef struct Node { char phrase[200]; struct Node *next; } Node;
static int readfile(const char *p,char *b,int cap){FILE*f=fopen(p,"r");if(!f)return -1;size_t n=fread(b,1,cap-1,f);int bad=ferror(f);b[n]=0;int extra=fgetc(f);fclose(f);return bad||extra!=EOF?-1:(int)n;}
static int tokenize(char*s,char w[MAXW][WL]){int n=0;while(*s){while(*s&&!isalnum((unsigned char)*s))s++;if(!*s||n==MAXW)break;int j=0;while(*s&&isalnum((unsigned char)*s)){if(j<WL-1)w[n][j++]=(char)tolower((unsigned char)*s);s++;}w[n][j]=0;if(j)n++;}return n;}
static unsigned long phash(char w[MAXW][WL],int i){unsigned long h=1469598103934665603UL;for(int k=0;k<K;k++){unsigned char*p=(unsigned char*)w[i+k];while(*p){h^=*p++;h*=1099511628211UL;}h^=255;h*=1099511628211UL;}return h;}
static int eqphrase(char a[MAXW][WL],int i,char b[MAXW][WL],int j){for(int k=0;k<K;k++)if(strcmp(a[i+k],b[j+k]))return 0;return 1;}
static int lcs(char a[MAXW][WL],int n,char b[MAXW][WL],int m){static int d[MAXW+1][MAXW+1];memset(d,0,sizeof(d));for(int i=1;i<=n;i++)for(int j=1;j<=m;j++)d[i][j]=!strcmp(a[i-1],b[j-1])?d[i-1][j-1]+1:(d[i-1][j]>d[i][j-1]?d[i-1][j]:d[i][j-1]);return d[n][m];}
static void jstr(const char*s){putchar('"');for(;*s;s++){if(*s=='"'||*s=='\\')putchar('\\');if(*s=='\n')fputs("\\n",stdout);else if(*s=='\r')fputs("\\r",stdout);else if((unsigned char)*s>=32)putchar(*s);}putchar('"');}
int main(int ac,char**av){if(ac!=3){fprintf(stderr,"Usage: similarity_engine fileA fileB\n");return 2;}char *ta=malloc(32768),*tb=malloc(32768);char a[MAXW][WL],b[MAXW][WL];if(!ta||!tb||readfile(av[1],ta,32768)<0||readfile(av[2],tb,32768)<0){fprintf(stderr,"Could not read input (maximum 32 KB each).\n");free(ta);free(tb);return 3;}int n=tokenize(ta,a),m=tokenize(tb,b),l=lcs(a,n,b,m);double score=n+m?200.0*l/(n+m):100.0;
 typedef struct{unsigned long h;int ix,used;} Entry;static Entry ht[HASH];memset(ht,0,sizeof(ht));for(int i=0;i<=n-K;i++){unsigned long h=phash(a,i),s=h%HASH;while(ht[s].used&&ht[s].h!=h)s=(s+1)%HASH;if(!ht[s].used){ht[s].used=1;ht[s].h=h;ht[s].ix=i;}}
 Node*head=NULL,*tail=NULL;int count=0;for(int j=0;j<=m-K&&count<100;j++){unsigned long h=phash(b,j),s=h%HASH,first=s;while(ht[s].used){if(ht[s].h==h&&eqphrase(a,ht[s].ix,b,j)){char p[200]="";for(int k=0;k<K;k++){if(k)strcat(p," ");strcat(p,b[j+k]);}int dup=0;for(Node*q=head;q;q=q->next)if(!strcmp(q->phrase,p))dup=1;if(!dup){Node*q=calloc(1,sizeof(Node));if(q){strcpy(q->phrase,p);if(!head)head=q;else tail->next=q;tail=q;count++;}}break;}s=(s+1)%HASH;if(s==first)break;}}
 printf("{\"similarity\":%.2f,\"lcs_length\":%d,\"word_count_a\":%d,\"word_count_b\":%d,\"matches\":[",score,l,n,m);int first=1;for(Node*q=head;q;q=q->next){if(!first)putchar(',');jstr(q->phrase);first=0;}puts("]}");while(head){Node*q=head->next;free(head);head=q;}free(ta);free(tb);return 0;}
