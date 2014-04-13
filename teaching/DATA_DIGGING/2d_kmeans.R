cluster_labels <- c("A", "B", "C", "D", "E", "F", "G", "H")

# Some simple data and initial means to play with
data_pair <- t(matrix(c(-3,3,-4,3,-4,4,3,-3,4,-3,4,-4),2,6))
pair_init <- data_pair[c(1,2),]
bad_init <- t(matrix(c(-0.5, -2.5, -.5, -4.25, .25, 4.25, 0.25, 2.5), 2, 4))



data_quad <- t(matrix(c(-3,3,-4,3,-4,4,-3,-3,-4,-3,-4,-4,3,3,4,3,4,4,3,-3,4,-3,4,-4),2,12))
quad_init <- data_pair[c(1,2,4,5),]

# Given a dataset, randomly select some of the data points as means
generate_means <- function(data, K) {
	N <- dim(data)[1]
	return(data[sample(1:N, K),])
}

distance <- function(a, b) {
	# Pythagorean theorem
	val <- sqrt((a[1] - b[1])^2 + (a[2] - b[2])^2)
	return(val)
}

closest <- function(observation, means) {
	# Compute the distance from the observation to each mean
	distances <- apply(means, 1, function(row) distance(row,observation))
	closest <- which.min(distances)

	# Return the index of the closes mean (note: ties are
	# broken in favor of lower index)
	return(which.min(distances))
}

kmeans_2d <- function(data, iters, means) {
	# Size of the data
	N <- dim(data)[1]
	K <- dim(means)[1]

  	# For each point, find the closest mean
  	assignments <- apply(data, 1, function(row) closest(row, means))	
  	
  	# Iterate until we have converged
  	for (ii in 1:iters) {  		
  		if (iters > 0) {
 	    for (jj in 1:K) {
 	       # Get the data points assigned to this mean
 	       obs <- subset(cbind(data, assignments), assignments == jj)
 	       
 	       # If there are no observations, set the mean to zero
 	       if (dim(obs)[1] == 0) {
 	         means[jj,] <- c(0.0, 0.0)	
 	       } else {
	 	     # Set the new mean to the observations
 		     means[jj,] <- c(mean(obs[,1]), mean(obs[,2]))
 		   }
 	    }
 	    # For each point, find the closest mean
  		assignments <- apply(data, 1, function(row) closest(row, means))	
 	    }
  	}
  	
  	# return a data frame with the result
  	result <- data.frame(id = 1:N)
  	result$x <- data[,1]
  	result$y <- data[,2]
  	result$assign <- factor(assignments)
  	
  	centers <- data.frame(cluster = 1:K)
  	centers$x <- means[,1]
  	centers$y <- means[,2]
  	
  	return(c(data = result, means = centers))
}

add_path <- function(data_fit, mean_pos, p) {
	x_path <- c()
	y_path <- c()
	
	with_mean <- merge(data_fit, mean_pos, by="assign")
	
	for (ii in 1:nrow(data_fit)) {
		xstart <- with_mean[ii,]$x
		ystart <- with_mean[ii,]$y
		xend <- with_mean[ii,]$mx
	    yend <- with_mean[ii,]$my
		
		x_path <- c(x_path, xstart, xend)
		y_path <- c(y_path, ystart, yend)	

		x_path <- c(x_path, NA)
		y_path <- c(y_path, NA)
		
	}
	path_frame <- data.frame(x=x_path, y=y_path)
		
	p <- p + geom_path(data=path_frame, aes(x=x, y=y))
	return(p)
}

plot_results <- function(res) {
	data_fit <- data.frame(x = res$data.x, y = res$data.y, assign = res$data.assign)
	mean_pos <- data.frame(mx = res$means.x, my = res$means.y, assign = res$means.cluster)
	mean_pos$mjittery <- mean_pos$my + (-1) ^ (1 + mean_pos$assign) / 2	
	mean_pos$mlabel <- sprintf("%s: (%.2f, %.2f)", cluster_labels[mean_pos$assign], mean_pos$mx, mean_pos$my)
	
	p <- ggplot() + geom_point(data=data_fit, aes(x=x,y=y,colour=assign, size=3))
	p <- p + geom_point(data=mean_pos, x=mean_pos$mx, y=mean_pos$my, size=6, shape=5)
	
	p <- p + geom_text(data=mean_pos, aes(x=mx, y=mjittery, label=mlabel))
	p <- p + theme(legend.position = "none") 

	
	p <- add_path(data_fit, mean_pos, p)
	
	p <- p + scale_y_continuous(breaks=-5:5, lim=c(min(data_fit$x) - 1, max(data_fit$x) + 1))
	p <- p + scale_x_continuous(breaks=-5:5, lim=c(min(data_fit$y) - 1, max(data_fit$y) + 1))
	
	return(p)
}

pair_0_plot <- qplot(data_pair[,1], data_pair[,2]) + scale_y_continuous("y", breaks=-5:5, lim=c(min(data_pair[2,]) - 1, max(data_pair[2,]) + 1)) + scale_x_continuous("x", breaks=-5:5, lim=c(min(data_pair[1,]) - 1, max(data_pair[1,]) + 1))

pair_1_res <- kmeans_2d(data_pair, 0, pair_init)
pair_1_plot <- plot_results(pair_1_res)
pair_2_res <- kmeans_2d(data_pair, 1, pair_init)
pair_2_plot <- plot_results(pair_2_res)
pair_3_res <- kmeans_2d(data_pair, 2, pair_init)
pair_3_plot <- plot_results(pair_3_res)

quad_0_plot <- qplot(data_quad[,1], data_quad[,2]) + scale_y_continuous("y", breaks=-5:5, lim=c(min(data_quad[2,]) - 1, max(data_quad[2,]) + 1)) + scale_x_continuous("x", breaks=-5:5, lim=c(min(data_quad[1,]) - 1, max(data_quad[1,]) + 1))
quad_1_res <- kmeans_2d(data_quad, 0, quad_init)
quad_1_plot <- plot_results(quad_1_res)
quad_2_res <- kmeans_2d(data_quad, 1, quad_init)
quad_2_plot <- plot_results(quad_2_res)
quad_3_res <- kmeans_2d(data_quad, 2, quad_init)
quad_3_plot <- plot_results(quad_3_res)
quad_4_res <- kmeans_2d(data_quad, 4, quad_init)
quad_4_plot <- plot_results(quad_4_res)

bad_0_plot <- qplot(data_quad[,1], data_quad[,2]) + scale_y_continuous("y", breaks=-5:5, lim=c(min(data_quad[2,]) - 1, max(data_quad[2,]) + 1)) + scale_x_continuous("x", breaks=-5:5, lim=c(min(data_quad[1,]) - 1, max(data_quad[1,]) + 1))
bad_1_res <- kmeans_2d(data_quad, 0, bad_init)
bad_1_plot <- plot_results(bad_1_res)
bad_2_res <- kmeans_2d(data_quad, 1, bad_init)
bad_2_plot <- plot_results(bad_2_res)
