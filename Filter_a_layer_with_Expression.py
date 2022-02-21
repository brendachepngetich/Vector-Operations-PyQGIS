from qgis.core import *
cases=iface.activeLayer()
expression= 'Deaths>50000'
request= QgsFeatureRequest().setFilterExpression(expression)
critical=0
with edit(cases):
    for x in cases.getFeatures(request):
        critical +=1
        x['Active']= "YES"
        cases.updateFeature(x)
print (critical)

    