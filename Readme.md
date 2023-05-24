# Simple Watering System

Watering my dill using a small 6V pump, soil moisture sensor (conductive), and quick connect mist nozzles.

## Hardware
- [mist nozzle](https://www.amazon.co.jp/gp/product/B0BVVQVWQ9/ref=ppx_yo_dt_b_asin_title_o04_s00?ie=UTF8&psc=1)
- [6v pump](https://www.amazon.co.jp/-/en/dp/B07VNDY385/?coliid=IIA1OL75K9PT7&colid=2WKC8BQOI0ZSZ&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it)
- [moisture sensor](https://www.amazon.co.jp/-/en/dp/B0116IYDES/?coliid=IFB94LWOY8I1X&colid=2WKC8BQOI0ZSZ&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it)
- [pi zero w](https://www.amazon.co.jp/-/en/dp/B07BHMRTTY/?coliid=I2GK0K9PBIYC80&colid=2WKC8BQOI0ZSZ&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it)
- [relays](https://www.amazon.co.jp/-/en/dp/B07W5MZ2C7/?coliid=I1E1Z24L18H0M9&colid=2WKC8BQOI0ZSZ&psc=1&ref_=list_c_wl_lv_ov_lig_dp_it)
- [1/4 inch quick connect hose](https://www.amazon.co.jp/-/en/CESFONJER-Diameter-Connection-Accessories-Refrigerator/dp/B07VVCGNQQ/ref=sr_1_2?crid=39PLELDYJXA3Y&keywords=10+Meter+1%2F4%22+%2F+6.3mm+Diameter+Tube&qid=1684913230&sprefix=10+meter+1%2F4%22+%2F+6.3mm+diameter+tube%2Caps%2C182&sr=8-2)
- [barbed hose connector G1/4](https://www.amazon.co.jp/-/en/gp/product/B0BQYMKBHJ/ref=ewc_pr_img_2?smid=A2RP5LLYB1DB9T&psc=1)
- [G1/4 to quick connect adapter](https://www.amazon.co.jp/-/en/gp/product/B0BTGHTTRG/ref=ewc_pr_img_1?smid=A6Y5N8A2KUYA8&psc=1)

## Flask
Run **flask** server to show watering log:
Connect to `Pi` via `ssh`:
```shell
ssh pi@'ipaddress'
```
Replace `ipaddress` with your `Pi`'s address. Enter password.
Use `nohup` to start flask server from `ssh`.

```shell
cd path/to/garden/
nohup python3 load_csv.py &
```

## Watering

```shell
cd path/to/garden/
nohup python3 watering.py &
```

## Kill
To kill python scripts run from `nohup`: 
```shell
ps aux | grep python3
```
Find PID of the python script, kill it:
```shell
kill PID
```