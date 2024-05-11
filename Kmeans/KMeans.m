%% Kmeans算法
% 输入：
% data 输入的不带分类标号的数据
% K 数据一共分多少类
% iniCentriods 自行指定初始聚类中心
% iterations 迭代次数

% 输出：
% Idx 返回的分类标号
% centroids 每一类的中心
% Distance 类内总距离

 
function [Idx,centroids,Distance]=KMeans(data,K,iniCentriods,iterations)
[numOfData,numOfAttr]=size(data); % numOfData是数据个数，numOfAttr是数据维数
centroids=iniCentriods;
%% 迭代
for iter=1:iterations
    pre_centroids=centroids;% 上一次求得的中心位置
    
    tags=zeros(numOfData,K);
    %% 寻找最近中心，更新中心
    for i=1:numOfData
        D=zeros(1,K);% 每个数据点与每个聚类中心的标准差
        Dist=D;
        
        % 计算每个点到每个中心点的标准差
        for j=1:K
            Dist(j)=norm(data(i,:)-centroids(j,:),2);
        end
        
        [minDistance,index]=min(Dist);% 寻找距离最小的类别索引
        tags(i,index)=1;% 标记最小距离所处的位置（类别）
    end
    
    
    %% 取均值更新聚类中心点
    for i=1:K
        if sum(tags(:,i))~=0
            % 未出现空类，计算均值作为下一聚类中心
            for j=1:numOfAttr
                centroids(i,j)=sum(tags(:,i).*data(:,j))/sum(tags(:,i));
            end
        else % 如果出现空类，从数据集中随机选中一个点作为中心
            randidx = randperm(size(data, 1));
            centroids(i,:) = data(randidx(1),:);
            tags(randidx,:)=0;
            tags(randidx,i)=1;
        end
    end
    
   
    if sum(norm(pre_centroids-centroids,2))<0.001  % 不断迭代直到位置不再变化
        break;
    end
    
    
end

%% 计算输出结果
Distance=zeros(numOfData,1);
Idx=zeros(numOfData,1);
for i=1:numOfData
    D=zeros(1,K);% 每个数据点与每个聚类中心的标准差
    Dist=D;
    % 计算每个点到每个中心点的标准差
    for j=1:K
        Dist(j)=norm(data(i,:)-centroids(j,:),2);
    end
    
    [distance,idx]=min(Dist);% 寻找距离最小的类别索引
    distance=Dist(idx);
    
    Distance(i)=distance;
    Idx(i)=idx;
end
Distance=sum(Distance,1);% 计算类内总距离
end