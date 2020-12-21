dx = 8
dy = 2.5

ground = box(pos = vector(0, 0, 0), size = vector(5, 0.2, 1), color = color.green)
ball1  = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball2  = sphere(pos = vector(dx, dy, 0), radius = 0.2, color = color.red)

calculatespeed = 1
tickinterval = 0.015

g = vector(0, -600, 0)
dragdiv  = 40

caliber  = 120
mass     = 0.01
dragcoef = (pi*caliber**2)/(4000000*mass*dragdiv)

muzzleVel = 100
dt = 0.0005
m = -0.1

def toRad(th) : return th*(pi/180)
def toDeg(th) : return th*(180/pi)
def length(v1, v2) : return sqrt(v1**2 + v2**2)

# Runge Kutta 4 Method
def rk4(th) :
  p = vector(0, 0, 0)
  v = vector(muzzleVel*cos(th), muzzleVel*sin(th), 0)
  i = 0
  while 1 :
    rate(calculatespeed*1000)
    
    k = length(v.x, v.y)*dragcoef
    
    vel1 = v
    acc1 = g - k*vel1
    
    vel2 = vel1 + acc1*dt/2
    acc2 = g - k*vel2
    vel3 = vel1 + acc2*dt/2
    acc3 = g - k*vel3
    
    vel4 = vel1 + acc3*dt
    acc4 = g - k*vel4
    
    p = p + (dt/6)*(vel1 + 2*(vel2 + vel3) + vel4)
    v = v + (dt/6)*(acc1 + 2*(acc2 + acc3) + acc4)
    ball1.pos = p
    i += 1
    time = i*tickinterval
    
    limit = (dy/dx)*p.x + m
    
    if p.x > dx | p.y < limit :
      endpos = p
      break
  return endpos

def solve(mod, tolerance) :
  if mod == 1 :
    faz   = 90
    sign = -1
  else :
    faz   = 0
    sign = 1
  angle = faz
  theta = toRad(angle)
  
  loopcount = 0
  
  while abs(dx - ball1.pos.x) + abs(dy - ball1.pos.y) >= tolerance :
    endPos = rk4(theta)
    
    errX = dx - endPos.x
    errY = dy - endPos.y
    cor = errX + errY
    
    angle += cor*sign
    theta = toRad(angle)
    
    if angle > 90 | dy > 0 & angle < 0 :
      print("can't solve")
      break
    
    loopcount += 1
  
  print(toDeg(theta), "/", loopcount)
  return theta

tolerance = 0.1

mod   = 0
theta1 = solve(mod, tolerance)
ball1.pos = vector(0, 0, 0)

mod   = 1
theta2 = solve(mod, tolerance)
