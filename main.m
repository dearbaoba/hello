ANT=8;
CELL=3;
USER=CELL;
RB=2;
FRAME=5;

H=rand(ANT,CELL,USER,RB)+rand(ANT,CELL,USER,RB)*i;
w=rand(ANT,CELL)+rand(ANT,CELL)*i;

H=reshape(H,1,ANT*CELL*USER*RB);
w=reshape(w,1,ANT*CELL);

RL=eye(CELL)
NRL=ones(CELL)-RL
RL=reshape(RL,1,CELL*USER)
NRL=reshape(NRL,1,CELL*USER)
t=[1:CELL*USER]
RL=repmat([1],ANT,1)*(RL.*t)
RL(RL==0)=[]
NRL=repmat([1],ANT,1)*(NRL.*t)
NRL(NRL==0)=[]

sANT=repmat([1:1:ANT],1,CELL);
s=sparse(sANT,RL,w,ANT,CELL*USER);
s=reshape(s,1,ANT*CELL*USER);
s=repmat(s,1,RB);

nANT=repmat([1:1:ANT],1,CELL*USER-CELL)
n=sparse(nANT,NRL,w,ANT,CELL*USER);
n=reshape(n,1,ANT*CELL*USER);
n=repmat(n,1,RB);

abs(H*s')
abs(H*n')
