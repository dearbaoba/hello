ANT=4;
RB=1;
CELL=2;
USER=CELL;
NOISE=0.1
H=rand(USER,ANT,CELL)+rand(USER,ANT,CELL)*i
W=zeros(CELL,ANT);
SINR=zeros(1,CELL);
COFF=ones(1,CELL);
CAB=zeros(1,CELL);
for x=1:5
    %for W
    for n=1:CELL
        Hi=H(:,:,n);
        Hi(n,:)=[];
        COFFi=COFF;
        COFFi(:,n)=[];
        c=H(n,:,n)'*H(n,:,n)/(COFF(:,n)*NOISE^2*ones(ANT)+(Hi'.*repmat(COFFi(1,:),ANT,1))*Hi);
        %c=inv(COFF(:,n)*NOISE*ones(ANT)+(Hi'.*repmat(COFFi(1,:),ANT,1))*Hi)*Hii'*Hii;
        [V,D]=eig(c);
        [Dmax Didx]=max(diag(D));
        W(n,:)=V(Didx,:);
    end
    W
    %for SINR
    for n=1:CELL
        SINR(:,n)=abs(H(n,:,n)*W(n,:).')/(NOISE^2+sum(diag(abs(H(:,:,n)*W.')))-abs(H(n,:,n)*W(n,:).'));
    end
    SINR;
    %for COFF
    for n=1:CELL
        COFF(:,n)=SINR(1,n)/(sum(SINR(1,:))-SINR(1,n));
    end
    total_SINR=sum(SINR)
    %for CAB
    for n=1:CELL
        CAB(1,n)=log2(1+abs(H(n,:,n)*W(n,:).')^2/(NOISE^2+abs(diag(H(:,:,n)*W.'))'*abs(diag(H(:,:,n)*W.'))-abs(H(n,:,n)*W(n,:).')^2));
    end
    total_cab=sum(CAB(1,:))
end
'over'
