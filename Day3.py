#Create Bendy Setup betwn 2 selected objects 
# select 2 positions
# Finding position for 2 points
import pymel.core as pm
import maya.mel
def ZeroOut(obj):

    try:
        grp = pm.createNode('transform',n = obj + '_Group')
        pm.delete(pm.parentConstraint(obj,grp))
        pm.parent(obj,grp)
    except:
        print (obj+' Zero Out failed')



def CreateSurface(pos1,pos2,Div = 10):



    try:
        pm.select(pos1)
        tempPos = pm.cluster(n='Temp')[1]
        JntPos1 = pm.createNode('joint',n = (pos1+'_Pos1Jnt'))
        pm.delete(pm.parentConstraint(tempPos,JntPos1))
        pm.makeIdentity(JntPos1,a=1,t=1,r=1,s=1)
        pm.delete(tempPos)
        
        
        
        
    except:
        tempPos = pm.createNode('transform',n = 'Temp')
        pm.delete(pm.parentConstraint(pos1,tempPos))
        JntPos1 = pm.createNode('joint',n = (pos1+'_Pos1Jnt'))
        pm.delete(pm.parentConstraint(tempPos,JntPos1))
        pm.makeIdentity(JntPos1,a=1,t=1,r=1,s=1)
        pm.delete(tempPos)

        

    try:
        pm.select(pos2)
        tempPos = pm.cluster(n='Temp')[1]
        JntPos2 = pm.createNode('joint',n = (pos2+'_Pos2Jnt'))
        pm.delete(pm.parentConstraint(tempPos,JntPos2))
        pm.makeIdentity(JntPos2,a=1,t=1,r=1,s=1)

        pm.delete(tempPos)
        
        
        
        
    except:
        tempPos = pm.createNode('transform',n = 'Temp')
        pm.delete(pm.parentConstraint(pos2,tempPos))
        JntPos2 = pm.createNode('joint',n = (pos2+'_Pos2Jnt'))
        pm.delete(pm.parentConstraint(tempPos,JntPos2))
        pm.makeIdentity(JntPos2,a=1,t=1,r=1,s=1)
        pm.delete(tempPos)
        



    pm.parent(JntPos2,JntPos1)

    pm.joint(JntPos1,e=1,oj = 'xyz',secondaryAxisOrient = 'yup')
    pm.joint(JntPos2,e=1,oj = 'none',ch=1,zso=1)

    distanceND = pm.createNode('distanceBetween')

    JntPos1.worldMatrix[0]>>distanceND.inMatrix1
    JntPos2.worldMatrix[0]>>distanceND.inMatrix2
    Dist = distanceND.distance.get()

    surface = pm.nurbsPlane(w = Dist,lr=.01,u =Div,ax =(0,1,0),ch=0)
    print surface
    bsSurface  = pm.duplicate(surface)
    print bsSurface
   
    pm.delete(pm.parentConstraint(JntPos1,JntPos2,surface[0]))
    pm.delete(JntPos1,JntPos2)
    fols = []
    for i in range(0,Div):
        val = ((.5/float(Div))*(i+1)*2)-((.5/float(Div*2))*2)

        fol = pm.createNode('transform',n=('Tst_'+str(i)+'_Follicle'),ss=1)
        folShape = pm.createNode('follicle',n  = fol.name()+'Shape',p = fol,ss=1)
        geo =  surface[0]
        geo.local >> folShape.inputSurface
        geo.worldMatrix[0] >> folShape.inputWorldMatrix
        folShape.outRotate >> fol.rotate
        folShape.outTranslate >> fol.translate
        fol.inheritsTransform.set(False)
        folShape.parameterV.set(0.5)
        folShape.parameterU.set(val)
        fols.append(fol)
        Ctrl = mel.eval("sphere -esw 360 -r 0.3 -d 1 -ut 0 -tol 0.01 -s 4 -nsp 2 -ch 0;")
        pm.PyNode(Ctrl[0])
        Ctrl = pm.rename(Ctrl[0],'Follicle_'+str(i)+'_Ctrl')
        ZeroOut(Ctrl)


    SknJnts = []
    for i in range(0,Div):
        val = ((.5/float(Div))*(i+1)*2)-((.5/float(Div*2))*2)

        fol = pm.createNode('transform',n=('Tst_'+str(i)),ss=1)
        folShape = pm.createNode('follicle',n  = fol.name()+'Shape',p = fol,ss=1)
        geo =  bsSurface[0]
        geo.local >> folShape.inputSurface
        geo.worldMatrix[0] >> folShape.inputWorldMatrix
        folShape.outRotate >> fol.rotate
        folShape.outTranslate >> fol.translate
        fol.inheritsTransform.set(False)
        folShape.parameterV.set(0.5)
        folShape.parameterU.set(val)
        pm.select(cl=1)
        jnt = pm.joint(n=('Follicle_'+str(i)+'_Jnt'))
        pm.delete(pm.parentConstraint(fol,jnt))
        #pm.delete(fol)
        ZeroOut(jnt)
        pm.makeIdentity(jnt,a=1,t=1,r=1,s=1)




CreateSurface('locator1','locator2',Div=5)




 