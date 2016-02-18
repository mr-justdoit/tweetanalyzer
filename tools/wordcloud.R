#!/usr/bin/Rscript

args <- commandArgs(TRUE)

library("yaml")
library("wordcloud")

data <- data.frame(yaml.load_file(args[1]))
png(args[2])
wordcloud(colnames(data), data, colors=brewer.pal(8, "Dark2"))
dev.off()
