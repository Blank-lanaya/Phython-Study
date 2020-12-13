# Trinket Website
# Space Setting
TargetRange = 10

ground = box(pos = vector(0, 0, 0), size = vector(5, 0.2, 1), color = color.green)
ball   = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball2  = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball3  = sphere(pos = vector(TargetRange, 0, 0), radius = 0.2, color = color.red)

CalculateSpeed = 5
DrawSpeed = 50

Gravity   = vector(0, -600, 0)
DragDiv   = 40
VelScale  = 1

Caliber   = 120
Mass      = 0.001
DragCoef  = (pi*Caliber**2)/(4000000*Mass)
DragCoef2 = (pi*Caliber**2)/(4000000*Mass*DragDiv)

MuzzleVel = 700

def toRad(th) :
  return th*pi/180

Theta  = toRad(45)
ball.v = vector(MuzzleVel*cos(Theta), MuzzleVel*sin(Theta), 0)
Dt     = 0.0001

attach_trail(ball)

# ACF Lua
# Drag = Bullet.Flight:GetNormalized() * (Bullet.DragCoef * Bullet.Flight:LengthSqr()) / ACF.DragDiv
#	Bullet.NextPos = Bullet.Pos + (Bullet.Flight * ACF.VelScale * DeltaTime)
#	Bullet.Flight = Bullet.Flight + (Bullet.Accel - Drag)*DeltaTime

def norm(v1, v2) :
  length = sqrt(v1**2 + v2**2)
  return vector(v1/length, v2/length, 0)

def length(v1, v2) :
  return sqrt(v1**2 + v2**2)

def lengthSqr(v1, v2) :
  return (v1**2 + v2**2)

# ACF Lua Ballistics Calculate Method
def euler() :
  ball.vel = ball.v
  while ball.pos.y >= 0 :
    rate(CalculateSpeed*1000)
    Drag     = norm(ball.vel.x, ball.vel.y)*(DragCoef*lengthSqr(ball.vel.x, ball.vel.y))/DragDiv
    ball.pos = ball.pos + (ball.vel*VelScale*Dt)
    ball.vel = ball.vel + (Gravity - Drag)*Dt

# Runge Kutta 4 Method
def rk4(th, C) :
  ball2.v   = vector(MuzzleVel*cos(th), MuzzleVel*sin(th), 0)
  ball2.vel = ball2.v
  if C == 1 :
    Cs = CalculateSpeed*1000
  else :
    Cs = DrawSpeed*10
  
  while ball2.pos.y >= 0 :
    rate(Cs)
    
    k = length(ball2.vel.x, ball2.vel.y)*DragCoef2
    
    vel1 = ball2.vel
    acc1 = Gravity - k*vel1
    
    vel2 = vel1 + acc1*Dt/2
    acc2 = Gravity - k*vel2
    vel3 = vel1 + acc2*Dt/2
    acc3 = Gravity - k*vel3
    
    vel4 = vel1 + acc3*Dt
    acc4 = Gravity - k*vel4
    
    ball2.pos = ball2.pos + (Dt/6)*(vel1 + 2*(vel2 + vel3) + vel4)
    ball2.vel = ball2.vel + (Dt/6)*(acc1 + 2*(acc2 + acc3) + acc4)

def clamp(n, min, max) :
  if n < min :
    n = min
  else if n > max :
    n = max
  return n

def Action(Trig, tolerance) :
  if Trig == 1 :
    Az   = 90
    Sign = -1
  else :
    Az   = 0
    Sign = 1
  angle = Az
  theta = toRad(angle)
  
  I = 0
  Index = 0
  while abs(ball2.pos.x - TargetRange) >= 0.1 :
    rk4(theta, 1)
    
    Error = ball2.pos.x - TargetRange
    IncreaseCoef = 3.5*Error
    
    angle -= IncreaseCoef*Sign
    theta = toRad(angle)
    
    if abs(ball2.pos.x - TargetRange) >= 0.1 :
      ball2.pos = vector(0, 0, 0)
    
    #print(IncreaseCoef)
    Index += 1
  
  print(theta*180/pi, "/", Index)
  return theta

tolerance = 0.1

Trig   = 0
theta1 = Action(Trig, tolerance)
ball2.pos = vector(0, 0, 0)

Trig   = 1
theta2 = Action(Trig, tolerance)
ball2.pos = vector(0, 0, 0)

attach_trail(ball2)
rk4(theta1, 0)
ball2.pos = vector(0, 0, 0)

rk4(theta2, 0)
ball2.pos = vector(0, 0, 0)
