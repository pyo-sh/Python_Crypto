from PIL import Image 
from Crypto import Random
from DES_CBC import block_size

# image 파일을 불러올 fileName과 저장할 파일의 path
fileName = "image.bmp"
path = "encrypted_image_"
# BMP 이미지를 불러오고, 이는 RGB 형식을 사용하기 때문에 변수 사용
imageFormat = "BMP"
imageMode = "RGB"
# key 와 iv 는 임의 생성
key = Random.new().read(8)
iv = Random.new().read(block_size)

# image 데이터를 ECB Mode로 암호화 하여 그 데이터를 가시화해 저장하는 함수
def encryptImage_ECB(path, imageData, imageSize):
    # 받은 데이터 암호화
    from DES_ECB import des_ECB
    encryptor = des_ECB(key)
    encrypted_data = encryptor.encrypt(imageData)
    
    # 암호화된 데이터 형태를 보기 위해 byte -> RGB
    imaged_data = Image.frombytes(imageMode, imageSize, encrypted_data)
    # RGB image로 구성된 데이터를 저장
    imaged_data.save(path+"DES_ECB."+imageFormat, imageFormat)

# image 데이터를 CBC Mode로 암호화 하여 그 데이터를 가시화해 저장하는 함수
def encryptImage_CBC(path, imageData, imageSize):
    # 받은 데이터 암호화
    from DES_CBC import des_CBC
    encryptor = des_CBC(key, iv)
    encrypted_data = encryptor.encrypt(imageData)
    
    # 암호화된 데이터 형태를 보기 위해 byte -> RGB
    imaged_data = Image.frombytes(imageMode, imageSize, encrypted_data)
    # RGB image로 구성된 데이터를 저장
    imaged_data.save(path+"DES_CBC."+imageFormat, imageFormat)

# 원본 image 파일을 불러와 데이터와 크기를 저장
try:
    with Image.open(fileName) as imageFile:
        data = imageFile.convert(imageMode).tobytes()
        size = imageFile.size
except Exception as e:
    print(e)

encryptImage_ECB(path, data, size)
encryptImage_CBC(path, data, size)