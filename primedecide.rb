#!/usr/bin/ruby

# = primedecide.rb - test test
# test
# test

# We start from 2, and go up one by one
def stupid_1_isprime? n
  return false if n <= 1

  cand = 2
  isprime = true

  while isprime && cand < n do
    if n % cand == 0
      isprime = false
    end
    cand += 1
  end

  return isprime
end


# We start from 3, go up 2 by 2 and up to the square root of n
def stupid_2_isprime? n
  return false if n <= 1
  return true if n == 2
  return false if n % 2 == 0

  cand = 3
  isprime = true

  while isprime && cand*cand <= n do
    if n % cand == 0
      isprime = false
    end
    cand += 2
  end

  return isprime
end


# We start from 5, go up in alternating steps of 2 and 4, and only up to the
# square root of n.
def stupid_3_isprime? n
  return false if n <= 1
  return true if n == 2
  return false if n % 2 == 0
  return true if n == 3
  return false if n % 3 == 0

  cand = 5
  isprime = true
  step = 4

  while isprime && cand*cand <= n do
    if n % cand == 0
      isprime = false
    end
    step = 6 - step
    cand += step
  end

  return isprime
end


# We start from 5, go up in alternating steps of 2 and 4, and only up to the
# square root of n.
def stupid_4_isprime? n
  return true if n == 2 || n == 3
  return false if n <= 1 || n % 2 == 0 || n % 3 == 0

  cand = 5
  step = 4

  while cand*cand <= n do
    return false if n % cand == 0
    step = 6 - step
    cand += step
  end

  true
end


# Main entry point of the program
return if ARGV.length == 0

candidate = Integer(ARGV[0])

puts "#{candidate} is prime: #{stupid_1_isprime? candidate}"
puts "#{candidate} is prime: #{stupid_2_isprime? candidate}"
puts "#{candidate} is prime: #{stupid_3_isprime? candidate}"
puts "#{candidate} is prime: #{stupid_4_isprime? candidate}"
