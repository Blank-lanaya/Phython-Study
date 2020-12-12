# Trinket Website
# Space Setting
ground = box(pos = vector(0, 0, 0), size = vector(15, 0.2, 3), color = color.green)
ball   = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball2  = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball3  = sphere(pos = vector(4, 0, 0), radius = 0.2, color = color.red)

CalculateSpeed = 5

Gravity   = vector(0, -600, 0)
DragDiv   = 39.97
MuzzleVel = 15

Caliber  = 120
Mass     = 0.0001
DragCoef = (pi*Caliber**2)/(4000000*Mass)

Theta = 45*pi/180

ball.v  = vector(MuzzleVel*cos(Theta), MuzzleVel*sin(Theta), 0)
ball2.v = vector(MuzzleVel*cos(Theta), MuzzleVel*sin(Theta), 0)

attach_trail(ball)
attach_trail(ball2)

# ACF Lua
# Drag = Bullet.Flight:GetNormalized() * (Bullet.DragCoef * Bullet.Flight:LengthSqr()) / ACF.DragDiv
#	Bullet.NextPos = Bullet.Pos + (Bullet.Flight * ACF.VelScale * DeltaTime)
#	Bullet.Flight = Bullet.Flight + (Bullet.Accel - Drag)*DeltaTime

# Normalized Function
def norm(v1, v2) :
  n = sqrt(v1**2+ v2**2)
  return vector(v1/n, v2/n, 0)

def length(v1, v2) :
  return sqrt(v1**2 + v2**2)

# ACF Lua Ballistics Calculate Method
def euler(Dt) :
  while ball.pos.y >= 0 :
    rate(CalculateSpeed*1000)
    Drag     = norm(ball.v.x, ball.v.y)*(DragCoef*length(ball.v.x, ball.v.y))/DragDiv
    ball.pos = ball.pos + (ball.v*MuzzleVel*Dt)
    ball.v   = ball.v + (Gravity - Drag)*Dt

# Runge Kutta 4 Method
def rk4(Dt) :
  while ball2.pos.y >= 0 :
    rate(CalculateSpeed*1000)
    
    k = length(ball2.v.x, ball2.v.y)*DragCoef*(1/DragDiv)
    
    vel1 = ball2.v
    acc1 = Gravity - k*vel1
    
    vel2 = vel1 + acc1*Dt/2
    acc2 = Gravity - k*vel2
    vel3 = vel1 + acc2*Dt/2
    acc3 = Gravity - k*vel3
    
    vel4 = vel1 + acc3*Dt
    acc4 = Gravity - k*vel4
    
    ball2.pos = ball2.pos + (Dt/6)*(vel1 + 2*(vel2 + vel3) + vel4)
    ball2.v   = ball2.v + (Dt/6) * (acc1 + 2*(acc2 + acc3) + acc4)

Dt1 = 0.015*0.002
Dt2 = 0.015*0.05

euler(Dt1)
rk4(Dt2)
