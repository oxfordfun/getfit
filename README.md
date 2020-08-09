# getfit
Monitor your weight loss towards a goal of your ideal weight

## Get code 
```
git clone https://github.com/oxfordfun/getfit

```
## Set up virutual environment
```
cd getfit
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requirements.txt
```

## Set up config
```
cp weight-example.csv weight.csv
cp config-example.yaml config.yaml
```

## Generate graph
```
python3 weight.py
```
![Example weight graph](https://github.com/oxfordfun/getfit/blob/master/example.png)

## Monitor your data
- Modify config.yaml for yourself
- Record data in weight.csv
- Generate graph daily to monitor your weight loss







