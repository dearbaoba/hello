#include <stdio.h>

#define NUM 3
#define SUM 4
#define NOT -1
#define YES -2

enum
{
    A,
    B,
    C,
};

typedef struct
{
    int a;
    int b;
    int c;
    int d;
    int know;
} T_Man;


main()
{
    T_Man man[20];
    int number = init(man); 
    int sum = 0;  
    
    notknow(man, number, B,C);//A不知
    
    do
    {
        sum = checkSum(man, number);
        notknow(man, number, A,C);//B不知
        notknow(man, number, A,B);//C不知
    }while(sum != checkSum(man, number));
    
    switch(ALastKnow(man, number))
    {
        case 0:
            printf("A know Blue-Blue.\n");
            break;
        case 1:
            printf("A know red-Blue.\n");
            break;
        case 2:
            printf("A know red-red.\n");
            break;
        default:
            printf("A dont know!!\n");
            break;
    }
}

int init(T_Man *pMan)
{
    int i,j,k,l;
    int number = 0;
    
    for(i=0;i<NUM;i++)
    {
        for(j=0;j<NUM;j++)
        {
            for(k=0;k<NUM;k++)
            {
                for(l=0;l<NUM;l++)
                {
                    if(i+j+k+l == SUM)
                    {
                        pMan[number].a = i;
                        pMan[number].b = j;
                        pMan[number].c = k;
                        pMan[number].d = l;
                        pMan[number].know = NOT;
                        number ++;
                    }
                }
            }
        }
    }
    return number;
}

int checkSum(T_Man *pMan, int num)
{
    int i;
    int sum = 0;
    
    for(i=0;i<num;i++)
    {
        if(pMan[i].know == NOT)
        {
            sum++;
        }
    }
    
    return sum;
}

notknow(T_Man *pMan, int num, int n1,int n2)
{
    int i,j;
    int sum = 0;
    
    for(i=0;i<num;i++)
    {
        if(pMan[i].know == NOT)
        {
            int *p1 = (int *)&pMan[i];
            for(j=0;j<num;j++)
            {
                int *p2 = (int *)&pMan[j];
                if(pMan[j].know == NOT)
                {
                    if((*(p1 + n1) == *(p2 + n1))&&(*(p1 + n2) == *(p2 + n2))&&(i!=j))
                    {
                        break;
                    }
                }
            }
            
            if(j == num)
            {
                pMan[i].know = YES;
            }
        }
    }
}

int ALastKnow(T_Man *pMan, int num)
{
    int i;
    int know = NOT;
    
    for(i=0;i<num;i++)
    {
        if(pMan[i].know == NOT)
        {
            printf("%d %d %d %d\n",pMan[i].a,pMan[i].b,pMan[i].c,pMan[i].d);
            if(know == NOT)
            {
                know = pMan[i].a;
            }else if(pMan[i].a != know)
            {
                return NOT;
            }
        }
    }
    
    return know;
}
