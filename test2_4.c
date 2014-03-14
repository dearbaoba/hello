#include <stdio.h>
#define NUM 3
#define MAN 4
#define SUM 4
#define EMPTY -1
enum
{
    A,
    B,
    C,
    D,
};

int card[20][MAN];
int num;

main()
{
    int i;
    
    //列举所有组合
    num = init();
    
    //找出A知道的组合
    find(B,C);
    //找出所有B和C知道的组合
    while(find(A,C)||find(A,B));
    //剩下的就是A不知道的组合，但如果A自己的全是同一个值，则他可以知道自己的
    for(i=0;i<num;i++)
    {
        if(card[i][A] != EMPTY)
        {
            printf("%d %d %d %d\n",card[i][A],card[i][B],card[i][C],card[i][D]);
        }
    }
}

int init()
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
                        card[number][A] = i;
                        card[number][B] = j;
                        card[number][C] = k;
                        card[number][D] = l;
                        number ++;
                    }
                }
            }
        }
    }
    return number;
}

int find(int n1, int n2)
{
    int i,j;
    int rtn = 0;
    
    for(i=0;i<num;i++)
    {
        for(j=0;j<num;j++)
        {
            //找出唯一的组合，既是知道的
            if(card[i][n1]==card[j][n1]&&card[i][n2]==card[j][n2]&&i!=j)
            {
                break;
            }
        }
        
        if(j == num)
        {
            empty(i);
            rtn = 1;
        }
    }
    
    return rtn;
}

empty(int i)
{
    card[i][A] = EMPTY;
    card[i][B] = EMPTY;
    card[i][C] = EMPTY;
    card[i][D] = EMPTY;
}
