#include <stdio.h>
#include <string.h>

typedef enum
{
	PRIO_NONE,
	PRIO_ZERO, // + -
	PRIO_ONE, // * /
	PRIO_TWO, // ^
}PRIO;

#define MAX_LEN 50

int expr(const char *exp);
int doCal(const char *exp1, const char *oper, const char *exp2);
int isOperZERO(const char *p);
int isOperONE(const char *p);
int isOperTwo(const char *p);
int isLeftBrckt(const char *p);
int isRightBrckt(const char *p);
int power(int a, int b);

main()
{
	int r = expr("2*(1+2^0*(1+1))-3/3");

	printf("result=%d\n", r);
}

int expr(const char *exp)
{
	const char *pHead = exp;
	const char *pOpr = exp;
	const char *pCurr = exp;

	PRIO prioCurr = PRIO_NONE;
	int lvl = 0;

	if(isLeftBrckt(pCurr))
	{
		pHead++; pOpr++; pCurr++;
	}
	
	while(*pCurr != 0 && lvl >=0)
	{
		if(isLeftBrckt(pCurr))
		{
			lvl++;
		}
		else if(isRightBrckt(pCurr))
		{
			lvl--;
		}
		else if (isOperTwo(pCurr) && lvl == 0)
		{
			if (prioCurr == PRIO_NONE || prioCurr > PRIO_TWO)
			{
				pOpr = pCurr;
				prioCurr = PRIO_TWO;
			}
		}
		else if (isOperONE(pCurr) && lvl == 0)
		{
			if (prioCurr == PRIO_NONE || prioCurr > PRIO_ONE)
			{
				pOpr = pCurr;
				prioCurr = PRIO_ONE;
			}
		}
		else if (isOperZERO(pCurr) && lvl == 0)
		{
			if (prioCurr == PRIO_NONE || prioCurr > PRIO_ZERO)
			{
				pOpr = pCurr;
				prioCurr = PRIO_ZERO;
			}
		}

		pCurr++;
	}

	return doCal(pHead, pOpr, pOpr+1);
}

int doCal(const char *exp1, const char *oper, const char *exp2)
{
	int rtn = 0;
	char tmp[MAX_LEN];

	memset(tmp, 0, MAX_LEN);
	memcpy(tmp, exp1, oper- exp1);
	switch(*oper)
	{
		case '+':
			rtn = expr(tmp) + expr(exp2);
			break;
		case '-':
			rtn = expr(tmp) - expr(exp2);
			break;
		case '*':
			rtn = expr(tmp) * expr(exp2);
			break;
		case '/':
			rtn = expr(tmp) / expr(exp2);
			break;
		case '^':
			rtn = power(expr(tmp) , expr(exp2));
			break;
		default:
			rtn = atoi(exp1);
			break;
	}

	return rtn;
}

int isOperZERO(const char *p)
{
	return *p=='+'||*p=='-';
}

int isOperONE(const char *p)
{
	return *p=='*'||*p=='/';
}

int isOperTwo(const char *p)
{
	return *p=='^';
}

int isLeftBrckt(const char *p)
{
	return *p=='(';
}

int isRightBrckt(const char *p)
{
	return *p==')';
}

int power(int a, int b)
{
	int rtn = 1;
	while(b-- > 0) rtn *= a;
	return rtn;
}
