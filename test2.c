#include <stdio.h>

#define TOP 2
#define SUM 4
#define NOT_MATCH -1
#define NOT_KNEW -1
/*
**假设红牌值1，蓝牌值0，则每个人分到的牌值总和不会超过TOP，所有牌总和为SUM。
**比如：某人分到(红红)，值2；（蓝蓝）值0；（红蓝）值1。只有这三种情况。
**某人是否知道自己的牌前提是：看到的另两人的牌后，剩余自己和D的牌所有组合中，值相等且只能是一个值。
*/

main()
{
    int A,B,C,D;
    int ALastKnow = NOT_MATCH;
    
    for(A=0;A<=TOP;A++)
        for(B=0;B<=TOP;B++)
            for(C=0;C<=TOP;C++)
                for(D=0;D<=TOP;D++)
                    if(stdMatch(A,B,C,D))
                        if(AKnew(B,C) == NOT_KNEW)//A不知道
                            if(BKnew(A,C) == NOT_KNEW)//B不知道
                                if(CKnew(A,B) == NOT_KNEW)//C不知道
                                    if(ALastKnow == NOT_MATCH)
                                        ALastKnow = A;
                                    else
                                        if(ALastKnow != A)
                                        {
                                            printf("A dont know!!\n");
                                            return; 
                                        }
    switch(ALastKnow)//A最后知道了
    {
        case 0:
            printf("A know Blue-Blue.\n");
            break;
        case 1:
            printf("A know Red-Blue.\n");
            break;
        case 2:
            printf("A know Red-Red.\n");
            break;
        default:
            printf("A dont know!!\n");
            break;
    }
}

int stdMatch(int a,int b,int c, int d)
{
    return ((a+b+c+d) == SUM);
}

int AKnew(int b, int c)
{
    int rtn = NOT_MATCH;
    int a,d;
    
    for(a=0;a<=TOP;a++)
    {
        d = a;
        if(stdMatch(a,b,c,d))
            if(rtn == NOT_MATCH)
                rtn = a;
            else
                if(rtn != a)
                    return NOT_KNEW;
    }

    return rtn;
}

int BKnew(int a, int c)
{
    int rtn = NOT_MATCH;
    int b,d;

    for(b=0;b<=TOP;b++)
    {
        d = b;
        if(stdMatch(a,b,c,d))
            if(AKnew(b,c) == NOT_KNEW)
                if(rtn == NOT_MATCH)
                    rtn = b;
                else
                    if(rtn != b)
                        return NOT_KNEW;
    }

    return rtn;
}

int CKnew(int a,int b)
{
    int rtn = NOT_MATCH;
    int c,d;

    for(c=0;c<=TOP;c++)
    {
        d = c;
        if(stdMatch(a,b,c,d))
            if(AKnew(b,c) == NOT_KNEW)
                if(BKnew(a,c) == NOT_KNEW)
                    if(rtn == NOT_MATCH)
                        rtn = c;
                    else
                        if(rtn != c)
                            return NOT_KNEW;
    }

    return rtn;
}


