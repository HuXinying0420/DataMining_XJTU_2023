clear
data=load('Iris .txt');
data=data(:,2:end);
K=10;


%% 产生随机初始点
[numOfData,numOfAttr]=size(data);   % numOfData是数据个数，numOfAttr是数据维数

centroids=zeros(K,numOfAttr);       % 随机初始化，最终迭代到每一类的中心位置
maxAttr=zeros(numOfAttr);        % 每一维最大的数
minAttr=zeros(numOfAttr);        % 每一维最小的数
for i=1:numOfAttr
    maxAttr(i)=max(data(:,i));    % 每一维最大的数
    minAttr(i)=min(data(:,i));    % 每一维最小的数
    for j=1:K
        centroids(j,i)=maxAttr(i)+(minAttr(i)-maxAttr(i))*rand();  % 随机初始化，选取每一维[min max]中初始化
    end
end

[Idx,C,distance]=KMeans(data,K,centroids,500);% 调用KMeans
Distance=sum(distance)% 计算类内距离之和

%% 计算准确率
c1=Idx(1:50,1);c2=Idx(51:100,1);c3=Idx(101:150,1);
Accuracy=(sum(c1==mode(Idx(1:50,1)))+sum(c2==mode(Idx(51:100,1)))+sum(c3==mode(Idx(101:150,1))))/numOfData