RangeX = 10
Height = -5

ground = box(pos = vector(0, 0, 0), size = vector(5, 0.2, 1), color = color.green)
ball   = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball2  = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball3  = sphere(pos = vector(RangeX, Height, 0), radius = 0.2, color = color.red)

CalculateSpeed = 1

Gravity   = vector(0, -600, 0)
DragDiv   = 40
VelScale  = 1

Caliber   = 120
Mass      = 100
DragCoef = (pi*Caliber**2)/(4000000*Mass*DragDiv)

MuzzleVel = 80
Dt = 0.0005
M = -0.1

def toRad(th) :
  return th*pi/180

def toDeg(th) :
  return th*180/pi

def length(v1, v2) :
  return sqrt(v1**2 + v2**2)

# Runge Kutta 4 Method
def rk4(th) :
  p = vector(0, 0, 0)
  v = vector(MuzzleVel*cos(th), MuzzleVel*sin(th), 0)
  I = 0
  while 1 :
    rate(CalculateSpeed*1000)
    
    k = length(v.x, v.y)*DragCoef
    
    vel1 = v
    acc1 = Gravity - k*vel1
    
    vel2 = vel1 + acc1*Dt/2
    acc2 = Gravity - k*vel2
    vel3 = vel1 + acc2*Dt/2
    acc3 = Gravity - k*vel3
    
    vel4 = vel1 + acc3*Dt
    acc4 = Gravity - k*vel4
    
    p = p + (Dt/6)*(vel1 + 2*(vel2 + vel3) + vel4)
    v = v + (Dt/6)*(acc1 + 2*(acc2 + acc3) + acc4)
    ball2.pos = p
    
    Limit = (Height/RangeX)*p.x + M
    if p.y < Limit :
      endpos = p
      break
  return endpos

def Action(Trig, tolerance) :
  if Trig == 1 :
    Az   = 90
    Sign = -1
  else :
    Az   = 0
    Sign = 1
  angle = Az
  theta = toRad(angle)
  
  Index = 0
  
  while abs(ball2.pos.x - RangeX) >= tolerance :
    EndPos = rk4(theta)
    
    Error = RangeX - EndPos.x
    IncreaseCoef = Error*2
    
    angle += IncreaseCoef*Sign
    theta = toRad(angle)
    
    print(angle)
    
    Index += 1
  
  print(toDeg(theta), "/", Index)
  return theta

tolerance = 0.1

Trig   = 0
theta1 = Action(Trig, tolerance)
ball2.pos = vector(0, 0, 0)

Trig   = 1
theta2 = Action(Trig, tolerance)
