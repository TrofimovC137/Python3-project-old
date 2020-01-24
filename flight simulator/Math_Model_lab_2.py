from math import *
g=9.8
e2=0.006694
A=6378137
class Plane():
    def __init__(self,psi0,phi0,lam0,H0,gamma0,theta0,m,p,s):
        self.psi=psi0
        self.phi=phi0
        self.lam=lam0
        self.gamma=gamma0
        self.theta=theta0
        self.H=H0
        self.m=m
        self.p=p
        self.s=s
        self.V=0
        self.Vphi=0
        self.Vlam=0
        #[[T],[lam],[phi],[H],[gamma],[theta],[psi]]
        self.data=[[],[],[],[],[],[],[]]
    def print_data(self):
        f=open('flight.txt','w')
        for i in range(0,len(self.data[0])):
            f.write(str(self.data[0][i])+' '+str(self.data[1][i])+' '+str(self.data[2][i])+' '+str(self.data[3][i])+' '+str(self.data[4][i])+' '+str(self.data[5][i])+' '+str(self.data[6][i])+'\n')
        f.close()
    def acceleration(self):
        Vo = sqrt((2*self.m*g)/(17.64*1.2*1.5))
        Ya = 17.64*1.2*1.5*Vo*Vo/2
        Xa = Ya/10
        Vot = (((2*self.m*g)/(1.2*self.s*1.5))**(0.5))*10
        Lp = (Vot**2/(2*g*(self.p/(self.m*g)-0.2)))
        #Time=2*Lp/Vot
        #Time=100
        Time=10
        dt=0.01
        t=0
        t0=t
        #dt=0.5
        V=0
        while t<Time:
            V=(0-Vot)/2*cos(pi*(t-t0)/Time)+(0+Vot)/2
            self.V=V
            self.Vphi=V*cos(self.psi)
            self.Vlam=V*sin(self.psi)
            rn = A*(1-e2)/(1 - e2*sin(self.phi))**(3/2)
            re = A/(1 - e2*sin(self.phi))**(1/2);
            self.phi+=self.Vphi*0.1/(rn+self.H)
            self.lam+=self.Vlam*0.1/((re+self.H)*cos(self.phi))
            self.data[0].append(t)
            self.data[1].append(self.lam)
            self.data[2].append(self.phi)
            self.data[3].append(self.H)
            self.data[4].append(self.gamma)
            self.data[5].append(self.theta)
            self.data[6].append(self.psi)
            t+=dt
    def otr(self):
        #Time=15
        Time=5
        t=self.data[0][-1]
        t0=t
        tf=t+Time
        theta0=0
        thetaf=30
        H0=self.H
        Hf=16
        #dt=0.5
        dt=0.01
        while (t<tf):
            self.theta=(theta0-thetaf)/2*cos(pi*(t-t0)/Time)+(theta0+thetaf)/2
            self.H=(H0-Hf)/2*cos(pi*(t-t0)/Time)+(H0+Hf)/2
            rn = A*(1-e2)/(1 - e2*sin(self.phi))**(3/2)
            re = A/(1 - e2*sin(self.phi))**(1/2);
            self.phi+=self.Vphi*0.1/(rn+self.H)
            self.lam+=self.Vlam*0.1/((re+self.H)*cos(self.phi))
            self.data[0].append(t)
            self.data[1].append(self.lam)
            self.data[2].append(self.phi)
            self.data[3].append(self.H)
            self.data[4].append(self.gamma)
            self.data[5].append(self.theta)
            self.data[6].append(self.psi)
            t+=dt
    def climb(self):
        #Time=2000
        Time=165
        t=self.data[0][-1]
        t0=t
        tf=t+Time
        V0=self.V
        Vf=700
        #dt=0.5
        dt=0.01
        H0=self.H
        Hf=3479.982
        theta0=30.5218
        thetaf=0
        while (t<tf):
            self.V=(V0-Vf)/2*cos(pi*(t-t0)/Time)+(V0+Vf)/2
            self.Vphi=self.V*cos(self.psi)
            self.Vlam=self.V*sin(self.psi)
            rn = A*(1-e2)/(1 - e2*sin(self.phi))**(3/2)
            re = A/(1 - e2*sin(self.phi))**(1/2);
            self.phi+=self.Vphi*0.1/(rn+self.H)
            self.lam+=self.Vlam*0.1/((re+self.H)*cos(self.phi))
            self.theta=(theta0-thetaf)/2*cos(pi*t/(Time+15))+(theta0+thetaf)/2
            self.H=(H0-Hf)/2*cos(pi*(t-t0)/Time)+(H0+Hf)/2
            self.data[0].append(t)
            self.data[1].append(self.lam)
            self.data[2].append(self.phi)
            self.data[3].append(self.H)
            self.data[4].append(self.gamma)
            self.data[5].append(self.theta)
            self.data[6].append(self.psi)
            t+=dt
    def swerve(self):
        gamma0=0
        gammaf=15
        self.theta=0
        self.V=570
        R=self.V**2/(g*tan(gammaf*180/pi))
        psi0=self.psi
        psif=305/(180/pi)
        #Time=(psi0-psif)/(self.V/R)
        #Time=1000
        #dt=0.5
        Time=387
        dt=0.1
        t=self.data[0][-1]
        t0=t
        tf=t+Time
        while (t<tf):
            if(t-t0<15):
                self.gamma=(gamma0-gammaf)/2*cos(pi*(t-t0)/15)+(gamma0+gammaf)/2
            if(tf-t<15):
                self.gamma=(gamma0-gammaf)/2*cos(pi*(tf-t)/15)+(gamma0+gammaf)/2
            self.psi=(psi0-psif)/2*cos(pi*(t-t0)/Time)+(psi0+psif)/2
            self.Vphi=self.V*cos(self.psi)
            self.Vlam=self.V*sin(self.psi)
            rn = A*(1-e2)/(1-e2*sin(self.phi))**(3/2)
            re = A/(1-e2*sin(self.phi))**(1/2);
            self.phi+=self.Vphi*dt/(rn+self.H)
            self.lam+=self.Vlam*dt/((re+self.H)*cos(self.phi))
            self.data[0].append(t)
            self.data[1].append(self.lam)
            self.data[2].append(self.phi)
            self.data[3].append(self.H)
            self.data[4].append(self.gamma)
            self.data[5].append(self.theta)
            self.data[6].append(self.psi)
            t+=dt
    def cruising_flight(self):
        lam0=self.lam
        lamf=12+14/60+25.24/3600
        phi0=self.phi
        phif=41+48/60+5.63/3600
        Time=5*60*60
        #dt=0.5
        dt=5
        t=self.data[0][-1]
        t0=t
        tf=t+Time
        while(t<tf):
            self.lam=(lam0-lamf)/2*cos(pi*(t-t0)/Time)+(lam0+lamf)/2
            self.phi=(phi0-phif)/2*cos(pi*(t-t0)/Time)+(phi0+phif)/2
            self.data[0].append(t)
            self.data[1].append(self.lam)
            self.data[2].append(self.phi)
            self.data[3].append(self.H)
            self.data[4].append(self.gamma)
            self.data[5].append(self.theta)
            self.data[6].append(self.psi)
            t+=dt
    def rad(self):
        for i in range(0,len(self.data[0])):
            self.data[4][i]/=(180/pi)
            self.data[5][i]/=(180/pi)
def run():
    Boeng=Plane(186.5/57,13+42/60+13/3600,100 + 44/60 + 35/3600,10,0,0,43998,2*10**6,1/7*60.9*60.9)
    Boeng.acceleration()
    Boeng.otr()
    Boeng.climb()
    Boeng.swerve()
    Boeng.cruising_flight()
    Boeng.rad()
    Boeng.print_data()
run()
