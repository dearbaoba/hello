ANT=8;
RB=1;
CELL=2;
USER=CELL;
NOISE=0.001;
H=rand(RB*CELL,ANT,USER)+rand(RB*CELL,ANT,USER)*i;
W=zeros(USER,ANT);
SINR=zeros(1,USER);
COFF=ones(1,RB*USER);
for x=1:5
    %for W
    for n=1:USER
        Hi=H(:,:,n);
        Hii=Hi((n-1)*RB+1:n*RB,:);
        Hij=Hi;
    %     Hij(Hij==0)=[];
        c=Hii'*Hii/(COFF(:,(n-1)*RB+1)*NOISE*ones(ANT)+(Hij'.*repmat(COFF(1,:),ANT,1))*Hij)
        [V,D]=eig(c);
        t=abs(D(1,1));
        tidx=1;
        for l=1:ANT
            if abs(D(l,l))>t
                t=abs(D(l,l));
                tidx=l;
            end
        end
        W(n,:)=V(tidx,:);
    end
    %for SINR
    for n=1:USER
        Hi=H(:,:,n);
        Hii=Hi((n-1)*RB+1:n*RB,:);
        Hij=Hi;
        Hij(Hij==0)=[];
        SINR(:,n)=abs(ones(1,RB)*(Hii*W(n,:).'))/(NOISE+abs(ones(1,RB*CELL)*(Hij*W(n,:).')));
    end
    %for COFF
    for n=1:USER
        COFF(:,(n-1)*RB+1:n*RB)=repmat([SINR(1,n)/sum(SINR(1,:))],1,RB);
    end
    sum(SINR)
end
'over'
