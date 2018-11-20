# MovieTools
Movie tools by Yitong, feel free to use and contribute 


## MovieStackCreator.py
    A script to combine seperated images from a timelapse movie taken by MetaMorph to tif image stacks. 
    Accepting file name example: MyExp1_w1YFP_s3_t15.TIF 
    Or in general, the regex r'([^ _]+)_(w\d[^ _]+_s\d+)_t(\d+).TIF'
    
    Output will be in a folder named "EachPosWave" in the working directory

    positional arguments:
    WorkDic               The directory containing all the images (only ends with .TIF)

    optional arguments:
    -h, --help            show this help message and exit
    -t MULTITHREAD, --MultiThread MULTITHREAD
                          Number of thread to use, default = 1
    --compressionOFF      Turn off compression if you are more CPU bound than IO bound (faster on a laptop with SSD). Of course it will increase final file sizes
