library(ggplot2)

# Need this for arrange
library(plyr)

movies <- read.csv("data_03.csv")

movies$Kill_Rate <- movies$Body_Count / movies$Length_Minutes

movies$Full_Title <- sprintf("%s (%i)", movies$Film, movies$Year)

arrange(movies, desc(Kill_Rate))

quality_scatter <- ggplot(movies) + aes(x=Year, y=IMDB_Rating, color=MPAA_Rating) + geom_point() + ylab("Average IMDB Rating")
quality_smooth <- ggplot(movies) + aes(x=Year, y=IMDB_Rating) + geom_smooth() + ylab("Average IMDB Rating")
death_hist <- ggplot(subset(movies, MPAA_Rating %in% c("G", "PG", "PG-13", "R"))) + aes(x=Body_Count) + geom_histogram(binwidth=50) + facet_grid(~MPAA_Rating) + scale_y_sqrt() + ylab("Number of Films") + xlab("Number of Deaths")
worst_movies <- ggplot(subset(movies, Kill_Rate > 2)) + aes(x=reorder(Full_Title, Kill_Rate, order=TRUE), y=Kill_Rate, fill=MPAA_Rating) + geom_bar() + coord_flip() + xlab("") + ylab("Deaths per Minute") + labs(fill = "MPAA Rating") + opts(legend.position="bottom") + geom_text(aes(label=sprintf("%0.2f", Kill_Rate)), hjust=1.2, size=3) 

ps <- .8
ggsave(quality_scatter, file="quality_scatter.pdf", scale=ps)
ggsave(quality_smooth, file="quality_smooth.pdf", scale=ps)
ggsave(death_hist, file="death_hist.pdf", scale=ps)
ggsave(worst_movies, file="worst_movies.pdf", scale=ps)
