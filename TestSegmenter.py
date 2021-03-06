from ParserHandler import get_circular_trajectory, get_rectangular_segmenter, get_size_preprocessor
from PIL.Image import open

if __name__ == '__main__':
    img = open("img/photo.jpg")
    width_image, height_image = img.size

    trajectory = get_circular_trajectory(width_image, height_image)
    preprocessor = get_size_preprocessor()
    segmenter = get_rectangular_segmenter(img, trajectory, [preprocessor])

    i = 0
    image = segmenter.get_current_segment()
    image.pil_image.save('img/segments/recorte' + str(i) + '.jpg')
    #print str(i) + ' -- ' + str(image.x_position_clipper) + ' -- ' + str(image.y_position_clipper)
    i += 1
    while (segmenter.has_next_segment()):
        image = segmenter.get_next_segment()
        image.pil_image.save('img/segments/recorte' + str(i) + '.jpg')
        #print str(i) + ' -- ' + str(image.x_position_clipper) + ' -- ' + str(image.y_position_clipper)
        i += 1