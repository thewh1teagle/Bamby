# Bamby
<img src="https://user-images.githubusercontent.com/61390950/144936845-23832b19-59e6-4117-8a1b-055ff9ec3f1e.png" style="pointer-events: none;cursor: none; user-select: none; width: 250px; height: 200px;">

**In memory ZIP bomb Creator**

*"A zip bomb, also known as a zip of death or decompression bomb,  
is a malicious archive file designed to crash or render  
useless the program or system reading it."*  
Read more at [Wikipedia](https://en.wikipedia.org/wiki/Zip_bomb)  




### Usage
```bash
git clone https://github.com/thewh1teagle/bamby
cd bamby
python3 main.py
```

### Sample output
```log
Before de-compression: 3.072KB
After de-compression: 10000000000GB
```
- `1000GB = 1TB, 1000TB = 1PB`


### How to protect against zip bomb?
Have a look under [`safe_unzip.py`](https://github.com/thewh1teagle/Bamby/blob/main/safe_unzip.py#L45)  
The idea is simple,  
Limit the possible resources of the process,  
no matter what, it will not hurt your system 😃  
