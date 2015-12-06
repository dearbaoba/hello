#include <stdio.h>

main()
{
    int arr[] = {1,-2,3,10,-4,7,2,-5};
    #define LENGTH 8
    int i;
    int totle = arr[0];
    int tminN = arr[0];
    int tmaxN = arr[0];
    int tminP = 0;
    int tmaxP = 0;
    
    int maxSum = arr[0];
    int minP = 0;
    int maxP = 0;

    for (i=1;i<LENGTH;i++)
    {
        totle += arr[i];
        if (totle >= tmaxN)
        {
            tmaxN = totle;
            tmaxP = i;
            if (tmaxN-tminN>=maxSum)
            {
                maxSum = tmaxN-tminN;
                maxP = tmaxP;
                minP = tminP;
            }
        }
        else if (totle < tminN)
        {
            tminN = totle;
            tminP = i+1;
            if (tminP > tmaxP)
            {
                tmaxN = tminN;
                tmaxP = tminP;
            }
        }
    }

    printf("maxSum:%d  form %d to %d\n",maxSum,minP,maxP);
    
    return 0;
}
