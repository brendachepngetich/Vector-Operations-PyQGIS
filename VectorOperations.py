from qgis.PyQt.QtCore import QVariant
from qgis.core import (
    QgsGeometry,
    QgsPoint,
    QgsPointXY,
    QgsVectorLayer,
    QgsFields,
    QgsField,
    QgsFeature,
    QgsExpression,
    QgsProject,
    QgsCoordinateTransform,
    QgsCoordinateReferenceSystem,
    QgsVectorDataProvider,
    )
points= QgsVectorLayer('Point?crs=epsg:21037&field=id:integer&field=name:string(20)&index=yes',"points","memory")
pointsdp=points.dataProvider()
#add features
A=QgsFeature()
A.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282371.77067196677671745,9857934.94832113943994045)))
A.setAttributes([1,"A"])
B=QgsFeature()
B.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282371.77067196677671745,9857899.74832113832235336)))
B.setAttributes([2,"B"])
C=QgsFeature()
C.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282398.95667903579305857,9857923.53450032509863377)))
C.setAttributes([3,"C"])
D=QgsFeature()
D.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282391.69078569998964667,9857903.20393287017941475)))
D.setAttributes([4,"D"])
X=QgsFeature()
X.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282354.35467462037922814,9857911.78751550242304802)))
X.setAttributes([5,"X"])
Y=QgsFeature()
Y.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282362.34182158601470292,9857930.63811318017542362)))
Y.setAttributes([6,"Y"])
Z=QgsFeature()
Z.setGeometry(QgsGeometry.fromPointXY(QgsPointXY(282364.42153724399395287,9857931.69000650011003017)))
Z.setAttributes([7,"Z"])
pointsdp.addFeatures([A,B,C,D,X,Y,Z])

#create a polygon 
polygon= QgsVectorLayer('Polygon?crs=epsg:21037&field=id:integer&field=area:double&index=yes',"polygon","memory")
polygondp=polygon.dataProvider()
poly=QgsFeature()
list=[QgsPointXY(282398.95667903579305857,9857923.53450032509863377),QgsPointXY(282391.69078569998964667,9857903.20393287017941475),
QgsPointXY(282354.35467462037922814,9857911.78751550242304802),QgsPointXY(282362.34182158601470292,9857930.63811318017542362),
QgsPointXY(282364.42153724399395287,9857931.69000650011003017)]
poly.setGeometry(QgsGeometry.fromPolygonXY([list]))
polygondp.addFeature(poly)
QgsProject.instance().addMapLayer(points)
QgsProject.instance().addMapLayer(polygon)

#create a line
line=QgsVectorLayer('LineString?crs=epsg:21037&field=id:integer&field=length:integer&index=yes',"line","memory")
linedp=line.dataProvider()
linefet=QgsFeature()
linefet.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(282371.77067196677671745,9857934.94832113943994045),
QgsPointXY(282371.77067196677671745,9857899.74832113832235336)]))
linedp.addFeature(linefet)
QgsProject.instance().addMapLayer(line)

#splitting
result= processing.run("native:splitwithlines", 
{'INPUT':'polygon',
'LINES':'line',
'OUTPUT':'memory:'
})["OUTPUT"]
QgsProject.instance().addMapLayer(result)
resultdp=result.dataProvider()
resultdp.addAttributes([QgsField("name",QVariant.String)])
result.updateFields()

#populate fields
features= result.getFeatures()
exp=QgsExpression('$area')
context=QgsExpressionContext()
context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(result))
with edit(result):
    for x in features:
        context.setFeature(x)
        x['area']= exp.evaluate(context)
        x['name']="splitted"
        x['id']=x.id()
        result.updateFeature(x)
        






