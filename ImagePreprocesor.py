from PIL.Image import open
from PIL.Image import Image as PIL_IMG
from Image import Image


#############################################################################################################
class ImagePreprocesor:
	'''
	Module for segmenting images
	'''


	def __init__(self, wideSegment, highSegment, horizontalStride, verticalStride, withResizeImgOut = None, highResizeImgOut = None):
		"""
		:rtype: ImagePreprocesor
		"""
		self.hSeg = highSegment
		self.wSeg = wideSegment
		self.strideH = horizontalStride
		self.strideV = verticalStride
		self.withResizeImgOut = withResizeImgOut
		self.highResizeImgOut = highResizeImgOut
		if self.withResizeImgOut is None:
			self.withResizeImgOut = self.wSeg
		if self.highResizeImgOut is None:
			self.highResizeImgOut = self.hSeg
		# Upper Left Corner of the rectangle
		self.resetXULCoordinate()
		self.resetYULCoordinate()


	def getNexSegment(self):
		'''
		Get the nex segment according with the Upper left corner (xUL, yUL) value and update it's value
		'''
		segment = self.copySegment()
		img = Image(self.xUL, self.yUL, self.resize(segment))
		self.moveUpperLeftCoorner()
		return img

	def moveUpperLeftCoorner(self):
		'''
		Move the upper left corner increasing it's value with the stride, horizontal and vertical
		'''
		self.xUL += self.strideH
		if (self.xUL + self.wSeg - self.horizontalTop) >= self.strideH:
			self.resetXULCoordinate()
			self.yUL += self.strideV
		if (self.yUL + self.hSeg - self.verticalTop) >= self.strideV:
			self.resetYULCoordinate()

	def resetXULCoordinate(self):
		'''
		Reset the coordinate xUL
		'''
		self.xUL = 0

	def resetYULCoordinate(self):
		'''
		Reset the cordinate yUL
		'''
		self.yUL = 0

	def resize(self, img):
		#Resize the PIL image "self.img"
		return img.resize((self.withResizeImgOut, self.highResizeImgOut))

	def copySegment(self):
		'''
			Copy a rectangular segment of a image "img" based on the upper left corner
		'''
		# Lower Right corner calculation
		xLR = self.xUL + self.wSeg
		yLR = self.yUL + self.hSeg
		return self.img.crop((self.xUL, self.yUL, xLR, yLR))

	def runSegmentation(self, imgPath):
		PILImage = open(imgPath)
		self.img = PILImage
		self.wImg , self.hImg = PILImage.size
		self.horizontalTop = self.wImg
		self.verticalTop = self.hImg
		i = 0
		while True:
			segment = self.getNexSegment()
			#Romper ciclo hasta que se reinicie la coordenada de recorte
			if(segment.xPositionClipper == 0 and segment.yPositionClipper == 0 and i != 0):
				break
			segment.PILImage.save('img/segments/cutout'+str(i)+'.jpg')
			i+=1
		return i+1