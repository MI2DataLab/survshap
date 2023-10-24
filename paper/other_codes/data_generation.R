library(rootoned)

# Experiment 1
# data generated with different time-dependent effects
## hazard
h <- function(t, x1, x2, x3, x4, x5, base_hazard_function){
  base_hazard_function(t) * exp((-0.9 + 0.1 * t + 0.9 * log(t)) * x1 
             + 0.5 * x2
             - 0.2 * x3
             + 0.1 * x4 
             + 1e-6 * x5)
}

## CHF
inth <- function(t, x1, x2, x3, x4, x5, base_hazard_function){
  as.numeric(integrate(h, 0, t, x1=x1, x2=x2, x3=x3, x4=x4, x5=x5, base_hazard_function=base_hazard_function)[1])
}

## SF
S <- function(t, x1, x2, x3, x4, x5, base_hazard_function){
  exp(-inth(t, x1, x2, x3, x4, x5, base_hazard_function))
}



generate_dataset <- function(base_hazard_function, seed=42){
    set.seed(seed)
    data <- data.frame()
    survs <- matrix(nrow=0, ncol=100)
    x1 <- rbinom(1000, 1, 0.5)
    x2 <- rbinom(1000, 1, 0.5)
    x3 <- rnorm(1000, 10, 2)
    x4 <- rnorm(1000, 20, 4)
    x5 <- rnorm(1000, 0, 1)
    X = data.frame(x1=x1, x2=x2, x3=x3, x4=x4, x5=x5)
    generated_t <- numeric(1000)
    survs <- matrix(nrow=1000, ncol=100)
    hazards <- matrix(nrow=1000, ncol=100)
    to_drop <- numeric(0)
    for (i in 1:1000){
      u <- runif(1)
      g <- function(t, x1, x2, x3, x4, x5, base_hazard_function){
        S(t, x1, x2, x3, x4, x5, base_hazard_function) - u
      }
      skip_to_next <- FALSE
      tryCatch({
        generated_t[i] <- brent(g, 1e-16, 20, x1=x1[i], x2=x2[i], x3=x3[i], x4=x4[i], x5=x5[i], base_hazard_function=base_hazard_function)$root
      },
      error=function(cond){
        message(i)
        to_drop <<- c(to_drop, i)
        skip_to_next <<- TRUE}
      )
      if(skip_to_next) next
      # survs[i, ] <- sapply(seq(1e-9, 16, length.out=100), S, x1[i], x2[i], x3[i], x4[i], x5[i])
      # hazards[i, ] <- sapply(seq(1e-9, 16, length.out=100), h, x1[i], x2[i], x3[i], x4[i], x5[i])
    }
    
    cl <- runif(1000, 11, 16)
    cr <- runif(1000, 0, 24)
    X$time <- pmin(generated_t, cl, cr)
    X$event <- as.numeric(generated_t < pmin(cl, cr))
    X
  }
  



## baseline hazard function -- EXP1_complex
h0 <- function(t){
  exp(-17.8 + 6.5 * t - 11 * t ^ 0.5 * log(t) + 9.5 * t ^ 0.5)
}

X <- generate_dataset(h0)

# event/censoring times histogram
c1 <- rgb(173,216,230,max = 255, alpha = 80, names = "lt.blue")
c2 <- rgb(255,192,203, max = 255, alpha = 80, names = "lt.pink")
hist(X$time[X$event==1], col=c1)
hist(X$time[X$event==0], col=c2, add=TRUE, breaks=0:16)

# number of events vs x1 variable
table(cut(X$time[X$event==1], breaks = c(0, 2, 4, 6, 8, 10, 12, 16)), X$x1[X$event==1])

# survival curves
fit <- survival::survfit(survival::Surv(time, event)~x1, data=X)
survminer::ggsurvplot(fit, data=X, pval = TRUE)
# write.csv(X, "data/exp1_data_complex.csv", row.names = FALSE)



## baseline hazard function -- EXP1_Weibull
h0 <- function(t){
  1.2 * 0.1 * t ^ (1.2 - 1)
}

X <- generate_dataset(h0)

# event/censoring times histogram
c1 <- rgb(173,216,230,max = 255, alpha = 80, names = "lt.blue")
c2 <- rgb(255,192,203, max = 255, alpha = 80, names = "lt.pink")
hist(X$time[X$event==1], col=c1)
hist(X$time[X$event==0], col=c2, add=TRUE, breaks=0:16)

# number of events vs x1 variable
table(cut(X$time[X$event==1], breaks = c(0, 2, 4, 6, 8, 10, 12, 16)), X$x1[X$event==1])

# survival curves
fit <- survival::survfit(survival::Surv(time, event)~x1, data=X)
survminer::ggsurvplot(fit, data=X, pval = TRUE)
# write.csv(X, "data/exp1_data_exponential.csv", row.names = FALSE)



## baseline hazard function -- EXP1_exponential
h0 <- function(t){
  0.08
}

X <- generate_dataset(h0)

# event/censoring times histogram
c1 <- rgb(173,216,230,max = 255, alpha = 80, names = "lt.blue")
c2 <- rgb(255,192,203, max = 255, alpha = 80, names = "lt.pink")
hist(X$time[X$event==1], col=c1)
hist(X$time[X$event==0], col=c2, add=TRUE, breaks=0:16)

# number of events vs x1 variable
table(cut(X$time[X$event==1], breaks = c(0, 2, 4, 6, 8, 10, 12, 16)), X$x1[X$event==1])

# survival curves
fit <- survival::survfit(survival::Surv(time, event)~x1, data=X)
survminer::ggsurvplot(fit, data=X, pval = TRUE)
# write.csv(X, "data/exp1_data_exponential.csv", row.names = FALSE)



## baseline hazard function -- EXP1_non_td
h0 <- function(t){
  exp(-17.8 + 6.5 * t - 11 * t ^ 0.5 * log(t) + 9.5 * t ^ 0.5)
}

h <- function(t, x1, x2, x3, x4, x5, base_hazard_function){
  base_hazard_function(t) * exp(1 * x1 
                                + 0.5 * x2
                                - 0.2 * x3
                                + 0.1 * x4 
                                + 1e-6 * x5)
}


X <- generate_dataset(h0)

# event/censoring times histogram
c1 <- rgb(173,216,230,max = 255, alpha = 80, names = "lt.blue")
c2 <- rgb(255,192,203, max = 255, alpha = 80, names = "lt.pink")
hist(X$time[X$event==1], col=c1)
hist(X$time[X$event==0], col=c2, add=TRUE, breaks=0:16)

# number of events vs x1 variable
table(cut(X$time[X$event==1], breaks = c(0, 2, 4, 6, 8, 10, 12, 16)), X$x1[X$event==1])

# survival curves
fit <- survival::survfit(survival::Surv(time, event)~x1, data=X)
survminer::ggsurvplot(fit, data=X, pval = TRUE)
# write.csv(X, "data/exp1_data_non_td.csv", row.names = FALSE)




# Experiment 2
# SurvLIME datasets
generate_from_random_ball <- function(num_points, dimension, radius){
  random_directions <- matrix(rnorm(num_points*dimension), ncol = dimension)
  random_directions <- random_directions / apply(random_directions, 1, norm, type="2")
  random_radii = runif(num_points) ^ (1/dimension)
  t(radius * t(random_directions * random_radii))
}

N <- 1000
dim <- 5
radius <- 8

X0 <- generate_from_random_ball(N, dim, radius)
X1 <- generate_from_random_ball(N, dim, radius)
X1 <- X1 + c(4, -8, 2, 4, 2)[col(X1)]


beta0 <- c(1e-6, 0.1, -0.15, 1e-6, 1e-6)
beta1 <- c(1e-6, -0.15, 1e-6, 1e-6, -0.1)
lambda <- 1e-5
v <- 2


times0 <- numeric(1000)
times1 <- numeric(1000)
for (i in 1:1000){
  times0[i] <- (- log(runif(1)) / (lambda * exp(beta0 %*% X0[i, ])))^(1/v)
}
for (i in 1:1000){
  times1[i] <- (- log(runif(1)) / (lambda * exp(beta1 %*% X1[i, ])))^(1/v)
}

event0 <- rbinom(1000, 1, 0.9)
event1 <- rbinom(1000, 1, 0.9)

X0$time <- times0
X1$time <- times1

X0$event <- event0
X1$event <- event1

# write.csv(X, "data/exp2_dataset0.csv", row.names = FALSE)
# write.csv(X, "data/exp2_dataset1.csv", row.names = FALSE)



