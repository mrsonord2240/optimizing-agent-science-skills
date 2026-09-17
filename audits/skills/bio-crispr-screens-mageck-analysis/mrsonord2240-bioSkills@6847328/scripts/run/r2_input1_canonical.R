pdf(file='r2_input1_canonical.pdf',width=4.5,height=4.5);
gstable=read.table('r2_input1_canonical.gene_summary.txt',header=T)
# 
#
# parameters
# Do not modify the variables beginning with "__"

# gstablename='__GENE_SUMMARY_FILE__'
startindex=3
# outputfile='__OUTPUT_FILE__'
targetgenelist=c("POLR2L","EIF3A","GTPBP10","PES1","MRPL53","TCEB2","MTG2","CHORDC1","RPSA","POLR3H")
# samplelabel=sub('.\\w+.\\w+$','',colnames(gstable)[startindex]);
samplelabel='HAP1_T18A,HAP1_T18B,HAP1_T18C_vs_HAP1_T0 neg.'


# You need to write some codes in front of this code:
# gstable=read.table(gstablename,header=T)
# pdf(file=outputfile,width=6,height=6)


# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")

######
# function definition

plotrankedvalues<-function(val, tglist, ...){
  
  plot(val,log='y',ylim=c(max(val),min(val)),type='l',lwd=2, ...)
  if(length(tglist)>0){
    for(i in 1:length(tglist)){
      targetgene=tglist[i];
      tx=which(names(val)==targetgene);ty=val[targetgene];
      points(tx,ty,col=colors[(i %% length(colors)) ],cex=2,pch=20)
      # text(tx+50,ty,targetgene,col=colors[i])
    }
    legend('topright',tglist,pch=20,pt.cex = 2,cex=1,col=colors)
  }
}



plotrandvalues<-function(val,targetgenelist, ...){
  # choose the one with the best distance distribution
  
  mindiffvalue=0;
  randval=val;
  for(i in 1:20){
    randval0=sample(val)
    vindex=sort(which(names(randval0) %in% targetgenelist))
    if(max(vindex)>0.9*length(val)){
      # print('pass...')
      next;
    }
    mindiffind=min(diff(vindex));
    if (mindiffind > mindiffvalue){
      mindiffvalue=mindiffind;
      randval=randval0;
      # print(paste('Diff: ',mindiffvalue))
    }
  }
  plot(randval,log='y',ylim=c(max(randval),min(randval)),pch=20,col='grey', ...)
  
  if(length(targetgenelist)>0){
    for(i in 1:length(targetgenelist)){
      targetgene=targetgenelist[i];
      tx=which(names(randval)==targetgene);ty=randval[targetgene];
      points(tx,ty,col=colors[(i %% length(colors)) ],cex=2,pch=20)
      text(tx+50,ty,targetgene,col=colors[i])
    }
  }
  
}




# set.seed(1235)



pvec=gstable[,startindex]
names(pvec)=gstable[,'id']
pvec=sort(pvec);

plotrankedvalues(pvec,targetgenelist,xlab='Genes',ylab='RRA score',main=paste('Distribution of RRA scores in \\n',samplelabel))

# plotrandvalues(pvec,targetgenelist,xlab='Genes',ylab='RRA score',main=paste('Distribution of RRA scores in \\n',samplelabel))


pvec=gstable[,startindex+1]
names(pvec)=gstable[,'id']
pvec=sort(pvec);

plotrankedvalues(pvec,targetgenelist,xlab='Genes',ylab='p value',main=paste('Distribution of p values in \\n',samplelabel))

# plotrandvalues(pvec,targetgenelist,xlab='Genes',ylab='p value',main=paste('Distribution of p values in \\n',samplelabel))



# you need to write after this code:
# dev.off()






# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(626.6496336270341,12.794258297905037,29.313630463777262,2.5191521105894026),c(812.604269094033,0.0,0.0,0.0),c(984.5685871591261,108.16963833683349,9.380361748408724,31.489401382367532),c(373.65806060923614,11.631143907186397,0.0,0.0))
targetgene="POLR2L"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(623.7349841683038,29.07785976796599,24.6234495895729,79.35329148356618),c(753.7283500276792,48.85080441018287,126.63488360351778,73.05541120709267),c(1061.5153328696085,0.0,15.243087841164176,42.825585880019844),c(890.1339446962614,180.28273056138914,141.87797144468195,132.25548580594364))
targetgene="EIF3A"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(589.9250504470311,27.91474537724735,10.552906966959814,27.71067321648343),c(916.9487197165811,5.8155719535931985,5.8627260927554525,13.855336608241714),c(573.603013478141,34.89343172155919,63.31744180175889,0.0),c(461.0975443711479,37.21966050299647,3.5176356556532715,0.0))
targetgene="GTPBP10"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(547.9540982413135,8.141800735030477,35.17635655653272,11.336184497652312),c(455.8511753454332,13.957372688623675,7.035271311306543,16.374488718831117),c(522.8881128962322,126.77946858833172,10.552906966959814,7.557456331768208),c(419.70952205717634,0.0,5.8627260927554525,2.5191521105894026))
targetgene="PES1"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(461.0975443711479,17.446715860779594,62.144896583207796,7.557456331768208),c(378.9044296349509,0.0,0.0,0.0),c(884.8875756705468,101.19095199252165,23.45090437102181,16.374488718831117),c(968.2465501902359,8.141800735030477,83.25071051712743,61.71922670944036))
targetgene="MRPL53"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(708.259818471485,50.01391880090151,0.0,0.0),c(524.6369025714704,1.1631143907186396,0.0,0.0),c(616.7398254673508,50.01391880090151,246.234495895729,288.4429166624866),c(573.0200835863949,9.304915125749117,0.0,0.0))
targetgene="TCEB2"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(789.8700033159361,100.02783760180301,91.45852704698505,89.42989992592379),c(1270.7871640064504,129.105697369769,193.46996106092993,99.5065083682814),c(419.70952205717634,47.68769001946423,0.0,5.038304221178805),c(806.7749701765723,170.97781543564003,158.29360450439722,76.83413937297678))
targetgene="MTG2"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(568.3566444524263,0.0,70.35271311306543,21.412792940009922),c(549.1199580248057,61.6450627080879,36.3489017750838,15.114912663536415),c(697.7670804200557,43.03523245658967,213.40322977629847,0.0),c(370.7434111505058,8.141800735030477,35.17635655653272,7.557456331768208))
targetgene="CHORDC1"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(390.5630274698724,0.0,31.658720900879445,8.817032387062909),c(856.906940866735,190.7507600778569,280.23830723371066,46.60431404590395),c(912.2852805826125,158.183557137735,111.3917957623536,240.57902656128795),c(775.2967560222841,20.936059032935514,174.7092375641125,60.45965065414566))
targetgene="RPSA"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(588.176260771793,9.304915125749117,26.968540026675083,0.0),c(558.446836292743,41.87211806587103,9.380361748408724,0.0),c(457.5999650206714,2.3262287814372793,39.866537430737075,25.191521105894026),c(711.7573978219615,0.0,0.0,0.0))
targetgene="POLR3H"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}



# 
#
# parameters
# Do not modify the variables beginning with "__"

# gstablename='__GENE_SUMMARY_FILE__'
startindex=9
# outputfile='__OUTPUT_FILE__'
targetgenelist=c("TSC2","TSC1","LacZ","DOT1L","DBF4","KCTD5","DEPDC5","OR52E4","CSK","IPCEF1")
# samplelabel=sub('.\\w+.\\w+$','',colnames(gstable)[startindex]);
samplelabel='HAP1_T18A,HAP1_T18B,HAP1_T18C_vs_HAP1_T0 pos.'


# You need to write some codes in front of this code:
# gstable=read.table(gstablename,header=T)
# pdf(file=outputfile,width=6,height=6)


# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")

######
# function definition

plotrankedvalues<-function(val, tglist, ...){
  
  plot(val,log='y',ylim=c(max(val),min(val)),type='l',lwd=2, ...)
  if(length(tglist)>0){
    for(i in 1:length(tglist)){
      targetgene=tglist[i];
      tx=which(names(val)==targetgene);ty=val[targetgene];
      points(tx,ty,col=colors[(i %% length(colors)) ],cex=2,pch=20)
      # text(tx+50,ty,targetgene,col=colors[i])
    }
    legend('topright',tglist,pch=20,pt.cex = 2,cex=1,col=colors)
  }
}



plotrandvalues<-function(val,targetgenelist, ...){
  # choose the one with the best distance distribution
  
  mindiffvalue=0;
  randval=val;
  for(i in 1:20){
    randval0=sample(val)
    vindex=sort(which(names(randval0) %in% targetgenelist))
    if(max(vindex)>0.9*length(val)){
      # print('pass...')
      next;
    }
    mindiffind=min(diff(vindex));
    if (mindiffind > mindiffvalue){
      mindiffvalue=mindiffind;
      randval=randval0;
      # print(paste('Diff: ',mindiffvalue))
    }
  }
  plot(randval,log='y',ylim=c(max(randval),min(randval)),pch=20,col='grey', ...)
  
  if(length(targetgenelist)>0){
    for(i in 1:length(targetgenelist)){
      targetgene=targetgenelist[i];
      tx=which(names(randval)==targetgene);ty=randval[targetgene];
      points(tx,ty,col=colors[(i %% length(colors)) ],cex=2,pch=20)
      text(tx+50,ty,targetgene,col=colors[i])
    }
  }
  
}




# set.seed(1235)



pvec=gstable[,startindex]
names(pvec)=gstable[,'id']
pvec=sort(pvec);

plotrankedvalues(pvec,targetgenelist,xlab='Genes',ylab='RRA score',main=paste('Distribution of RRA scores in \\n',samplelabel))

# plotrandvalues(pvec,targetgenelist,xlab='Genes',ylab='RRA score',main=paste('Distribution of RRA scores in \\n',samplelabel))


pvec=gstable[,startindex+1]
names(pvec)=gstable[,'id']
pvec=sort(pvec);

plotrankedvalues(pvec,targetgenelist,xlab='Genes',ylab='p value',main=paste('Distribution of p values in \\n',samplelabel))

# plotrandvalues(pvec,targetgenelist,xlab='Genes',ylab='p value',main=paste('Distribution of p values in \\n',samplelabel))



# you need to write after this code:
# dev.off()






# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(367.82876169177536,1658.6011211647801,1062.325968007288,1490.0784734136316),c(351.50672472288517,1047.9660660374943,1262.8312003795245,1322.5548580594364),c(359.66774320733026,938.6333133099422,1443.4031640363924,1998.947199752691),c(265.8160306362117,1079.3701545868976,965.0047148675475,566.8092248826156))
targetgene="TSC2"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(591.6738401222694,1491.112648901296,2097.683395987901,1371.6783242159297),c(276.3087686876411,928.1652837934745,1109.2277767493317,1098.3503202169795),c(680.2791836676734,1489.9495345105775,2028.5032280933865,1721.8404675878567),c(516.4758840870253,2129.662449405829,2397.8549719369803,1912.0364519373566))
targetgene="TSC1"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(156.22521098794897,314.0408854940327,290.7912142006704,433.29416302137724),c(374.8239203927283,229.133534971572,252.09722198848445,292.2216448283707),c(270.4794697701803,509.4441031347642,111.3917957623536,309.8557096024965),c(53.629550040639195,86.07046491317934,78.56052964292306,45.34473799060925),c(252.40864312605189,405.92692236080524,313.06957335314115,532.8006713896586),c(666.8717961575135,612.9612839087231,171.1916019084592,663.7965811403076),c(837.0873245473683,796.7333576422682,348.24592990967386,702.8434388544433),c(133.4909452098519,282.63679694462945,246.234495895729,316.15358987897),c(398.1411160625714,735.0882949341802,899.3421826286864,660.0178529744235),c(498.987987334643,674.606346616811,617.9313301764247,574.3666812143838),c(311.8674920841519,348.9343172155919,804.3660199260481,361.49832786957927),c(504.23435636035765,995.6259184551556,561.6491596859723,833.8393486050923),c(123.58113705016858,0.0,32.83126611943054,85.65117176003969),c(336.35054753748716,939.7964277006608,447.9122734865166,511.3878784496487),c(253.57450290954404,426.86298139374077,572.2020666529322,384.1706968648839),c(1234.6455107181937,1951.7059476258773,1380.0857222346335,1525.3466029618833),c(848.1629924905438,735.0882949341802,685.938952852388,583.1837136014467),c(202.85960232763523,255.8851659581007,454.9475447978231,449.66865174020836),c(122.41527726667643,503.62853118117096,660.142958044264,328.74935043191704),c(512.3953748448027,1299.1987744327205,555.7864335932169,733.0732641815162),c(426.1217508663832,1175.9086490165446,654.2802319515085,663.7965811403076),c(487.91231939146746,936.3070845285049,1024.8045210136531,777.1584261168307),c(468.09270307210085,362.8916899042156,899.3421826286864,364.0174799801687),c(914.6170001495967,735.0882949341802,1220.6195725116852,971.1331386322147),c(405.1362747635244,757.1874683578344,619.1038753949758,673.8731895826652),c(620.2374048178273,410.57937992367977,162.98378537860157,1730.6574999749196),c(884.8875756705468,652.5071731931569,391.63010299606424,773.3796979509466),c(760.140578836886,1408.5315271602726,731.6682163758804,986.2480512957511),c(251.8257132343058,201.21878959432465,493.64153701000913,450.92822779550306),c(175.46189741556955,98.86472321108437,371.69683428069567,236.80029839540384),c(732.1599440330742,864.1939923039492,535.8531648778484,1200.3759806958503),c(497.8221275511508,509.4441031347642,320.1048446644477,298.5195251048442),c(516.4758840870253,421.04740944014753,653.1076867329574,492.4942376202282),c(615.5739656838587,1353.8651507964964,1086.949417596861,667.5753093061917),c(397.55818617082537,582.7203097500385,436.1868213010057,371.5749363119369),c(257.0720822600205,321.0195718383445,388.11246734041094,554.2134643296686),c(573.0200835863949,1129.3840733877992,1178.407944643846,808.6478274991982),c(1014.8809415299222,1014.2357487066538,820.7816529857633,1146.2142103181782),c(839.4190441143527,890.945623290478,862.9932808536026,1250.7590229076384),c(1012.5492219629378,1182.8873353608565,824.2992886414166,590.7411699332149),c(676.7816043171969,1002.6046047994673,1098.6748697823718,862.8095978768704),c(542.7077292155989,942.1226564820981,647.244960640202,377.8728165884104),c(89.77120332889605,46.52457562874559,220.438501087605,253.17478711423496),c(208.68890124509602,394.2957784536188,318.9322994458966,279.6258842754237),c(686.6914124768801,437.33101091020853,688.2840432894901,1418.2826382618337),c(15.739107077144112,81.41800735030478,100.83888879539379,96.987356257692),c(308.95284262542145,265.19008108384986,181.74450887541903,273.3280039989502),c(346.2603556971705,460.5932987245813,664.8331389184683,468.5622925696289),c(352.08965461463123,585.0465385314758,695.3193146007967,346.38341520604286),c(405.71920465527046,849.073505224607,505.36698919552003,600.8177783755725),c(671.5352352914821,902.5767671976644,432.6691856453524,599.5582023202778),c(380.65321931018906,319.8564574476259,444.3946378308633,231.76199417422504),c(402.80455519654004,624.5924278159094,840.7149217011319,348.90256731663226),c(258.23794204351265,809.5276159401732,602.6882423352605,681.4306459144334),c(245.41348442509894,76.76554978743022,284.928488107915,142.33209424830125),c(101.42980116381761,151.20487079342314,413.90846214853497,381.6515447542945),c(172.54724795683916,432.67855334733395,344.7282942540206,416.9196743025461),c(341.01398667145577,780.4497561722072,298.9990307305281,335.04723070839054),c(299.62596435748424,487.34492971111,179.39941843831684,331.26850254250644),c(128.2445761841372,169.81470104492138,107.87416010670033,161.22573507772177),c(303.7064735997068,497.8129592275778,427.979004771148,312.3748617130859),c(85.6906940866735,388.48020650002564,540.5433457520527,118.40014919770192),c(121.24941748318427,258.211394739538,107.87416010670033,364.0174799801687),c(53.629550040639195,38.38277489371511,154.77596884874396,47.86389010119865),c(157.9740006631872,77.92866417814885,136.0152453519265,193.974712515384),c(388.2313079028881,498.9760736182964,281.41085245226174,258.21309133541376),c(510.06365527781844,1150.3201324207346,595.652971023954,845.1755331027446),c(152.72763163747248,321.0195718383445,491.2964465729069,685.2093740803175),c(122.41527726667643,255.8851659581007,263.8226741739954,426.99628274490374),c(118.91769791619996,310.5515423218768,393.9751934331664,275.8471561095396),c(240.16711539938424,327.9982581826564,263.8226741739954,482.4176291778706),c(417.9607323819381,562.9473651078216,234.5090437102181,433.29416302137724),c(93.8517125711186,76.76554978743022,556.958978811768,379.1323926437051),c(342.762776346694,545.500649247042,354.1086560024293,639.8646360897083),c(297.877174682246,204.7081327664806,385.7673769033088,147.37039846948005),c(1258.545636279783,2542.5680581109464,1527.826419772071,1651.3042084913534),c(580.0152422873479,1116.589815089894,899.3421826286864,647.4220924214765),c(549.7028879165517,761.839925920709,749.2563946541468,622.2305713155824),c(225.0109382139862,457.10395555242536,457.2926352349253,469.8218686249236),c(821.9311473619703,894.4349664626338,691.8016789451434,594.519898099099),c(0.0,0.0,0.0,0.0),c(153.31056152921857,332.65071574553093,144.22306188178413,248.13648289305615),c(452.9365258867028,267.5163098652871,264.99521939254646,380.3919686989998),c(241.3329751828764,324.50891501050046,97.3212531397405,391.7281531966521),c(357.33602364034596,288.45236889822263,562.8217049045235,486.1963573437547),c(483.8318101492449,702.5210919940583,252.09722198848445,552.9538882743739),c(511.2295150613106,897.9243096347898,1181.9255802994992,712.9200472968009),c(258.8208719352587,277.98433938175486,350.5910203467761,1236.9036862993967),c(68.20279733429115,137.2474981047995,241.54431502152465,201.5321688471522),c(150.39591207048818,126.77946858833172,198.1601419351343,206.570473068331),c(197.03030341017444,450.12526920811354,130.15251925917104,177.60022379655288),c(151.56177185398033,334.9769445269682,152.43087841164177,414.4005221919567),c(403.9704149800322,416.394951877273,576.8922475271365,694.0264064673804),c(0.0,0.0,0.0,0.0),c(122.41527726667643,60.48194831736926,235.6815889287692,196.4938646259734),c(284.46978717208617,353.58677477846646,513.5748057253776,390.4685771413574))
targetgene="LacZ"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(612.0763863333822,1917.9756302950368,1639.2182155344244,2150.096326388055),c(479.75130090702237,749.0456676228039,939.2087200594235,2157.6537827198235),c(89.18827343714997,809.5276159401732,494.8140822285602,369.0557842013475),c(324.6919497025656,266.35319547456845,927.4832678739126,932.086280918079))
targetgene="DOT1L"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(1.1658597834921565,238.43845009732112,62.144896583207796,47.86389010119865),c(391.7288872533646,1008.4201767530606,1214.7568464189299,1112.2056568252212),c(220.34749908001757,364.05480429493423,209.8855941206452,360.23875181428457),c(353.83844428986947,1289.8938593069713,948.5890818078323,826.281892273324))
targetgene="DBF4"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(337.5164073209793,903.739881588383,1453.9560710033522,1254.5377510735225),c(576.5176629368714,1616.729003098909,1850.276354873621,1338.9293467782675),c(348.5920752641548,495.4867304461405,1823.3078148469458,852.7329894345128),c(491.40989874194395,935.1439701377863,1167.8550376768862,874.1457823745227))
targetgene="KCTD5"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(365.49704212479105,675.7694610075297,707.0447667863076,998.8438118486981),c(361.99946277431457,1751.6502724222712,899.3421826286864,1006.4012681804663),c(238.418325724146,273.33188181888033,1164.337402021233,712.9200472968009),c(128.8275060758833,533.8695053398556,473.70826829464056,599.5582023202778))
targetgene="DEPDC5"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(473.9220019895616,983.9947745479691,991.9732548942226,620.9709952602877),c(345.6774258054244,735.0882949341802,518.264986599582,710.4008951862115),c(237.25246594065385,829.3005605823901,606.2058779909138,730.5541120709267),c(294.96252522351557,749.0456676228039,1156.1295854913753,476.1197489013971))
targetgene="OR52E4"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(884.3046457788007,1398.0634976438048,1139.71395243166,632.30717975794),c(138.73731423556663,1030.5193501767146,629.6567823619356,927.0479766969002),c(67.61986744254507,307.06219914972087,358.7988368766337,182.6385280177317),c(486.74645960797534,1588.8142577216618,1489.132427559885,911.9330640333637))
targetgene="CSK"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}




# parameters
# Do not modify the variables beginning with "__"
targetmat=list(c(122.9982071584225,244.25402205091433,410.3908264928817,423.21755457901963),c(197.03030341017444,694.3792912590279,330.6577516314075,457.22610807197657),c(154.47642131271073,429.189210175178,689.4565885080412,478.6389010119865),c(159.13986044667936,538.5219629027301,494.8140822285602,622.2305713155824))
targetgene="IPCEF1"
collabel=c("HAP1_T0","HAP1_T18A","HAP1_T18B","HAP1_T18C")

# set up color using RColorBrewer
#library(RColorBrewer)
#colors <- brewer.pal(length(targetgenelist), "Set1")

colors=c( "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",  "#A65628", "#F781BF",
          "#999999", "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854", "#FFD92F", "#E5C494", "#B3B3B3", 
          "#8DD3C7", "#FFFFB3", "#BEBADA", "#FB8072", "#80B1D3", "#FDB462", "#B3DE69", "#FCCDE5",
          "#D9D9D9", "#BC80BD", "#CCEBC5", "#FFED6F")


## code

targetmatvec=unlist(targetmat)+1
yrange=range(targetmatvec[targetmatvec>0]);
# yrange[1]=1; # set the minimum value to 1
for(i in 1:length(targetmat)){
  vali=targetmat[[i]]+1;
  if(i==1){
    plot(1:length(vali),vali,type='b',las=1,pch=20,main=paste('sgRNAs in',targetgene),ylab='Read counts',xlab='Samples',xlim=c(0.7,length(vali)+0.3),ylim = yrange,col=colors[(i %% length(colors))],xaxt='n',log='y')
    axis(1,at=1:length(vali),labels=(collabel),las=2)
    # lines(0:100,rep(1,101),col='black');
  }else{
    lines(1:length(vali),vali,type='b',pch=20,col=colors[(i %% length(colors))])
  }
}



dev.off()
Sweave("r2_input1_canonical_summary.Rnw");
library(tools);

texi2dvi("r2_input1_canonical_summary.tex",pdf=TRUE);

