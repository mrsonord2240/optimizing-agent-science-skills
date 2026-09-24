for (p in c("patchwork","cowplot","gridExtra","ggplot2","ragg","png","gtable","grid","svglite")) cat(p, as.character(packageVersion(p)), "\n")
cat(R.version.string, "\n")
cat(capabilities("cairo"), "\n")
print(.libPaths())
