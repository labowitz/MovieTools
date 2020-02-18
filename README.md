# MovieTools
Movie tools by Yitong, feel free to use and contribute 


## MovieStackCreator.py
A script to combine seperated images from a timelapse movie taken by MetaMorph to tif image stacks. Accepting file name example: 
MyExp1_w1YFP_s3_t15.TIF 
Or in general, the regex r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF'

    positional arguments:
      WorkDic               The directory containing all the images (only ends with .TIF)

    optional arguments:
      -h, --help            show this help message and exit
      -t MULTITHREAD, --MultiThread MULTITHREAD
                            Number of thread to use, default = 1
      --compressionOFF      Turn off compression if you are more CPU bound than IO bound (faster on a laptop with SSD). 
                            Of course it will increase final file sizes
      --normalize           Normalize across a each image using 1-99 percentile to 0~65535(16bit)


## GenerateStage.py
A script to generate a stage file for metamoreph. Be careful, this script also generate z-distance, so it will damage the objective if set too high. The generated pattern will be a AxB grid in CxD wells in 24 well plate, start from coodinate (0,0)

    positional arguments:
      A                     Number positions in the x-axis for each well
      B                     Number positions in the y-axis for each well
      C                     Number wells (24 well plate format) in the x-axis
      D                     Number wells (24 well plate format) in the y-axis
      offset                auto-focusing offset in microns

    optional arguments:
      -h, --help            show this help message and exit
      -z Z                  z-distance of the objective in microns
      -i I                  Intervals between different positions
      -n POSNAME, --PosName POSNAME
                            Prefix of the position names
      -o OUTPUT, --Output OUTPUT
                            Directory for the output file
