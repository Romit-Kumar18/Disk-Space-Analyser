import os
path = 'C:/Users/yashr/videos'
sizes={}
obj=os.scandir(path)
for i in obj:
    full_path=os.path.join(path,i)
    if os.path.isfile(full_path):
        size=os.stat(full_path).st_size
        print(f"File: {i.name}, Size: {round(size/(1024*1024),2)} MB")
obj.close()