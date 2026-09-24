pdf(file='r2_new2_paired_test.pdf',width=4.5,height=4.5);
gstable=read.table('r2_new2_paired_test.gene_summary.txt',header=T)
# 
#
# parameters
# Do not modify the variables beginning with "__"

# gstablename='__GENE_SUMMARY_FILE__'
startindex=3
# outputfile='__OUTPUT_FILE__'
targetgenelist=c("GENE4","GENE6","GENE2","GENE7","GENE3","GENE1","GENE0","GENE5","GENE9","GENE8")
# samplelabel=sub('.\\w+.\\w+$','',colnames(gstable)[startindex]);
samplelabel='D0_treat,D1_treat,D2_treat,D3_treat,D4_treat,D5_treat_vs_D0_baseline,D1_baseline,D2_baseline,D3_baseline,D4_baseline,D5_baseline neg.'


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
targetmat=list(c(301.77243904165573,72.2194134312481),c(248.27615418773715,86.49635858300971),c(283.0039626694863,101.67959763200622),c(307.5516725696634,92.40286716937695),c(267.7253498199872,84.13390835956312),c(281.80417131048995,108.0896152938164),c(356.3096268202682,114.03065278618121),c(342.3495407354344,101.58293275446489),c(363.9628077117523,110.39499171474961),c(366.34831585504025,98.251149901616),c(345.1147087523272,103.54942567330846),c(318.075995340553,100.78626290909908),c(336.91862672120595,84.889485963046),c(301.6167341890088,95.54830308588282),c(304.1236613761644,96.5956177504059),c(287.1989883554945,85.3849278906901),c(283.76098275191345,82.69572189187828),c(323.6562759605627,90.56156957049483),c(352.67381430169405,106.42860926710246),c(371.4444025543099,112.64642048019869),c(363.9628077117523,115.47897159634992),c(347.1263363194363,122.81393737702),c(377.1859746161798,122.24584975321137),c(369.6935910756427,118.31430863242065))
targetgene="GENE4"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(327.2231266716749,106.42860926710246),c(314.22450764385485,95.54830308588282),c(320.3154303846176,95.14305206994868),c(334.68858485522196,88.89389753003351),c(317.2266514794118,101.3921459717812),c(322.2612058055603,121.23564958630759),c(330.85893919024903,98.82656574802371),c(321.0133087349258,99.5713895316042),c(302.0116915054966,104.58472899292069),c(336.94999421235184,90.06355407648132),c(310.9518385930059,87.0102812949328),c(322.2612058055603,100.78626290909908),c(380.54837694409593,112.76364553300141),c(352.0478280083929,121.6983649830718),c(354.10694831530253,109.668708874521),c(381.04747667638446,92.40286716937695),c(373.6999674570654,109.30217154404782),c(327.84148642556994,111.01095624770333),c(367.2170643759907,122.89970355843974),c(372.41423128160574,117.67527853735042),c(365.37078762553085,133.63604260206532),c(360.69479246221556,112.28702845898971),c(326.2902700931093,115.7740106486296),c(348.7675387506063,115.39296767853372))
targetgene="GENE6"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(344.1902517583543,102.62758750756308),c(332.65125346247595,108.62333403447731),c(327.3553299535103,115.47897159634992),c(345.99563164087135,79.53664515845105),c(347.9035144796187,107.14489184252056),c(315.28585503054813,97.86492195521214),c(405.9990645741151,126.7007253179791),c(375.32371746349327,136.78493915452697),c(413.24210469400117,124.19436567909332),c(398.00804685485855,134.5105028414981),c(381.3691832071171,128.71768885779315),c(405.9654151057058,121.23564958630759),c(292.0769389921246,101.3605802543833),c(285.1296458249794,115.66373531448973),c(292.15583210904686,99.50074911132037),c(323.38153806957257,90.06355407648132),c(318.6210543430576,87.72937452877522),c(295.7548728605142,113.93229720159026),c(372.06481440075623,115.29766003936099),c(346.2288556446178,113.65219209162903),c(363.9628077117523,120.56295147795024),c(386.70100006920916,104.09943263385505),c(369.5167588661281,130.155875325478),c(337.60697751058694,129.99967244796838))
targetgene="GENE2"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(340.55443923978015,102.62758750756308),c(354.95731419028044,101.58293275446489),c(323.83538016906397,97.32190059063453),c(342.60351760517653,86.5545844371379),c(337.44549300227544,97.07758656872669),c(320.86613565055785,100.78626290909908),c(465.3840023774932,146.97284136885577),c(455.81950182904865,146.84265526883044),c(406.90619508199774,137.993739643437),c(460.1968041759302,146.20706830597618),c(448.9977220939368,148.8522994053809),c(458.97808099579794,135.84235435574223),c(431.44975220413426,127.9677325711589),c(422.84532510098984,144.83111204596975),c(393.5303859011016,137.993739643437),c(404.7922749262482,138.01947248084153),c(422.50406768466723,125.12222268858106),c(359.92809999062575,134.38168387879875),c(306.6201890664213,101.3605802543833),c(268.64255746094994,92.53098825159178),c(313.9795207726142,97.32190059063453),c(308.68237724822836,100.59046299451161),c(331.8678815476924,98.51577303641152),c(299.94008332552147,86.17955813966442))
targetgene="GENE7"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(414.48262711745485,107.69561652028224),c(361.74611528135136,113.65219209162903),c(432.9538234869007,117.65782011703577),c(428.5370731761119,153.22500758466305),c(401.5880247299807,151.7286723407506),c(392.0147135556815,115.39296767853372),c(386.6080644750529,92.49152948212475),c(343.31936946273026,114.65796370305938),c(368.18674745308795,112.57384023543547),c(332.4271754980921,125.15325046991562),c(347.20631304779585,104.26851890715088),c(393.40978371068394,119.77497910936412),c(379.3364394379046,138.10379059659724),c(429.63412619206076,141.81379721167872),c(435.0657933575685,137.2674568032084),c(421.75284510472227,115.79599809833314),c(415.5320533664384,126.56040915626589),c(458.97808099579794,129.99967244796838),c(380.54837694409593,119.09868179890037),c(378.2332036453808,105.60601920018627),c(398.4583155993265,118.38410295726439),c(381.04747667638446,107.60840227319846),c(368.1223560024823,125.12222268858106),c(396.1999240206888,127.07833149408144))
targetgene="GENE3"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(395.0916270183926,146.97284136885577),c(387.9314909183393,149.85997010312147),c(382.9705365477626,119.83666863772162),c(393.4852281405988,125.15325046991562),c(391.82720468446036,113.61673094710234),c(398.99006433069366,143.14570674045956),c(315.103751609761,110.22963102664183),c(331.6814247351801,116.66950692592007),c(290.7478521952683,92.96420354926283),c(326.7736521052674,111.1173719125419),c(311.64904002482876,92.04393393182974),c(290.17459224050447,96.40425147826868),c(398.7274395369668,149.50685587521536),c(429.63412619206076,119.6868217602111),c(414.6500846077797,123.4680828388647),c(421.75284510472227,121.64428083057219),c(402.9824275936265,132.31315502700525),c(408.75555541571066,146.06704769434648),c(359.94543933884233,131.76875433069827),c(403.4487505550729,119.6868217602111),c(363.25881775486306,133.63604260206532),c(357.30267842652074,125.15325046991562),c(366.72795313883654,127.99859562395073),c(373.87880154065,121.23564958630759))
targetgene="GENE1"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(403.5751895617323,111.49663827982162),c(382.1125185545642,118.68105014878076),c(366.0747775824201,121.28923431817886),c(377.65536264068965,116.96565464478095),c(385.55239179805443,119.3694768178417),c(386.43443293567185,113.93229720159026),c(500.5301900570434,149.50685587521536),c(482.0048774660366,154.8888281602732),c(405.4982151682192,131.45719408137947),c(464.71962289018995,133.34084629505028),c(484.5549951169038,158.9196046791748),c(458.97808099579794,163.59509341766807),c(339.34250173358873,105.16160201392266),c(327.8021098259967,98.56561792017385),c(313.2755308157249,116.93153727680716),c(318.8587193553128,105.26908918030286),c(331.1706801158695,107.14489184252056),c(344.5823282855991,118.31430863242065),c(386.6080644750529,116.56466729254079),c(373.3840600089016,129.74453787451455),c(344.95507887574206,111.12127455497823),c(430.7984825332418,113.45668500543752),c(401.5880247299807,114.33582418094475),c(372.48373138564756,125.61766101713798))
targetgene="GENE0"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(349.03800178311985,105.16160201392266),c(367.5650876451265,119.6868217602111),c(400.5702854699943,107.48986035383516),c(359.5640877836506,113.45668500543752),c(355.5727302296704,122.96494298705379),c(352.9527492156136,100.78626290909908),c(438.7213772412826,130.50174707751847),c(464.5479603747113,155.89459977170355),c(487.16105016737447,143.80400236526594),c(514.4706287470473,139.18912902728934),c(500.5906280488301,152.447765574593),c(484.0893437858416,157.75241150989422),c(425.39006467317733,120.36568905208016),c(457.7591592836404,148.85419849169114),c(430.1378636593436,143.07771952503734),c(421.75284510472227,139.18912902728934),c(388.34119752534593,153.16685880843542),c(425.49639727573975,143.14570674045956),c(477.503377439407,131.76875433069827),c(414.1168665553272,125.72145142879317),c(416.05806452155826,143.80400236526594),c(386.70100006920916,123.98359392346781),c(399.49642043451206,131.59406179316284),c(397.5949941756912,129.99967244796838))
targetgene="GENE5"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(379.3364394379046,129.2347398243387),c(399.5694356458895,136.78493915452697),c(397.05033568554796,119.11038579749301),c(381.04747667638446,126.32290701636342),c(402.2852261618036,115.05491741478718),c(357.1379596806209,134.38168387879875),c(521.133127662297,136.83678334341744),c(505.28076692113694,150.8657417145518),c(484.3450903398174,156.87709348938102),c(490.72583049718355,162.5822599562455),c(512.4430523898192,178.33512199292014),c(475.71892285582703,151.90972960212034),c(358.733501832651,115.29766003936099),c(332.65125346247595,107.61756242304696),c(364.6667976686416,113.30012307566408),c(345.99563164087135,114.62634155188533),c(370.9111617297739,96.35849333488426),c(397.5949941756912,102.24693338604254),c(358.733501832651,115.29766003936099),c(368.53491637242234,105.60601920018627),c(372.41068719442353,98.77446627109177),c(356.1719737479558,98.251149901616),c(381.3691832071171,127.27950239010832),c(341.79218797559423,109.55028577075987))
targetgene="GENE9"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(478.71531494559844,155.8418921411143),c(448.06087201068186,147.84842688026077),c(469.5613012451427,150.34054792732348),c(464.71962289018995,161.4126034097977),c(469.91376504862325,153.16685880843542),c(447.81751975577856,167.97710484849847),c(275.10981390544515,91.22452222894496),c(296.76759055252955,91.52521664016143),c(283.7079526263756,87.1539408274339),c(267.97700881989056,78.36698861200324),c(285.8525870473821,85.57209482724797),c(285.9893817754972,99.32559243215562),c(485.9869399827468,146.97284136885577),c(505.28076692113694,134.7733959316663),c(478.00918072781394,161.96107337098135),c(476.02666967583934,150.88569449176742),c(499.19622518518435,148.1332061715385),c(478.5090631658319,160.67375246378114),c(338.1305642273974,116.56466729254079),c(338.470225826251,103.59447597732559),c(333.69123956551374,103.13216331246346),c(368.60972521217013,116.96565464478095),c(363.2419459797221,107.86398507636298),c(368.29852092064027,94.94358100132521))
targetgene="GENE8"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetgenelist=c("GENE23","GENE22","GENE26","GENE12","GENE10","GENE37","GENE28","GENE33","GENE36","GENE18")
# samplelabel=sub('.\\w+.\\w+$','',colnames(gstable)[startindex]);
samplelabel='D0_treat,D1_treat,D2_treat,D3_treat,D4_treat,D5_treat_vs_D0_baseline,D1_baseline,D2_baseline,D3_baseline,D4_baseline,D5_baseline pos.'


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
targetmat=list(c(382.9722519564787,407.9763355238927),c(379.20303237267666,371.1297246177975),c(399.1623055562158,371.1305313568227),c(408.184388961943,371.9507817704034),c(394.61601041175186,402.6922109517551),c(405.9654151057058,338.87555065088384),c(404.78712706792373,509.336915778276),c(440.3022421923151,472.71265737226236),c(463.2253916331393,516.3870994025459),c(444.36693867602105,480.7288405900497),c(447.603319230291,483.94974637594856),c(460.37315115080037,479.0999164374565),c(427.8139396855601,419.3794008025109),c(411.20738037343966,429.4644780807575),c(451.961552322911,452.4742094624277),c(399.1387515334235,446.8088007430632),c(421.10966482102145,416.3549823947611),c(383.644292625667,502.4706440685519),c(271.474001386871,316.7518132949478),c(283.1899883703877,309.7776563205464),c(249.2124447388014,309.39648993739036),c(303.02885385540367,280.71757114747425),c(282.36657988826767,291.95185294002243),c(283.1992414654924,292.13409538869297))
targetgene="GENE23"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(416.90650212983763,430.782466081129),c(388.90131964563517,433.4875645264789),c(403.3862452975514,461.1896035451711),c(403.66157024768324,439.79086146437635),c(405.77123332091804,398.3776515487006),c(375.2738716956524,419.2124268827744),c(340.55443923978015,424.44742981523),c(405.38840800966454,421.41830518931476),c(433.65781344378996,418.33891597168275),c(383.30888603351434,476.05021440425844),c(377.1859746161798,424.98410120087016),c(390.6196434006791,460.11120023719144),c(289.65306397974183,264.80451591457637),c(250.21581164232884,301.7314834291036),c(286.52391245393267,286.88172189030325),c(329.03506146239727,285.3961973332655),c(307.4658314338915,303.4573446815012),c(276.22389069048023,322.80817540450573),c(298.13662652308153,337.02392934582446),c(317.1339938257424,360.06623689206367),c(332.2832596517352,355.1523088717932),c(323.38153806957257,297.0927627977436),c(335.3538887068068,334.3783537367252),c(297.1499430155166,318.42616397367533))
targetgene="GENE22"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(407.2110020803065,350.96100913080215),c(383.08234728186005,433.4875645264789),c(394.2343758579909,392.91901656368117),c(352.779859712261,439.79086146437635),c(382.06638463894,415.6358891609187),c(352.9527492156136,445.5044954677568),c(458.11237734034484,487.7977924742196),c(453.879844374457,437.51065097220027),c(453.3695322366895,444.4850982199129),c(427.40636849754696,483.0681536829453),c(454.57533354851984,460.21966965914874),c(424.1013271207373,433.8191316522091),c(302.9843765478471,314.2177987885882),c(325.862452371405,320.8411440462802),c(260.4762840490297,305.03879289601866),c(299.63673981970885,293.58379315840017),c(297.70501138837113,320.71558229371925),c(280.4091011554875,331.57219826616654),c(445.99300227843094,471.3266981828823),c(444.18155710149847,404.32018779499884),c(402.68225534066215,459.01075502448526),c(481.68019306866404,481.8984971364975),c(443.4201106393537,482.51155990826373),c(386.43443293567185,433.8191316522091))
targetgene="GENE26"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(289.65306397974183,333.2229075862851),c(297.7374192798254,294.6910821490912),c(307.64361116061076,332.6375408247061),c(299.63673981970885,326.3341764589388),c(306.0714285702457,304.895531149186),c(305.52036394553113,319.8868344506188),c(386.6080644750529,387.7042194730161),c(363.6857727359431,384.20475556639195),c(360.44285792730597,432.86457277625505),c(401.40016089055337,430.43360909279386),c(412.04604620732397,354.512964284313),c(390.6196434006791,368.08896018975315),c(404.78712706792373,419.3794008025109),c(408.29789419155213,431.4760213036182),c(413.24210469400117,393.6452994039098),c(391.2238187834689,435.1122352785851),c(406.4684347527409,412.0404229917066),c(431.0766778957494,408.98773354417017),c(332.07087669644045,368.6991106753192),c(355.9271429175763,404.32018779499884),c(354.81093827219183,398.0029964452815),c(365.2176111764753,395.3439126993596),c(385.55239179805443,355.95115075199783),c(322.2612058055603,430.8977906983221))
targetgene="GENE12"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(327.2231266716749,330.6888930799255),c(316.1641650984465,309.7776563205464),c(322.4274002552854,322.46958106150544),c(289.4603977126244,332.1824591911779),c(313.74064432029746,306.33371761687084),c(332.0266968905772,290.6734249117495),c(376.9125644255218,406.70932827071294),c(385.9918334637476,413.372132297872),c(380.1545767202055,424.14917869351166),c(376.5246579621247,433.9425787321373),c(390.4328018208146,391.9058124441188),c(394.80485386568637,410.4484040211136),c(381.76031445028735,397.84027749845444),c(385.9918334637476,400.2971013492775),c(391.41841603043383,380.5722082797947),c(362.95620181934544,354.4059335736863),c(389.0383989571688,397.65855831485817),c(323.6562759605627,385.6170059130747),c(276.32175141163657,296.47969724407113),c(289.00896073416277,309.7776563205464),c(294.26780197971465,309.39648993739036),c(297.375330462579,298.2624193441914),c(307.4658314338915,299.14278527844664),c(258.0879786754487,338.87555065088384))
targetgene="GENE10"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(450.8407523031965,444.71954586610667),c(452.9100156471611,475.7299722065534),c(443.51367284023974,453.92677514288494),c(465.8503275687549,459.67502275398914),c(419.7152619573757,461.65785612683356),c(429.68160774074704,461.5718707141349),c(392.66775200600983,419.3794008025109),c(436.4229272831317,488.80500315514786),c(433.65781344378996,454.65305798311357),c(438.71341528319635,459.67502275398914),c(411.3488447755011,438.6468726438761),c(458.97808099579794,435.27980212915253),c(369.64093938837345,394.039255738915),c(370.474573827014,376.1585826749492),c(379.45058676331627,413.2549360900824),c(395.74663749772867,407.0404781638377),c(370.9111617297739,395.5012786133309),c(397.5949941756912,446.96516594470023),c(362.3693143512251,391.5052412325555),c(403.4487505550729,338.9450330520264),c(384.37851646154115,366.772834315451),c(345.99563164087135,352.0666204807907),c(377.1859746161798,375.36666806574317),c(347.3724685956039,438.2011430830395))
targetgene="GENE37"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(496.89437753846926,499.2008577528377),c(464.5479603747113,445.55682386364305),c(436.47377327134706,485.1569372727154),c(496.37935389000825,457.3357096610935),c(454.57533354851984,475.32062756983953),c(470.1386422358174,452.8078478524741),c(382.9722519564787,409.24334277707254),c(405.38840800966454,405.3259594064292),c(411.1301348233334,406.7183905280249),c(414.96861703333263,415.22807398897237),c(406.4684347527409,442.2423388130882),c(389.22457324567665,419.2124268827744),c(357.52156432645955,366.1650961689596),c(380.1728610999725,392.25092845783473),c(366.0747775824201,354.42602603156456),c(365.2176111764753,355.57559012013405),c(359.05873738878483,379.68122746879766),c(378.0640120056573,363.70694875892275),c(317.52762662214377,342.0919583585436),c(284.1598170976835,331.904631772014),c(297.787751764161,313.0279041385335),c(265.7155994627607,340.37005501631256),c(294.9162056610796,326.4683281644586),c(272.03868022547294,321.3475049275623))
targetgene="GENE28"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(505.37794008180896,468.7926836765227),c(508.1902531030245,574.2955901267272),c(504.0568091327169,542.5332816507761),c(526.9083802112616,538.0420113659924),c(528.4786853217455,563.7690953324571),c(493.85483487085855,595.9535545929336),c(476.29143993321566,492.8658214869387),c(452.9100156471611,480.75883026370514),c(488.569030081153,453.2004923026563),c(465.8503275687549,519.3275066228274),c(453.878132116697,493.29795841590004),c(502.22525580087313,430.8977906983221),c(353.8857518078854,345.89298011808296),c(373.3840600089016,369.11818139493676),c(365.37078762553085,350.7946118304215),c(335.8192895337869,342.7093681092082),c(360.4531402524306,345.88384547820397),c(340.3971178205918,318.42616397367533),c(438.7213772412826,440.9185241065673),c(464.5479603747113,465.67225609224994),c(445.6256427109076,446.66394674059876),c(435.32130124750154,436.2818918250329),c(416.22925479826125,417.79316886244595),c(442.23723913576885,482.0212573913434))
targetgene="GENE33"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(379.3364394379046,397.84027749845444),c(396.65994946400195,407.33750262928993),c(394.2343758579909,380.5722082797947),c(416.0993217118976,418.7370436283158),c(385.55239179805443,366.73754925963414),c(357.1379596806209,369.5496306666966),c(402.36325205554095,447.25356037246627),c(466.487617829303,441.53373741792166),c(423.09796409045094,422.69661301305445),c(418.36073106902745,437.4515483714807),c(421.8068662528443,457.343296723779),c(403.17527479570094,461.5718707141349),c(464.17206487130176,439.65151685338753),c(425.75481128287737,466.6780277036803),c(469.5613012451427,426.3280272141975),c(393.4852281405988,485.40746677584093),c(440.63130491206215,450.1523643853548),c(412.9407658807179,487.86393929911725),c(396.30356452458403,428.2484515747694),c(402.478921827777,417.3952187435934),c(431.54584357312217,402.3606934866532),c(411.5765029976378,444.4694876501676),c(426.6872762756045,428.57956737008226),c(400.3851344856961,414.830415451944))
targetgene="GENE36"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
targetmat=list(c(332.07087669644045,339.557943852184),c(348.1685130992095,357.04892205777264),c(342.8431090050742,335.5426721856205),c(340.34210824804666,326.3341764589388),c(362.54474454789926,322.8728619952465),c(319.4710654955554,392.92035829779206),c(443.56912726604816,415.5783790429715),c(438.3625847377234,429.4644780807575),c(360.44285792730597,416.88635029122554),c(419.4914357475924,481.8984971364975),c(370.21396029795096,373.92848159805834),c(393.40978371068394,417.751756405831),c(513.8615026251487,518.2059665505345),c(505.28076692113694,503.89157732660306),c(530.8084274945091,530.9127562071183),c(489.5951258186186,502.9523149725581),c(494.3158151624242,516.3089418988575),c(492.4597647158562,496.62796216077805),c(288.4411264735504,293.94568273771154),c(257.97444146069563,294.6910821490912),c(298.49174172105023,303.58622721556145),c(280.4147602841049,287.7355104261611),c(278.1833712973304,280.44636119854374),c(277.61896084548266,297.9767772964668))
targetgene="GENE18"
collabel=c("D0_baseline","D1_baseline","D2_baseline","D3_baseline","D4_baseline","D5_baseline","D0_treat","D1_treat","D2_treat","D3_treat","D4_treat","D5_treat")

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
Sweave("r2_new2_paired_test_summary.Rnw");
library(tools);

texi2dvi("r2_new2_paired_test_summary.tex",pdf=TRUE);

