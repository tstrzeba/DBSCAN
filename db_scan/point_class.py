class point(object):

    #float number coordinate
    __coordinate = []
    __in_cluster = False
    __cluster_name = None
    
    
    def __init__(self,*cor):
        self.__coordinate = cor
        
        
    def setCoordinate(self,*arg):
        self.__coordinate = arg

    def showPoint(self):
        print self.__coordinate
        
    def isInCluster(self):
        return self.__in_cluster
        
    def getCluster(self):
        if(self.__in_cluster == True):
            return self.__cluster_name
        else:
            return None
            
    def setCluster(self,cName):
        if(isinstance(cName,str) == False):
            raise Exception('Incorrect class name. Name should be a string variable')
            return False
        else:
            if(self.__in_cluster == True):
                print "Previous cluster: %s, currently set: %s" %(self.__cluster_name, cName)
            
            self.__cluster_name = cName
            self.__in_cluster = True
            return True
            
            
            
        
        
pt = point(1,2,3,4,5)
print pt.getCluster()
print pt.isInCluster()
print pt.setCluster("hahaha")
print pt.getCluster()
print pt.isInCluster()
print pt.setCluster("xaxaa")
print pt.getCluster()
print pt.setCluster(2)

      
                
        