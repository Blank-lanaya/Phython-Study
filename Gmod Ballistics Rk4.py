dx = 8
dy = 2

box1 = box(pos = vector(0, 0, 0), size = vector(5, 0.2, 1), color = color.green)
ball1 = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball2 = sphere(pos = vector(dx, dy, 0), radius = 0.2, color = color.red)

calculatespeed = 1

gravity = 600
g = vector(0, -gravity, 0)

dragdiv  = 40
caliber  = 120
mass     = 0.01
dragcoef = (pi*caliber**2)/(4000000*mass*dragdiv)

muzzlevel = 100

dt = 0.0005
m = -0.1

kp = 2
ki = 0.75
kd = 0.5
pidDt = 0.1

def toRad(th) : return th*(pi/180)
def toDeg(th) : return th*(180/pi)
def length(v1, v2) : return sqrt(v1**2 + v2**2)

def clamp(n, min, max) :
  if n < min : n = min
  if n > max : n = max
  return n

# Quadratic formula solver
def tth(mod) :
  if mod == 1 :sign = 1
  else : sign = -1
  
  root = (muzzlevel**4 - gravity*(gravity*dx**2 + 2*dy*muzzlevel**2))
  tangent = (muzzlevel**2 + sign*sqrt(root))/(gravity*dx)
  
  return toDeg(atan(tangent))

# Runge Kutta 4 method
def rk4(th) :
  p = vector(0, 0, 0)
  v = vector(muzzlevel*cos(th), muzzlevel*sin(th), 0)
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
    
    limit = (dy/dx)*p.x + m
    
    if p.x > dx | p.y < limit :
      endpos = p
      break
  return endpos

def solve(mod, tolerance) :
  if mod == 1 : sign = -1
  else : sign = 1
  
  angle = tth(mod)
  theta = toRad(angle)
  
  loopcount = 0
  i = preverr = 0
  print("first angle:", angle)
  while abs(dx - ball1.pos.x) + abs(dy - ball1.pos.y) >= tolerance :
    endPos = rk4(theta)
    
    errX = dx - endPos.x
    errY = dy - endPos.y
    err = clamp(errX + errY, -20, 20)
    
    p = err
    i = i + p*pidDt
    d = (p - preverr)/pidDt
    preverr = err
    
    pidcontrol = p*kp + i*ki + d*kd*0.1
    
    angle += pidcontrol*sign
    theta = toRad(angle)
    
    if angle > 90 | dy > 0 & angle < 0 :
      print("can't solve")
      break
    
    loopcount += 1
    
  print("optimal angle:", toDeg(theta), "/ loopcount:", loopcount)
  return theta

tolerance = 0.1
mod = 0

theta1 = solve(mod, tolerance)
ball1.pos = vector(0, 0, 0)

mod = 1
theta2 = solve(mod, tolerance)
ball1.pos = vector(0, 0, 0)
