# Trinket Website
ground = box(pos = vector(0, 0, 0), size = vector(15, 0.2, 3), color = color.green)
ball   = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball2  = sphere(pos = vector(0, 0, 0), radius = 0.2, color = color.yellow)
ball3  = sphere(pos = vector(4, 0, 0), radius = 0.2, color = color.red)


Gravity   = vector(0, -600, 0)
DragDiv   = 39.97
MuzzleVel = 15

Caliber  = 120
Mass     = 0.0001
DragCoef = (pi*Caliber**2)/(4000000*Mass)

Theta = 45*pi/180

ball.v = vector(MuzzleVel*cos(Theta), MuzzleVel*sin(Theta), 0)

Dt = 0.015*0.002

attach_trail(ball)
attach_trail(ball2)


# Drag = Bullet.Flight:GetNormalized() * (Bullet.DragCoef * Bullet.Flight:LengthSqr()) / ACF.DragDiv
#	Bullet.NextPos = Bullet.Pos + (Bullet.Flight * ACF.VelScale * DeltaTime)
#	Bullet.Flight = Bullet.Flight + (Bullet.Accel - Drag)*DeltaTime

def norm(v1, v2) :
  n = sqrt(v1**2+ v2**2)
  return vector(v1/n, v2/n, 0)

def length(v1, v2) :
  return sqrt(v1**2 + v2**2)

while ball.pos.y >= 0 :
  rate(1000)
  Drag     = norm(ball.v.x, ball.v.y)*(DragCoef*length(ball.v.x, ball.v.y))/DragDiv
  ball.pos = ball.pos + (ball.v*MuzzleVel*Dt)
  ball.v   = ball.v + (Gravity - Drag)*Dt

dt = 0.015*0.05

Theta2 = 20*pi/180

ball2.v = vector(MuzzleVel*cos(Theta2), MuzzleVel*sin(Theta2), 0)

Range = 4

while ball2.pos.x <= Range :
  rate(1000)
  
  k = length(ball2.v.x, ball2.v.y)*DragCoef*(1/DragDiv)
  
  vel1 = ball2.v
  acc1 = Gravity - k * vel1
  
  vel2 = vel1 + acc1*dt/2
  acc2 = Gravity - k*vel2
  vel3 = vel1 + acc2*dt/2
  acc3 = Gravity - k*vel3
  
  vel4 = vel1 + acc3*dt
  acc4 = Gravity - k*vel4
  
  ball2.pos = ball2.pos + (dt/6)*(vel1 + 2*(vel2 + vel3) + vel4)
  ball2.v   = ball2.v + (Dt/6) * (acc1 + 2*(acc2 + acc3) + acc4)

  
