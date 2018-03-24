def watershedding_3D(Track,Field_in,threshold=3e-3,target='maximum',level=None,compactness=0,method='watershed'):
    """
    Function using watershedding to determine cloud volumes associated with tracked updrafts
    
    Parameters:
    Track:         pandas.DataFrame 
                   output from trackpy/maketrack
    Field_in:      iris.cube.Cube 
                   containing the field to perform the watershedding on 
    threshold:  float 
                   threshold for the watershedding field to be used for the mask
                   
    target:        string
                   Switch to determine if algorithm looks strating from maxima or minima in input field (maximum: starting from maxima (default), minimum: starting from minima)

    level          slice
                   levels at which to seed the particles for the watershedding algorithm
    compactness    float
                   parameter describing the compactness of the resulting volume
    
    Output:
    Watershed_out: iris.cube.Cube
                   Cloud mask, 0 outside and integer numbers according to track inside the clouds
    
    """
    
    import numpy as np
    import copy
    from skimage.morphology import watershed
    from skimage.segmentation import random_walker
    from iris.analysis import MIN,MAX
#    from scipy.ndimage.measurements import watershed_ift

    #Set level at which to create "Seed" for each cloud and threshold in total water content:
    # If none, use all levels (later reduced to the ones fulfilling the theshold conditions)
    if level==None:
        level=slice(None)
         
    Watershed_out=copy.deepcopy(Field_in)
    Watershed_out.rename('watershedding_output_mask')
    Watershed_out.data[:]=0
    Watershed_out.units=1
    cooridinates=Field_in.coords(dim_coords=True)
    maximum_value=Field_in.collapsed(cooridinates,MAX).data
    minimum_value=Field_in.collapsed(cooridinates,MIN).data
    range_value=maximum_value-minimum_value

    for i, time in enumerate(Field_in.coord('time').points):        
#        print('doing watershedding for',WC.coord('time').units.num2date(time).strftime('%Y-%m-%d %H:%M:%S'))
        Tracks_i=Track[Track['frame']==i]
        data_i=Field_in[i,:].data
 
        if target == 'maximum':
            unmasked=data_i>threshold
        elif target == 'minimum':
            unmasked=data_i<threshold
        else:
            raise ValueError('unknown type of target')
        markers = np.zeros_like(unmasked).astype(np.int16)
        for index, row in Tracks_i.iterrows():
            markers[:,int(row.y), int(row.x)]=row.particle
        markers[~unmasked]=0
        maximum_value=np.amax(data_i)
        minimum_value=np.amin(data_i)
        range_value=maximum_value-minimum_value
        if target == 'maximum':
            data_i_watershed=1500-(data_i-minimum_value)*1000/range_value
        elif target == 'minimum':
            data_i_watershed=1500-(maximum_value-data_i)*1000/range_value
        else:
            raise ValueError('unknown type of target')

        data_i_watershed[~unmasked]=2000
        data_i_watershed=data_i_watershed.astype(np.uint16)
        #res1 = watershed_ift(data_i_watershed, markers)
        
        if method=='watershed':
            res1 = watershed(data_i_watershed,markers.astype(np.int8), mask=unmasked,compactness=compactness)
        elif method=='random_walker':
            #res1 = random_walker(Mask, markers,mode='cg')
             res1=random_walker(data_i_watershed, markers.astype(np.int8), beta=130, mode='bf', tol=0.001, copy=True, multichannel=False, return_full_prob=False, spacing=None)
        else:
            print('unknown method')
        Watershed_out.data[i,:]=res1
    return Watershed_out

def watershedding_2D(Track,Field_in,threshold=0,target='maximum',compactness=0,method='watershed'):
    """
    Function using watershedding to determine cloud volumes associated with tracked updrafts
    
    Parameters:
    :param CommonData or CommonDataList data: Data to collocate
    
    :param pandas.DataFrame Track: output from trackpy/maketrack
    :param iris.cube.Cube Field_in: containing the field to perform the watershedding on 
    :param float threshold: threshold for the watershedding field to be used for the mask
    :param string target:Switch to determine if algorithm looks strating from maxima or minima in input field ('maximum': starting from maxima (default), 'minimum': starting from minima)
    :param slice level: levels at which to seed the particles for the watershedding algorithm
    :param float compactness: parameter describing the compactness of the resulting volume
    
    Output:
        
    :return iris.cube.Cube Watershed_out: Cloud mask, 0 outside and integer numbers according to track inside the clouds
    """
    
    import numpy as np
    import copy
    from skimage.morphology import watershed
    from skimage.segmentation import random_walker
    from iris.analysis import MIN,MAX

#    from scipy.ndimage.measurements import watershed_ift

    Watershed_out=copy.deepcopy(Field_in)
    Watershed_out.rename('watershedding_output_mask')
    Watershed_out.data[:]=0
    Watershed_out.units=1
    cooridinates=Field_in.coords(dim_coords=True)
    maximum_value=Field_in.collapsed(cooridinates,MAX).data
    minimum_value=Field_in.collapsed(cooridinates,MIN).data
    range_value=maximum_value-minimum_value

    for i, time in enumerate(Field_in.coord('time').points):        
#        print('doing watershedding for',WC.coord('time').units.num2date(time).strftime('%Y-%m-%d %H:%M:%S'))
        Tracks_i=Track[Track['frame']==i]
        data_i=Field_in[i,:].data        
        
        if target == 'maximum':
            unmasked=data_i>threshold
        elif target == 'minimum':
            unmasked=data_i<threshold
        else:
            raise ValueError('unknown type of target')
        markers = np.zeros_like(unmasked).astype(np.int16)
        for index, row in Tracks_i.iterrows():
            markers[int(row.y), int(row.x)]=row.particle
        markers[~unmasked]=0
        if target == 'maximum':
            data_i_watershed=1000-(data_i-minimum_value)*1000/range_value
        elif target == 'minimum':
            data_i_watershed=1000-(maximum_value-data_i)*1000/range_value
        else:
            raise ValueError('unknown type of target')

        data_i_watershed[~unmasked]=2000
        data_i_watershed=data_i_watershed.astype(np.uint16)

        data_i_watershed=data_i_watershed.astype(np.uint16)
        #res1 = watershed_ift(data_i_watershed, markers)
        
        if method=='watershed':
            res1 = watershed(data_i_watershed,markers.astype(np.int8), mask=unmasked,compactness=compactness)
        elif method=='random_walker':
            #res1 = random_walker(Mask, markers,mode='cg')
              res1=random_walker(data_i_watershed, markers.astype(np.int8), beta=130, mode='bf', tol=0.001, copy=True, multichannel=False, return_full_prob=False, spacing=None)
        else:
            print('unknown method')
        Watershed_out.data[i,:]=res1
    return Watershed_out

def mask_cube_particle(variable_cube,Mask,particle):
    import numpy as np 
    from copy import deepcopy
    variable_cube_out=deepcopy(variable_cube)
    mask=Mask.data!=particle
    variable_cube_out.data=np.ma.array(variable_cube_out.data,mask=mask)    
    return variable_cube_out

def mask_cube_untracked(variable_cube,Mask):
    import numpy as np 
    from copy import deepcopy
    variable_cube_out=deepcopy(variable_cube)
    mask=Mask.data!=0
    variable_cube_out.data=np.ma.array(variable_cube_out.data,mask=mask)    
    return variable_cube_out

def mask_particle(Mask,particle,masked=False):
    import numpy as np 
    from copy import deepcopy
    Mask_i=deepcopy(Mask)
    Mask_i.data[Mask_i.data!=particle]=0
    if masked:
        Mask_i.data=np.ma.array(Mask_i.data,mask=Mask_i.data)
    return Mask_i   

def mask_particle_surface(Mask,particle,masked=False,z_coord=None):
    from iris.analysis import MAX
    import numpy as np 
    from copy import deepcopy
    Mask_i=deepcopy(Mask)
    Mask_i.data[Mask_i.data!=particle]=0
    for coord in  Mask_i.coords():
        if coord.ndim>1 and Mask_i.coord_dims(z_coord)[0] in Mask_i.coord_dims(coord):
            Mask_i.remove_coord(coord.name())
    Mask_i_surface=Mask_i.collapsed(z_coord,MAX)
    if masked:
        Mask_i_surface.data=np.ma.array(Mask_i_surface.data,mask=Mask_i_surface.data)
    return Mask_i_surface    