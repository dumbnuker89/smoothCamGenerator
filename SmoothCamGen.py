
with nuke.thisNode():
    
    import nuke    
    
import nuke


###from NUKE Python Developer's Guide v10.0v1 documentation »###
##added bake functionality as a script button

def bakeCurve( curve, first, last, inc ):
    '''bake an expresison curve into a keyframes curve'''
    try:
        for f in xrange( first, last, inc ):
            curve.setKey( f, curve.evaluate( f ) )
        curve.setExpression( 'curve' )
    except:
        for f in range( first, last, inc ):
            curve.setKey( f, curve.evaluate( f ) )
        curve.setExpression( 'curve' )

####################################################
def getCurves( knob, views ):
    '''return a list of all animation curves found in the given knob'''
    curves = []
    for v in views:
        curves.extend( knob.animations( v ) )
    return curves

####################################################
def bakeExpressionKnobs( node, first, last, inc, views ):  
    '''bake all knobs in node that carry expressions'''
    # GET ALL KNOBS WITH EXPRESSIONS IN THEM
    expKnobs = [ k for k in node.knobs().values() if k.hasExpression() ]

    # GET ALL CURVES INSIDE THAT KNOB INCLUDING SPLIT FIELDS AND VIEWS
    allCurves = []
    for k in expKnobs:
        allCurves += getCurves( k, views )

    # BAKE ALL CURVES
    for c in allCurves:
        bakeCurve( c, first, last, inc )

####################################################
def bakeDependentNodes():
    '''Add this to onUserDestroy callback - not yet implemented'''
    parentNode = nuke.thisNode() 
    depNodes  = parentNode.dependent( nuke.EXPRESSIONS )
    
    ret = nuke.getFramesAndViews( 'bake curves in dependent nodes?', '%s-%s' % (parentNode.firstFrame(), parentNode.lastFrame()) )
    if not ret:
        return
    fRange = nuke.FrameRange( ret[0] )
    views = ret[1]

    for n in depNodes:
        bakeExpressionKnobs( n, fRange.first(), fRange.last(), fRange.increment(), views )
        

####################################################
def bakeSelectedNodes():
    '''bake selected nodes' knobs that carry expressions'''
    ret = nuke.getFramesAndViews( 'bake curves in selected nodes?', '%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()) )
    if not ret:
        return
    fRange = nuke.FrameRange( ret[0] )
    views = ret[1]

    for n in nuke.selectedNodes():
        bakeExpressionKnobs( n, fRange.first(), fRange.last(), fRange.increment(), views )

   
#grab source cam data

srcCam = nuke.selectedNode()
srcName = srcCam.name()
srcCamX = srcCam.xpos()
srcCamY = srcCam.ypos()
srcFocalLength = srcCam["focal"].value()
srcHaperture = srcCam["haperture"].value()
srcVaperture = srcCam["vaperture"].value()

#create dest cam

try:

    destCam = nuke.createNode("Camera3")

except:
    destCam = nuke.createNode("Camera2")
nuke.extractSelected()
destCam["xpos"].setValue(srcCamX-100)
destCam["ypos"].setValue(srcCamY)


#set user knob

destCam.addKnob(nuke.Tab_Knob("Smoothing"))
destCam.addKnob(nuke.Double_Knob("smooth","smooth"))
destCam["smooth"].setRange(0.01,1)
destCam["smooth"].setValue(2)
destCam.addKnob(nuke.XYZ_Knob("offset","offset"))

destCam.addKnob(nuke.PyScript_Knob("bake","bake","bakeSelectedNodes()"))





#set expressions

destCam["translate"].setExpression(srcName+".translate.x.integrate(frame-smooth,frame+smooth)/(2*smooth)+offset.x",0)
destCam["translate"].setExpression(srcName+".translate.y.integrate(frame-smooth,frame+smooth)/(2*smooth)+offset.y",1)
destCam["translate"].setExpression(srcName+".translate.z.integrate(frame-smooth,frame+smooth)/(2*smooth)+offset.z",2)

destCam["rotate"].setExpression(srcName+".rotate.x.integrate(frame-smooth,frame+smooth)/(2*smooth)+offset.x",0)
destCam["rotate"].setExpression(srcName+".rotate.y.integrate(frame-smooth,frame+smooth)/(2*smooth)+offset.y",1)
destCam["rotate"].setExpression(srcName+".rotate.z.integrate(frame-smooth,frame+smooth)/(2*smooth)+offset.z",2)

destCam["focal"].setExpression(srcName+".focal")
destCam["haperture"].setExpression(srcName+".haperture")
destCam["vaperture"].setExpression(srcName+".vaperture")
