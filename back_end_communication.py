import requests

#http post
def post(faceName,isActive):
    # defining the api-endpoint  
    API_ENDPOINT = "http://ptsv2.com/t/ya1h9-1571410758/post"
    
    # your API key here 
    API_KEY = "XXXXXXXXXXXXXXXXX"
  
    # your source code here 
    source_code = "person num: " + faceName 
    option = 'activate' if isActive else  'inactivate'
    
    # data to be sent to api 
    data = {'api_dev_key':API_KEY, 
            'api_option': option, 
            'api_paste_code':source_code, 
            'api_paste_format':'python'} 

    # sending post request and saving response as response object 
    r = requests.post(url = API_ENDPOINT, data = data) 

#il faudrait poster une image pour etre sur de l utilisateur si nouveau si qui de plusieurs personnes en meme temps devant la camera