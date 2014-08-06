#include <stdio.h>
#include <string.h>
#include <assert.h>

enum
{
	PRIO_NONE,
	PRIO_ZERO, // + -
	PRIO_ONE, // * /
	PRIO_TOP,
};

#define MAX_LEN 50

main()
{
	assert(expr("1") == 1);
	assert(expr("1+2") == 3);
	assert(expr("3-2") == 1);
	assert(expr("1+2+3") == 6);
	assert(expr("1+2-3") == 0);
	assert(expr("(1+2)-3") == 0);
	assert(expr("3-2-1") == 0);
}

int expr(const char *exp)
{
	const char *pHead = exp;
	const char *pOpr = exp;
	const char *pCurr = exp;

	int prioBase = 0;
	int prioCurr = PRIO_NONE;

	if(isLeftBrckt(pCurr))
	{
		pHead++; pOpr++; pCurr++; prioBase += PRIO_TOP;
	}
	
	while(*pCurr != 0)
	{
		if(isLeftBrckt(pCurr))
		{
			prioBase += PRIO_TOP;
		}
		else if(isRightBrckt(pCurr))
		{
			prioBase -= PRIO_TOP;
		}
		else if (isOprONE(pCurr))
		{
			if (prioCurr == PRIO_NONE || prioCurr >= PRIO_ONE + prioBase)
			{
				pOpr = pCurr;
				prioCurr = PRIO_ONE + prioBase;
			}
		}
		else if (isOprZERO(pCurr))
		{
			if (prioCurr == PRIO_NONE || prioCurr >= PRIO_ZERO + prioBase)
			{
				pOpr = pCurr;
				prioCurr = PRIO_ZERO + prioBase;
			}
		}

		pCurr++;
	}

	return doCal(pHead, pOpr, pOpr+1);
}

int doCal(const char *exp1, const char *opr, const char *exp2)
{
	int rtn = 0;
	char tmp[MAX_LEN];

	memset(tmp, 0, MAX_LEN);
	memcpy(tmp, exp1, opr- exp1);
	switch(*opr)
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
		default:
			rtn = atoi(exp1);
			break;
	}
	return rtn;
}

int isLeftBrckt(const char *p)
{
	return *p=='(';
}

int isRightBrckt(const char *p)
{
	return *p==')';
}

int isOprZERO(const char *p)
{
	return *p=='+'||*p=='-';
}

int isOprONE(const char *p)
{
	return *p=='*'||*p=='/';
}
