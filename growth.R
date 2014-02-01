## Set up the plotting
pdf("/tmp/growth.pdf")

## Set up the data
x <- seq(0.1, 50, .1)
y <- x*log(x)
z <- x*x

## Plot the data
plot(x, y, type='l', col="blue")
lines(x, x, col="green")
lines(x, z, col="red")
abline(v=0, h=0)

## Embellishments
legend(20, 180,
       c(expression(x),
         expression(x %.% log * phantom(i) * x), # Hack to get the spacing right
         expression(x^2)),
       col=c("green", "blue", "red"),
       lty=c("solid","solid","solid"))

## Shutoff the plotting
dev.off()
