clear 
data=load('Iris .txt');
data=data(:,2:end);

matrix=[5.9016,2.7484,4.3935,1.4339;6.8500,3.0737,5.7421,2.0711;5.0060,3.4280,1.4620,0.2460];
[Idx,C,distance]=KMeans(data,3,matrix,500);
Distance=sum(distance)

c1=Idx(1:50,1);c2=Idx(51:100,1);c3=Idx(101:150,1);
accuracy=(sum(c1==mode(Idx(1:50,1)))+sum(c2==mode(Idx(51:100,1)))+sum(c3==mode(Idx(101:150,1))))/150
