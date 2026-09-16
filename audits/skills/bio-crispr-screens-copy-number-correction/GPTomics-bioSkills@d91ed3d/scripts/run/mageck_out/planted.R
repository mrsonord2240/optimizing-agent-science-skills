pdf(file='planted.pdf',width=4.5,height=4.5);
gstable=read.table('planted.gene_summary.txt',header=T)
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
targetmat=list(c(626.5754651890535,12.79594799030711,29.317889315966255,2.519491461469395),c(812.5080916032935,0.0,0.0,0.0),c(984.4520564691268,108.18392391805102,9.381724581109202,31.49364326836744),c(373.61383552203097,11.632679991188281,0.0,0.0))
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
targetmat=list(c(623.661160699802,29.081699977970704,24.627027025411653,79.36398103628595),c(753.639140920415,48.857255962990784,126.65328184497423,73.06525238261246),c(1061.389694985364,0.0,15.245302444302453,42.831354844979714),c(890.028591017381,180.30653986341838,141.89858428927667,132.27330172714323))
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
targetmat=list(c(589.8552286244857,27.918431978851878,10.554440153747851,27.714406076163346),c(916.840192318494,5.816339995594141,5.863577863193251,13.857203038081673),c(573.5351234846778,34.89803997356484,63.326640922487115,0.0),c(461.0429701995733,37.2245759718025,3.5181467179159505,0.0))
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
targetmat=list(c(547.8892439792653,8.142875993831797,35.181467179159505,11.337711576612278),c(455.79722211892073,13.959215989425939,7.036293435831901,16.376694499551068),c(522.8262253717032,126.79621190395227,10.554440153747851,7.558474384408186),c(419.6598464522032,0.0,5.863577863193251,2.519491461469395))
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
targetmat=list(c(461.0429701995733,17.44901998678242,62.153925349848464,7.558474384408186),c(378.8595836026835,0.0,0.0,0.0),c(884.7828429367285,101.20431592333804,23.454311452773005,16.376694499551068),c(968.1319513293189,8.142875993831797,83.26280565734416,61.72754080600018))
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
targetmat=list(c(708.175990888093,50.020523962109614,0.0,0.0),c(524.574808065254,1.1632679991188282,0.0,0.0),c(616.6668299255987,50.020523962109614,246.27027025411655,288.4817723382457),c(572.9522625868275,9.306143992950625,0.0,0.0))
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
targetmat=list(c(789.7765165871325,100.04104792421923,91.47181466581472,89.44194688216352),c(1270.6367573136154,129.12274790218993,193.4980694853773,99.5199127280411),c(419.6598464522032,47.693987963871955,0.0,5.03898292293879),c(806.6794826247907,171.00039587046774,158.3166023062178,76.84448957481655))
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
targetmat=list(c(568.2893754040252,0.0,70.36293435831901,21.415677422489857),c(549.0549657749659,61.65320395329789,36.354182751798156,15.116948768816371),c(697.6844947267879,43.04091596739664,213.43423422023434,0.0),c(370.69953103277953,8.142875993831797,35.181467179159505,7.558474384408186))
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
targetmat=list(c(390.5168015596891,0.0,31.663320461243558,8.818220115142882),c(856.805519839915,190.77595185548782,280.2790218606374,46.61059203718381),c(912.1773051356918,158.20444788016064,111.40797940067178,240.61143457032722),c(775.2049941408754,20.938823984138907,174.73462032315888,60.467795075265485))
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
targetmat=list(c(588.1066459309349,9.306143992950625,26.972458170688956,0.0),c(558.3807401405704,41.87764796827781,9.381724581109202,0.0),c(457.5458048124716,2.3265359982376563,39.87232946971411,25.19491461469395),c(711.6731562751946,0.0,0.0,0.0))
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
targetmat=list(c(367.7852265435281,1658.820166743449,1062.480308810617,1490.279199459147),c(351.4651214037202,1048.104467206064,1263.0146717318262,1322.7330172714323),c(359.62517397362416,938.7572752888943,1443.6128699181784,1999.216474675965),c(265.7845694197287,1079.5127031822726,965.1449162816091,566.8855788306139))
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
targetmat=list(c(591.6038113180365,1491.3095748703377,2097.9881594505455,1371.8631007700856),c(276.2760655810338,928.2878632968249,1109.3889317161631,1098.4982772006563),c(680.1986677912794,1490.146306871219,2028.7979406648649,1722.0724139143315),c(516.41475549535,2129.9437063865744,2398.2033460460398,1912.2940192552708))
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
targetmat=list(c(156.20672062387564,314.0823597620836,290.83346201438525,433.35253137273594),c(374.77955731773153,229.16379582640914,252.1338481173098,292.2610095304498),c(270.44745660253096,509.51138361404674,111.40797940067178,309.8974497607356),c(53.62320260222597,86.08183193479329,78.57194336678957,45.350846306449114),c(252.37876876917224,405.980531692471,313.1150578945196,532.8724441007771),c(666.7928671407229,613.0422355356225,171.21647360524292,663.8860000971856),c(836.9882493130053,796.8385793963973,348.2965250736791,702.9381177499612),c(133.47514560771464,282.6741237858752,246.27027025411655,316.1961784144091),c(398.0939932317428,735.1853754430994,899.4728442138447,660.1067629049815),c(498.9289285598416,674.6954394889203,618.0211067805686,574.4440532150221),c(311.830580349901,348.98039973564846,804.482882830114,361.5470247208582),c(504.17467664049417,995.7574072457169,561.7307592939135,833.9516737463698),c(123.56651034425984,0.0,32.83603603388221,85.66270968995943),c(336.3107380596129,939.9205432880132,447.9773487479644,511.4567666782872),c(253.5444905648728,426.91935567660994,572.2851994476613,384.2224478740828),c(1234.499381646898,1951.9637025213938,1380.2862289956913,1525.5520799197186),c(848.0626063721608,735.1853754430994,686.0386099936104,583.2622733301649),c(202.83559245189824,255.9189598061422,455.01364218379626,449.72922587228703),c(122.40078854855928,503.6950436184526,660.2388673955601,328.79363572175606),c(512.3347292103981,1299.370355015731,555.8671814307202,733.1720152875939),c(426.07131632855635,1176.0639471091354,654.3752895323669,663.8860000971856),c(487.8545715006863,936.4307392906567,1024.9534104861802,777.2631158633084),c(468.03730097377667,362.93961572507436,899.4728442138447,364.0665161823276),c(914.5087487270929,735.1853754430994,1220.796911116835,971.2639583964518),c(405.08832400594616,757.2874674263571,619.1938223532073,673.9639659430632),c(620.1639953127003,410.6336036889463,163.0074645967724,1730.8906340294743),c(884.7828429367285,652.5933475056626,391.68700126130915,773.4838786711043),c(760.0506107967681,1408.7175469329009,731.7745173265178,986.3809071652681),c(251.79590787132196,201.2453638475573,493.71325608087176,450.9889716030217),c(175.44113025293495,98.8777799251004,371.75083652645213,236.83219737812314),c(732.0732876999546,864.3081233452893,535.9310166958631,1200.5376813901667),c(497.76320676414105,509.51138361404674,320.15135133035153,298.5597381841233),c(516.41475549535,421.1030156810158,653.2025739597282,492.56058071726676),c(615.5011081298981,1354.043950974316,1087.1073358360288,667.6652372893897),c(397.51113233389253,582.7972675585329,436.2501930215779,371.6249905667358),c(257.04165595197446,321.06196775679655,388.16885454339325,554.2881215232669),c(572.9522625868275,1129.5332271443822,1178.5791505018435,808.7567591316758),c(1014.7608231573414,1014.3696952316182,820.9009008470551,1146.3686149685748),c(839.3196929044065,891.0632873250224,863.1186614620466,1250.9275106195546),c(1012.4293795659403,1183.0435551038483,824.4190475649712,590.8207477145731),c(676.7015024041777,1002.7370152404299,1098.8344915624152,862.9258255532678),c(542.6434958986129,942.2470792862508,647.338996096535,377.9237192204093),c(89.76057826894348,46.530719964753125,220.47052765606625,253.2088918776742),c(208.66420143040105,394.34785170128276,318.9786357577129,279.66355222310284),c(686.6101376676326,437.3887676686794,688.3840411388877,1418.4736928072693),c(15.737244241957622,81.42875993831797,100.85353924692392,97.0004212665717),c(308.9162758606496,265.22510379909284,181.7709137589908,273.36482356942935),c(346.21937332306766,460.65412765105594,664.9297296861147,468.6254118333075),c(352.04798230157047,585.1238035567706,695.4203345747196,346.4300759520418),c(405.6711849037965,849.1856393567446,505.4404118072583,600.8987135604507),c(671.4557543235252,902.6959673162106,432.73204630366195,599.6389678297161),c(380.60816629623434,319.8986997576777,444.45920203004846,231.79321445518434),c(402.75688041454504,624.6749155268108,840.8370655819122,348.9495674135112),c(258.207377747675,809.6345273867043,602.7758043362662,681.5224403274714),c(245.38443799496883,76.77568794184266,284.969884151192,142.35126757302083),c(101.41779622594912,151.22483988544766,413.9685971414435,381.70295641261333),c(172.52682576368355,432.7356956722041,344.77837835576315,416.9758368731849),c(340.97362524241515,780.5528274087337,299.0424710228558,335.09236437542955),c(299.5905014950451,487.409291630789,179.42548261371348,331.31312718322545),c(128.2293975270621,169.8371278713489,107.88983268275582,161.24745353404128),c(303.6705277799971,497.87870362285844,428.04118401310734,312.41694122220497),c(85.68055198399149,388.5315117056886,540.6218789864178,118.41609868906157),c(121.23506675285871,258.24549580437986,107.88983268275582,364.0665161823276),c(53.62320260222597,38.38784397092133,154.79845558830183,47.87033776791851),c(157.95530331742648,77.93895594096149,136.0350064260834,194.0008425331434),c(388.185357968288,499.04197162197727,281.45173743327604,258.247874800613),c(510.003285618997,1150.4720511285211,595.7395109004343,845.2893853229821),c(152.70955523677395,321.06196775679655,491.36782493559446,685.3016775196754),c(122.40078854855928,255.9189598061422,263.8610038436963,427.05380271906245),c(118.90362316145759,310.59255576472714,394.03243240658645,275.88431503089873),c(240.1386899143163,328.0415757515095,263.8610038436963,482.48261487138916),c(417.9112637586524,563.0217115735128,234.54311452773004,433.35253137273594),c(93.84060455389545,76.77568794184266,557.0398970033589,379.18346495114395),c(342.72220793596597,545.5726915867305,354.16010293687236,639.9508312132264),c(297.8419188014942,204.73516784491375,385.82342339811595,147.3902504959596),c(1258.3966784587594,2542.9038460737584,1528.0483911481613,1651.5266529931885),c(579.9465933610309,1116.737279154075,899.4728442138447,647.5093055976346),c(549.6378266728162,761.9405394228324,749.3652509160975,622.3143909829406),c(224.98430657020896,457.16432365369946,457.35907332907357,469.8851575640422),c(821.8338659688981,894.5530913223788,691.9021878568036,594.5999849067772),c(0.0,0.0,0.0,0.0),c(153.29241613462423,332.69464774798485,144.24401543455397,248.1699089547354),c(452.88291762966935,267.5516397973305,265.033719416335,380.44321068187867),c(241.30441171001686,324.55177175415304,97.33539252900798,391.78092225849093),c(357.29373038222303,288.4904637814694,562.9034748665521,486.26185206359327),c(483.7745452157343,702.6138714677722,252.1338481173098,553.0283757925322),c(511.16900741469755,898.0428953197353,1182.0972972197594,713.0160835958388),c(258.79023864552533,278.0210517893999,350.6419562189564,1237.070307581473),c(68.19472504848302,137.26562389602174,241.57940796356195,201.5593169175516),c(150.37811164537283,126.79621190395227,198.18893177593188,206.5982998404904),c(197.00698347339542,450.1847156589865,130.17142856289018,177.62414803359235),c(151.5438334410734,335.0211837462225,152.45302444302453,414.45634541171546),c(403.9226022102456,416.4499436845405,576.9760617382159,694.1198976348184),c(0.0,0.0,0.0,0.0),c(122.40078854855928,60.48993595417907,235.7158301003687,196.52033399461283),c(284.4361181509378,353.6334717321238,513.6494208157288,390.5211765277562))
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
targetmat=list(c(612.0039427427964,1918.2289305469476,1639.456370548833,2150.3859623641288),c(479.6945189307823,749.1445914325253,939.3451736835589,2157.944436748537),c(89.1777173710932,809.6345273867043,494.8859716535104,369.1054991052664),c(324.6535201026072,266.38837179821167,927.6180179571724,932.2118407436761))
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
targetmat=list(c(1.1657217957005646,238.46993981935978,62.153925349848464,47.87033776791851),c(391.68252335538966,1008.553355236024,1214.9333332536416,1112.355480238738),c(220.3214193874067,364.1028837241932,209.9160875023184,360.28727899012347),c(353.79656499512134,1290.0642110227805,948.7268982646681,826.3931993619616))
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
targetmat=list(c(337.47645985531346,903.8592353153294,1454.1673100719263,1254.7067478117588),c(576.4494279739291,1616.942518775171,1850.54517362379,1339.1097117709835),c(348.5508169144688,495.5521676246208,1823.5727154531012,852.8478597073903),c(491.351736887788,935.2674712915378,1168.0247103480956,874.2635371298801))
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
targetmat=list(c(365.45378295212697,675.8587074880392,707.1474903011061,998.9783644726151),c(361.9566175650253,1751.8816066729553,899.4728442138447,1006.5368388570233),c(238.39010722076546,273.36797979292464,1164.5065636301797,713.0160835958388),c(128.8122584249124,533.9400115955422,473.7770913460147,599.6389678297161))
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
targetmat=list(c(473.8659099522795,984.1247272545286,992.1173744522981,621.0546452522059),c(345.6365124252174,735.1853754430994,518.3402831062834,710.4965921343694),c(237.2243854250649,829.4100833717245,606.2939510541821,730.6525238261246),c(294.92761431224284,749.1445914325253,1156.2975546217092,476.18388621771567))
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
targetmat=list(c(884.1999820388783,1398.2481349408315,1139.879536604768,632.3923568288182),c(138.72089368836717,1030.6554472192818,629.7482625069551,927.1728578207374),c(67.61186415063274,307.10275176737065,358.85096522742697,182.66313095653115),c(486.6888497049857,1589.0240867963194,1489.3487772510857,912.055909051921))
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
targetmat=list(c(122.98364944640956,244.28627981495393,410.45045042352757,423.2745655268584),c(197.00698347339542,694.4709954739404,330.70579148409934,457.2877002566952),c(154.4581379303248,429.2458916748476,689.5567567115263,478.70337767918505),c(159.12102511312708,538.5930835920175,494.8859716535104,622.3143909829406))
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
Sweave("planted_summary.Rnw");
library(tools);

texi2dvi("planted_summary.tex",pdf=TRUE);

